# -*- coding: utf-8 -*-

import logging

import requests

# from apps.jd_product.models import WareInfoModel
from jd_sdk.config import JdConfig
from jd_sdk.sign import JdSign
from jd_sdk.custom_exception import NetworkError

# TODO 待配置日志详情
logger = logging.getLogger(__name__)


class JdSdk(object):

    def __init__(self):
        # 签名
        self.sign = JdSign()

    def send_request(self, params_dict, **kwargs):
        """
        请求封装：GET|POST均可，这里是GET请求
        :param params_dict: {"method": "", "access_token":""}
        :param kwargs: 请求配置：超时，请求头等
        :return:
        """

        sign_result = self.sign.get_sign_url(params_dict)

        response_dict = {}
        stat = None

        for i in range(JdConfig.HTTP_GET_RETRY):
            try:
                if sign_result is not None:
                    response = requests.get(sign_result, **kwargs)
                else:
                    logger.error(f'jd sdk send_request is failed, retry is {i}')
            except NetworkError as e:
                logger.exception(f'jd sdk send_request is failed, error is {e}')
            else:
                if response.status_code == 200 and response.text:
                    response_dict = response.json()
                    stat = response
                    stat.retry_num = i
                    break
        return stat, response_dict


if __name__ == "__main__":
    jd_api = JdSdk()
