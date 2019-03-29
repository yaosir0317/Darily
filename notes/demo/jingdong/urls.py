"""jingdong URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include, re_path
from django.views.static import serve
from rest_framework.documentation import include_docs_urls

# from jingdong.settings import MEDIA_ROOT, STATIC_ROOT

urlpatterns = [
    # path('api-auth/', include('rest_framework.urls')),
    # drf文档，title自定义
    path('docs/', include_docs_urls(title='京东')),
    # 生产环境开启配置
    # re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # re_path(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),
    # 控制台及首页
    path('', include('jd_dashboard.urls')),
    # 用户中心
    re_path('user/', include('jd_user.urls')),
    # Dashboard应用页面
    re_path('jd_dashboard/', include('jd_dashboard.urls')),
    # 京东监控中心
    re_path('jd_monitor/', include('jd_monitor.urls')),
]

# 全局404页面配置
handler404 = 'jd_user.views.page_not_found'

# 全局500页面配置
handler500 = 'jd_user.views.server_error'
