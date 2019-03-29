#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2019/1/24

from __future__ import absolute_import, unicode_literals
import os
from datetime import timedelta

from celery import Celery, platforms
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jingdong.settings')

app = Celery('jingdong')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: [app_config.split('.')[0] for app_config in settings.INSTALLED_APPS])

# 允许root 用户运行celery
platforms.C_FORCE_ROOT = True

app.conf.update(
    CELERYBEAT_SCHEDULE={
        # 店铺信息同步
        'shop_info': {
            "task": "jd_shop.tasks.task_shop_info",
            "schedule": timedelta(hours=24),  # 每隔24小时调用一次
            "args": (),
        },
        # 商品信息同步
        'product_info': {
            "task": "jd_product.tasks.task_product_info",
            "schedule": timedelta(hours=24),  # 每隔24小时调用一次
            "args": (),
        },
        # 刷新access_token
        'refresh_token': {
            "task": "jd_product.tasks.task_refresh_token",
            "schedule": timedelta(hours=1),  # 每隔1小时调用一次
            "args": (),
        }
    },
    # 创建Queue的实例时，传入name和routing_key，name即队列名称
    CELERY_QUEUES={
        'default': {
            'exchange': 'default'
        },
        'shop_info_router': {
            'exchange': 'shop_info_queue'
        },
        'refresh_token_router': {
            'exchange': 'refresh_token_queue'
        },
        'product_router': {
            'exchange': 'product_queue'
        }
    },
    CELERY_ROUTES={
        'jd_shop.tasks.task_shop_info': {
            'queue': 'shop_info_queue',
            'routing_key': 'shop_info_router',
        },
        'jd_product.tasks.task_product_info': {
            'queue': 'product_queue',
            'routing_key': 'product_router',
        },
        'jd_product.tasks.task_refresh_token': {
            'queue': 'refresh_token_queue',
            'routing_key': 'refresh_token_router',
        }
    }

)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
