from selenium import webdriver
from lxml import etree
import re
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from openpyxl import Workbook


class LagouSpider(object):
    wb = Workbook()  # 创建一个新的excel
    ws = wb.active  # 获得这个excel的第一个sheet表名

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        path = r"C:\Users\Administrator\新建文件夹\pa1\chromedriver.exe"
        self.driver = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
        #python职位
        self.url = 'https://www.lagou.com/jobs/list_python?city=%E5%8C%97%E4%BA%AC&cl=false&fromSearch=true&labelWords=&suginput='
        self.position = []

    def run(self):
        self.driver.get(self.url)
        while True:
            source = self.driver.page_source
            WebDriverWait(driver=self.driver,timeout=20).until(
                EC.presence_of_element_located((By.XPATH,"//div[@class='pager_container']/span[last()]"))
            )
            self.parse_list_page(source)
            #点“下一页”
            next_btn = self.driver.find_element_by_xpath(
                "//div[@class='pager_container']/span[last()]")
            if "pager_next_disabled" in next_btn.get_attribute("class"):
                break
            else:
                next_btn.click()
            time.sleep(1)


    def parse_list_page(self,source):
        html = etree.HTML(source)
        links = html.xpath("//a[@class='position_link']/@href")
        #每一页的所有职位的详情url
        for link in links:
            self.request_detail_page(link)
            time.sleep(1)

    def request_detail_page(self,url):
        try:
            # self.driver.get(url)
            print(url)
            self.driver.execute_script("window.open('%s')"%url)
            self.driver.switch_to.window(self.driver.window_handles[1])

            WebDriverWait(driver=self.driver,timeout=20).until(
                EC.presence_of_element_located((By.XPATH,"//div[@class='job-name']/span[@class='name']"))
            )
            #获取职位详情页的源代码
            source = self.driver.page_source
            self.parse_detail_page(source, url)
            #关闭当前详情页，并且切换到列表页
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
        except Exception:
            self.ws.save("lagou_python.xlsx")


    def parse_detail_page(self, source, url):

        html = etree.HTML(source)
        company = html.xpath("/html/body/div[3]/div/div[1]/div/div[1]/text()")[0]
        job_name = html.xpath("/html/body/div[3]/div/div[1]/div/span/text()")[0]
        tag_list = html.xpath("/html/body/div[3]/div/div[1]/dd/p[1]//text()")
        tag = "/".join(tag_list)[1:]
        advantage = html.xpath("//*[@id='job_detail']/dd[1]/p/text()")[0]
        job_detail_list = html.xpath("//*[@id='job_detail']/dd[2]/div//text()")
        job_detail = "\n".join(job_detail_list)
        ls = [company, job_name, tag, url, advantage, job_detail]
        self.ws = ls
        print("successful")

    def head(self):

        ls = ["公司", "职位", "tags", "地址", "职位诱惑", "职位描述"]
        self.ws = ls

if __name__ == '__main__':

    spider = LagouSpider()
    spider.head()
    spider.run()
    print("finish")
