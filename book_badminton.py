"""
@user:Do丶
@time:2018/12/26 22:55
"""
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# 程序基于python3.7开发，程序运行无需电脑有python环境，但注意把chromedriver放到chrome的安装目录，比如我的是“C:\Users\dell\AppData\Local\Google\Chrome\Application”
# 不同chrome浏览器的chromedriver有差异，百度下下载与版本对应的chromedriver即可
# 还需要把chromedriver所在的文件夹路径添加到环境变量中，要不程序找不到
# 程序打包用的pyinstaller，在cmd命令行中输入“pyinstaller -F 'book_badminton.py' -i 'pi.ico'”命令即可打包程序
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton, QLabel, QLineEdit, QGridLayout, QComboBox, \
    QCheckBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QCoreApplication, QSettings
from book_yumaoqiu import Book


class Example(QWidget):
    def __init__(self):  # 初始化界面
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 500, 350)  # 设置主窗口在屏幕出现的位置
        self.setWindowIcon(QIcon('1.bmp'))  # 设置窗口图标
        QToolTip.setFont(QFont('SansSerif', 10))  # 设置提示框的字体
        self.setWindowTitle('约球emm..')  # 标题
        # self.setToolTip('This is a <b>QWidget</b> widget')
        lbl1 = QLabel('此脚本用于定三天后的英东羽毛球场地', self)
        lbl1.setFixedSize(300, 20)  # 设置label的长度，默认没这么长
        lbl1.setFont(QFont("Roman times", 12, QFont.Bold))
        lbl1.move(60, 20)  # 标签位置
        title = QLabel('netid', self)
        author = QLabel('password', self)
        review = QLabel('预约时间')
        combo = QComboBox()  # 下拉栏
        combo.addItem("早上")
        combo.addItem("下午")
        combo.addItem("晚上")
        self.playtime = combo.currentText()
        self.name = QLineEdit()  # 文本输入框
        self.name.textChanged.connect(self.change1)  # 绑定change1，得到改变的值，下类似
        self.ps = QLineEdit()
        self.ps.textChanged.connect(self.change2)
        self.ps.setEchoMode(QLineEdit.Password)
        self.bt = QLineEdit()
        self.bt.textChanged.connect(self.change3)
        self.booktime = self.bt.text()
        combo.activated[str].connect(self.change4)
        # <b>标签是常用的html语法，表示字体加粗
        self.bt.setToolTip(
            '登陆时间，需要补0，日期时刻之间有个空格，格式样例：<b>2019-09-27 10:05:10</b>')
        grid = QGridLayout()  # 设置网格布局并在网格中设置各个元件的位置
        grid.setSpacing(10)
        grid.addWidget(title, 0, 0)
        grid.addWidget(self.name, 0, 1)
        grid.addWidget(author, 1, 0)
        grid.addWidget(self.ps, 1, 1)
        grid.addWidget(review, 2, 0)
        grid.addWidget(self.bt, 2, 1)
        grid.addWidget(combo, 3, 0)
        self.checkBox_remeberpassword = QCheckBox()  # 是否保存密码的勾选框
        self.checkBox_remeberpassword.setText("记住密码")
        grid.addWidget(self.checkBox_remeberpassword, 3, 1)
        self.setLayout(grid)
        self.init_login_info()  # 读入保存的配置文件中的登录名、密码等信息
        qbtn = QPushButton('退出', self)
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.setToolTip('退出')
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(340, 300)
        cbtn = QPushButton('约！', self)
        cbtn.resize(qbtn.sizeHint())
        cbtn.move(110, 300)
        cbtn.clicked.connect(self.book_place)  # 绑定订场函数
        # self.show()

    def book_place(self):
        self.save_login_info()  # 记住密码
        Example.hide(self)  # 现在界面已经没用了，隐藏界面
        Book().auto_book(
            self.netid,
            self.password,
            self.booktime,
            self.playtime)  # 传入输入的参数，调用订场函数
        Example.close(self)  # 关闭程序

    def save_login_info(self):
        settings = QSettings("config.ini", QSettings.IniFormat)
        settings.setValue("account", self.name.text())
        settings.setValue("password", self.ps.text())
        settings.setValue("logtime", self.bt.text())
        settings.setValue(
            "remeberpassword",
            self.checkBox_remeberpassword.isChecked())

    def init_login_info(self):  # 在界面中初始化用户名、登陆密码、预定时间的信息
        # QSettings了解一下，打开config,ini文件
        settings = QSettings("config.ini", QSettings.IniFormat)
        the_account = settings.value("account")  # 赋值，下同
        the_password = settings.value("password")
        the_logtime = settings.value("logtime")
        the_remeberpassword = settings.value("remeberpassword")
        self.name.setText(the_account)
        self.bt.setText(the_logtime)
        if the_remeberpassword == "true" or the_remeberpassword:  # 是否选了记住密码
            self.checkBox_remeberpassword.setChecked(True)
            self.ps.setText(the_password)

    def change1(self, a):  # 检测文本输入框内更新的函数，下同
        self.netid = a

    def change2(self, b):
        self.password = b

    def change3(self, c):
        self.booktime = c

    def change4(self, d):
        self.playtime = d


if __name__ == '__main__':  # 程序的主入口
    app = QApplication(sys.argv)
    w = Example()
    w.show()
    sys.exit(app.exec_())
