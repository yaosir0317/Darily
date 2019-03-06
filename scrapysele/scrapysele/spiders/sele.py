# -*- coding: utf-8 -*-
import scrapy
from time import sleep
from selenium import webdriver
from lxml import etree


class SeleSpider(scrapy.Spider):
    name = 'sele'
    start_urls = ["https://www.lagou.com/jobs/list_python?city=%E5%8C%97%E4%BA%AC&cl="
                  "false&fromSearch=true&labelWords=&suginput="]

    def __init__(self):
        # 创建浏览器对象
        self.bro = webdriver.Chrome(executable_path=
                                    r'C:\Users\Administrator\新建文件夹\pa1\chromedriver.exe')

    def parse(self, response):
        for i in range(1, 16):
            a = response.xpath(r"//*[@id='s_position_list']/ul/li[%s]/div[1]/div[1]/div[1]/a/@href" % i)[0]
            sleep(1)
            # 打开新窗口
            print(a)
            new_window = 'window.open("%s");' % a
            self.bro.execute_script(self, new_window)

            # 切换到新的窗口
            handles = self.bro.window_handles
            print(handles)
            self.bro.switch_to.window(handles[-1])
            detail_text = self.bro.page_source
            detail_page = etree.HTML(detail_text)
            company = detail_page.xpath("/html/body/div[3]/div/div[1]/div/div[1]/text()")[0]
            job_name = detail_page.xpath("/html/body/div[3]/div/div[1]/div/span/text()")[0]
            tag_list = detail_page.xpath("/html/body/div[3]/div/div[1]/dd/p[1]//text()")
            tag = "/".join(tag_list)[1:]
            advantage = detail_page.xpath("//*[@id='job_detail']/dd[1]/p/text()")[0]
            job_detail_list = detail_page.xpath("//*[@id='job_detail']/dd[2]/div//text()")
            job_detail = "\n".join(job_detail_list)
            ls = [company, job_name, tag, advantage, job_detail, a]
            print(ls)
            sleep(1)
            self.bro.close()
            self.bro.switch_to.window(handles[0])

        print("=" * 50)
        self.bro.find_elements_by_xpath(r"//*[@id='order']/li/div[4]/div[2]").click()

    def close(self, spider):
        self.bro.quit()
