from django.db import models

# Create your models here.


class RankMonitorModel(models.Model):
    """
    排名监控
    """

    goods_id = models.IntegerField(default='', verbose_name='商品ID', help_text='京东商品的SPU_ID')
    goods_name = models.CharField(default='', max_length=255, verbose_name='商品名称', help_text='商品名称')
    web_rank = models.CharField(default='', max_length=64, verbose_name='Web端排名信息', help_text='Web端排名信息')
    web_rank_diff = models.IntegerField(default=0, verbose_name='Web端排名差值', help_text='Web端排名差值')
    wap_rank = models.CharField(default='', max_length=64, verbose_name='Wap端排名信息', help_text='Wap端排名信息')
    wap_rank_diff = models.IntegerField(default=0, verbose_name='Wap端排名差值', help_text='Wap端排名差值')
    wx_rank = models.CharField(default='', max_length=64, verbose_name='Wx端排名信息', help_text='Wx端排名信息')
    wx_rank_diff = models.IntegerField(default=0, verbose_name='Wx端排名差值', help_text='Wx端排名差值')
    qq_rank = models.CharField(default='', max_length=64, verbose_name='QQ端排名信息', help_text='QQ端排名信息')
    qq_rank_diff = models.IntegerField(default=0, verbose_name='QQ端排名差值', help_text='QQ端排名差值')
    keyword = models.CharField(default='', max_length=255, verbose_name='关键词', help_text='关键词')
    cate_id = models.CharField(default='', max_length=16, verbose_name='类目ID组合', help_text='类目ID组合')
    cate_name = models.CharField(default='', max_length=255, verbose_name='类目名称', help_text='类目名称')
    sku_id = models.IntegerField(default=0, verbose_name='商品SKU_ID', help_text='京东商品SKU_ID，SPU_ID对应下的多个SKU_ID')
    sku_name = models.CharField(default='', max_length=255, verbose_name='SKU名称', help_text='SKU名称')
    is_monitor = models.BooleanField(default=False, verbose_name='是否已监控', help_text='是否已监控')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')

    class Meta:
        managed = True
        verbose_name = verbose_name_plural = '排名监控'
        db_table = 'rank_monitor'
        ordering = ['-updated_time']
        unique_together = (('goods_id', 'updated_time'),)

    def __str__(self):
        return self.goods_id