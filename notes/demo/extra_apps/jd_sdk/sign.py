#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2019/1/19

import time
import hashlib
import logging

from jd_sdk.config import JdConfig
from jd_sdk.apis import JdSignApi

from jd_sdk.custom_exception import SignError

logger = logging.getLogger(__name__)


class JdSign(object):
    """
    京东签名
    """

    def get_sign_url(self, params_dict):
        """
        获取签名链接
        :param params_dict:
        :return:
        """

        # 配置额外的参数
        _params_dict = self.add_sign_params(params_dict)
        # 组装签名URL
        sign_url = self.make_sign_url(_params_dict)
        return sign_url

    @staticmethod
    def make_sign_url(params_dict):
        """
        组装签名链接
        :param params_dict: {"method": "", "access_token":""}
        :return: sign_url or None
        """

        sign_url = None
        try:
            keys = params_dict.keys()
            keys = sorted(keys)
            md5_str = JdConfig.APP_KEY
            sign_url = JdSignApi.JD_SIGN_API_V_1
            for key in keys:
                md5_str += key
                md5_str += params_dict[key]
                sign_url += ('&' + key + '=' + params_dict[key])
            md5_str += JdConfig.APP_SECRET
            sign_hash = hashlib.md5()
            sign_hash.update(md5_str.encode(encoding="utf-8"))
            sign = sign_hash.hexdigest()
            params_dict['sign'] = sign.upper()
            sign_url += '&sign=' + sign.upper()
        except SignError as e:
            logger.exception(f"get_sign_param_error is {e}")

        finally:
            return sign_url

    @staticmethod
    def add_sign_params(params_dict):
        """
        额外参数配置
        :param params_dict:
        :return:
        """

        params_dict["app_key"] = JdConfig.APP_KEY
        params_dict["timestamp"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        return params_dict
