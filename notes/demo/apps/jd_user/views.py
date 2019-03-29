import base64
import json
import logging

from django.db.models import Q
from django.views.generic import View
from django.contrib.auth import get_user_model
from django.http.response import JsonResponse
from django.contrib.auth.backends import ModelBackend
from django.shortcuts import redirect, reverse, render, render_to_response
from django.contrib.auth import login, authenticate, logout
from django.http.response import HttpResponseRedirect

from .models import JdAuthUserModel, UserProfileModel
from jd_shop.models import JdShopInfoModel
from jd_product.tasks import task_product_info
from jd_sdk.authorized import JdWebAuthorized
from jd_sdk.config import JdConfig
from jd_sdk.sdk import JdSdk
from jd_sdk.apis import JdShopApi

logger = logging.getLogger(__name__)

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


class JdRedirectUrlView(View):
    """
    应用回调地址：接收京东请求的链接：URL+code+state
    """

    # 处理授权逻辑
    def get(self, request):
        """
        参数 ：code 为code模式授权时的code，isv的软件需要 通过此code 换取token
        参数 ：state  state中如果有“+”号，因浏览器交互的原因，会出现“+”号替换成空格的现象，导致授权报错
              如果出现此种情况，请把的state中的空格再替换成“+”号；state包含购买用户的信息
        """
        code = request.GET.get('code', '')
        state = request.GET.get('state', '')

        jd_auth_dict = {}

        # 处理初次从京东授权时state包含用户的情况，自定义state值，忽略
        if state not in ['random', ''] and not state.startswith('username'):
            state_str = base64.b64decode(state).decode('utf-8')
            if '+' not in state_str:
                state_str.replace('+', ' ')
            state_dict = dict(eval(state_str))
            jd_dict = state_dict.get('jos_parameters', {})
            jd_auth_dict['user_name'] = jd_dict['user_name']
            jd_auth_dict['app_end_date'] = int(jd_dict['end_date']) // 1000
            jd_auth_dict['item_code'] = jd_dict['item_code']
            jd_auth_dict['article_num'] = int(jd_dict['article_num'])
            jd_auth_dict['version_no'] = int(jd_dict['version_no'])

            # access_token 获取
            jd_auth_dict = self.get_access_token(code, jd_auth_dict)
            if not isinstance(jd_auth_dict, dict):
                return HttpResponseRedirect(jd_auth_dict)
            # 店铺信息同步
            shop, _ = self.get_shop_info(jd_auth_dict['access_token'])
            # 已经存在的用户直接登录
            user_obj = UserProfileModel.objects.filter(jdauthusermodel__uid=jd_auth_dict['uid']).first()
            if user_obj:
                jd_auth_dict['shop'] = shop
                # 商品信息同步,异步任务
                task_product_info.apply_async(queue='product_router')
                user = UserProfileModel.objects.get(jdauthusermodel__uid=jd_auth_dict['uid'])
                login(request, user=user)
                response = redirect(reverse('dashboard:base'))
                return response
            # 跳转到绑定手机号的页面
            else:
                state = base64.b64encode(json.dumps(jd_auth_dict).encode('utf-8')).decode('utf-8')
                resposne = redirect(reverse('jd_user:register'))
                resposne.set_cookie('state', state)
                return resposne
        elif state.startswith('username'):
            # 处理直接平台注册的用户，会和已经注册的用户重复授权有冲突，但不影响
            # access_token 获取
            jd_auth_dict = self.get_access_token(code, jd_auth_dict)
            # 店铺信息同步
            shop, _ = self.get_shop_info(jd_auth_dict['access_token'])
            jd_auth_dict['shop'] = shop

            username = state.replace('username:', '')
            jd_auth_dict['user'] = UserProfileModel.objects.get(username=username)
            JdAuthUserModel.objects.create(**jd_auth_dict)
            # 商品信息同步,异步任务
            task_product_info.apply_async(queue='product_router')
            login(request, user=jd_auth_dict['user'])
            response = redirect(reverse('dashboard:base'))
            return response
        else:
            # 处理已经注册，但是授权未成功的情况
            # access_token 获取
            jd_auth_dict = self.get_access_token(code, jd_auth_dict)
            # 店铺信息同步
            shop, _ = self.get_shop_info(jd_auth_dict['access_token'])
            jd_auth_dict['shop'] = shop
            jd_auth_dict['user'] = UserProfileModel.objects.filter(username=request.user.username).first()
            JdAuthUserModel.objects.create(**jd_auth_dict)
            # 商品信息同步,异步任务
            task_product_info.apply_async(queue='product_router')
            login(request, user=jd_auth_dict['user'])
            response = redirect(reverse('dashboard:base'))
            return response

    @staticmethod
    def get_access_token(code, jd_auth_dict):
        # 根据code获取令牌token
        jd_web_auth_obj = JdWebAuthorized(code=code)
        response_dict = jd_web_auth_obj.get_access_token(code)

        # 异常情况出处理
        if JdConfig.ERROR_CODE_DICT.get(str(response_dict['code'])):
            # TODO 邮箱告警和异常页面提醒
            logger.warning(f'jd auth code is fail, error is {response_dict["error_description"]}')
            redirect_url = jd_web_auth_obj.get_code_url()
            return redirect_url

        # 正常情况处理
        elif response_dict['code'] == 0:
            jd_auth_dict['access_token'] = response_dict['access_token']
            jd_auth_dict['expires_in'] = int(response_dict['expires_in']) // 1000
            jd_auth_dict['refresh_token'] = response_dict['refresh_token']
            jd_auth_dict['auth_start_time'] = int(response_dict['time']) // 1000
            jd_auth_dict['auth_end_time'] = (int(response_dict['time']) + int(response_dict['expires_in'])) // 1000
            jd_auth_dict['uid'] = response_dict['uid']
        # 其他未知情况处理
        else:
            logger.warning(f'jd auth info is {response_dict}')
        return jd_auth_dict

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


