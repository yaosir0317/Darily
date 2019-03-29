from __future__ import absolute_import, unicode_literals
import logging
import json
from datetime import datetime, timedelta
from jd_user.models import JdAuthUserModel

from jingdong import celery_app
from celery import group

from jd_sdk.apis import JdWareApi, JdSkuApi
from jd_sdk.sdk import JdSdk
from jd_sdk.authorized import JdWebAuthorized
from jd_product.models import WareInfoModel, SkuInfoModel

logger = logging.getLogger('jd_product')


@celery_app.task()
def update_ware_info(access_token, is_first_sync, page_num=1):
    jd_api = JdSdk()
    count = 1
    now = datetime.now()
    zero_yesterday = now - timedelta(days=1, hours=now.hour, minutes=now.minute, seconds=now.second,
                                     microseconds=now.microsecond)

    def create_or_update_ware_info(data):
        for item in data:
            ware_info = {}
            ware_info['title'] = item.get('title')
            ware_info['ad_title'] = item.get('adWords', {}).get('words', '')
            ware_info['item_num'] = item.get('itemNum')
            ware_info['status'] = item.get('wareStatus')
            ware_info['off_time'] = item.get('offlineTime', '')
            ware_info['on_time'] = item.get('onlineTime')
            ware_info['cate_id'] = item.get('categoryId')
            ware_info['colType'] = item.get('colType')
            ware_info['brand_id'] = item.get('brandId')
            ware_info['template_id'] = item.get('templateId')
            ware_info['transport_id'] = item.get('transportId')
            ware_info['outer_id'] = item.get('outerId')
            ware_info['bar_code'] = item.get('barCode')
            ware_info['ware_location'] = item.get('wareLocation')
            ware_info['modified_time'] = item.get('modified')
            ware_info['created_time'] = item.get('created')
            ware_info['delivery'] = item.get('delivery')
            ware_info['wrap'] = item.get('wrap')
            ware_info['pack_listing'] = item.get('packListing')
            ware_info['weight'] = item.get('weight')
            ware_info['width'] = item.get('width')
            ware_info['height'] = item.get('height')
            ware_info['length'] = item.get('length')
            ware_info['props_json'] = json.dumps(item.get('props'))
            ware_info['features_json'] = json.dumps(item.get('features'))
            ware_info['images_json'] = json.dumps(item.get('images'))
            ware_info['shop_categorys_json'] = json.dumps(item.get('shopCategorys'))
            ware_info['mobile_desc'] = item.get('mobileDesc')
            ware_info['introduction'] = item.get('introduction')
            ware_info['zhuang_ba_introduction'] = item.get('zhuangBaIntroduction')
            ware_info['zhuang_ba_id'] = item.get('zhuangBaId')
            ware_info['introduction_use_flag'] = item.get('introductionUseFlag')
            ware_info['after_sales'] = item.get('afterSales')
            ware_info['logo'] = item.get('logo')
            ware_info['market_price'] = item.get('marketPrice')
            ware_info['cost_price'] = item.get('costPrice')
            ware_info['jd_price'] = item.get('jdPrice')
            ware_info['brand_name'] = item.get('brandName')
            ware_info['stock_num'] = item.get('stockNum')
            ware_info['cate_sec_id'] = item.get('categorySecId')
            ware_info['shop_id'] = item.get('shopId')
            ware_info['promise_id'] = item.get('promiseId')
            ware_info['multi_category_id'] = item.get('multiCategoryId')
            ware_info['multi_cate_props_json'] = json.dumps(item.get('multiCateProps'))
            ware_info['sell_point'] = item.get('sellPoint')
            ware_info['ware_tax_json'] = json.dumps(item.get('wareTax'))
            ware_info['after_sale_desc'] = item.get('afterSaleDesc')
            ware_info['zhuang_ba_mobile_desc'] = item.get('zhuangBaMobileDesc')
            ware_info['mobile_zhuang_ba_id'] = item.get('mobileZhuangBaId')
            ware_info['mobile_desc_use_flag'] = item.get('mobileDescUseFlag')
            ware_info['fit_case_html_pc'] = item.get('fitCaseHtmlPc')
            ware_info['fit_case_html_app'] = item.get('fitCaseHtmlApp')
            ware_info['special_services'] = item.get('specialServices')
            ware_info['parent_id'] = item.get('parentId')
            ware_info['ware_group_id'] = item.get('wareGroupId')
            ware_info['business_type'] = item.get('businessType')
            ware_info['design_concept'] = item.get('designConcept')
            ware_info['is_archival'] = item.get('isArchival')

            for key in list(ware_info.keys()):
                if not ware_info.get(key):
                    del ware_info[key]

            WareInfoModel.objects.update_or_create(ware_id=item.get('wareId'), defaults=ware_info)

    while count <= 3:
        _, ret = jd_api.send_request(
            {"method": JdWareApi.JD_WARE_LIST_V_1, "access_token": access_token,
             "360buy_param_json": json.dumps(
                 {"wareId": "", "searchKey": "", "searchField": "", "categoryId": "",
                  "shopCategoryIdLevel1": "",
                  "shopCategoryIdLevel2": "", "templateId": "", "promiseId": "", "brandId": "",
                  "featureKey": "",
                  "featureValue": "", "wareStatusValue": "8" if is_first_sync else "", "itemNum": "", "barCode": "",
                  "colType": "",
                  "startCreatedTime": "", "endCreatedTime": "", "startJdPrice": "", "endJdPrice": "",
                  "startOnlineTime": "", "endOnlineTime": "",
                  "startModifiedTime": "" if is_first_sync else str(zero_yesterday), "endModifiedTime": "",
                  "startOfflineTime": "", "endOfflineTime": "", "startStockNum": "", "endStockNum": "",
                  "orderField": "",
                  "orderType": "", "pageNo": str(page_num), "pageSize": "", "transportId": "", "claim": "",
                  "groupId": "",
                  "multiCategoryId": "", "warePropKey": "", "warePropValue": "",
                  "field": "adWords,offlineTime,colType,brandId,templateId,transportId,barCode,wareLocation,modified,created,delivery,packListing,weight,height,length,props,features,images,shopCategorys,mobileDesc,introduction,zhuangBaIntroduction,zhuangBaId,introductionUseFlag,afterSales,logo,marketPrice,costPrice,jdPrice,brandName,stockNum,categorySecId,shopId,promiseId,multiCategoryId,multiCateProps,sellPoint,wareTax,afterSaleDesc,zhuangBaMobileDesc,mobileZhuangBaId,mobileDescUseFlag,fitCaseHtmlPc,fitCaseHtmlApp,specialServices,parentId,wareGroupId,businessType,designConcept,isArchival"})})
        response_name = JdWareApi.JD_WARE_LIST_V_1.replace('.', '_')

        ware_response = ret.get(f'{response_name}_responce')

        page_info = ware_response.get('page')
        data = page_info.get('data')
        current_page_no = page_info.get('pageNo')
        page_size = page_info.get('pageSize')
        total_item = page_info.get('totalItem')
        total_page, mod = divmod(total_item, page_size)
        actual_page = total_page + 1 if mod else total_page

        if ware_response.get('code') == '0':
            create_or_update_ware_info(data)  # 保存当前页所有ware信息
            # 并行查询更新当前页所有ware_id所对应的sku信息
            group(update_sku_info.s(access_token, is_first_sync, item.get('wareId')) for item in data)()
            # 并行翻页查询后续ware信息
            if current_page_no == 1:
                group((update_ware_info.s(access_token, is_first_sync, page_no) for page_no in
                       range(current_page_no + 1, actual_page + 1)))()
            return
        count += 1


