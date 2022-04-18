from ReportDataClass import ReportData
from GetDataClass import data as dt
import logger

if __name__ == '__main__':

    log = logger.Logger()
    list = dt()
    # list.get_list()
    nrows = list.write_excel_xls_append()
    print(nrows)

    for i in range(190, nrows):
        type, content, phone = list.read_data(i)  # 获取数据
        if ((type is None) & (content is None) & (phone is None)):  # 返回值为空则跳出循环
            continue
        firtype, sectype = list.type_to_code(i)  # 类型转code
        count1, count2 = list.picture_count(i)
        if ((count1 == 0) | (count2 == 0)):
            list.tag_data_error(i)
            continue

        log.write("{0}开始操作APP{0}".format("*" * 10))
        report = ReportData()
        report.app_clear()
        report.open_location()
        report.open_album()
        report.open_app()  # 启动APP
        # report.login(phone, "bgfg1000lbfwlXP#") # 登录
        message = report.login(phone, "bgfg1000lbfwlXP#")
        if message == '当前网络名称:WIFI':
            report.goto_disposal()
            report.fill_in_disposal()
            report.fill_in_Report_type(firtype, sectype)  # 选择事件类型
            report.fill_in_location()
            report.write_Event(content)  # 事件概述
            report.getpicture(count1, count2)  # 选择图片
            submitresult = report.submit()  # 提交事件
            if submitresult == '上报成功':
                list.tag_submit(i)
            # report.logout() # 退出登录
            report.stop_app()  # 停止APP
            list.delete_picture()  # 删除图片
            log.write("当前阶段{}".format(report.state))
        else:
            list.tag_login_error(i)
            continue
