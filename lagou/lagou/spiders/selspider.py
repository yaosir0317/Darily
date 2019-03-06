# -*- coding: utf-8 -*-
import scrapy


class SelspiderSpider(scrapy.Spider):
    name = 'selspider'
    allowed_domains = ['www.xxx.com']
    start_urls = ['http://www.xxx.com/']

    def parse(self, response):
        pass
