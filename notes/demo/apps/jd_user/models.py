from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfileModel(AbstractUser):
    """
    平台自主用户
    """

    nick_name = models.CharField(default='', max_length=128, verbose_name='用户名称', help_text='用户注册平台的昵称')
    phone = models.CharField(default='', max_length=11, verbose_name='手机号', help_text='手机号')
    nickname = models.CharField(default='', max_length=50, blank=True, verbose_name='昵称', help_text='昵称')

    class Meta:
        verbose_name = verbose_name_plural = '平台自主用户表'
        db_table = 'jd_user'

    def __str__(self):
        return self.username


class JdAuthUserModel(models.Model):
    """
    京东授权用户表
    """

    shop = models.ForeignKey('jd_shop.JdShopInfoModel', db_column='shop_id', on_delete=models.CASCADE,
                             verbose_name='店铺ID', help_text='店铺ID')
    user = models.ForeignKey('UserProfileModel', db_column='user_id', on_delete=models.CASCADE, verbose_name='用户ID',
                             help_text='用户ID')
    uid = models.CharField(default='', max_length=128, null=False, verbose_name='用户唯一ID',
                           help_text='用户唯一ID')
    user_name = models.CharField(default='', max_length=128, verbose_name='授权用户名称',
                                 help_text='授权使用应用时的用户名称，包括子账户名称')
    item_code = models.CharField(default='', max_length=32, verbose_name='应用服务编码', help_text='应用服务编码')
    article_num = models.IntegerField(default=0, verbose_name='未知', help_text='不确定作用')
    version_no = models.IntegerField(default=0, verbose_name='版本号', help_text='版本号')
    app_end_date = models.IntegerField(default=0, verbose_name='服务到期时间', help_text='服务到期时间')
    access_token = models.CharField(default='', max_length=128, verbose_name='令牌Token', help_text='令牌Token')
    refresh_token = models.CharField(default='', max_length=128, verbose_name='令牌刷新凭证', help_text='令牌刷新凭证')
    expires_in = models.IntegerField(default=0, verbose_name='令牌Token失效时间', help_text='令牌Token失效时间')
    auth_start_time = models.IntegerField(default=0, verbose_name='服务登录授权时间点', help_text='服务登录授权时间点')
    auth_end_time = models.IntegerField(default=0, verbose_name='服务登录授权到期时间点', help_text='服务登录授权到期时间点')
    is_first_sync = models.BooleanField(default=True, verbose_name='是否是第一次同步数据', help_text='是否是第一次同步数据')

    class Meta:
        verbose_name = verbose_name_plural = '京东授权用户表'
        db_table = 'jd_auth_user'

    def __str__(self):
        return self.user_name


class VerifyCode(models.Model):
    """
    验证码
    """
    code = models.CharField(default='', max_length=10, verbose_name='验证码', help_text='验证码')
    phone = models.CharField(default='', max_length=11, verbose_name='电话', help_text='电话')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间', help_text='添加时间')

    class Meta:
        managed = True
        db_table = 'jd_verify_code'
        verbose_name = "短信验证"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