@celery_app.task()
def update_sku_info(access_token, is_first_sync, ware_id, page_num=1):
    jd_api = JdSdk()
    count = 1
    now = datetime.now()
    zero_yesterday = now - timedelta(days=1, hours=now.hour, minutes=now.minute, seconds=now.second,
                                     microseconds=now.microsecond)

    def create_or_update_sku_info(data):
        for item in data:
            sku_info = {}
            sku_info['ware_info_id'] = item.get('wareId')
            sku_info['status'] = item.get('status')
            sku_info['jd_price'] = item.get('jdPrice')
            sku_info['sale_attrs_json'] = json.dumps(item.get('saleAttrs'))
            sku_info['features_json'] = json.dumps(item.get('features'))
            sku_info['outer_id'] = item.get('outerId')
            sku_info['bar_code'] = item.get('barCode')
            sku_info['cate_id'] = item.get('categoryId')
            sku_info['img_tag'] = item.get('imgTag')
            sku_info['logo'] = item.get('logo')
            sku_info['sku_name'] = item.get('skuName')
            sku_info['stock_num'] = item.get('stockNum')
            sku_info['fixed_delivery_time'] = item.get('fixedDeliveryTime')
            sku_info['relative_delivery_time'] = item.get('relativeDeliveryTime')
            sku_info['parent_id'] = item.get('parentId')
            sku_info['modified_time'] = item.get('modified')
            sku_info['created_time'] = item.get('created')
            sku_info['multi_cate_props_json'] = json.dumps(item.get('multiCateProps'))
            sku_info['props_json'] = json.dumps(item.get('props'))
            sku_info['capacity'] = item.get('capacity')

            for key in list(sku_info.keys()):
                if not sku_info.get(key):
                    del sku_info[key]

            SkuInfoModel.objects.update_or_create(sku_id=item.get('skuId'), defaults=sku_info)

    while count <= 3:
        _, ret = jd_api.send_request(
            {"method": JdSkuApi.JD_SKU_LIST_V_1, "access_token": access_token,
             "360buy_param_json": json.dumps(
                 {"wareId": ware_id, "skuId": "", "skuStatuValue": "1" if is_first_sync else "", "maxStockNum": "",
                  "minStockNum": "",
                  "endCreatedTime": "", "endModifiedTime": "", "startCreatedTime": "",
                  "startModifiedTime": "" if is_first_sync else str(zero_yesterday),
                  "outId": "", "colType": "", "itemNum": "", "wareTitle": "", "orderFiled": "",
                  "orderType": "",
                  "pageNo": str(page_num), "page_size": "",
                  "field": "skuId,status,saleAttrs,features,outerId,barCode,categoryId,imgTag,logo,skuName,stockNum,fixedDeliveryTime,relativeDeliveryTime,parentId,created,modified,multiCateProps,props,capacity"})})
        response_name = JdSkuApi.JD_SKU_LIST_V_1.replace('.', '_')
        sku_response = ret.get(f'{response_name}_responce')
        page_info = sku_response.get('page')
        data = page_info.get('data')
        current_page_no = page_info.get('pageNo')
        page_size = page_info.get('pageSize')
        total_item = page_info.get('totalItem')
        total_page, mod = divmod(total_item, page_size)
        actual_page = total_page + 1 if mod else total_page

        if sku_response.get('code') == '0':
            create_or_update_sku_info(data)  # 保存当前页所有sku信息
            # 并发翻页查询后续sku信息
            if current_page_no == 1:
                group(
                    (update_sku_info.s(access_token, is_first_sync, ware_id, page_no) for page_no in
                     range(current_page_no + 1, actual_page + 1)))()
            return
        count += 1


