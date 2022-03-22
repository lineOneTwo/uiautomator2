import sys

import requests
import json
import xlrd
import urllib.request
import os
from xlutils.copy import copy


fileurl = 'http://121.30.189.198:5130/'  # 线上环境地址
events_url = "http://121.30.189.198:5130/smart_community_information/search/emergency/1/10" # 事件列表接口地址
details_url = "http://121.30.189.198:5130/smart_community_information/emergency/" # 事件详情接口地址
header = {"content-type": "application/x-www-form-urlencoded"}
body = {"userAcceptance": 0, "userId": "3", "emergencyStatus": 2}

dir = r'C:\Users\Administrator\Nox_share\ImageShare\res\drawable-hdpi'  # 本地图片保存路径


class data:

    def get_message_data(self):
        get_json = requests.post(events_url, data=body, headers=header)
        message_json = json.loads(get_json.text)
        message_data = message_json["data"]["resultList"]
        # print(message_data)
        return message_data

    def get_list(self):
        message_data = self.get_message_data()
        for i in range(len(message_data)):
            dic = message_data[i]
            # print(dic["emergencyId"])
            # print(dic["emergencySource"])
            # print(dic["emergencyTypeId"])
            # print(dic["emergencyTypeDetails"])
            # print(dic["emergencyTitle"])
            # print(dic["orgTreePath"])
            # print(dic["orgTreePathDetails"])
            # print(dic["citizenName"])
            # print(dic["citizenPhone"])
            # print(dic["citizenAddress"])
            # print(dic["emergencyAddress"])
            # print(dic["emergencyContent"])
            # print(dic["createTime"])
            # print(dic["handlerPeople"])
            # print(dic["citizenUserId"])
            # print(dic["emergencyStatus"])
            # print(dic["emergencyStatusDesc"])
            # print(dic["startTime"])
            # print(dic["stopTime"])
            # print(dic["superviseStatus"])
            # print(dic["superviseStatusDesc"])
            # print(dic["emergencyFileList"])
            # print(dic["sort"], '\n\t')

        # # 存储数据
        # def save_data(self):
        #     message_data = self.get_message_data()
        #     for q in range(len(message_data)):
        #         workbook = xw.Workbook('test.xlsx')  # 创建工作簿
        #         worksheet1 = workbook.add_worksheet("sheet1")  # 创建子表
        #         worksheet1.activate()  # 激活表
        #         title = ['事件id', '来源', '类型', '类型描述', '标题', '姓名', '手机号', '地址', '事件概述']  # 设置表头
        #         worksheet1.write_row('A1', title)  # 从A1单元格开始写入表头
        #         i = 2  # 从第二行开始写入数据
        #         for j in range(len(message_data)):
        #             insertData = [message_data[j]["emergencyId"], message_data[j]["emergencySource"],
        #                           message_data[j]["emergencyTypeId"],
        #                           message_data[j]["emergencyTypeCodeDesc"], message_data[j]["emergencyTitle"],
        #                           message_data[j]["citizenName"],
        #                           message_data[j]["citizenPhone"], message_data[j]["citizenAddress"],
        #                           message_data[j]["emergencyContent"]]
        #             row = 'A' + str(i)
        #             worksheet1.write_row(row, insertData)
        #             i += 1
        #         workbook.close()  # 关闭表

    # 追加事件数据
    def write_excel_xls_append(self):
        message_data =self.get_message_data() # 获取接口返回的事件数据
        index = len(message_data)  # 获取需要写入数据的行数

        workbook = xlrd.open_workbook('test.xlsx')  # 打开工作簿
        worksheet = workbook.sheet_by_name('sheet1')  # 获取工作簿中的sheet1
        cols = worksheet.col_values(0,1)  # 获取第一列内容，从第二行开始
        rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数

        new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
        new_worksheet = new_workbook.get_sheet(0) # 获取第一个sheet
        count = 0  # 追加条数

        for i in range(index):
            if message_data[i]['emergencyId']  in cols:
                print("事件{0}已添加".format(message_data[i]['emergencyId']))
            else:
                new_worksheet.write(count + rows_old, 0, message_data[i]['emergencyId'])  # 追加写入数据，从count+rows_old行开始写入
                new_worksheet.write(count + rows_old, 1, message_data[i]['emergencySource'])
                new_worksheet.write(count + rows_old, 2, message_data[i]['emergencyTypeId'])
                new_worksheet.write(count + rows_old, 3,
                                    message_data[i]['emergencyTypeCodeDesc'])
                new_worksheet.write(count + rows_old, 4, message_data[i]['emergencyTitle'])
                new_worksheet.write(count + rows_old, 5, message_data[i]['citizenName'])
                new_worksheet.write(count + rows_old, 6, message_data[i]['citizenPhone'])
                new_worksheet.write(count + rows_old, 7, message_data[i]['citizenAddress'])
                new_worksheet.write(count + rows_old, 8, message_data[i]['emergencyContent'])
                new_worksheet.write(count + rows_old, 9, 0)
                count += 1
                # print("事件{0}写入成功".format(message_data[i]['emergencyId']))
        new_workbook.save('test.xlsx')  # 保存工作簿
        rows_new = count + rows_old  # 获取表格中已存在的数据的行数
        print("当前行数{}".format(rows_new))
        print("{0}写入数据完成{0}".format("*" * 10))
        return rows_new

    # 读取数据
    def read_data(self,i):
        type = None
        content = None
        phone = None
        workbook = xlrd.open_workbook('test.xlsx') # 打开excel
        worksheet = workbook.sheet_by_name('sheet1') # 获取sheet1内容
        # 判断是否已上传，并获取字段值
        if worksheet.row_values(i)[9] == 1:
            print("事件{0}已上传".format(worksheet.row_values(i)[0]))
            return type, content, phone
        else:
            type = worksheet.row_values(i)[3]
            content = worksheet.row_values(i)[8]
            # print("事件概述：{0}".format(content))
            phone = worksheet.row_values(i)[6]
            return type, content, phone

    def tag_submit(self,i):
        workbook = xlrd.open_workbook('test.xlsx') # 打开excel
        new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
        new_worksheet = new_workbook.get_sheet(0)  # 获取第一个sheet
        new_worksheet.write(i, 9, 1)  # 将是否上传改为1
        new_workbook.save('test.xlsx')  # 保存工作簿

    #     # 读取数据
    #
    # def read_data(self, i):
    #     type = None
    #     content = None
    #     phone = None
    #     count = 0
    #     # 打开excel
    #     workbook = xlrd.open_workbook('test.xlsx')
    #     # 获取sheet内容
    #     worksheet = workbook.sheet_by_name('sheet1')
    #
    #     # 判断是否已上传，并获取字段值
    #     if worksheet.row_values(i)[9] == 1:
    #         print("事件{0}已上传".format(worksheet.row_values(i)[0]))
    #         return type, content, phone
    #
    #     else:
    #
    #         type = worksheet.row_values(i)[3]
    #         content = worksheet.row_values(i)[8]
    #         # print("事件概述：{0}".format(content))
    #         phone = worksheet.row_values(i)[6]
    #         new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    #         new_worksheet = new_workbook.get_sheet(0)
    #         new_worksheet.write(i, 9, 1)  # 将是否上传改为1
    #         new_workbook.save('test.xlsx')
    #         return type, content, phone

    # 获取类型文字  需要从第一行开始取
    def get_eventtype(self,i):
        global firsttype, secondtype
        # 打开excel
        Excelfile = xlrd.open_workbook('test.xlsx')
        # 获取sheet内容
        sheet = Excelfile.sheet_by_name('sheet1')
        # 获取第三列值
        type = sheet.row_values(i)[3]
        # 切片并将大类小类分别赋值
        eventtype = str(type).split('-')
        # 切片后长度为2，则包含大类小类；否则返回大类，小类置空
        if len(eventtype) == 2 :
            firsttype = eventtype[0]
            secondtype = eventtype[1]
        else:
            firsttype = eventtype[0]
            secondtype = ''
        return firsttype, secondtype


    # 获取图片张数，并下载图片
    def picture_count(self,i):
        workbook = xlrd.open_workbook('test.xlsx') # 打开excel
        worksheet = workbook.sheet_by_name('sheet1') # 获取sheet1内容
        # 获取第i行的事件id
        id = worksheet.row_values(i)[0]
        print("事件id：{0}".format(id))
        try:
            self.delete_picture()
            url = details_url + id
            print(url)
            header = {"content-type": "application/x-www-form-urlencoded"}
            get_json = requests.get(url=url, headers=header)
            message_json = json.loads(get_json.text)
            message_data = message_json["data"]["emergency_fileList"]
            count = len(message_data)
            print('图片张数 ：{}'.format(count))
            for j in range(count):
                path = fileurl + message_data[j]['fileUrl']
                print("图片地址：{0}".format(path))
                urllib.request.urlretrieve(path, dir + '\\{0}.jpeg'.format(j))  # 下载图片到指定路径 dir
            return count
        except(ConnectionError):
            print("获取图片超时")


    # 清空图片
    def delete_picture(self):
        # 指定路径

        for root, dirs, files in os.walk(dir):
            for name in files:
                if name.endswith(".jpeg"):  # 填写规则
                    os.remove(os.path.join(root, name))
                    print("Delete File: " + os.path.join(root, name))


        # 类型转code

    def type_to_code(self,i):
        global fircode, seccode
        eventtype = self.get_eventtype(i)
        print('事件类型：{0}'.format(eventtype))

        # excel表中的事件大类，对应到APP的大类code码
        if eventtype[0] == '矛盾纠纷':
            fircode = 1
        elif eventtype[0] == '治安问题':
            fircode = 2
        elif eventtype[0] == '风险隐患':
            fircode = 3
        elif eventtype[0] == '信访问题':
            fircode = 4
        elif eventtype[0] == '疫情防控':
            fircode = 5
        elif eventtype[0] in ['其他事件','宣传工作']:
            fircode = 6

        # excel表中的事件小类，对应到APP的小类code码
        if fircode <= 5 :
            # 小类转换
            typelist_1 = ['劳资关系', '涉疫隐患', '国家安全', '军队退役人员群体', '情况摸底']
            typelist_2 = ['权属纠纷', '涉黑涉恶', '涉疫排查']
            typelist_3 = ['经济纠纷']
            typelist_4 = ['旅游领域']
            typelist_5 = ['消防安全', '环境卫生','道路交通安全']
            typelist_6 = ['医患关系', '涉疫宣传', '其他','涉疫矛盾纠纷']
            typelist_7 = ['物业纠纷']
            typelist_8 = ['教育领域']
            typelist_9 = ['小区物业管理群体']
            typelist_10 = ['']
            typelist_17 = ['邻里纠纷']
            if eventtype[1] in typelist_1:
                seccode = 1
            elif eventtype[1] in typelist_2:
                seccode = 2
            elif eventtype[1] in typelist_3:
                seccode = 3
            elif eventtype[1] in typelist_4:
                seccode = 4
            elif eventtype[1] in typelist_5:
                seccode = 5
            elif eventtype[1] in typelist_6:
                seccode = 6
            elif eventtype[1] in typelist_7:
                seccode = 7
            elif eventtype[1] in typelist_8:
                seccode = 8
            elif eventtype[1] in typelist_9:
                seccode = 9
            elif eventtype[1] in typelist_10:
                seccode = 10
            elif eventtype[1] in typelist_17:
                seccode = 17
        else:
            seccode = ''

        print('fircode :{0},seccode :{1}'.format(fircode,seccode))
        return fircode , seccode



if __name__ == '__main__':
    # data().get_list()
    data().write_excel_xls_append()
    # data().read_data(2)
    data().picture_count(2)
    #data().delete_picture()
    # data().read_data(2)
    # data().get_eventtype(i)
    # data().type_to_code(i)
