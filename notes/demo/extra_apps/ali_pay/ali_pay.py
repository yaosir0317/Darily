#!/usr/bin/python
# -*- coding:utf-8 -*-
from alipay import AliPay, ISVAliPay

# 应用信息
app_id = "2016091600526458"
app_private_key_string = open("./keys/app_private_key.txt").read()
ali_pay_public_key_string = open("./keys/alipay_public_key.txt").read()


class AliPayJzz(object):
    def __init__(self):
        self.ali_pay = AliPay(
            appid=app_id,
            app_notify_url=None,  # 默认回调url
            app_private_key_string=app_private_key_string,
            alipay_public_key_string=ali_pay_public_key_string,
            sign_type="RSA2",
            debug=False  # 默认False
        )

    def pc_pay(self, out_trade_no, total_amount, subject, return_url, notify_url):
        """
        :param out_trade_no: 订单号
        :param total_amount: 金额
        :param subject: 商品描述
        :param return_url: 回跳的url
        :param notify_url: 返回通知
        :return: order_string or none
        """
        try:
            order_string = self.ali_pay.api_alipay_trade_page_pay(
                out_trade_no=out_trade_no,
                total_amount=total_amount,
                subject=subject
                # return_url=None
                # notify_url=notify_url
            )
        except Exception as e:
            print("pc_pay_error %s" % str(e))
            return None
        return order_string

    def app_pay(self, out_trade_no, total_amount, subject, notify_url):
        try:
            order_string = self.ali_pay.api_alipay_trade_app_pay(
                out_trade_no=out_trade_no,
                total_amount=total_amount,
                subject=subject,
                notify_url=notify_url
            )
        except Exception as e:
            print("app_pay_error %s" % str(e))
            return None
        return order_string

    def verify_pay_result(self, data, signature):
        """
        :param data: ali pay return data
        :param signature: data.pop("sign")
        :return: "trade succeed" or none
        """
        try:
            result = self.ali_pay.verify(data, signature)
        except Exception as e:
            print("verify_pay_result_error %s:" % str(e))
            return None
        if result and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            return "trade succeed"


if __name__ == "__main__":
    pay_test = AliPayJzz()
    url = pay_test.pc_pay("112233445566", 100, "京至尊会员", "https://example.com", "https://example.com")
    re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
    print("re_url", re_url)
