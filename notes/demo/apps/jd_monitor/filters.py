import django_filters

from .models import RankMonitorModel


class RankMonitorListFilter(django_filters.rest_framework.FilterSet):
    """
    过滤的类
    """

    goods_id = django_filters.CharFilter(help_text='商品ID')
    is_monitor = django_filters.BooleanFilter(help_text='是否已监控：布尔值：False/True')

    class Meta:
        model = RankMonitorModel
        fields = ['goods_id', 'is_monitor']
