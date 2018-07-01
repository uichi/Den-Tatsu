import requests, cchardet, datetime, re
from bs4 import BeautifulSoup
from collections import OrderedDict

# Scrape train traffic information.
class TrainData:

    def __init__(self):
        self.url = OrderedDict()
        self.url = {
                '都営浅草線': 'https://www.kotsu.metro.tokyo.jp/subway/schedule/asakusa_log.html',\
                '都営三田線': 'https://www.kotsu.metro.tokyo.jp/subway/schedule/mita_log.html',\
                '都営新宿線': 'https://www.kotsu.metro.tokyo.jp/subway/schedule/shinjuku_log.html',\
                '都営大江戸線': 'https://www.kotsu.metro.tokyo.jp/subway/schedule/oedo_log.html'
              }

    def scrape_delay_data(self, line_name):
        line_name_list = [i.find('img').get('alt') for i in self.soup.find_all(class_="acess_i")]
        traffic_status_list =  [i.text for i in self.soup.find_all(class_="text-tit-xlarge")]
        traffic_cause_list = [i.text for i in self.soup.find_all(class_="cause")]
        line_info_dict = {}
        for i, line_info in enumerate(self.soup.find_all("tr")):
            # range error measure.
            if len(self.soup.find_all("tr")) == i+1:
                break
            # make the traffic status dictionary
            # This line have a traffic jam.
            if bool(self.soup.find_all("tr")[i+1](class_="cause")):
                line_info_dict[line_info.find(class_="text-tit-xlarge").text] = self.soup.find_all("tr")[i+1](class_="cause").text
            # Line information is not exist.
            elif bool(line_info.find(class_="acess_i")) is False:
                continue
            # This line traffic is not problem.
            else:
                line_info_dict[line_info.find(class_="text-tit-xlarge").text] = ""

        return line_info_dict

    def scrape_deley_toei_data(self):
        url = self.url
        delay_info = OrderedDict()
        for rail_name in url:
            response = requests.get(url[rail_name])
            response_encoding = cchardet.detect(response.content)["encoding"]
            soup = BeautifulSoup(response.content, 'lxml', from_encoding=response_encoding)
            try:
                rail_info = soup.find(class_='InformationUnkou').find(class_='operation__item')
                release_time = rail_info.find(class_='haishin').text
                release_date = re.split('[年月日時分]', release_time)[0:3]
                date_now = datetime.datetime.strptime(''.join(release_date), "%Y%m%d")
                # Only report today's information.
                if date_now + datetime.timedelta(days=1) < datetime.datetime.today():
                    delay_info[rail_name] = {'time': time_now.strftime("%Y年%m月%d日%H時%M分 配信"), 'status': '平常運転', 'cause': '遅延情報はありません。'}
                else:
                    status = rail_info.find(class_='state')
                    rail_status = rail_info.find(class_='state').text
                    rail_delay_cause = rail_info.find(class_='txt').text
                    delay_info[rail_name] = {'time': release_time, 'status': rail_status, 'cause': rail_delay_cause}
            except:
                time_now = datetime.datetime.today()
                delay_info[rail_name] = {'time': time_now.strftime("%Y年%m月%d日%H時%M分 配信"), 'status': '平常運転', 'cause': '遅延情報はありません。'}
        return delay_info
