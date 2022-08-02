import requests
import json
import xlrd
import urllib.request
import os
from xlutils.copy import copy
import logger
import time

events_url = "http://111.53.13.252/admin_community/smart_community_information/search/emergency/{0}/10"  # 事件列表接口
header = {"content-type": "application/x-www-form-urlencoded"}

log = logger.Logger()


class data:

    def get_message_data(self, citizenPhone):
        try:
            body = {"userAcceptance": 0, "userId": "315", "pageNum": "1", "count": "10", "emergencyStatus": '2',
                    'citizenPhone': citizenPhone, "orgId": "100", "emergencyTypeOneId": "", "emergencyTypeTwoId": "",
                    "orgSubsetCode": "", "citizenName": "", "superviseStatus": "", "ifThisOrg": "",
                    'startDate': '2022-01-01 00:00:00', 'endDate': '2022-08-01 23:59:59'}
            get_json = requests.post(events_url.format(1), data=body, headers=header)  # 获取第一页的数据
            # rep = get_json.json()
            # print(rep)
            message_json = json.loads(get_json.text)
            print(message_json)
            message_data = message_json["data"]["resultList"]
            print(message_data)
            pages = message_json["data"]["totalPages"]
            print(pages)
            if pages >= 2:
                for i in range(2, pages + 1):
                    next_pages = requests.post(events_url.format(i), data=body, headers=header)
                    next_pages_json = json.loads(next_pages.text)
                    # print(next_pages_json)
                    next_pages_data = next_pages_json["data"]["resultList"]
                    message_data = next_pages_data + message_data
            return message_data
        except Exception:
            log.write("接口调用异常")



    def get_message_data_no(self, citizenPhone):
        body = {"userAcceptance": 0, "userId": "315", "pageNum": "1", "count": "10", "emergencyStatus": '2',
                'citizenPhone': citizenPhone, "orgId": "100", "emergencyTypeOneId": "", "emergencyTypeTwoId": "",
                "orgSubsetCode": "", "citizenName": "", "superviseStatus": "", "ifThisOrg": "",
                'startDate': '2022-01-01 00:00:00', 'endDate': '2022-08-01 23:59:59'}
        get_json = requests.post(events_url.format(1), data=body, headers=header)  # 获取第一页的数据
        # rep = get_json.json()
        # print(rep)
        message_json = json.loads(get_json.text)
        print(message_json)
        message_data = message_json["data"]["resultList"]
        print(message_data)
        pages = message_json["data"]["totalPages"]
        print(pages)
        if pages >= 2:
            for i in range(2, pages + 1):
                next_pages = requests.post(events_url.format(i), data=body, headers=header)
                next_pages_json = json.loads(next_pages.text)
                # print(next_pages_json)
                next_pages_data = next_pages_json["data"]["resultList"]
                message_data = next_pages_data + message_data
        return message_data



if __name__ == '__main__':
    data().get_message_data_no('13834027505')
