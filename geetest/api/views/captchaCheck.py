import json

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response

from api.utils.geetest import GeeTestLib


class CaptchaCheck(APIView):
    def get(self, request):
        gt = GeeTestLib(
            settings.GEE_TEST["gee_test_access_id"],
            settings.GEE_TEST["gee_test_access_key"])
        gt.pre_process()
        # 设置 geetest session, 用于是否启用滑动验证码向 geetest 发起远程验证, 如果取不到的话只是对本地轨迹进行校验
        # self.request.session[gt.GT_STATUS_SESSION_KEY] = status
        # request.session["user_id"] = user_id
        response_str = gt.get_response_str()
        response_str = json.loads(response_str)

        obj = Response({"error_no": 0, "data": response_str})
        obj["Access-Control-Allow-Headers"] = "Content-Type"
        obj["Access-Control-Allow-Origin"] = "*"
        return obj
