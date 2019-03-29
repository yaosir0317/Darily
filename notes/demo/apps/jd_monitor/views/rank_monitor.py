#!/usr/bin/env python
# *_* coding: UTF-8 *_*

"""
@author: Siffre@三弗 
@contact: Siffre@aliyun.com

@version: 1.0
@license: Apache Licence
@file: rank_monitor.py
@time: 2019/1/13 12:34 PM


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

from collections import OrderedDict

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from ..serializers.rank_serializer import RankMonitorSerializer
from ..models import RankMonitorModel
from ..filters import RankMonitorListFilter


class RankMonitorPagination(PageNumberPagination):
    """
    列表自定义分页
    """
    # 默认每页显示的个数
    page_size = 12
    # 可以动态改变每页显示的个数
    page_size_query_param = 'page_size'
    page_size_query_description = '每页大小'
    # 页码参数
    page_query_param = 'page'
    page_query_description = '页码'
    # 最多能显示多少页
    max_page_size = 20

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
            ('total', len(data)),
            ('message', '请求成功')
        ]), status=status.HTTP_200_OK)


class RankMonitorSearchFilter(filters.SearchFilter):
    """
    自定义搜索
    """

    search_title = '搜索过滤'
    search_description = '根据某些字段进行搜索过滤: goods_id,is_monitor'


class RankMonitorOrderingFilter(filters.OrderingFilter):
    """
    自定义排序
    """

    ordering_title = '排序过滤'
    ordering_description = '根据某些字段进行排序: updated_time,goods_id'


class RankMonitorListView(generics.ListAPIView):
    """
    排名监控列表
    """

    pagination_class = RankMonitorPagination
    queryset = RankMonitorModel.objects.all()
    serializer_class = RankMonitorSerializer
    filter_backends = (DjangoFilterBackend, RankMonitorSearchFilter, RankMonitorOrderingFilter)
    # 过滤
    filter_class = RankMonitorListFilter
    # 搜索
    search_fields = ('goods_id', 'is_monitor')
    # 排序
    ordering_fields = ('updated_time', 'goods_id')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class RankMonitorCreateView(generics.CreateAPIView):
    """
    排名监控添加
    """

    queryset = RankMonitorModel.objects.all()
    serializer_class = RankMonitorSerializer


class RankMonitorUpdateView(generics.UpdateAPIView):
    """
    排名监控内容更新或局部更新
    """

    lookup_field = 'goods_id'
    queryset = RankMonitorModel.objects.all()
    serializer_class = RankMonitorSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response({
            'message': '更新成功',
            'result': serializer.data
        }, status=status.HTTP_200_OK)


class RankMonitorRetrieveView(generics.RetrieveAPIView):
    """
    单条监控内容详情获取
    """

    lookup_field = 'goods_id'
    queryset = RankMonitorModel.objects.all()
    serializer_class = RankMonitorSerializer


class RankMonitorDeleteView(generics.DestroyAPIView):
    """
    删除某条监控内容
    """

    lookup_field = 'goods_id'
    queryset = RankMonitorModel.objects.all()
    serializer_class = RankMonitorSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': '删除成功'}, status=status.HTTP_200_OK)
