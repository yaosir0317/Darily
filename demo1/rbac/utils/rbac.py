from app01.models import Role


def initial_sesson(user, request):
    """
    功能：将当前登录人的所有权限录入session中
    :param user: 当前登录人
    """
    # 查询当前登录人的所有权限列表
    # 查看当前登录人的所有角色
    # ret=Role.objects.filter(user=user)

    # 筛选所需要的字段
    permissions = Role.objects.filter(
        userinfo__username=user).values(
        "permissions__url",
        "permissions__title",
        "permissions__name",
        "permissions__pk",
        "permissions__pid",
        "permissions__menu__title",
        "permissions__menu__icon",
        "permissions__menu__pk",
    ).distinct()

    permission_list = []
    permission_names = []
    permission_menu_dict = {}

    for item in permissions:
        # 构建权限列表
        permission_list.append({
            "url": item["permissions__url"],
            "id": item["permissions__pk"],                 
            "pid": item["permissions__pid"],
            "title": item["permissions__title"],
        })
        # 构建别名列表
        permission_names.append(item["permissions__name"])
        # 构建菜单权限列表
        # 菜单权限
        menu_pk = item["permissions__menu__pk"]
        if menu_pk:  # 判断是否是菜单
            if menu_pk not in permission_menu_dict:  # 添加新的菜单

                permission_menu_dict[menu_pk] = {
                    "menu_title": item["permissions__menu__title"],
                    "menu_icon": item["permissions__menu__icon"],
                    "children": [
                        {
                            "title": item["permissions__title"],
                            "url": item["permissions__url"],
                            "pk": item["permissions__pk"],
                        }
                    ],

                }
            # 更新已存在的菜单
            else:
                permission_menu_dict[menu_pk]["children"].append({
                    "title": item["permissions__title"],
                    "url": item["permissions__url"],
                    "pk": item["permissions__pk"],
                })

    print("-------------->", permission_menu_dict)
    # 将当前登录人的权限列表注入session中
    request.session["permission_list"] = permission_list
    # 将别名列表注入session中,列表中是字典
    request.session["permission_names"] = permission_names
    # 将当前登录人的菜单权限列表注入session中
    request.session["permission_menu_dict"] = permission_menu_dict
