import uiautomator2 as u2
import random
import time
from GetDataClass import *


def sleep():
    time.sleep(1)


class ReportData:
    state = 0

    def __init__(self):
        # self.d = u2.connect("emulator-5554")
        self.d = u2.connect("127.0.0.1:62001")

    # 清除APP缓存
    def app_clear(self):
        self.d.app_clear('com.wanggeyuan.zongzhi')
        print("清除APP缓存")


    # 打开相册
    def open_album(self):
        self.d.app_start('com.android.gallery3d', 'com.android.gallery3d.app.GalleryActivity')
        self.d.click(0.485, 0.677)
        self.d.app_stop('com.android.gallery3d')
        print("启动相册")
        self.state = 0


    # 打开APP，定位在登录页
    def open_app(self):
        self.d.app_stop('com.wanggeyuan.zongzhi')
        self.d.app_start('com.wanggeyuan.zongzhi', 'com.wanggeyuan.zongzhi.main.ui.activity.LoginActivity')
        print("启动APP")
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
        print("完成登录")
        self.state = 2

    # 进入处置页面
    def goto_disposal(self):
        try:
            self.d.xpath('//*[@resource-id="com.wanggeyuan.zongzhi:id/fab01Add"]').click()
            sleep()
            self.state = 3
        except:
            print('未找到加号按钮')




    # 打开自行处置
    def fill_in_disposal(self):
        try:
            self.d.xpath('//*[@resource-id="com.wanggeyuan.zongzhi:id/fb_one"]').click()
            sleep()
            self.state = 4
        except:
            print('未找到指派按钮')


    # 填写事件描述
    def write_Event(self, str):
        self.d.click(0.143, 0.165)
        sleep()
        self.d.send_keys(str, clear=True)
        self.state = 5

    # 确定位置
    def fill_in_location(self):
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

    # 上传图片
    def getpicture(self,num):
        try:
            self.d.xpath('//*[@resource-id="com.wanggeyuan.zongzhi:id/shijian_photo"]').click()
            sleep()
            self.d.xpath('//*[@text="相册"]').click()
            sleep()
            self.d.xpath('//*[@resource-id="com.android.packageinstaller:id/permission_allow_button"]').click()
            sleep()
            self.d.xpath(
                '//*[@resource-id="com.wanggeyuan.zongzhi:id/grid_view_album_select"]/android.widget.FrameLayout[1]/android.widget.ImageView[1]').click()
            sleep()
            for i in range(1, num + 1):
                self.d.xpath((
                                 '//*[@resource-id="com.wanggeyuan.zongzhi:id/grid_view_image_select"]/android.widget.FrameLayout[{0}]/android.widget.ImageView[1]').format(
                    i)).click()
            sleep()
            self.d.xpath('//android.support.v7.widget.LinearLayoutCompat').click()
            print("上传图片")
            sleep()
        except:
            print("未获取到目标图片")


    # 确定紧急程度类型
    # setid=1:一般，2：紧急；3：重大，4：突发，5：疑难复杂
    def fill_in_degree_emergency(self, setId):
        self.d.click(0.151, 0.539)
        sleep()
        if setId == 1:
            self.d.click(0.179, 0.422)
            sleep()
        elif setId == 2:
            self.d.click(0.179, 0.478)
            sleep()
        elif setId == 3:
            self.d.click(0.179, 0.541)
            sleep()
        elif setId == 4:
            self.d.click(0.179, 0.599)
            sleep()
        elif setId == 5:
            self.d.click(0.179, 0.657)
            sleep()

        self.state = 7


    # 填写上报类型
    # 1:矛盾纠纷，2：治安问题；3：风险隐患，4：利益群体信访诉求；5：其他
    def fill_in_Report_type(self, pId, bId):
        self.d.click(0.151, 0.597)
        sleep()
        if pId == 1:
            self.d.click(0.107, 0.131)
            sleep()
            self.report_Type_1(bId)
        elif pId == 2:
            self.d.click(0.107, 0.212)
            sleep()
            self.report_Type_2(bId)
        elif pId == 3:
            self.d.click(0.107, 0.293)
            sleep()
            self.report_Type_3(bId)
        elif pId == 4:
            self.d.click(0.103, 0.375)
            sleep()
            self.report_Type_4(bId)
        elif pId == 5:
            self.d.click(0.107, 0.456)
            sleep()
            self.report_Type_5(bId)
        elif pId == 6:
            self.d.click(0.107, 0.536)
            sleep()

        self.state = 8

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
        self.d.xpath('//*[@resource-id="com.wanggeyuan.zongzhi:id/right_text"]').click()

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
        print("退出登录")
        self.state = 9

    # 关闭APP
    def stop_app(self):
        self.d.app_stop("com.wanggeyuan.zongzhi")
        self.state = 10

if __name__ == '__main__':
    rep = ReportData()
    rep.app_clear()
    rep.open_album()
    rep.open_app()
    rep.login()
    rep.goto_disposal()
    rep.fill_in_disposal()
    rep.getpicture(2)
