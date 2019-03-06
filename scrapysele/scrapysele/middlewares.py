# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from time import sleep
from scrapy import signals
from scrapy.http import HtmlResponse


class ScrapyseleDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        bro = spider.bro
        bro.get(url=request.url)
        sleep(1)
        # 包含了动态加载出来的新闻数据
        page_text = bro.page_source
        sleep(1)
        # 返回新实例化的响应对象
        return HtmlResponse(url=spider.bro.current_url, body=page_text, encoding=
                            'utf-8', request=request)
