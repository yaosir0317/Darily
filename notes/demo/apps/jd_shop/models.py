from django.db import models


# Create your models here.
# TODO 京东店铺后台接口


class JdShopInfoModel(models.Model):
    """
    京东店铺信息
    """

    shop_id = models.IntegerField(primary_key=True, verbose_name='店铺ID', help_text='店铺唯一ID')
    shop_name = models.CharField(default='', max_length=64, verbose_name='店铺名称', help_text='店铺名称')
    open_time = models.CharField(default='', max_length=64, verbose_name='开店时间', help_text='开店时间')
    vender_id = models.IntegerField(default=0, verbose_name='商家编号', help_text='商家编号')
    brief = models.TextField(default='', verbose_name='商家简介', help_text='商家简介')
    logo_url = models.CharField(default='', max_length=128, verbose_name='商家Logo', help_text='商家Logo')
    category_main = models.IntegerField(default=0, verbose_name='主营类目ID', help_text='主营类目ID')
    category_main_name = models.CharField(default='', max_length=64, verbose_name='主营类目名称', help_text='主营类目名称')

    class Meta:
        verbose_name = verbose_name_plural = '店铺基础信息'
        db_table = 'jd_shop_info'

    def __str__(self):
        return str(self.shop_id)


class JdCategoryModel(models.Model):
    """
    京东商家后台类目
    """
    cid = models.IntegerField(primary_key=True)
    create_time = models.CharField(default='', max_length=13, verbose_name='创建时间', help_text='创建时间')

    is_home_show = models.BooleanField(default=False)
    is_open = models.BooleanField(default=False)
    modify_time = models.CharField(default='', max_length=13, verbose_name='更新时间', help_text='更新时间')
    name = models.CharField(default='', max_length=64, verbose_name='店类分类名称', help_text='店类分类名称')
    order_no = models.IntegerField(default=0)
    parent_cid = models.IntegerField(default=0)
    shop_info = models.ForeignKey('JdShopInfoModel', related_name='shop_info', on_delete=models.CASCADE,
                                  to_field='shop_id', verbose_name='店铺信息', help_text='店铺信息')
    status = models.SmallIntegerField(default=1)
    vender_id = models.IntegerField(default=0, verbose_name='商家编号', help_text='商家编号')

    class Meta:
        verbose_name = verbose_name_plural = '京东后台类目信息'
        db_table = 'jd_category'

    def __str__(self):
        return ''
