from django.db import models


# Create your models here.


class SkuInfoModel(models.Model):
    """
    店铺内所有商品对应的sku信息
    """

    sku_id = models.CharField(default='', primary_key=True, max_length=16, verbose_name='SKU_ID', help_text='商品SKU_ID')
    ware_info = models.ForeignKey('WareInfoModel', on_delete=models.CASCADE, verbose_name='商品ware信息',
                                  to_field='ware_id', help_text='商品ware信息')
    status = models.CharField(default='0', choices=(
        ('0', '---'),
        ('1', '上架'),
        ('2', '下架'),
        ('4', '删除')
    ), max_length=2, verbose_name='SKU状态', help_text='SKU状态')
    jd_price = models.IntegerField(default=0, verbose_name='京东价', help_text='京东价')
    sale_attrs_json = models.TextField(default='', verbose_name='销售属性集合', help_text='销售属性集合')
    features_json = models.TextField(default='', verbose_name='特殊属性集合', help_text='特殊属性集合')
    outer_id = models.CharField(default='', max_length=64, verbose_name='外部ID', help_text='外部ID')
    bar_code = models.CharField(default='', max_length=128, verbose_name='SKU条形码', help_text='SKU条形码')
    cate_id = models.IntegerField(default=0, verbose_name='类目ID', help_text='类目ID')
    img_tag = models.IntegerField(default=0, verbose_name='图片标签', help_text='图片标签')
    logo = models.CharField(default='', max_length=128, verbose_name='sku颜色的主图', help_text='sku颜色的主图')
    sku_name = models.CharField(default='', max_length=128, verbose_name='sku名称', help_text='sku名称')
    stock_num = models.IntegerField(default=0, verbose_name='总库存数', help_text='总库存数')
    fixed_delivery_time = models.CharField(default='', max_length=32,
                                           verbose_name='大件商品固定发货时效 格式：订单开始日期,订单结束日期,发货日期,完成发货天数',
                                           help_text='大件商品固定发货时效 格式：订单开始日期,订单结束日期,发货日期,完成发货天数')
    relative_delivery_time = models.CharField(default='', max_length=32, verbose_name='大件商品相对发货时效（完成发货天数）',
                                              help_text='大件商品相对发货时效（完成发货天数）')
    parent_id = models.IntegerField(default=0, verbose_name='父ID', help_text='父ID')
    modified_time = models.CharField(default='', max_length=32, verbose_name='修改时间', help_text='修改时间')
    created_time = models.CharField(default='', max_length=32, verbose_name='创建时间', help_text='创建时间')
    multi_cate_props_json = models.TextField(verbose_name='多级SKU属性', help_text='多级SKU属性')
    props_json = models.TextField(default='', verbose_name='SKU属性', help_text='SKU属性')
    capacity = models.CharField(default='', max_length=8, verbose_name='容量，在有特殊要求的类目下必填！最多支持6位小数。',
                                help_text='容量，在有特殊要求的类目下必填！最多支持6位小数。')

    class Meta:
        verbose_name = verbose_name_plural = 'SKU信息'
        db_table = 'jd_sku_info'

    def __str__(self):
        return f'{self.sku_id}'


