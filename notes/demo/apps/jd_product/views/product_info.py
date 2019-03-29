from django.shortcuts import render

# Create your views here.
import logging

from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from jd_product.tasks import task_product_info

from jd_user.models import JdAuthUserModel

logger = logging.getLogger(__name__)


class ProductView(View):

    def post(self, request, *args, **kwargs):
        # 查询当前用户非空的access_token信息
        access_token_info_list = JdAuthUserModel.objects.filter(user=request.user).exclude(
            access_token='').values(
            'id', 'access_token', 'is_first_sync')

        task_product_info.delay(access_token_info_list)

        return HttpResponse('操作成功')
