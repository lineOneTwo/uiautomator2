from ReportDataClass import ReportData
from GetDataClass import data as dt

if __name__ == '__main__':
    list = dt()
    # list.get_list()
    nrows = list.write_excel_xls_append()
    print(nrows)

    for i in range(1,nrows):
        type, content, phone = list.read_data(i) # 获取数据
        if ((type is None)&(content is None)&(phone is None)): # 返回值为空则跳出循环
            continue
        firtype, sectype  = list.type_to_code(i) # 类型转code
        count = list.picture_count(i)
        print("{0}开始操作APP{0}".format("*"*10))
        report = ReportData()
        report.app_clear()
        report.open_location()
        report.open_album()
        report.open_app() # 启动APP
        #report.login('13734206025', "bgfg1000lbfwlXP#") # 登录
        report.login(phone, "bgfg1000lbfwlXP#") # 登录
        report.goto_disposal()
        report.fill_in_disposal()
        report.fill_in_location()
        report.write_Event(content) # 事件概述
        report.fill_in_Report_type(firtype, sectype) # 选择事件类型
        report.getpicture(count)  # 选择图片
        report.submit() # 提交事件
        list.tag_submit(i)
        # report.logout() # 退出登录
        report.stop_app() # 停止APP
        list.delete_picture() # 删除图片
        print("当前阶段{}".format(report.state))

