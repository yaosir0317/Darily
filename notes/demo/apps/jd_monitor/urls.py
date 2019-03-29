#!/usr/bin/env python
# *_* coding: UTF-8 *_*

"""
@author: Siffre@三弗 
@contact: Siffre@aliyun.com

@version: 1.0
@license: Apache Licence
@file: urls.py
@time: 2019/1/13 11:03 AM


 　　　　　　　 ┏┓　 ┏┓+ +
 　　　　　　　┏┛┻━━━┛┻┓ + +
 　　　　　　　┃　　　　　　┃ 　
 　　　　　　　┃　　　━　　 ┃ ++ + + +
 　　　　　　 ████━████  ┃+
 　　　　　　　┃　　　　　　　┃ +
 　　　　　　　┃　　　┻　　　┃
 　　　　　　　┃　　　　　　┃ + +
 　　　　　　　┗━┓　　　┏━┛
 　　　　　　　　 ┃　　　┃　　　　　　　　　　　
 　　　　　　　　 ┃　　　┃ + + + +
 　　　　　　　　 ┃　　　┃　　　　Code is far away from bug with the animal protecting　　　　　　　
 　　　　　　　　 ┃　　　┃ + 　　　　神兽保佑,代码无bug　　
 　　　　　　　　 ┃　　　┃
 　　　　　　　　 ┃　　　┃　　+　　　　　　　　　
 　　　　　　　　 ┃　 　 ┗━━━┓ + +
 　　　　　　　　 ┃ 　　　　   ┣┓
 　　　　　　　　 ┃ 　　　　　 ┏┛
 　　　　　　　　 ┗┓┓┏━┳┓┏┛ + + + +
 　　　　　　　　  ┃┫┫ ┃┫┫
 　　　　　　　　  ┗┻┛ ┗┻┛+ + + +
           
"""

from django.urls import path

from .views.rank_monitor import RankMonitorListView, RankMonitorCreateView, RankMonitorUpdateView, RankMonitorRetrieveView, \
    RankMonitorDeleteView

app_name = 'jd_monitor'

urlpatterns = [
    # 关键词排名监控
    # 监控列表
    path('rank_monitor_list', RankMonitorListView.as_view(), name='rank_monitor_list'),
    # 添加监控信息
    path('rank_monitor_create', RankMonitorCreateView.as_view(), name='rank_monitor_create'),
    # 监控内容更新
    path('rank_monitor_update/<goods_id>', RankMonitorUpdateView.as_view(), name='rank_monitor_update'),
    # 监控内容删除
    path('rank_monitor_delete/<goods_id>', RankMonitorDeleteView.as_view(), name='rank_monitor_delete'),
    # 查看某条监控的具体内容
    path('rank_monitor_obj/<goods_id>', RankMonitorRetrieveView.as_view(), name='rank_monitor_obj')
]
