import requests
import json
import xlsxwriter as xw
import xlrd
import urllib.request
import os

url = "http://121.30.189.198:6003/smart_community_information/search/emergency/1/10"
header = {"content-type": "application/x-www-form-urlencoded"}
body = {"userAcceptance": 0, "userId": "3", "emergencyStatus": 2}
dir = r'C:\Users\Administrator\Nox_share\ImageShare\res\mipmap-xhdpi-v4'  # 图片保存路径

class data:

    def get_message_data(self):
        get_json = requests.post(url, data=body, headers=header)
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


    # 存储数据
    def save_data(self):
        message_data = self.get_message_data()
        for q in range(len(message_data)):
            workbook = xw.Workbook('test.xlsx')  # 创建工作簿
            worksheet1 = workbook.add_worksheet("sheet1")  # 创建子表
            worksheet1.activate()  # 激活表
            title = ['事件id', '来源', '类型', '类型描述', '标题', '姓名', '手机号', '地址', '事件概述']  # 设置表头
            worksheet1.write_row('A1', title)  # 从A1单元格开始写入表头
            i = 2  # 从第二行开始写入数据
            for j in range(len(message_data)):
                insertData = [message_data[j]["emergencyId"], message_data[j]["emergencySource"], message_data[j]["emergencyTypeId"],
                              message_data[j]["emergencyTypeCodeDesc"], message_data[j]["emergencyTitle"], message_data[j]["citizenName"],
                              message_data[j]["citizenPhone"], message_data[j]["citizenAddress"], message_data[j]["emergencyContent"]]
                row = 'A' + str(i)
                worksheet1.write_row(row, insertData)
                i += 1
            workbook.close()  # 关闭表


    # 读取数据
    def read_data(self,i):
        global secondtype, firsttype
        # 打开excel
        Excelfile = xlrd.open_workbook(r'D:\Program Files\JetBrains\PyCharm Community Edition 2020.2\appium\test.xlsx')
        # 获取sheet内容
        sheet = Excelfile.sheet_by_name('sheet1')
        # 获取字段值
        type = sheet.row_values(i)[3]
        content = sheet.row_values(i)[8]
        print("事件概述：{0}".format(content))
        phone = sheet.row_values(i)[6]
        return type, content,phone



    # 获取类型文字  需要从第一行开始取
    def get_eventtype(self,i):
        global firsttype, secondtype
        # 打开excel
        Excelfile = xlrd.open_workbook(r'D:\Program Files\JetBrains\PyCharm Community Edition 2020.2\appium\test.xlsx')
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
        # 打开excel
        Excelfile = xlrd.open_workbook(r'D:\Program Files\JetBrains\PyCharm Community Edition 2020.2\appium\test.xlsx')
        # 获取sheet内容
        sheet = Excelfile.sheet_by_name('sheet1')
        # 获取第i行的事件id
        id = sheet.row_values(i)[0]
        print("事件id：{0}".format(id))
        url = "http://sqwy.wt.com:5130/smart_community_information/emergency/{0}".format(id)
        header = {"content-type": "application/x-www-form-urlencoded"}
        get_json = requests.get(url=url, headers=header)
        message_json = json.loads(get_json.text)
        message_data = message_json["data"]["emergency_fileList"]
        count = len(message_data)
        print('图片张数 ：{}'.format(count))
        for j in range(count):
            fileurl = 'http://sqwy.wt.com:5130/'
            path = fileurl + message_data[j]['fileUrl']
            print(path)
            urllib.request.urlretrieve(path, dir + '\\{0}.jpeg'.format(j))  # 下载图片到指定路径 dir
        return count


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
        global fircode,seccode
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
            typelist_6 = ['医患关系', '涉疫宣传', '其他']
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
    #data().save_data()
    data().picture_count(2)
    data().delete_picture()
    # for i in range(1,5):
    #     data().read_data(i)
    #     data().get_eventtype(i)
    #     data().type_to_code(i)
