#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2019/2/13


import os
import sys

import django

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(BASE_DIR))
sys.path.insert(0, os.path.join(BASE_DIR, 'fixture'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'jingdong.settings'
django.setup()

from jd_product.models import WareInfoModel, SkuInfoModel


def save_product_info():
    """
    存储产品测试数据
    :return:
    """

    ware_list = [10995746221, ]
    sku_list = [
        14672350445,
        38670321615,
        10099869210,
        38628684948,
        38653959515,
        31991929565,
        14773703463,
        37611584329,
        17424291832,
        41080204581,
        39910122408,
        38376395727,
        39891357227,
        29153544451,
        37024218710,
        38616001326,
        38642226041,
        25480440408,
        38628684951,
        32211116153,
        39050448994,
        37188694136,
        38376395731,
        37119904896,
        39992790974,
        37611584326,
        30205426915,
        27566669396,
        21139823693,
        11162643500,
        35865279801,
        30395981395,
        40222794976,
        10570097773,
        10091843461,
        29585930387,
        40459937709,
        38628684950,
        38616001328,
        10070018647,
        30285898233,
        38642067183,
        40044966249,
        10156021312,
        17876899001,
        22856741317,
        25111541109,
        37023294780,
        38616001333,
        38670321618,
        11135098354,
        21139823691,
        10099869211,
        38653959518,
        40459937712,
        30202153039,
        30213319636,
        41473455264,
        41080204584,
        39207339621,
    ]

    if not WareInfoModel.objects.filter(ware_id=ware_list[0], status='8'):
        ware_obj = WareInfoModel.objects.update_or_create(ware_id=ware_list[0], status='8')
    else:
        ware_obj = WareInfoModel(ware_id=ware_list[0], status='8')

    for sku_id in sku_list:
        SkuInfoModel.objects.update_or_create(
            sku_id=sku_id,
            defaults={'ware_info': ware_obj, 'status': '1'}
        )


if __name__ == '__main__':
    print(BASE_DIR)
    save_product_info()
