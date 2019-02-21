import cv2
from aip import AipOcr
import time
import datetime
from selenium import webdriver
from PIL import Image
import os
"""
@user:Do丶
@time:2018/12/25 22:10
"""
# !/usr/bin/env python
# -*- coding:utf-8 -*-
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException

'''
使用的浏览器为chrome，依赖包请事先安装好，使用中大netid登陆，验证码识别使用的百度ai，有时候会填错重新登陆即可，没时间改进，见谅。
'''


class Book:
    # 默认浏览器设置为chrome
    # 百度ai识图申请得账号密钥
    APP_ID = '15273108'
    API_KEY = 'BQl4DK7sGjwvMKFvBB9UNVPD'
    SECRET_KEY = 'dYGm5MvIzXVWQXqHU1h1fYRs5xMQEKyF'
    aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    # 定义参数变量，调用百度ai识图的参数
    options = {
        'detect_direction': 'true',
        'language_type': 'CHN_ENG',
    }

    # 自动订的函数，前两个参数不用介绍，第三个是开始刷场的时间，最后一个是定早上or下午or晚上的场
    def auto_book(self, username, password, buytime, ex_time):
        # 生成有头的chrome浏览器
        self.driver = webdriver.Chrome()
        # 最大化窗口
        self.driver.maximize_window()
        # 得到选择的是早上，下午还是晚上
        sw = {
            "早上": [
                '09:01-10:00',
                '10:01-11:00'],
            "下午": [
                '14:01-15:00',
                '15:01-16:00',
                '16:01-17:00'],
            "晚上": [
                '19:01-20:00',
                '20:01-21:00',
                '21:01-22:00']}
        sw1 = sw.get(ex_time, None)
        # 进入定羽毛球的初始页面，等1.5秒刷新完成，这些都是登陆的操作，不影响按点抢场
        self.driver.get("http://gym.sysu.edu.cn/product/show.html?id=61")
        time.sleep(1.5)
        # 点击登陆按钮进入登陆界面
        self.driver.find_element_by_link_text("登录").click()
        time.sleep(0.2)
        # 输入传入的用户名和密码
        self.driver.find_element_by_id("username").send_keys(username)
        time.sleep(0.2)
        self.driver.find_element_by_id("password").send_keys(password)
        # 得到验证码字符串
        t1 = self.Convertimg()
        t2 = t1.replace(' ', '')
        t = t2.replace('.', '')
        # 检验验证码字符串长度是否是4且由数字和字母构成，不是则点击验证码刷新验证码并再次验证，直到满足要求
        # while len(t)!=4 or t.__contains__(':') or t.__contains__('.'):
        while len(t) != 4 or t.isalnum() == False:
            imglocation = ("//img[@name='captchaImg']")  # 验证码的xpath地址
            item = self.driver.find_element_by_xpath(imglocation)
            item.click()
            time.sleep(0.1)
            t1 = self.Convertimg()
            t2 = t1.replace(' ', '')
            t = t2.replace('.', '')
            # if len(t)==4:
            #     break
        self.driver.find_element_by_id("captcha").send_keys(t)  # 填入验证码
        time.sleep(1)
        self.driver.find_element_by_name("submit").click()  # 点击提交按钮登陆
        # 刷新页面，成为登陆页面
        self.driver.get("http://gym.sysu.edu.cn/product/show.html?id=61")
        self.driver.execute_script('window.open()')  # 另外打开一个选项卡，进行两个场一起定
        self.driver.execute_script('window.open()')  # 另外打开一个选项卡，进行两个场一起定
        self.driver.switch_to.window(self.driver.window_handles[1])  # 切换选项卡
        # 这个选项卡也进入相同页面
        self.driver.get('http://gym.sysu.edu.cn/product/show.html?id=61')
        self.driver.switch_to.window(self.driver.window_handles[2])  # 切换选项卡
        # 这个选项卡也进入相同页面
        self.driver.get('http://gym.sysu.edu.cn/product/show.html?id=61')
        while True:  # 进入一个无限循环，一直判断是否到达预定时间
            now = datetime.datetime.now()
            if now.strftime('%Y-%m-%d %H:%M:%S') == buytime:  # 其实就是一个字符串匹配的过程
                self.driver.refresh()  # 刷新页面
                # 因为中大的羽毛球场不是0点整开始放场的，往往迟个两分钟，所以我们需要检测是否有三天后的标签
                while self.is_element_exist(
                        '//*[@id="datesbar"]/div/ul/li[4]') != True:
                    self.driver.refresh()  # 不存在则刷新页面直到出现为止
                    time.sleep(1.2)  # 1.2秒刷新一次
                if self.is_element_exist(
                        '//*[@id="datesbar"]/div/ul/li[4]'):  # 出现了
                    self.driver.find_element_by_xpath(
                        '//*[@id="datesbar"]/div/ul/li[4]').click()  # 点击三天后的标签
                    block_list = self.driver.find_elements_by_xpath(
                        '//span[@class="cell football easyui-tooltip tooltip-f"]')  # 得到元素（场地）列表
                    for block_place in block_list:  # 对每一个场地进行是否有场的判断
                        if block_place.get_attribute(
                                "data-timer") == sw1[0]:  # 是否在我们选的时间有场
                            block_place.click()  # 有的话就订下来
                            self.driver.find_element_by_xpath(
                                '//*[@id="reserve"]').click()  # 确定
                            time.sleep(1)  # 等待确认页面出现
                            break
                    self.driver.find_element_by_xpath(
                        '//*[@id="reserve"]').click()  # 确定

                    self.driver.switch_to.window(
                        self.driver.window_handles[0])  # 切换到第一个选项卡进行类似的操作
                    self.driver.refresh()  # 刷新
                    self.driver.find_element_by_xpath(
                        '//*[@id="datesbar"]/div/ul/li[4]').click()
                    block_list = self.driver.find_elements_by_xpath(
                        '//span[@class="cell football easyui-tooltip tooltip-f"]')
                    for block_place in block_list:
                        if block_place.get_attribute(
                                "data-timer") == sw1[1]:
                            block_place.click()
                            self.driver.find_element_by_xpath(
                                '//*[@id="reserve"]').click()
                            time.sleep(1)
                            break
                    self.driver.find_element_by_xpath(
                        '//*[@id="reserve"]').click()

                    self.driver.switch_to.window(
                        self.driver.window_handles[1])  # 切换到第一个选项卡进行类似的操作
                    self.driver.refresh()  # 刷新
                    self.driver.find_element_by_xpath(
                        '//*[@id="datesbar"]/div/ul/li[4]').click()
                    block_list = self.driver.find_elements_by_xpath(
                        '//span[@class="cell football easyui-tooltip tooltip-f"]')
                    for block_place in block_list:
                        if block_place.get_attribute(
                                "data-timer") == sw1[2]:
                            block_place.click()
                            self.driver.find_element_by_xpath(
                                '//*[@id="reserve"]').click()
                            time.sleep(1)
                            break
                    self.driver.find_element_by_xpath(
                        '//*[@id="reserve"]').click()
                break
        self.conf()
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.conf()
        self.driver.switch_to.window(self.driver.window_handles[2])
        self.conf()

    def conf(self):  # 确认并购买的函数
        time.sleep(1)
        try:
            self.driver.find_element_by_xpath(
                '//button[@class="confirm"]').click()
            time.sleep(1)
            self.driver.find_element_by_xpath(
                '//img[@src="/images/payment/ydzx.png"]').click()
            self.driver.find_element_by_xpath(
                '//button[@class="button-large button-info"]').click()
            now = datetime.datetime.now()
            print(now.strftime('%Y-%m-%d %H:%M:%S'))
            print('purchase success')
        except ElementNotVisibleException as e:
            print("没有抢到，被定完了")

    def is_element_exist(self, command):  # 基于xpath判断元素是否存在
        try:
            s2 = self.driver.find_element_by_xpath(command)
        except NoSuchElementException as e:
            return False
        return True

    def Convertimg(self):
        imglocation = ("//img[@name='captchaImg']")  # 验证码的xpath地址
        item = self.driver.find_element_by_xpath(imglocation)
        item.screenshot("yanzhengma.png")
        self.clearimage('yanzhengma.png')
        result = self.aipOcr.basicGeneral(
            self.get_file_content('final.png'), self.options)
        text = result['words_result'][0]['words']
        os.remove('clear.png')
        # os.remove('final.png')
        return text

    def clearimage(self, originadd):
        img = Image.open(originadd)  # 读取系统的内照片
        # 将黑色干扰线替换为白色
        width = img.size[0]  # 长度
        height = img.size[1]  # 宽度
        for i in range(0, width):  # 遍历所有长度的点
            for j in range(0, height):  # 遍历所有宽度的点
                data = (img.getpixel((i, j)))  # 打印该图片的所有点
                if (data[0] <= 25 and data[1] <=
                        25 and data[2] <= 25):  # RGBA的r,g,b均小于25
                    img.putpixel((i, j), (255, 255, 255, 255))  # 则这些像素点的颜色改成白色
        img = img.convert("RGB")  # 把图片强制转成RGB
        img.save('clear.png')  # 保存修改像素点后的图片
        # 灰度化
        Grayimg = cv2.cvtColor(cv2.imread('clear.png'), cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(Grayimg, 160, 255, cv2.THRESH_BINARY)
        cv2.imwrite('clear.png', thresh)
        os.remove('yanzhengma.png')
        self.ResizeImage('clear.png', 'final.png', 90, 32, 'png')

    def ResizeImage(self, filein, fileout, width, height, type):  # 改变图片尺寸
        img = Image.open(filein)
        out = img.resize((width, height), Image.ANTIALIAS)
        out.save(fileout, type)

    def get_file_content(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()


# 第一个参数为用户名，第二个参数为密码，第三个参数为登陆时间（建议前两三分钟登陆即可）
# if __name__ =='main':
#     b1=Book()
#     b1.auto_book('', '', '2019-01-23 00:02:15','下午')
