import sys

import requests
import json
import xlrd
import urllib.request
import os
from xlutils.copy import copy
import logger
import time

fileurl = 'http://111.53.13.252/'  # 京东云线上环境地址
events_url = "http://111.53.13.252/admin_community/smart_community_information/search/emergency/{0}/10"  # 事件列表接口
details_url = "http://111.53.13.252/admin_community/smart_community_information/emergency/"  # 事件详情接口地址
header = {"content-type": "application/x-www-form-urlencoded"}
citizenPhone = ''  # 需上传的手机号

# dir1 = r'C:\Users\Administrator\Nox_share\ImageShare\res\drawable-hdpi'  # 事发时图片保存路径
# dir2 = r'C:\Users\Administrator\Nox_share\ImageShare\res\mipmap-xhdpi-v4'  # 处置后图片保存路径
dir1 = r'C:\Users\admin\Nox_share\ImageShare\res\drawable-hdpi'  # 事发时图片保存路径
dir2 = r'C:\Users\admin\Nox_share\ImageShare\res\mipmap-xhdpi-v4'  # 处置后图片保存路径

log = logger.Logger()


class data:

    def get_message_data(self, citizenPhone):
        try:
            body = {"userAcceptance": 0, "userId": "3", "emergencyStatus": '2', 'citizenPhone': citizenPhone,
                    'startDate': '2022-04-18 00:00:00', 'endDate': '2022-04-18 23:59:59'}
            get_json = requests.post(events_url.format(1), data=body, headers=header)
            message_json = json.loads(get_json.text)
            # print(message_json)
            message_data = message_json["data"]["resultList"]
            pages = message_json["data"]["totalPages"]
            if pages > 1:
                for i in range(2, pages + 1):
                    next_pages = requests.post(events_url.format(i), data=body, headers=header)
                    next_pages_json = json.loads(next_pages.text)
                    # print(next_pages_json)
                    next_pages_data = next_pages_json["data"]["resultList"]
                    message_data = next_pages_data + message_data
            return message_data
        except Exception:
            log.write("接口调用异常")

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

        try:
            personbook = xlrd.open_workbook("平城区网格员基本信息.xls")  # 打开指定文档
            sheetName = personbook.sheet_names()  # 获取表格所有sheet名称
            rows_new = ''  # 行数
            for i in range(len(sheetName)):
                personsheet = personbook.sheet_by_name(sheetName[i])  # 获取总表
                rows_old = personsheet.nrows  # 获取表格中已存在的数据的行数
                for i in range(2, rows_old):  # 从第二行开始
                    person_phone = personsheet.cell_value(i, 2)  # 获取指定单元格数据
                    log.write(person_phone)
                    message_data = self.get_message_data(person_phone)  # 获取接口返回的事件数据
                    index = len(message_data)  # 获取需要写入数据的行数

                    workbook = xlrd.open_workbook('test.xlsx')  # 打开工作簿
                    worksheet = workbook.sheet_by_name('sheet1')  # 获取工作簿中的sheet1
                    cols = worksheet.col_values(0, 1)  # 获取第一列内容，从第二行开始
                    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数

                    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
                    new_worksheet = new_workbook.get_sheet(0)  # 获取第一个sheet
                    count = 0  # 追加条数

                    for i in range(index):
                        if message_data[i]['emergencyId'] in cols:
                            log.write("事件{0}已添加".format(message_data[i]['emergencyId']))
                        else:
                            new_worksheet.write(count + rows_old, 0,
                                                message_data[i]['emergencyId'])  # 追加写入数据，从count+rows_old行开始写入
                            new_worksheet.write(count + rows_old, 1, message_data[i]['createTime'])
                            new_worksheet.write(count + rows_old, 2, message_data[i]['emergencyTypeId'])
                            new_worksheet.write(count + rows_old, 3,
                                                message_data[i]['emergencyTypeCodeDesc'])
                            new_worksheet.write(count + rows_old, 4, message_data[i]['emergencyTitle'])
                            new_worksheet.write(count + rows_old, 5, message_data[i]['citizenName'])
                            new_worksheet.write(count + rows_old, 6, message_data[i]['citizenPhone'])
                            new_worksheet.write(count + rows_old, 7, message_data[i]['citizenAddress'])
                            new_worksheet.write(count + rows_old, 8, message_data[i]['emergencyContent'])
                            new_worksheet.write(count + rows_old, 9, 0)
                            new_worksheet.write(count + rows_old, 10, time.strftime("%Y-%m-%d, %H:%M:%S"))
                            count += 1
                            # print("事件{0}写入成功".format(message_data[i]['emergencyId']))
                    new_workbook.save('test.xlsx')  # 保存工作簿
                    rows_new = count + rows_old  # 获取表格中已存在的数据的行数
                    log.write("当前行数{}".format(rows_new))
                    log.write("{0}写入数据完成{0}".format("*" * 10))
            return rows_new
        except:
            workbook = xlrd.open_workbook('test.xlsx')  # 打开工作簿
            worksheet = workbook.sheet_by_name('sheet1')  # 获取工作簿中的sheet1
            rows_new = worksheet.nrows  # 获取表格中已存在的数据的行数
            return rows_new

    # 读取数据
    def read_data(self, i):
        type = None
        content = None
        phone = None
        workbook = xlrd.open_workbook('test.xlsx')  # 打开excel
        worksheet = workbook.sheet_by_name('sheet1')  # 获取sheet1内容
        # 判断是否已上传，并获取字段值
        if worksheet.row_values(i)[9] == 1:
            log.write("事件{0}已上传".format(worksheet.row_values(i)[0]))
            return type, content, phone
        elif worksheet.row_values(i)[9] == 2:
            log.write("{0}账号登录失败".format(worksheet.row_values(i)[6]))
            return type, content, phone
        elif worksheet.row_values(i)[9] == 0:
            type = worksheet.row_values(i)[3]
            content = worksheet.row_values(i)[8]
            # print("事件概述：{0}".format(content))
            phone = worksheet.row_values(i)[6]
            return type, content, phone
        elif worksheet.row_values(i)[9] == 3:
            log.write("{0}数据异常".format(worksheet.row_values(i)[0]))
            return type, content, phone

    # 标记上传成功
    def tag_submit(self, i):
        try:
            workbook = xlrd.open_workbook('test.xlsx')  # 打开excel
            new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
            new_worksheet = new_workbook.get_sheet(0)  # 获取第一个sheet
            new_worksheet.write(i, 9, 1)  # 上传成功为1
            new_worksheet.write(i, 10, time.strftime("%Y-%m-%d, %H:%M:%S"))  # 标记时间
            new_workbook.save('test.xlsx')  # 保存工作簿
        except:
            log.write("修改状态失败")

    # 标记登录失败
    def tag_login_error(self, i):
        try:
            workbook = xlrd.open_workbook('test.xlsx')  # 打开excel
            new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
            new_worksheet = new_workbook.get_sheet(0)  # 获取第一个sheet
            new_worksheet.write(i, 9, 2)  # 登录失败为2
            new_worksheet.write(i, 10, time.strftime("%Y-%m-%d, %H:%M:%S"))  # 标记时间
            new_workbook.save('test.xlsx')  # 保存工作簿
        except:
            log.write("修改状态失败")

    # 标记数据异常
    def tag_data_error(self, i):
        try:
            workbook = xlrd.open_workbook('test.xlsx')  # 打开excel
            new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
            new_worksheet = new_workbook.get_sheet(0)  # 获取第一个sheet
            new_worksheet.write(i, 9, 3)  # 数据异常为3
            new_worksheet.write(i, 10, time.strftime("%Y-%m-%d, %H:%M:%S"))  # 标记时间

            new_workbook.save('test.xlsx')  # 保存工作簿
        except:
            log.write("修改状态失败")

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
    def get_eventtype(self, i):
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
        if len(eventtype) == 2:
            firsttype = eventtype[0]
            secondtype = eventtype[1]
        else:
            firsttype = eventtype[0]
            secondtype = ''
        return firsttype, secondtype

    # 获取事发时图片张数，并下载图片
    def picture_count(self, i):
        workbook = xlrd.open_workbook('test.xlsx')  # 打开excel
        worksheet = workbook.sheet_by_name('sheet1')  # 获取sheet1内容
        # 获取第i行的事件id
        id = worksheet.row_values(i)[0]
        log.write("事件id：{0}".format(id))
        try:
            self.delete_picture()
            url = details_url + id
            log.write(url)
            header = {"content-type": "application/x-www-form-urlencoded"}
            get_json = requests.get(url=url, headers=header)
            message_json = json.loads(get_json.text)

            # 下载事发时图片
            shifa = message_json["data"]["emergency_fileList"]
            shifacount = len(shifa)
            log.write('事发时图片张数 ：{}'.format(shifacount))
            # 判断数组中是否包含图片地址
            for t in range(shifacount):
                shifafiles = message_json["data"]["emergency_fileList"][t]["fileUrl"]
                if shifafiles:
                    shifapath = fileurl + shifafiles
                    log.write("事发时图片地址：{0}".format(shifapath))
                    urllib.request.urlretrieve(shifapath, dir1 + '\\{0}.jpeg'.format(t))  # 下载图片到指定路径 dir
                    time.sleep(3)
                else:
                    shifacount = 0
                    log.write("事发时图片地址为0")

            # 下载处置后图片
            chuzhi = message_json["data"]["emergency_results_root"]["emergency_results_fileList"]
            chuzhicount = len(chuzhi)
            log.write('处置后图片张数 ：{}'.format(chuzhicount))
            # 判断数组中是否包含图片地址
            for j in range(chuzhicount):
                chuzhifiles = message_json["data"]["emergency_results_root"]["emergency_results_fileList"][j]["fileUrl"]
                if chuzhifiles:
                    chuzhipath = fileurl + chuzhifiles
                    log.write("处置后图片地址：{0}".format(chuzhipath))
                    urllib.request.urlretrieve(chuzhipath, dir2 + '\\{0}.jpeg'.format(j))  # 下载图片到指定路径 dir
                else:
                    chuzhicount = 0
                    log.write("处置后图片地址为0")

            return shifacount, chuzhicount
        except:
            log.write("获取图片超时")

    # 清空图片
    def delete_picture(self):
        # 指定路径

        for root, dirs, files in os.walk(dir1):
            for name in files:
                if name.endswith(".jpeg"):  # 填写规则
                    os.remove(os.path.join(root, name))
                    print("Delete File: " + os.path.join(root, name))

        for root, dirs, files in os.walk(dir2):
            for name in files:
                if name.endswith(".jpeg"):  # 填写规则
                    os.remove(os.path.join(root, name))
                    print("Delete File: " + os.path.join(root, name))

        # 类型转code

    def type_to_code(self, i):
        global fircode, seccode
        eventtype = self.get_eventtype(i)
        print('事件类型：{0}'.format(eventtype))

        # excel表中的事件大类，对应到APP的大类code码
        if eventtype[0] == '疫情防控':
            fircode = 5
            typelist_1 = ['']
            typelist_2 = ['涉疫排查']
            typelist_3 = []
            typelist_4 = []
            typelist_5 = []
            typelist_6 = ['涉疫宣传', '其他', '涉疫矛盾纠纷', '涉疫隐患']
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
        elif eventtype[0] == '治安问题':
            fircode = 2
            typelist_1 = ['涉黑涉恶']
            typelist_2 = ['']
            typelist_3 = ['']
            typelist_4 = ['']
            typelist_5 = ['治安乱点', '治安和刑事案件']
            typelist_6 = ['黄赌毒问题']
            typelist_7 = ['传销组织']
            typelist_8 = ['']
            typelist_9 = ['电信诈骗']
            typelist_10 = ['']
            typelist_12 = ['非法集资']
            typelist_13 = ['民爆物品、危险化学品等']
            typelist_14 = ['校园周边秩序']
            typelist_15 = ['人口密集场所安全']
            typelist_16 = ['其他']
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
            elif eventtype[1] in typelist_12:
                seccode = 12
            elif eventtype[1] in typelist_13:
                seccode = 13
            elif eventtype[1] in typelist_14:
                seccode = 14
            elif eventtype[1] in typelist_15:
                seccode = 15
            elif eventtype[1] in typelist_16:
                seccode = 16
            else:
                seccode = ''
        elif eventtype[0] == '风险隐患':
            fircode = 3
            typelist_1 = ['国家安全', '铁路沿线安全', '道路交通安全', '消防安全', '校园周边安全']
            typelist_2 = ['']
            typelist_3 = ['']
            typelist_4 = ['']
            typelist_5 = ['环境卫生', '其他']
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
            else:
                seccode = ''
        elif eventtype[0] == '信访问题':
            fircode = 4
            typelist_1 = ['退役军人群体']
            typelist_2 = ['']
            typelist_3 = ['']
            typelist_4 = ['非法集资或民间融资群体']
            typelist_5 = ['']
            typelist_6 = ['']
            typelist_7 = ['']
            typelist_8 = ['农民工讨薪群体']
            typelist_9 = ['其他', '小区物业管理群体', '房地产群体', '征地拆迁补偿群体']
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
            else:
                seccode = ''
        elif eventtype[0] in ['其他事件', '宣传工作', '矛盾纠纷']:
            fircode = 6
            seccode = ''

        # excel表中的事件小类，对应到APP的小类code码
        # if fircode <= 5 :
        #     # 小类转换
        #     typelist_1 = ['劳资关系', '涉黑涉恶', '国家安全', '军队退役人员群体', '情况摸底','铁路沿线安全','道路交通安全','消防安全','校园周边安全']
        #     typelist_2 = ['权属纠纷', '道路交通', '涉疫排查']
        #     typelist_3 = ['经济纠纷']
        #     typelist_4 = ['旅游领域']
        #     typelist_5 = ['消防安全', '环境卫生','道路交通安全','其他','治安乱点']
        #     typelist_6 = ['医患关系', '涉疫宣传', '其他', '涉疫矛盾纠纷', '涉疫隐患','黄赌毒问题']
        #     typelist_7 = ['物业纠纷','传销组织','']
        #     typelist_8 = ['教育领域']
        #     typelist_9 = ['小区物业管理群体','征地拆迁补偿群体']
        #     typelist_10 = ['']
        #     typelist_12 = ['民爆物品、危险化学品等']
        #     typelist_13 = ['']
        #     typelist_14 = ['']
        #     typelist_15 = ['人口密集场所安全']
        #     typelist_16 = ['']
        #     typelist_17 = ['邻里纠纷']
        #     if eventtype[1] in typelist_1:
        #         seccode = 1
        #     elif eventtype[1] in typelist_2:
        #         seccode = 2
        #     elif eventtype[1] in typelist_3:
        #         seccode = 3
        #     elif eventtype[1] in typelist_4:
        #         seccode = 4
        #     elif eventtype[1] in typelist_5:
        #         seccode = 5
        #     elif eventtype[1] in typelist_6:
        #         seccode = 6
        #     elif eventtype[1] in typelist_7:
        #         seccode = 7
        #     elif eventtype[1] in typelist_8:
        #         seccode = 8
        #     elif eventtype[1] in typelist_9:
        #         seccode = 9
        #     elif eventtype[1] in typelist_10:
        #         seccode = 10
        #     elif eventtype[1] in typelist_12:
        #         seccode = 12
        #     elif eventtype[1] in typelist_13:
        #         seccode = 13
        #     elif eventtype[1] in typelist_14:
        #         seccode = 14
        #     elif eventtype[1] in typelist_15:
        #         seccode = 15
        #     elif eventtype[1] in typelist_16:
        #         seccode = 16
        #     elif eventtype[1] in typelist_17:
        #         seccode = 17
        # else:
        #     seccode = ''

        print('fircode :{0},seccode :{1}'.format(fircode, seccode))
        return fircode, seccode


if __name__ == '__main__':
    # data().get_list()
    data().write_excel_xls_append()
    # data().read_excel()
    # data().read_data(2)
    data().picture_count(82)
    # data().delete_picture()
    # data().read_data(2)
    # data().get_eventtype(i)
    # data().type_to_code(i)
