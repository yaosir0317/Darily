#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2019/1/20

from django.urls import path
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from .views import BaseView

app_name = 'dashboard'

urlpatterns = [
    # 初始页
    path('', BaseView.as_view(), name='base'),
    # index内容基础模板页面，过渡页面
    path('index', TemplateView.as_view(template_name='index.html'), name='index'),
    # 系统主题配置, layuiadmin自动查询默认的路径
    path('theme.html', TemplateView.as_view(template_name=''), name='theme'),
    # 系统侧面板, layuiadmin自动查询默认的路径
    path('about.html', TemplateView.as_view(template_name=''), name='about'),
    # home首页
    path('home.html', login_required(TemplateView.as_view(template_name='home.html'), login_url=settings.LOGIN_URL),
         name='home'),
]
