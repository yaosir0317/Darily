#!/usr/bin/env python
# *_* coding: UTF-8 *_*

"""
@author: Siffre@三弗 
@contact: Siffre@aliyun.com

@version: 1.0
@license: Apache Licence
@file: apis.py
@time: 2019/1/17 9:58 PM
"""


class JdSignApi(object):
    """
    京东签名相关接口集合
    """

    # 签名基础接口
    JD_SIGN_API_V_1 = 'https://api.jd.com/routerjson?v=2.0'


class JdShopApi(object):
    """
    京东店铺相关接口集合
    """

    # 查询商家基本店铺信息，包括商家编号,店铺编号,店铺名称,开店时间,logoUrl,店铺简介,主营类目编号,主营类目名称
    # 文档地址：http://jos.jd.com/api/detail.htm?id=494
    JD_SHOP_INFO_V_1 = 'jingdong.vender.shop.query'

    # 获取商家所有的店内分类
    # 文档地址：http://jos.jd.com/api/detail.htm?apiName=jingdong.vender.shopcategory.findShopCategoriesByVenderId&id=2801
    JD_SHOP_ALL_CATE_V_1 = 'jingdong.vender.shopcategory.findShopCategoriesByVenderId'


class JdWareApi(object):
    """
    京东商品ware相关接口
    """

    # 获取所有商品ware数据--搜索过滤接口
    # 文档地址：https://jos.jd.com/api/detail.htm?id=1587
    JD_WARE_LIST_V_1 = 'jingdong.ware.read.searchWare4Valid'

    # 获取商品ware详情数据，根据ware结构体中的字段返回对应的信息
    # 文档地址：https://jos.jd.com/api/detail.htm?id=1244
    JD_WARE_DETAIL_V_1 = 'jingdong.ware.read.findWareById'

    # 获取指定商品wareId的广告词，多个sku_id对应一个广告词
    JD_AD_TITLE_V_1 = ''


class JdSkuApi(object):
    """
    京东商品ware对应的sku相关接口
    """

    # 获取所有商品ware对应的sku列表数据--搜索过滤接口
    # 文档地址： https://jos.jd.com/api/detail.htm?id=1227
    JD_SKU_LIST_V_1 = 'jingdong.sku.read.searchSkuList'

    # 获取商品SKU详情，根据sku结构体中的字段返回对应的信息
    # 文档地址：https://jos.jd.com/api/detail.htm?id=1223
    JD_SKU_DETAIL_V_1 = 'jingdong.sku.read.findSkuById'
