# -*- coding: utf-8 -*-
# 第三方授权登录

import json
import requests
from urllib import parse

from jd_sdk.config import JdConfig
from jd_sdk.custom_exception import NetworkError


class JdWebAuthorized(object):
    """京东网页授权基础操作
    # 第一步 获取code
    # 第二步 获取access_token, 同时获取用户信息
    """

    app_key = JdConfig.APP_KEY
    app_secret = JdConfig.APP_SECRET
    # 回调地址
    redirect_uri = JdConfig.REDIRECT_URI
    # 自定义state
    base_state = ''
    # 授权code的response_type值
    code_response_type = 'code'
    # 获取access_token的grant_type值
    access_token_grant_type = 'authorization_code'
    # 刷新access_token的grant_type值
    refresh_token_grant_type = 'refresh_token'
    # 授权code获取地址
    authorized_code_url = 'https://oauth.jd.com/oauth/authorize'
    # 获取access_token的url, 获取用户信息
    authorized_access_token_url = 'https://oauth.jd.com/oauth/token'
    # 刷新token的url, POST请求
    authorized_refresh_token_url = 'https://oauth.jd.com/oauth/token'

    def __init__(self, code='', state=''):

        self.code = code  # 当有code值时才能获取access_token
        self.state = state or self.base_state or 'random'

        self.access_data = {}  # 获取access_token后返回的数据
        self.access_token = ''
        self.refresh_token = ''
        self.expires_in = 0  # token过期时间
        self.time = 0  # 授权的时间点
        self.uid = ''
        self.user_nick = ''

    def add_code(self, code):
        """添加code"""
        self.code = code

    def add_access_data(self, access_data):
        """添加access_data"""
        self.access_token = access_data.get('access_token', '')
        self.expires_in = access_data.get('expires_in', 0)
        self.refresh_token = access_data.get('refresh_token', '')
        self.uid = access_data.get('uid', 0)
        self.user_nick = access_data.get('user_nick', '')
        self.time = access_data.get('time', '0')

    def get_code_url(self):
        """获取code的重定向url地址"""

        params_str = self.get_code_params_str()

        return self.authorized_code_url + '?' + params_str

    def get_access_token(self, code=None):
        """获取access_token
        @param code: 获取access_token的code
        @return:
        """
        if code is None:
            code = self.code

        assert code, '[get_access_token][ERROR]，请传入参数code'
        access_token_params = self.get_access_token_params(code)

        # 发送请求，获取access_token
        response = requests.get(self.authorized_access_token_url, params=access_token_params)
        access_token = self.format_access_token_response(response.text)
        self.access_data = access_token
        self.add_access_data(self.access_data)
        return access_token

    def refresh_access_token(self, refresh_token=None):
        """刷新token
        @param refresh_token: 刷新token
        @return:
        """

        if refresh_token is None:
            refresh_token = self.refresh_token
        assert refresh_token, '[refresh_access_token][ERROR]，请传入参数refresh_token'
        # 发送请求，刷新token
        params = self.get_refresh_token_params(refresh_token)
        response = requests.post(self.authorized_refresh_token_url, params=params)
        access_token = self.format_access_token_response(response.text)
        self.access_data = access_token
        self.add_access_data(self.access_data)
        return access_token

    def get_access_token_params(self, code):
        """获取授权access_token参数
        @param code: 获取token的code
        @return:
        """

        grant_type = self.access_token_grant_type
        client_id = self.app_key
        client_secret = self.app_secret
        code = code
        redirect_uri = self.redirect_uri  # 成功授权后的回调地址
        state = self.state

        params = {
            'grant_type': grant_type,
            'code': code,
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'client_secret': client_secret,
            'state': state
        }
        return params

    def get_access_token_params_str(self, code):
        """获取授权access_token参数
        @param code: 获取token的code
        @return:
        """
        params = self.get_access_token_params(code)
        data_str = parse.urlencode(params, encoding='utf-8')
        return data_str

    def get_access_token_url(self, code):
        """获取access_token的url地址"""
        params_str = self.get_access_token_params_str(code)
        return self.authorized_access_token_url + '?' + params_str

    def get_refresh_token_url(self, refresh_token):
        """刷新token的url地址
        @param refresh_token: 用来刷新token的字符串
        @return:
        """
        params_str = self.get_refresh_token_params_str(refresh_token)
        return self.authorized_refresh_token_url + '?' + params_str

    def get_code_params_str(self):
        """获取授权code的url参数"""
        response_type = self.code_response_type
        client_id = self.app_key
        redirect_uri = self.redirect_uri  # 成功授权后的回调地址
        scope = 'read'  # 权限参数
        state = self.state  # 状态参数

        params = {
            'response_type': response_type,
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'scope': scope,
            'state': state,
        }
        data_str = parse.urlencode(params, encoding='utf-8')
        return data_str

    def get_refresh_token_params(self, refresh_token):
        """获取刷新token的参数
        @param refresh_token: 用来刷新token的字符串
        @return:
        """
        grant_type = self.refresh_token_grant_type
        client_id = self.app_key
        client_secret = self.app_secret
        refresh_token = refresh_token

        params = {
            'grant_type': grant_type,
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': refresh_token,
        }
        return params

    def get_refresh_token_params_str(self, refresh_token):
        """获取刷新token的参数
        @param refresh_token: 用来刷新token的字符串
        @return:
        """
        params = self.get_refresh_token_params(refresh_token)
        data_str = parse.urlencode(params, encoding='utf-8')
        return data_str

    @staticmethod
    def format_access_token_response(token_response):
        """格式化access_token返回值
        @param token_response: token返回值，json格式
        @return: 字典格式
        """
        try:
            response_dict = json.loads(token_response)
        except NetworkError:
            response_dict = {}

        return response_dict

    @staticmethod
    def __format_str_to_dict(str_data):
        """格式化回调数据（str类型）"""
        # 字符串 转化为  [('access_token', 'token'), ('expires_in', 'access_token有效期'), ('refresh_token', '刷新时用的token'), ]
        try:
            parse_data = parse.parse_qsl(str_data)
        except NetworkError:
            parse_data = []
            print('----------- [__format_str_to_dict]回调数据解析出错 ----------------------')
            print(str_data)

        # 再转化为字典
        return dict(parse_data)
