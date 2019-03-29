#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2019/2/2

from django.urls import path
from django.views.generic import TemplateView

from .views import (
    JdRedirectUrlView, AccountLoginView,
    ChangePasswordView, AccountLogOutView
)

from .rest_views import SmsCodeView, UserView

app_name = 'jd_user'

urlpatterns = [
    # 京东应用回调地址
    path('jd_redirect_url', JdRedirectUrlView.as_view(), name='jd_redirect_url'),
    # 账户登录API
    path('account_login', AccountLoginView.as_view(), name='account_login'),
    # 账户注册API
    path('account_register', UserView.as_view({'post': 'create'}), name='account_register'),
    # 修改密码API
    path('change_password', ChangePasswordView.as_view(), name='change_password'),
    # 退出登陆API
    path('account_logout', AccountLogOutView.as_view(), name='account_logout'),
    # 手机验证码API
    path('code', SmsCodeView.as_view({'post': 'create'})),
    # 用户注册API
    path('user_create', UserView.as_view({'post': 'create'})),
    # 登陆
    path('login.html', TemplateView.as_view(template_name='login.html'), name='login'),
    # 忘记密码
    path('forgot.html', TemplateView.as_view(template_name='forgot.html'), name='forgot'),
    # 注册
    path('register.html', TemplateView.as_view(template_name='register.html'), name='register')

]
