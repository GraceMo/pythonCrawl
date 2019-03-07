'''搜索关键字python,并爬取详情页的信息
设置搜索
获取每页的详情页列表
爬取详情页,获取信息
点击下一页,进入循环,直到页码结束
'''
from selenium import webdriver
from lxml import etree
import re, time, csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class LaGouSpider():
    driver_path = r'D:\chromedriver\chromedriver.exe'

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=self.driver_path)
        self.domain_url = "https://www.lagou.com/"
        self.title = ['title', 'salary', 'education', 'work_year', 'work_sort', 'address', 'company_name', 'require', 'url']
        self.file = open('LaGou1.csv', 'a', encoding='utf8', newline='')
        self.writer = csv.DictWriter(self.file, self.title)
        self.writer.writeheader()

    def run(self):
        self.set_search()
        while True:
            print(self.driver.current_url)
            detail_page_datas = []
            WebDriverWait(driver=self.driver, timeout=10).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(@class,'pager_next')]"))
            )
            detail_url_list = self.parse_page_url()
            for detail_url in detail_url_list:
                data_dict = self.parse_detail(detail_url)
                print(data_dict)
                detail_page_datas.append(data_dict)
            self.writer.writerows(detail_page_datas)
            next_page_tag = self.driver.find_element_by_xpath("//span[contains(@class,'pager_next ')]")
            if "pager_next_disabled" in next_page_tag.get_attribute('class'):
                break
            next_page_tag.click()
            time.sleep(1)
        self.file.close()

    def parse_detail(self, detail_url):
        # 返回详情页的详细信息data_dict,打开并切换到新的窗口,并关闭切换回来
        self.driver.execute_script("window.open('%s')" % detail_url)
        self.driver.switch_to.window(self.driver.window_handles[1])
        WebDriverWait(self.driver, timeout=10).until(
            EC.presence_of_element_located((By.XPATH, "//dd[@class='job_request']"))
        )
        text = self.driver.page_source
        html = etree.HTML(text)
        title = html.xpath("//span[@class='name']/text()")[0]
        salary = html.xpath("//span[@class='salary']/text()")[0].strip()
        education = html.xpath("//dd[@class='job_request']/p/span[4]/text()")[0].replace('/', '').strip()
        work_year = html.xpath("//dd[@class='job_request']/p/span[3]/text()")[0].replace('/', '').strip()
        work_sort = html.xpath("//dd[@class='job_request']/p/span[5]/text()")[0].replace('/', '').strip()
        address = html.xpath("//div[@class='work_addr']//text()")
        address = ''.join(address).replace('查看地图', '').strip()
        address = re.sub('\s', '', address)
        company_name = html.xpath("//em[@class='fl-cn']/text()")[0].strip()
        require = html.xpath("//div[@class='job-detail']//text()")
        require = ''.join(require).strip()
        data_dict = {
            'title': title,
            'salary': salary,
            'education': education,
            'work_year': work_year,
            'work_sort': work_sort,
            'address': address,
            'company_name': company_name,
            'require': require,
            'url': self.driver.current_url
        }
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        return data_dict

    def parse_page_url(self):  # 返回每页的详情页url--detail_url_list
        text = self.driver.page_source
        html = etree.HTML(text)
        url_detail_list = html.xpath("//div[@class='s_position_list ']//li//a[@class='position_link']/@href")
        print(url_detail_list)
        return url_detail_list

    def set_search(self):
        # 切换城市,设置搜索(python爬虫),返回搜索页面
        self.driver.get(self.domain_url)
        self.driver.implicitly_wait(10)
        city_switch_tag = self.driver.find_element_by_xpath('//div[@id="changeCityBox"]//li[1]/a')
        city_switch_tag.click()  # 切换城市为北京
        input_tag = self.driver.find_element_by_id('search_input')
        search_tag = self.driver.find_element_by_id('search_button')
        input_tag.send_keys('python爬虫')
        search_tag.click()


if __name__ == '__main__':
    spider = LaGouSpider()
    spider.run()
