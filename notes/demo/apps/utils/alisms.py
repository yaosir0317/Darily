#!/usr/bin/env python
# *_* coding: UTF-8 *_*

"""
@author: Siffre@三弗 
@contact: Siffre@aliyun.com

@version: 1.0
@license: Apache Licence
@file: alisms.py
@time: 2018/12/15 11:34 AM


 　　　　　　　 ┏┓　 ┏┓+ +
 　　　　　　　┏┛┻━━━┛┻┓ + +
 　　　　　　　┃　　　　　　┃ 　
 　　　　　　　┃　　　━　　 ┃ ++ + + +
 　　　　　　 ████━████  ┃+
 　　　　　　　┃　　　　　　　┃ +
 　　　　　　　┃　　　┻　　　┃
 　　　　　　　┃　　　　　　┃ + +
 　　　　　　　┗━┓　　　┏━┛
 　　　　　　　　 ┃　　　┃　　　　　　　　　　　
 　　　　　　　　 ┃　　　┃ + + + +
 　　　　　　　　 ┃　　　┃　　　　Code is far away from bug with the animal protecting　　　　　　　
 　　　　　　　　 ┃　　　┃ + 　　　　神兽保佑,代码无bug　　
 　　　　　　　　 ┃　　　┃
 　　　　　　　　 ┃　　　┃　　+　　　　　　　　　
 　　　　　　　　 ┃　 　 ┗━━━┓ + +
 　　　　　　　　 ┃ 　　　　   ┣┓
 　　　　　　　　 ┃ 　　　　　 ┏┛
 　　　　　　　　 ┗┓┓┏━┳┓┏┛ + + + +
 　　　　　　　　  ┃┫┫ ┃┫┫
 　　　　　　　　  ┗┻┛ ┗┻┛+ + + +
           
"""

import base64
import datetime
import hmac
import json
import urllib
import uuid

import requests

from django.conf import settings


class AliSMS(object):
    _defaults = [
        ('action', 'SendSms'),
        ('format', 'JSON'),
        ('region_id', 'cn-hangzhou'),
        ('signature_method', 'HMAC-SHA1'),
        ('signature_version', '1.0'),
        ('sms_version', '2017-05-25'),
        ('domain', 'https://dysmsapi.aliyuncs.com'),
    ]

    def __init__(self, access_key, access_secret, sign_name, **settings):
        for k, v in self._defaults:
            setattr(self, k, settings.get(k, v))

        self.access_key = access_key
        self.access_secret = access_secret
        self.sign_name = sign_name

    def send(self, phone, template_code, template_params):
        body = self._create_body(phone, template_code, template_params)
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
        }
        response = requests.post(self.domain, data=body, headers=headers)
        response_dict = json.loads(response.text)
        return response_dict

    def _create_body(self, phone, template_code, template_params):
        params = self._create_params(phone, template_code, template_params)
        text = 'POST&%2F&' + self.parse_params(**params)
        signature = self.sign(text, self.access_secret)
        body = 'Signature={}&{}'.format(signature, self.stringify(**params))
        return body.encode('utf-8')

    def _create_params(self, phone, template_code, template_params):
        return {
            'AccessKeyId': self.access_key,
            'Action': self.action,
            'Format': self.format,
            'PhoneNumbers': phone,
            'RegionId': self.region_id,
            'SignName': self.sign_name,
            'SignatureMethod': self.signature_method,
            'SignatureNonce': str(uuid.uuid4()),
            'SignatureVersion': self.signature_version,
            'TemplateCode': template_code,
            'TemplateParam': json.dumps(template_params),
            'Timestamp': datetime.datetime.utcnow().isoformat("T"),
            'Version': self.sms_version,
        }

    def quote(self, text):
        return urllib.parse.quote(text, safe='~')

    @staticmethod
    def stringify(**kwargs):
        pairs = []
        for k, v in sorted(kwargs.items()):
            pairs.append('{}={}'.format(k, v))
        return '&'.join(pairs)

    def parse_params(self, **kwargs):
        pairs = []
        for k, v in sorted(kwargs.items()):
            pair = '{}={}'.format(self.quote(k), self.quote(v))
            pairs.append(pair)
        return self.quote('&'.join(pairs))

    def sign(self, text, secret):
        text = text.encode('utf-8')
        key = (secret + '&').encode('utf-8')
        digest = hmac.new(key, text, 'sha1').digest()
        signature = self.quote(base64.b64encode(digest))
        return signature


if __name__ == '__main__':
    access_key = settings.ALI_SMS_KEY
    access_secret = settings.ALI_SMS_SECRET
    sign_name = settings.ALI_SMS_SIGN_NAME
    template_code = settings.ALI_SMS_TEMPLATE_CODE
    template_params = {
        'code': '0000'
    }
    sms = AliSMS(access_key, access_secret, sign_name)
    response_dict = sms.send('17611598281,17778137149', template_code, template_params)
    print(response_dict)
