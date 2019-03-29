# Create your views here.

import logging

from django.http.response import HttpResponse
from django.views.generic import View
from apps.jd_shop.tasks import task_shop_info

logger = logging.getLogger(__name__)


class ShopInfoView(View):

    def post(self, request, *args, **kwargs):
        # todo  获取access_token
        access_token = 'e4324a61d2d043119b55e4cfd257aaffzmjr'
        task_shop_info.delay(access_token)
        return HttpResponse('操作成功')
