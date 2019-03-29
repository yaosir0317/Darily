#!/usr/bin/env python
# *_* coding: UTF-8 *_*

from django.urls import path

from .views.product_info import ProductView

app_name = 'jd_product'

urlpatterns = [
    # 添加商品信息
    path('product_info', ProductView.as_view(), name='product_info'),

]
