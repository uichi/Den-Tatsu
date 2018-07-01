from scrape_train_delay import TrainData
from collections import OrderedDict

class ArrangeTrainData:

    def report_format(self):
        train_data = TrainData()
        delay_info = train_data.scrape_deley_toei_data()
        global delay_report
        delay_report = ''
        for i, rail_name in enumerate(delay_info):
            delay_report += '*' + rail_name + "の運行情報*\n" + \
                delay_info[rail_name]['time'] + "\n" + \
                delay_info[rail_name]['status'] + "\n" + \
                delay_info[rail_name]['cause']
            if i+1 != len(delay_info):
                delay_report += "\n----------------------------------------\n"
        return delay_report