@celery_app.task()
def task_product_info(access_token_info_list=None):
    """
    获取所有用户的店铺商品信息并更新
    """
    if not access_token_info_list:  # 查询所有用户的非空token
        access_token_info_list = JdAuthUserModel.objects.exclude(access_token='').values(
            'id', 'access_token', 'is_first_sync')
    group((update_ware_info.s(access_token_info.get('access_token'), access_token_info.get('is_first_sync')) for
           access_token_info in access_token_info_list))()
    JdAuthUserModel.objects.filter(
        id__in=(access_token_info.get('id') for access_token_info in access_token_info_list)).update(
        is_first_sync=False)


@celery_app.task()
def refresh_token(auth_user_id, refresh_token):
    jd_auth = JdWebAuthorized()
    response = jd_auth.refresh_access_token(refresh_token)
    expires_in = response.get('expires_in')
    start_time = int(response.get('time')) // 1000
    JdAuthUserModel.objects.filter(id=auth_user_id).update(expires_in=expires_in,
                                                           auth_start_time=start_time,
                                                           auth_end_time=start_time + expires_in)


@celery_app.task()
def task_refresh_token():
    next_hours_timestamp = int((datetime.now() + timedelta(hours=1)).timestamp())
    # 查询所有过期时间小于未来一小时的access_token
    access_token_info_list = JdAuthUserModel.objects.filter(auth_end_time__lte=next_hours_timestamp).exclude(
        access_token='').values('id', 'refresh_token')

    group((refresh_token.s(access_token_info.get('id'), access_token_info.get('refresh_token')) for
           access_token_info in access_token_info_list))()
