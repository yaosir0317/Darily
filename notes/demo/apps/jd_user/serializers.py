import re
import base64
from datetime import datetime, timedelta
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework import status

from .models import VerifyCode, JdAuthUserModel
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    """
    短信验证码
    """
    phone = serializers.CharField(max_length=11, help_text='手机号')

    # 函数名必须：validate + 验证字段名
    def validate_phone(self, phone):
        """
        手机号码验证
        """
        # 是否已经注册
        if User.objects.filter(phone=phone).count():
            raise serializers.ValidationError('用户已经存在', code=status.HTTP_200_OK)

        # 是否合法
        if not re.match(settings.REGEX_MOBILE, phone):
            raise serializers.ValidationError('手机号码非法', code=status.HTTP_200_OK)

        # 验证码发送频率
        # 60s内只能发送一次
        one_minutes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_minutes_ago, phone=phone).count():
            raise serializers.ValidationError('距离上一次发送未超过60s', code=status.HTTP_200_OK)

        return phone


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情
    """

    class Meta:
        model = User
        fields = '__all__'


class UserRegSerializer(serializers.ModelSerializer):
    """
    用户注册
    """
    # PddUser中没有code字段，这里需要自定义一个code字段
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, label='验证码',
                                 error_messages={
                                     'blank': '请输入验证码',
                                     'required': '请输入验证码',
                                     'max_length': '验证码格式错误',
                                     'min_length': '验证码格式错误'
                                 },
                                 help_text='验证码')
    # 图片验证码
    # img_code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, label='图片验证码',
    #                                    error_messages={
    #                                        'blank': '请输入图片验证码',
    #                                        'required': '请输入图片验证码',
    #                                        'max_length': '图片验证码格式错误',
    #                                        'min_length': '图片验证码格式错误'
    #                                    }, help_text='图片验证码')
    # 图片验证码ID
    # img_code_id = serializers.CharField(required=True, write_only=True, label='图片验证码ID', help_text='图片验证码ID')
    # 验证用户名是否存在
    username = serializers.CharField(label='手机号', help_text='手机号', required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message='该手机号已经注册')])

    # 输入密码的时候不显示明文
    password = serializers.CharField(
        style={'input_type': 'password'}, label='密码', write_only=True, help_text='密码'
    )

    # 密码加密保存
    def create(self, validated_data):
        user = super(UserRegSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    # 验证短信code
    def validate_code(self, code):
        # 用户注册，已post方式提交注册信息，post的数据都保存在initial_data里面
        # username就是用户注册的手机号，验证码按添加时间倒序排序，为了后面验证过期，错误等

        verify_records = VerifyCode.objects.filter(phone=self.initial_data['phone']).order_by('-add_time')

        if verify_records:
            # 最近的一个验证码
            last_record = verify_records[0]
            # 有效期为五分钟。
            five_minutes_ago = datetime.now() - timedelta(hours=0, minutes=settings.CODE_VERIFICATION_TIME, seconds=0)
            if five_minutes_ago > last_record.add_time:
                return serializers.ValidationError(detail='验证码过期', code=status.HTTP_200_OK)

            if last_record.code != code:
                raise serializers.ValidationError(detail='验证码错误', code=status.HTTP_200_OK)

        else:
            raise serializers.ValidationError(detail='验证码错误', code=status.HTTP_200_OK)

    def validate(self, attr):
        attr['phone'] = attr['username']
        # code是自己添加得，数据库中并没有这个字段，验证完就删除掉
        del attr['code']
        # del attr['img_code_id']
        # del attr['img_code']
        return attr

    class Meta:
        model = User
        fields = ('username', 'code', 'password')
