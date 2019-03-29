#!/usr/bin/env python
# *_* coding: UTF-8 *_*

"""
@author: Siffre@三弗 
@contact: Siffre@aliyun.com

@version: 1.0
@license: Apache Licence
@file: config.py
@time: 2019/1/17 10:18 PM
"""


class JdConfig(object):
    """
    京东SDK配置
    """

    # 后台回调接口，只需要在后台配置即可
    APP_CALLBACK_URL = 'http://wuxianjingzun.com/user/jd_redirect_url'

    # 京麦开发者后台接口管理查找相关信息
    APP_KEY = "9C684CD66DFD564EF4E8BFC3724231EB"

    APP_SECRET = "bc07e1fa7cc2441b93030c494357680a"

    # 回调地址
    REDIRECT_URI = 'http://wuxianjingzun.com/user/jd_redirect_url'

    # 重试次数
    HTTP_GET_RETRY = 3

    # 超时设置
    HTTP_GET_TIMEOUT = 8

    # 异常code
    ERROR_CODE_DICT = {
        "101": "没找到应用（确认应用是否已“上线运行”；确认应用类型是否为“通用应用”，“无线应用”、“网站应用”无法被授权）",
        "201": "您的IP服务受限，请联系客服解决",
        "202": "请输入用户名",
        "203": "用户名不存在",
        "204": "请输入密码",
        "205": "登录信息与密码不匹配",
        "206": "用户名与密码不匹配，还可尝试{0}次，如失败账户将被冻结2小时",
        "207": "登录失败超过6次，账户已被冻结2个小时",
        "208": "容器检查登录用户不在应授权用户中（个人账号不能给商家应用授权）",
        "209": "未知异常，请联系管理员",
        "301": "缺少responsetype参数 或者为空",
        "302": "缺少clientId 参数 或者为空",
        "303": "缺少redirectUri 参数 或者为空",
        "304": "防止session伪造（在授权过程中点击了回退按钮）",
        "305": "拼写的redirect_uri和注册应用的“回调页面URL”不一致",
        "251": "调用验证登录信息接口返回的json串格式错误，解析失败",
        "401": "没有此流程的认证权限（应用使用了错误的授权方式进行授权）",
        "402": "错误的code（1、code码超时，code码时效为5分钟；2、测试环境与正式环境code码混用；3、自己编造的code码）",
        "403": "url不匹配（请求url与开发者中心创建应用时填写的url不一致；2、没有填写url）",
        "404": "错误的请求（JOS授权安全机制限制：用户在授权页面输入账号密码出错后，重新在原页面输入账号密码均会报404。处理方法："
               "请重新获取授权页面，或回退两次即可）",
        "405": '"code":"405","error_description":"用户[xxx]无权给app[xxxxxxxxxxxx]授权"（'
               '请将报错信息，包含用户名及appkey发送至jos#jd.com申请绑定授权关系）',
    }
