from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from jd_user.models import JdAuthUserModel
from jd_shop.models import JdShopInfoModel


@method_decorator(login_required, 'dispatch')
class BaseView(View):
    """
    基础应用页面
    """

    def get(self, request, *args, **kwargs):
        obj = JdAuthUserModel.objects.get(user=request.user)
        return render(request, 'base.html', {'shop_obj': obj.shop})
