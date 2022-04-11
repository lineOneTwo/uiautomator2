import uiautomator2 as u2
import random
import time
from GetDataClass import *
from GetDataClass import *

def sleep():
    time.sleep(2)


class ReportData:
    state = 0

    def __init__(self):
        # self.d = u2.connect("emulator-5554")
        self.d = u2.connect("127.0.0.1:62001")

    # 清除APP缓存
    def app_clear(self):
        self.d.app_clear('com.wanggeyuan.zongzhi')
        log.write("清除APP缓存")


    # 打开相册
    def open_album(self):
        self.d.app_start('com.android.gallery3d', 'com.android.gallery3d.app.GalleryActivity')
        self.d.click(0.485, 0.677)
        self.d.app_stop('com.android.gallery3d')
        log.write("启动相册")
        self.state = 0


    # 打开APP，定位在登录页
    def open_app(self):
        self.d.app_stop('com.wanggeyuan.zongzhi')
        self.d.app_start('com.wanggeyuan.zongzhi', 'com.wanggeyuan.zongzhi.main.ui.activity.LoginActivity')
        log.write("启动APP")
        self.state = 1

    # 登陆
    def login(self,username,password):  # ,username,password
        # 用户名
        self.d(resourceId="com.wanggeyuan.zongzhi:id/username_et").click()
        sleep()
        self.d.send_keys(username, clear=True)
        # 密码
        self.d(resourceId="com.wanggeyuan.zongzhi:id/password_et").click()
        sleep()
        self.d.send_keys(password, clear=True)
        # 点登录
        self.d.xpath('//*[@resource-id="com.wanggeyuan.zongzhi:id/login_btn"]').click()
        sleep()
        message = self.d.toast.get_message() # 获取提示信息
        log.write(message)
        log.write("登录账号：{0}".format(username))
        self.state = 2
        return message



    # 进入处置页面
    def goto_disposal(self):
        try:
            self.d.xpath('//*[@resource-id="com.wanggeyuan.zongzhi:id/fab01Add"]').click()
            sleep()
            self.state = 3
        except:
            log.write('未找到加号按钮')



    # 打开自行处置
    def fill_in_disposal(self):
        try:
            self.d.xpath('//*[@resource-id="com.wanggeyuan.zongzhi:id/fb_two"]').click()
            sleep()
            self.state = 4
        except:
            log.write('未找到指派按钮')


    # 填写事件描述
    def write_Event(self, str):
        try:
            self.d.click(0.143, 0.165)
            sleep()
            self.d.send_keys(str, clear=True)
            self.state = 5
        except:
            log.write("未找到输入框")

    # 开启定位权限
    def open_location(self):
        self.d.app_start('com.android.settings', 'com.android.settings.Settings$ManageApplicationsActivity')
        sleep()
        self.d.click(0.081, 0.703)
        sleep()
        self.d.click(0.121, 0.405)
        sleep()
        self.d.click(0.909, 0.204)
        sleep()
        self.d.app_stop('com.android.settings')


    # 确定位置
    def fill_in_location(self):
        try:
            self.d.click(0.37, 0.48)
            sleep()
            self.d.click(0.932, 0.498)
            sleep()
            self.d.click(0.932, 0.498)
            sleep()
            self.d.swipe(0.454, 0.102, random.randint(1, 100) / 100, random.randint(1, 100) / 100, duration=0.1)
            self.d.swipe(0.454, 0.102, random.randint(1, 100) / 100, random.randint(1, 100) / 100, duration=0.1)
            self.d.swipe(0.454, 0.102, random.randint(1, 100) / 100, random.randint(1, 100) / 100, duration=0.1)
            self.d.swipe(0.454, 0.102, random.randint(1, 100) / 100, random.randint(1, 100) / 100, duration=0.1)
            sleep()
            self.d.click(0.163, 0.561)
            self.state = 6
        except:
            log.write("未找到确定按钮")

    # 上传事发时 处置后图片
    def getpicture(self,num1,num2):
        try:
            if num1 > 0:
                self.d.xpath('//*[@resource-id="com.wanggeyuan.zongzhi:id/shijian_photo"]').click()
                sleep()
                self.d.xpath('//*[@text="相册"]').click()
                sleep()
                self.d.xpath('//*[@resource-id="com.android.packageinstaller:id/permission_allow_button"]').click()
                sleep()
                self.d.xpath('//*[@text="drawable-hdpi"]').click()
                sleep()
                for i in range(1, num1 + 1):
                    self.d.xpath((
                        '//*[@resource-id="com.wanggeyuan.zongzhi:id/grid_view_image_select"]/android.widget.FrameLayout[{0}]/android.widget.ImageView[1]').format(
                        i)).click()
                sleep()
                self.d.xpath('//android.support.v7.widget.LinearLayoutCompat').click()
                # 事发时图片
                self.d.xpath('//*[@resource-id="com.wanggeyuan.zongzhi:id/tv_shifashi"]').click()
            else:
                log.write("无需上传事发时图片")



            if num2 > 0:
                self.d.xpath('//*[@resource-id="com.wanggeyuan.zongzhi:id/shijian_photo"]').click()
                sleep()
                self.d.xpath('//*[@text="相册"]').click()
                sleep()
                self.d.xpath('//*[@text="mipmap-xhdpi-v4"]').click()
                sleep()
                for i in range(1, num2 + 1):
                    self.d.xpath((
                        '//*[@resource-id="com.wanggeyuan.zongzhi:id/grid_view_image_select"]/android.widget.FrameLayout[{0}]/android.widget.ImageView[1]').format(
                        i)).click()
                sleep()
                self.d.xpath('//android.support.v7.widget.LinearLayoutCompat').click()
                # 处置后图片
                self.d.xpath('//*[@resource-id="com.wanggeyuan.zongzhi:id/tv_chuzhihou"]').click()
            else:
                log.write("无需上传处置后图片")

            sleep()
        except:
            log.write("未获取到目标图片")


    # 确定紧急程度类型
    # setid=1:一般，2：紧急；3：重大，4：突发，5：疑难复杂
    def fill_in_degree_emergency(self, setId):
        self.d.xpath('//*[@resource-id="com.wanggeyuan.zongzhi:id/shangbao_chengduBtn"]').click()
        sleep()
        if setId == 1:
            self.d.xpath('//*[@resource-id="com.wanggeyuan.zongzhi:id/md_contentRecyclerView"]/android.widget.LinearLayout[1]').click()
            sleep()
        elif setId == 2:
            self.d.xpath('//*[@resource-id="com.wanggeyuan.zongzhi:id/md_contentRecyclerView"]/android.widget.LinearLayout[2]').click()
            sleep()
        elif setId == 3:
            self.d.xpath('//*[@resource-id="com.wanggeyuan.zongzhi:id/md_contentRecyclerView"]/android.widget.LinearLayout[3]').click()
            sleep()
        elif setId == 4:
            self.d.xpath('//*[@resource-id="com.wanggeyuan.zongzhi:id/md_contentRecyclerView"]/android.widget.LinearLayout[4]').click()
            sleep()
        elif setId == 5:
            self.d.xpath('//*[@resource-id="com.wanggeyuan.zongzhi:id/md_contentRecyclerView"]/android.widget.LinearLayout[5]').click()
            sleep()

        self.state = 7


    # 填写上报类型
    # 1:矛盾纠纷，2：治安问题；3：风险隐患，4：利益群体信访诉求；5：其他
    def fill_in_Report_type(self, pId, bId):
        try:
            self.d.xpath('//*[@resource-id="com.wanggeyuan.zongzhi:id/shangbao_type"]').click()
            sleep()
            if pId == 1:
                self.d.xpath('//*[@text="矛盾纠纷"]').click()
                sleep()
                self.report_Type_1(bId)
            elif pId == 2:
                self.d.xpath('//*[@text="治安问题"]').click()
                sleep()
                self.report_Type_2(bId)
            elif pId == 3:
                self.d.xpath('//*[@text="风险隐患"]').click()
                sleep()
                self.report_Type_3(bId)
            elif pId == 4:
                self.d.xpath('//*[@text="利益群体信访诉求"]').click()
                sleep()
                self.report_Type_4(bId)
            elif pId == 5:
                self.d.xpath('//*[@text="疫情防控"]').click()
                sleep()
                self.report_Type_5(bId)
            elif pId == 6:
                self.d.xpath('//*[@text="其他事件"]').click()
                sleep()

            self.state = 8
        except:
            log.write("未找到事件类型")

    # 1:劳资关系，2：权属纠纷，3：经济纠纷；4：旅游领域，5：环境污染，6：医患，7：物业纠纷。8：教育，9：保险，10：交通事故纠纷；11：国土，12：集体土地，13：村矿，14：婚姻，15：邻里，16：农村干部。17：涉疫矛盾，18：其他
    def report_Type_1(self, setId):
        if setId == 1:
            self.d.click(0.107, 0.212)
            sleep()
        elif setId == 2:
            self.d.click(0.107, 0.293)
            sleep()
        elif setId == 3:
            self.d.click(0.103, 0.375)
            sleep()
        elif setId == 4:
            self.d.click(0.107, 0.456)
            sleep()
        elif setId == 5:
            self.d.click(0.107, 0.536)
            sleep()
        elif setId == 6:
            self.d.click(0.087, 0.615)
            sleep()
        elif setId == 7:
            # 物业纠纷
            self.d.click(0.107, 0.695)
            sleep()
        elif setId == 8:
            # 8：教育，
            self.d.click(0.107, 0.776)
            sleep()
        elif setId == 9:
            # 保险
            self.d.click(0.107, 0.857)
            sleep()
        elif setId == 10:
            self.d.click(0.107, 0.938)
            sleep()
        elif setId == 11:
            # 11：国土
            self.d.swipe(0.107, 0.938, 0.107, 0.857, duration=0.2)
            sleep()
            self.d.click(0.107, 0.938)
            sleep()
        elif setId == 12:
            # 12：集体土地，
            self.d.swipe(0.107, 0.938, 0.107, 0.776, duration=0.2)
            sleep()
            self.d.click(0.107, 0.938)
            sleep()
        elif setId == 13:
            # 13：村矿
            self.d.swipe(0.107, 0.938, 0.107, 0.695, duration=0.2)
            sleep()
            self.d.click(0.107, 0.938)
            sleep()
        elif setId == 14:
            # 14：婚姻
            self.d.swipe(0.107, 0.938, 0.087, 0.615, duration=0.2)
            sleep()
            self.d.click(0.107, 0.938)
            sleep()
        elif setId == 15:
            # 15：邻里
            self.d.swipe(0.107, 0.938, 0.107, 0.536, duration=0.3)
            sleep()
            self.d.click(0.107, 0.938)
            sleep()
        elif setId == 16:
            # 16：农村干部。
            self.d.swipe(0.107, 0.938, 0.107, 0.456, duration=0.4)
            sleep()
            self.d.click(0.107, 0.938)
            sleep()
        elif setId == 17:
            # 17：涉疫矛盾
            self.d.swipe(0.107, 0.938, 0.103, 0.375, duration=0.5)
            sleep()
            self.d.click(0.107, 0.938)
            sleep()
        elif setId == 18:
            # 18：其他
            self.d.swipe(0.107, 0.938, 0.107, 0.293, duration=0.5)
            sleep()
            self.d.click(0.107, 0.938)
            sleep()

    def report_Type_2(self, setId):

        if setId == 1:
            self.d.click(0.107, 0.293)
            sleep()
        elif setId == 2:
            self.d.click(0.103, 0.375)
            sleep()
        elif setId == 3:
            self.d.click(0.107, 0.456)
            sleep()
        elif setId == 4:
            self.d.click(0.107, 0.536)
            sleep()
        elif setId == 5:
            self.d.click(0.087, 0.615)
            sleep()
        elif setId == 6:
            #
            self.d.click(0.107, 0.695)
            sleep()
        elif setId == 7:
            # 8：教育，
            self.d.click(0.107, 0.776)
            sleep()
        elif setId == 8:
            # 保险
            self.d.click(0.107, 0.857)
            sleep()
        elif setId == 9:
            self.d.click(0.107, 0.938)
            sleep()
        elif setId == 10:
            # 11：国土
            self.d.swipe(0.107, 0.938, 0.107, 0.857, duration=0.2)
            sleep()
            self.d.click(0.107, 0.938)
            sleep()
        elif setId == 11:
            # 12：集体土地，
            self.d.swipe(0.107, 0.938, 0.107, 0.776, duration=0.2)
            sleep()
            self.d.click(0.107, 0.938)
            sleep()
        elif setId == 12:
            # 13：村矿
            self.d.swipe(0.107, 0.938, 0.107, 0.695, duration=0.2)
            sleep()
            self.d.click(0.107, 0.938)
            sleep()
        elif setId == 13:
            # 14：婚姻
            self.d.swipe(0.107, 0.938, 0.087, 0.615, duration=0.2)
            sleep()
            self.d.click(0.107, 0.938)
            sleep()
        elif setId == 14:
            # 15：邻里
            self.d.swipe(0.107, 0.938, 0.107, 0.536, duration=0.3)
            sleep()
            self.d.click(0.107, 0.938)
            sleep()
        elif setId == 15:
            # 16：农村干部。
            self.d.swipe(0.107, 0.938, 0.107, 0.456, duration=0.4)
            sleep()
            self.d.click(0.107, 0.938)
            sleep()
        elif setId == 16:
            # 17：涉疫矛盾
            self.d.swipe(0.107, 0.938, 0.103, 0.375, duration=0.5)
            sleep()
            self.d.click(0.107, 0.938)
            sleep()

    def report_Type_3(self, setId):
        if setId == 1:
            self.d.click(0.103, 0.375)
            sleep()
        elif setId == 2:
            self.d.click(0.107, 0.456)
            sleep()
        elif setId == 3:
            self.d.click(0.107, 0.536)
            sleep()
        elif setId == 4:
            self.d.click(0.087, 0.615)
            sleep()
        elif setId == 5:
            self.d.click(0.107, 0.695)
            sleep()

    def report_Type_4(self, setId):

        if setId == 1:
            self.d.click(0.107, 0.456)
            sleep()
        elif setId == 2:
            self.d.click(0.107, 0.536)
            sleep()
        elif setId == 3:
            self.d.click(0.087, 0.615)
            sleep()
        elif setId == 4:
            #
            self.d.click(0.107, 0.695)
            sleep()
        elif setId == 5:
            #
            self.d.click(0.107, 0.776)
            sleep()
        elif setId == 6:
            #
            self.d.click(0.107, 0.857)
            sleep()
        elif setId == 7:
            self.d.click(0.107, 0.938)
            sleep()
        elif setId == 8:
            #
            self.d.swipe(0.107, 0.938, 0.107, 0.857, duration=0.2)
            sleep()
            self.d.click(0.107, 0.938)
            sleep()
        elif setId == 9:
            #
            self.d.swipe(0.107, 0.938, 0.107, 0.776, duration=0.2)
            sleep()
            self.d.click(0.107, 0.938)
            sleep()

    def report_Type_5(self, setId):
        if setId == 1:
            self.d.click(0.107, 0.536)
            sleep()
        if setId == 2:
            self.d.click(0.087, 0.615)
            sleep()
        elif setId == 3:
            #
            self.d.click(0.107, 0.695)
            sleep()
        elif setId == 4:
            #
            self.d.click(0.107, 0.776)
            sleep()
        elif setId == 5:
            #
            self.d.click(0.107, 0.857)
            sleep()
        elif setId == 6:
            self.d.click(0.107, 0.938)
            sleep()

    # 提交事件
    def submit(self):
        try:
            self.d.xpath('//*[@resource-id="com.wanggeyuan.zongzhi:id/right_text"]').click()
            submitresult = self.d.toast.get_message()  # 获取提示信息
            log.write(submitresult)
            return submitresult
        except:
            log.write("未找到提交按钮")

    # 退出
    def logout(self):
        # 退出登录
        self.d.xpath(
            '//*[@resource-id="com.wanggeyuan.zongzhi:id/tabLayout_father"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[2]').click()
        sleep()
        self.d.xpath('//*[@text="设置"]').click()
        sleep()
        self.d.xpath('//*[@resource-id="com.wanggeyuan.zongzhi:id/logout_btn"]').click()
        sleep()
        self.d.xpath('//*[@resource-id="com.wanggeyuan.zongzhi:id/md_buttonDefaultPositive"]').click()
        log.write("退出登录")
        self.state = 9

    # 关闭APP
    def stop_app(self):
        self.d.app_stop("com.wanggeyuan.zongzhi")
        self.state = 10

if __name__ == '__main__':
    rep = ReportData()
    rep.app_clear()
    rep.open_location()
    rep.open_album()
    rep.open_app()
    # rep.login()
    # rep.goto_disposal()
    # rep.fill_in_disposal()
    # rep.getpicture(2)
