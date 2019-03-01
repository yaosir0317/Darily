# -*- coding: utf-8 -*-
import scrapy

from ..items import ProjectbossItem


class SpiderbossSpider(scrapy.Spider):
    # 爬虫文件的名称
    name = 'spiderBoss'
    # 允许的域名
    # allowed_domains = ['www.xxx.com']
    # 起始url列表,列表内url,依次在parse方法执行
    start_urls = ['https://www.zhipin.com/c101010100/?query=%E7%88%AC%E8%99%AB&page=1&ka=page-1']
    url_page = "https://www.zhipin.com/c101010100/?query=爬虫&page=%s&ka=page-2"
    page = 1

    # 解析+管道持久化存储
    def parse(self, response):
        data_list = response.xpath("//div[@class='job-list']//ul/li")

        # 单个用extract_first,多个使用extract
        for data in data_list:
            # 实例化一个item对象
            item = ProjectbossItem()
            job_name = data.xpath("./div/div[1]/h3/a/div/text()").extract_first()
            salary = data.xpath("./div/div[1]/h3/a/span/text()").extract_first()
            company = data.xpath("./div/div[2]/div/h3/a/text()").extract_first()

            # 将解析到的数据全部封装到item对象中
            item["job_name"] = job_name
            item["salary"] = salary
            item["company"] = company

            # 将item提交给管道
            yield item

        # 分页的请求
        if self.page <= 10:
            self.page += 1
            new_url = format(self.url_page % self.page)
            # 手动发起请求
            yield scrapy.Request(url=new_url, callback=self.parse)
