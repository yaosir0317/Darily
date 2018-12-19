from rest_framework.views import APIView
from app01.models import UserInfo, Token
from django.contrib import auth
from rest_framework.response import Response
import uuid
import datetime


from api.utils.captcha_verify import verify


class LoginView(APIView):
    def post(self, request):
        print("request.data", request.data)
        print(verify(request.data))
        res = {"user": None, "msg": None}

        try:
            if verify(request.data):
                # 1 获取数据
                user = request.data.get("user")
                pwd = request.data.get("pwd")
                user_obj = auth.authenticate(username=user, password=pwd)

                if user_obj:
                    random_str = str(uuid.uuid4())
                    Token.objects.update_or_create(
                        user=user_obj, defaults={
                            "key": random_str, "created": datetime.datetime.now()})
                    res["user"] = user_obj.username
                    res["token"] = random_str

                else:
                    res["msg"] = "用户名或者密码错误！"
            else:
                res["msg"] = "验证码异常！"
        except Exception as e:
            res["msg"] = str(e)

        return Response(res)
