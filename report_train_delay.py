import requests, json
from datetime import date
from arrange_train_report import ArrangeTrainData

WEB_HOOK_URL = "Your web hook url"

rail_data = ArrangeTrainData()
delay_report = rail_data.report_format()

requests.post(
    WEB_HOOK_URL,
    data = json.dumps({
        'fields': [
            {
                'value': delay_report,
            }
        ],
        'username': "Den-Tatsu",
        'icon_emoji': ":male-pilot: ",
        'mrkdwn_in': ["text"],
    }))
