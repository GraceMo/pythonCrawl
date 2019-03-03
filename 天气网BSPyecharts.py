from bs4 import BeautifulSoup
import requests
from pyecharts import Bar

'''
构造url列表
爬取数据,BeautufulSoup
数据可视化
'''


class Weather_Spider():
    def __init__(self, url, headrs):
        self.url = url
        self.headers = headers

    def get_urls(self):
        areas = ['hb', 'db', 'hd', 'hz', 'hn', 'xb', 'xn', 'gat']
        # url_list = list(map(lambda x:self.url.format(x),areas))
        return [self.url.format(i) for i in areas]

    def get_response(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def parse(self, response, parser='lxml'):
        html = BeautifulSoup(response, parser)  # html5lib容错能力强于lxml的解析方式
        div = html.find('div', class_='conMidtab')
        tables = div.find_all('table')
        weather_list = []
        for table in tables:
            trs = table.find_all('tr')
            for index, tr in enumerate(trs[2:]):
                tds = tr.find_all('td')
                city_name = list(tds[0].stripped_strings)[0]
                if index == 0:
                    city_name = list(tds[1].stripped_strings)[0]
                low_temp = tds[-2].string
                city_dict = {'city_name': city_name, 'low_temp': int(low_temp)}
                weather_list.append(city_dict)
        return weather_list

    def process_data(self, weather_list):
        weather_list.sort(key=lambda x: x['low_temp'])
        data0 = weather_list[0:10]
        data1 = weather_list[-10:]
        data1.reverse()
        citys0 = list(map(lambda x: x['city_name'], data0))
        temps0 = list(map(lambda x: x['low_temp'], data0))
        chart = Bar('十大最低/高温度城市排行')
        chart.add('最低', citys0, temps0)
        chart.render('temper.html')

    def run(self):
        url_list = self.get_urls()
        weather_list = []
        for url in url_list:
            response = self.get_response(url)
            if 'gat' in url:
                weather_list_area = self.parse(response, parser='html5lib')
            else:
                weather_list_area = self.parse(response)
            weather_list += weather_list_area
        self.process_data(weather_list)


if __name__ == '__main__':
    url = 'http://www.weather.com.cn/textFC/{}.shtml'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    spider = Weather_Spider(url, headers)
    spider.run()