class AccountLoginView(View):
    """
    用户登录
    """

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        remember = request.POST.get("remember")  # 暂时先不处理

        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            user_obj = JdAuthUserModel.objects.filter(user__username=username).first()
            if not user_obj:
                jd_web_auth_obj = JdWebAuthorized()
                redirect_url = jd_web_auth_obj.get_code_url()
                return JsonResponse({"errcode": -2, "errmsg": "请重新授权", "redirect_url": redirect_url})
            # 检测用户是否绑定授权店铺
            return JsonResponse({"errcode": 0, "errmsg": "登录成功"})
        else:
            return JsonResponse({"errcode": -1, "errmsg": "用户名或者密码错误"})


class AccountLogOutView(View):
    def get(self, request):
        logout(request)
        return redirect("/user/account_login")


class ChangePasswordView(View):
    """
    修改密码，忘记密码
    """

    def post(self, request, *args, **kwargs):
        phone = request.POST.get('phone')
        code = request.POST.get('code')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')

        if not all([phone, code, password, repassword]):
            return JsonResponse({"errcode": -1, "errmsg": "参数不完整"})

        if password != repassword:
            return JsonResponse({"errcode": -1, "errmsg": "两次密码输入不一致"})

        try:
            user = User.objects.get(
                Q(username=phone) | Q(phone=phone))
        except User.DoesNotExist:
            # 用户名不存在
            user = None

        if user:
            user.set_password(password)
            user.save()

            return JsonResponse({"errcode": 0, "errmsg": "密码重置成功"})

        else:
            return JsonResponse({"errcode": -1, "errmsg": "用户不存在，请注册再使用"})


def page_not_found(request):
    # 全局404处理函数
    response = render_to_response('404.html', {})
    response.status_code = 404  # 这个状态码会影响浏览器的显示
    return response


def server_error(request):
    # 全局500处理函数
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
