from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect
from app01.models import Permission
import re


class PermissionMiddleWare(MiddlewareMixin):

    def process_request(self, request):
        # print("permission_list", request.session.get("permission_list"))
        current_path = request.path
        print("当前访问地址", current_path)

        # 设置白名单放行
        for reg in ["/login/", "/admin/*", "/register/", "/get_valid_img/", "/logout/"]:
            ret = re.search(reg, current_path)
            if ret:
                return None
        # /customers/edit/1

        # 校验是否登录
        if not request.user.is_authenticated:
            return redirect("/login/")

        # 校验权限

        permission_list = request.session.get("permission_list")
        # 面包屑导航列表
        request.breadcrumb = []
        for item in permission_list:
            # reg = "^%s$" % item["url"]
            ret = re.search("^{}$".format(item["url"]), current_path)
            if ret:
                # 确定是否有自关联字段,也就是确定面包屑的第一层
                show_id = item["pid"] or item["id"]
                request.show_id = show_id

                # 确定面包屑列表
                if item["pid"]:  # 有pid不是第一层
                    ppermission = Permission.objects.filter(pk=item["pid"]).first()
                    request.breadcrumb.extend(
                        [{
                            "title": ppermission.title,  # 一层
                            "url": ppermission.url,
                        }, {
                            "title": item["title"],  # 二层
                            "url": request.path
                        },
                        ]

                    )
                # 没有pid,是第一层面包屑导航
                else:
                    request.breadcrumb.append(
                        {
                            "title": item["title"],
                            "url": item["url"]
                        }
                    )

                return None

        return HttpResponse("无访问权限！")
