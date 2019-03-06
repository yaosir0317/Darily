from lxml import etree
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
# 驱动路径
path = r'C:\Users\Administrator\新建文件夹\pa1\chromedriver.exe'

# 创建浏览器对象
chrome_obj = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
# chrome_obj = webdriver.Chrome(r"C:\Users\Administrator\新建文件夹\pa1\chromedriver.exe")


def get_data(obj):
    isolation = "="*50
    obj.get(
        "https://www.lagou.com/jobs/list_python?city=%E5%8C%97%E4%BA%AC&cl=false&fromSearch=true&labelWords=&suginput=")
    n = 0
    while n < 30:
        page_text = obj.page_source
        tree = etree.HTML(page_text)
        for i in range(1, 16):
            a = tree.xpath(r"//*[@id='s_position_list']/ul/li[%s]/div[1]/div[1]/div[1]/a/@href" % i)[0]
            sleep(3)
            # 打开新窗口
            print(a)
            new_window = 'window.open("%s");' % a
            obj.execute_script(new_window)

            # 切换到新的窗口
            handles = obj.window_handles
            obj.switch_to_window(handles[-1])
            detail_text = obj.page_source
            detail_page = etree.HTML(detail_text)
            company = detail_page.xpath("/html/body/div[3]/div/div[1]/div/div[1]/text()")[0]
            job_name = detail_page.xpath("/html/body/div[3]/div/div[1]/div/span/text()")[0]
            tag_list = detail_page.xpath("/html/body/div[3]/div/div[1]/dd/p[1]//text()")
            tag = "/".join(tag_list)[1:]
            advantage = detail_page.xpath("//*[@id='job_detail']/dd[1]/p/text()")[0]
            job_detail_list = detail_page.xpath("//*[@id='job_detail']/dd[2]/div//text()")
            job_detail = "\n".join(job_detail_list)
            ls = [company, a, job_name, tag, advantage, job_detail, "\n", "\n"]
            with open("lagou.txt", "a") as f:
                for item in ls:
                    f.write(item)
            sleep(2)
            obj.close()
            obj.switch_to_window(handles[0])
        sleep(2)
        print("="*50)
        obj.find_element_by_xpath(r"//*[@id='order']/li/div[4]/div[2]").click()
        sleep(2)
    obj.quit()


get_data(chrome_obj)
