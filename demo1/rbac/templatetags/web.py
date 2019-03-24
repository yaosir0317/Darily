from django import template

register = template.Library()


@register.inclusion_tag("base/menu.html")
def get_menu_styles(request):
    # 获取菜单栏
    permission_menu_dict = request.session.get("permission_menu_dict")
    for val in permission_menu_dict.values():
        # 循环菜单获取其子菜单
        for item in val["children"]:
            # print("===========================", item, request.path, request.show_id, item["pk"])
            # 前端样式↓
            val["class"] = ""
            val["cls"] = "aria-expanded='flase'"
            val["in"] = ""
            val["url"] = ""
            # 前端样式↑

            # ret = re.search("^{}$".format(item["url"]), request.path)
            # 判断当前访问的地址,对其对应的菜单和子菜单添加特殊样式
            if request.show_id == item["pk"]:
                val["class"] = "active"
                val["cls"] = "aria-expanded='true'"
                val["in"] = "in"
                val["url"] = request.path
                return {"permission_menu_dict": permission_menu_dict}
    return {"permission_menu_dict": permission_menu_dict}


@register.filter
def has_permission(btn_url, request):  # 根据权限显示相应的功能按钮
    permission_names = request.session.get("permission_names")
    return btn_url in permission_names


# 在保留当前请求条件的情况下额外增加键值
@register.simple_tag
def gen_role_url(request, rid):
    params = request.GET.copy()
    params._mutable = True  # 为False无法增加,因此先copy
    params['rid'] = rid  # 增加键值
    return params.urlencode()  # 转换成 键&值 形式
