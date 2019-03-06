# -*- coding: utf-8 -*-
import scrapy


class LagouComSpider(scrapy.Spider):
    name = 'lagou.com'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=']

    def parse(self, response):
        result = []
        url_page = "https://www.zhipin.com/c101010100/?query=爬虫&page=%s&ka=page-2"
        page = 1
        data_list = response.xpath("//div[@class='job-list']//ul/li")

        # 单个用extract_first,多个使用extract
        for data in data_list:
            job_name = data.xpath("./div/div[1]/h3/a/div/text()").extract_first()
            salary = data.xpath("./div/div[1]/h3/a/span/text()").extract_first()
            company = data.xpath("./div/div[2]/div/h3/a/text()").extract_first()
            dic = {
                "job_name": job_name,
                "salary": salary,
                "company": company
            }
            result.append(dic)
            print(dic)

        if self.page <= 10:
            self.page += 1
            new_url = format(self.url_page % self.page)
            # 手动发起请求
            yield scrapy.Request(url=new_url, callback=self.parse)

        return result