#!/usr/bin/python
# -*- coding:utf-8 -*-

from .aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkcore.client import AcsClient
import uuid
from aliyunsdkcore.profile import region_provider
import const
import random

acs_client = AcsClient(const.ACCESS_KEY_ID, const.ACCESS_KEY_SECRET, const.REGION)
region_provider.add_endpoint(const.PRODUCT_NAME, const.REGION, const.DOMAIN)


# 6位随机数字验证码(字符串)
def get_validation_code(length=6):
    return "".join(map(lambda i: str(random.randint(0, 9)), range(length)))


def send_sms(business_id, phone_numbers, sign_name, template_code, validation_code):
    template_param = "{\"code\":\"%s\"}" % validation_code
    sms_request = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    sms_request.set_TemplateCode(template_code)
    # 短信模板变量参数
    if template_param is not None:
        sms_request.set_TemplateParam(template_param)
    # 设置业务请求流水号，必填。
    sms_request.set_OutId(business_id)
    # 短信签名
    sms_request.set_SignName(sign_name)
    # 数据提交方式
    # smsRequest.set_method(MT.POST)
    # 数据提交格式
    # smsRequest.set_accept_format(FT.JSON)
    # 短信发送的号码列表，必填。
    sms_request.set_PhoneNumbers(phone_numbers)
    # 调用短信发送接口，返回json
    sms_response = acs_client.do_action_with_exception(sms_request)
    return sms_response


if __name__ == '__main__':
    __business_id = uuid.uuid1()
    send_sms(__business_id, "11111", "大主宰科技", "SMS_5250008", get_validation_code())