class WareInfoModel(models.Model):
    """
    店铺列表中的所有商品ware信息
    """

    ware_id = models.CharField(primary_key=True,max_length=32, verbose_name='商品ID', help_text='商品唯一ID')
    title = models.CharField(default='', max_length=255, verbose_name='商品名称', help_text='商品名称')
    ad_title = models.CharField(default='', max_length=255, verbose_name='商品广告词', help_text='商品广告词')
    item_num = models.CharField(default='', max_length=32, verbose_name='商品货号', help_text='商品货号')
    status = models.CharField(default='0', choices=(
        ('0', '---'),
        ('1', '从未上架'),
        ('2', '自主下架'),
        ('4', '系统下架'),
        ('8', '上架'),
        ('513', '从未上架待审'),
        ('514', '自主下架待审'),
        ('516', '系统下架待审'),
        ('520', '上架待审核'),
        ('1028', '系统下架审核失败')
    ), max_length=4, help_text='商品状态', verbose_name='商品状态')
    off_time = models.CharField(default='', max_length=16, verbose_name='商品下架时间', help_text='商品下架时间')
    on_time = models.CharField(default='', max_length=16, verbose_name='商品上架时间', help_text='商品上架时间')
    cate_id = models.IntegerField(default=0, verbose_name='类目ID', help_text='类目ID')
    colType = models.IntegerField(default=0, verbose_name='合作类型', help_text='合作类型')
    brand_id = models.IntegerField(default=0, verbose_name='品牌ID', help_text='品牌ID')
    template_id = models.IntegerField(default=0, verbose_name='关联板式id', help_text='关联板式id ')
    transport_id = models.IntegerField(default=0, verbose_name='运费模板ID', help_text='运费模板ID')
    outer_id = models.CharField(default='', max_length=16, verbose_name='外部ID', help_text='外部ID')
    bar_code = models.CharField(default='', max_length=32, verbose_name='条形码', help_text='条形码')
    ware_location = models.IntegerField(default=0, verbose_name='商品产地', help_text='商品产地 ')
    modified_time = models.CharField(default='', max_length=16, verbose_name='商品最后一次修改时间',
                                     help_text='商品最后一次修改时间')
    created_time = models.CharField(default='', max_length=16, verbose_name='商品创建时间，只读属性',
                                    help_text='商品创建时间，只读属性')
    delivery = models.CharField(default='', max_length=255, verbose_name='发货地', help_text='发货地')
    wrap = models.CharField(default='', max_length=255, verbose_name='包装规格', help_text='包装规格')
    pack_listing = models.CharField(default='', max_length=255, verbose_name='包装清单', help_text='包装清单')
    weight = models.IntegerField(default=0, verbose_name='重', help_text='重')
    width = models.IntegerField(default=0, verbose_name='宽', help_text='宽')
    height = models.IntegerField(default=0, verbose_name='高', help_text='高')
    length = models.IntegerField(default=0, verbose_name='长', help_text='长')
    props_json = models.TextField(default='', verbose_name='商品属性', help_text='商品属性')
    features_json = models.TextField(default='', verbose_name='特殊属性集合', help_text='特殊属性集合')
    images_json = models.TextField(default='', verbose_name='商品图片', help_text='商品图片')
    shop_categorys_json = models.TextField(verbose_name='店内分类', help_text='店内分类')
    mobile_desc = models.TextField(default='', verbose_name='移动端详情介绍', help_text='移动端详情介绍')
    introduction = models.TextField(default='', verbose_name='PC端详情介绍', help_text='PC端详情介绍')
    zhuang_ba_introduction = models.TextField(verbose_name='装吧详情介绍', help_text='装吧详情介绍')
    zhuang_ba_id = models.BigIntegerField(default=0, verbose_name='装吧ID', help_text='商品描述装吧实例ID')
    introduction_use_flag = models.CharField(default='0', choices=(
        ('0', '使用默认的商品描述'),
        ('1', '使用装吧商详')
    ), max_length=2, verbose_name='商品描述使用标识', help_text='商品描述使用标识')
    after_sales = models.TextField(default='', verbose_name='售后服务', help_text='售后服务')
    logo = models.CharField(default='', max_length=128, verbose_name='商品主图', help_text='商品主图')
    market_price = models.IntegerField(default=0, verbose_name='市场价', help_text='市场价')
    cost_price = models.IntegerField(default=0, verbose_name='成本价', help_text='成本价')
    jd_price = models.IntegerField(default=0, verbose_name='京东价', help_text='京东价')
    brand_name = models.CharField(default='', max_length=128, verbose_name='品牌名称', help_text='品牌名称')
    stock_num = models.IntegerField(default=0, verbose_name='总库存数', help_text='总库存数')
    cate_sec_id = models.IntegerField(default=0, verbose_name='二级叶子类目', help_text='二级叶子类目')
    shop_id = models.IntegerField(default=0, verbose_name='店铺ID', help_text='店铺ID')
    promise_id = models.IntegerField(default=0, verbose_name='时效模板ID', help_text='时效模板ID')
    multi_category_id = models.IntegerField(default=0, verbose_name='四级类目ID', help_text='四级类目ID')
    multi_cate_props_json = models.TextField(verbose_name='四级类目属性列表', help_text='四级类目属性列表')
    sell_point = models.CharField(default='', max_length=128, verbose_name='卖点', help_text='卖点')
    ware_tax_json = models.TextField(default='', verbose_name='税率', help_text='税率')
    after_sale_desc = models.TextField(default='', verbose_name='售后图文详情', help_text='售后图文详情')
    zhuang_ba_mobile_desc = models.TextField(default='', verbose_name='移动版装吧商详', help_text='移动版装吧商详')
    mobile_zhuang_ba_id = models.BigIntegerField(default=0, verbose_name='移动版装吧实例ID', help_text='移动版装吧实例ID')
    mobile_desc_use_flag = models.CharField(default='0', choices=(
        ('0', '使用默认的移动商详'),
        ('1', '使用装吧移动版商详')
    ), max_length=2, verbose_name='移动版商品描述使用标识', help_text='移动版商品描述使用标识')
    fit_case_html_pc = models.TextField(default='', verbose_name='装修案例PC版描述', help_text='装修案例PC版描述')
    fit_case_html_app = models.TextField(default='', verbose_name='装修案例移动版描述', help_text='装修案例移动版描述')
    special_services = models.CharField(default='', max_length=255,
                                        verbose_name='特色服务,装修类目才可填写,装修类必填,最大为5,每个值最长为8个字符',
                                        help_text='特色服务,装修类目才可填写,装修类必填,最大为5,每个值最长为8个字符')
    parent_id = models.IntegerField(default=0, verbose_name='商品父ID', help_text='商品父ID')
    ware_group_id = models.IntegerField(default=0, verbose_name='商品分组ID', help_text='商品分组ID')
    business_type = models.CharField(default='', max_length=64, verbose_name='商品业务类型', help_text='商品业务类型')
    design_concept = models.CharField(default='', max_length=128, verbose_name='商品设计理念,适用范围是toplife类目',
                                      help_text='商品设计理念,适用范围是toplife类目')
    is_archival = models.BooleanField(default=False, verbose_name='是否归档商品', help_text='是否归档商品')

    class Meta:
        verbose_name = verbose_name_plural = '商品ware信息'
        db_table = 'jd_ware_info'

    def __str__(self):
        return f'{self.ware_id}'
