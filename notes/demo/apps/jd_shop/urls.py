#!/usr/bin/env python
# *_* coding: UTF-8 *_*

from django.urls import path

from .views.shop_info import ShopInfoView

app_name = 'jd_shop'

urlpatterns = [
    # 添加商店信息

    path('shop_info', ShopInfoView.as_view(), name='shop_info'),

]
