#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "chenwei"
# Date: 2019/2/4


from random import choice
import base64

from django.http.response import JsonResponse
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets
from rest_framework import status
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import authentication
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .serializers import SmsSerializer, UserRegSerializer, UserDetailSerializer
from .models import JdAuthUserModel
from jd_sdk.apis import JdShopApi
from jd_sdk.sdk import JdSdk
from jd_sdk.authorized import JdWebAuthorized
from jd_shop.models import JdShopInfoModel
from utils.alisms import AliSMS
from django.conf import settings
from .models import VerifyCode
from jd_product.tasks import task_product_info

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 用户名和手机都能登录
            user = User.objects.get(
                Q(username=username) | Q(phone=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


@method_decorator(csrf_exempt, name='dispatch')
class SmsCodeView(CreateModelMixin, viewsets.GenericViewSet):
    """
    手机验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成四位数字的验证码
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # 验证合法
        if not serializer.is_valid(raise_exception=False):
            return JsonResponse({
                'errmsg': serializer._errors['phone'],
                'errcode': -1
            })

        phone = serializer.validated_data["phone"]

        ali_sms = AliSMS(settings.ALI_SMS_KEY, settings.ALI_SMS_SECRET, settings.ALI_SMS_SIGN_NAME)
        # 生成验证码
        code = self.generate_code()
        template_params = {
            'code': code
        }
        sms_status = ali_sms.send(phone, settings.ALI_SMS_TEMPLATE_CODE, template_params)

        if sms_status["Code"] != 'OK':
            return Response({
                "errcode": -1,
                "errmsg": sms_status["Message"],
                "data": {}
            }, status=status.HTTP_200_OK)
        else:
            code_record = VerifyCode(code=code, phone=phone)
            code_record.save()
            return Response({
                "errcode": 0,
                "errmsg": "验证码获取成功",
                "data": {
                    "expire": 90
                }
            }, status=status.HTTP_201_CREATED)


@method_decorator(csrf_exempt, name='dispatch')
class UserView(CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    用户行为操作
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            return JsonResponse({
                'errmsg': serializer._errors,
                'errcode': -1
            })
        user = self.perform_create(serializer)
        # 授权信息绑定
        state = request.COOKIES.get('state')
        if state:
            state_dict = eval(base64.b64decode(state).decode('utf-8'))
            # 绑定店铺信息
            shop, _ = self.get_shop_info(state_dict['access_token'])
            state_dict['shop'] = shop
            # 商品信息同步,异步任务
            task_product_info.apply_async(queue='product_router')
            # 绑定用户
            state_dict['user'] = user
            JdAuthUserModel.objects.update_or_create(uid=state_dict['uid'], defaults=state_dict)

        else:
            # 直接注册的用户获取获取授权信息,state为传递绑定的账户
            jd_web_auth_obj = JdWebAuthorized(code='', state=f'username:{user.username}')
            redirect_url = jd_web_auth_obj.get_code_url()
            re_dict = {}
            re_dict["errcode"] = 2
            re_dict["errmsg"] = '注册成功'
            re_dict["redirect_url"] = redirect_url
            return Response(re_dict, status=status.HTTP_200_OK)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["username"] = user.username
        re_dict["errmsg"] = '注册成功'
        re_dict["errcode"] = 0

        headers = self.get_success_headers(serializer.data)
        response = Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)
        # 删除该cookie信息
        response.set_cookie('state', '')
        return response

    # 这里需要动态权限配置
    # 1.用户注册的时候不应该有权限限制
    # 2.当想获取用户详情信息的时候，必须登录才行
    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []

        return []

    # 这里需要动态选择用哪个序列化方式
    # 1.UserRegSerializer（用户注册），只返回username和phone，会员中心页面需要显示更多字段，所以要创建一个UserDetailSerializer
    # 2.问题又来了，如果注册的使用userdetailSerializer，又会导致验证失败，所以需要动态的使用serializer
    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer

        return UserDetailSerializer

    # 虽然继承了Retrieve可以获取用户详情，但是并不知道用户的id，所有要重写get_object方法
    # 重写get_object方法，就知道是哪个用户了
    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()

    @staticmethod
    def get_shop_info(access_token):
        jd_api = JdSdk()
        stat, ret = jd_api.send_request({"method": JdShopApi.JD_SHOP_INFO_V_1, "access_token": access_token})
        response_name = JdShopApi.JD_SHOP_INFO_V_1.replace('.', '_')
        shop_response = ret.get(f'{response_name}_responce')
        data = shop_response.get('shop_jos_result')
        if shop_response.get('code') == '0':
            shop = JdShopInfoModel.objects.update_or_create(shop_id=data['shop_id'], defaults=data)
            return shop
