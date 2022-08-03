from ReportDataClass import ReportData
from GetDataClass import data as dt
import logger

if __name__ == '__main__':

    # 申请一个日志对象
    log = logger.Logger()
    # 申请一个数据对象对数据进行操作
    list = dt()
    # list.get_list()
    # 追加数据
    nrows = list.write_excel_xls_append()
    print(nrows)  # 当前文件行数

    for i in range(3003, nrows):  # 从指定行数开始上传事件
        type, content, phone = list.read_data(i)  # 获取上传事件需要的登录账号，事件类型code，事件内容
        if (type is None) & (content is None) & (phone is None):  # 其中任一值未获取到，跳出循环，获取下一行数据
            continue
        firtype, sectype = list.type_to_code(i)  # 事件类型转code，code对应在app上对应类型
        count1, count2 = list.picture_count(i)  # 获取事件中的图片数目， 图片为必填项，当图片为空判定为数据问题
        if (count1 == 0) | (count2 == 0):
            list.tag_data_error(i)  # 标记当前数据的状态为数据异常 ，并跳出循环
            continue

        log.write("{0}开始操作APP{0}".format("*" * 10))
        report = ReportData()
        report.app_clear()  # 清除APP缓存
        report.open_location()   # 开启定位权限
        report.open_album()  # 打开相册
        report.open_app()  # 启动APP
        # report.login(phone, "bgfg1000lbfwlXP#") # 登录
        message = report.login(phone, "bgfg1000lbfwlXP#")
        if message == '当前网络名称:WIFI':  # 获取登录成功的提示信息，登录失败则标记数据为登录失败
            report.goto_disposal()  # 进入处置页面
            report.fill_in_disposal()  # 打开自行处置
            report.fill_in_Report_type(firtype, sectype)  # 选择事件类型
            report.fill_in_location()  # 选择位置
            # report.fill_in_degree_emergency(3) # 选择事件紧急类型
            report.write_Event(content)  # 事件概述
            report.getpicture(count1, count2)  # 选择图片
            submitresult = report.submit()  # 提交事件
            if submitresult == '上报成功':  # 获取上报事件提示，上报成功则标记事件为上报成功
                list.tag_submit(i)
            # report.logout() # 退出登录
            report.stop_app()  # 停止APP
            list.delete_picture()  # 删除图片
            log.write("当前阶段{}".format(report.state))
        else:
            list.tag_login_error(i)  # 登录失败时标记数据，跳出循环，获取下一行数据
            continue
