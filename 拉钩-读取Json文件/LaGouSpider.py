import requests
import math, datetime
import pandas as pd
import random, time
from LaGouSettings import headers, user_agents


class LaGouSpider():
    def __init__(self):
        self.total_page = 1
        self.headers = headers

    def get_time(self):
        now = datetime.datetime.now()
        timeStamp = int(now.timestamp() * 1000)
        geshi = "%Y%m%d%H%M%S"
        time1 = datetime.datetime.strftime(now, geshi)
        return time1, timeStamp

    def get_data_json(self, i):
        requests_url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false'
        data = {
            'first': 'true',
            'pn': i,
            'kd': '自然语言处理'
        }
        time1, timeStamp = self.get_time()
        self.headers['Cookie'] = self.headers['Cookie'].format(timeStamp=timeStamp, time=time1)
        self.headers['User-Agent'] = random.choice(user_agents)
        response = requests.post(requests_url, data=data, headers=self.headers)
        print(i,response.status_code)
        response = response.json()
        return response['content']['positionResult']

    def analyse_data(self, response_json):
        every_page_job = []
        for job in response_json['result']:
            python_job = []
            python_job.append(job['companyFullName'])
            python_job.append(job['companyShortName'])
            python_job.append(job['companySize'])
            python_job.append(job['financeStage'])
            python_job.append(job['district'])
            python_job.append(job['positionName'])
            python_job.append(job['workYear'])
            python_job.append(job['education'])
            python_job.append(job['salary'])
            python_job.append(job['positionAdvantage'])
            every_page_job.append(python_job)
        return every_page_job

    def run(self,num=1):
        for i in range(num, self.total_page + 1):
            response_json = self.get_data_json(i)
            data_list = self.analyse_data(response_json)
            if num == 1:
                total_count = response_json['totalCount']
                self.total_page = math.ceil(total_count / 15)
                df = pd.DataFrame(data=data_list,
                                  columns=['公司全名', '公司简称', '公司规模', '融资阶段', '区域', '职位名称', '工作经验', '学历要求', '工资', '职位福利'])
                df.to_csv('LG自然语言处理.csv', index=False, encoding='utf-8-sig', mode='a')
            print(data_list)
            df = pd.DataFrame(data=data_list,
                              columns=['公司全名', '公司简称', '公司规模', '融资阶段', '区域', '职位名称', '工作经验', '学历要求', '工资', '职位福利'])
            df.to_csv('LG自然语言处理.csv', index=False, encoding='utf-8-sig', mode='a',header=0)
            time.sleep(15)
            if num == 1:
                self.run(num=2)


if __name__ == "__main__":
    spider = LaGouSpider()
    spider.run()
