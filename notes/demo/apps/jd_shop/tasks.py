from __future__ import absolute_import, unicode_literals
import logging

from jd_user.models import JdAuthUserModel
from jingdong import celery_app
from celery import chain, group

from jd_sdk.apis import JdShopApi
from jd_sdk.sdk import JdSdk
from jd_shop.models import JdCategoryModel, JdShopInfoModel

logger = logging.getLogger('jd_shop')


@celery_app.task()
def task_update_shop_info(access_token):
    """
    更新店铺信息
    :param access_token:
    :return:
    """

    jd_api = JdSdk()
    _, ret = jd_api.send_request({"method": JdShopApi.JD_SHOP_INFO_V_1, "access_token": access_token})
    response_name = JdShopApi.JD_SHOP_INFO_V_1.replace('.', '_')
    shop_response = ret.get(f'{response_name}_responce')
    data = shop_response.get('shop_jos_result')
    if shop_response.get('code') == '0':
        shop_id = data.pop('shop_id')
        JdShopInfoModel.objects.update_or_create(shop_id=shop_id, defaults=data)
        return access_token


@celery_app.task()
def task_update_shop_category(access_token):
    """
    更新店铺类目
    :param access_token:
    :return:
    """
    if access_token:
        jd_api = JdSdk()
        _, cate_ret = jd_api.send_request({"method": JdShopApi.JD_SHOP_ALL_CATE_V_1, "access_token": access_token})
        cate_response_name = JdShopApi.JD_SHOP_ALL_CATE_V_1.replace('.', '_')

        cate_response = cate_ret.get(f'{cate_response_name}_responce')

        if cate_response.get('code') == '0' and cate_response.get('shopCategoryResult').get('is_success'):
            shop_category_list = cate_response.get('shopCategoryResult').get('shop_category_list')
            for shop_category in shop_category_list:
                cid = shop_category.pop('cid')
                shop_info_id = shop_category.pop('shop_id')
                shop_category['shop_info_id'] = shop_info_id
                JdCategoryModel.objects.update_or_create(cid=cid, defaults=shop_category)


@celery_app.task()
def task_shop_info(access_token_list=None):
    """
    获取所有用户的店铺信息并更新
    """
    if not access_token_list:  # 查询所有用户的非空token
        access_token_list = JdAuthUserModel.objects.exclude(access_token='').values(
            'access_token')
    group(
        (chain(task_update_shop_info.s(access_token_info.get('access_token'), ), task_update_shop_category.s()) for
         access_token_info in
         access_token_list)
    )()
