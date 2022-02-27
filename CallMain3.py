import sys
import math
import xlwt
import random
import time
from ctypes import *
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from MatplotlibWidget_2 import MyFigure
from MatplotlibWidget_3 import MyFigure1
import numpy as np
import pandas as pd
from Main5 import Ui_MainWindow

from view2_up import Ui_Form
from sign3 import Ui_SignForm
from signup2 import Ui_signup

from PyQt5.QtSql import QSqlDatabase , QSqlQuery
db=QSqlDatabase.addDatabase('QSQLITE')
db.setDatabaseName('D:\program pyqt\exp02\DataUser.db')

#登录界面切进主界面
def exchange_In(self):
    Mainwin.show()
    win.close()
#主界面切回登录界面
def exchange_Out(self):
    Mainwin.return_ok=1
    Mainwin.close()
    win.show()
    #Mainwin.close()
#注册界面显示
def exchange_SignIn(self):
    Signwin.show()




class SignForm(QWidget, Ui_SignForm):
    def __init__(self):
        super(SignForm, self).__init__()
        self.setupUi(self)  # 初始化

        self.mainForm = MainForm()
        self.Sign = signupForm()
        self.pushButton.clicked.connect(self.SignIn_user)
        self.pushButton_2.clicked.connect(exchange_SignIn)
        self.pushButton_3.clicked.connect(exchange_In)

    def IDmatch(self, user, code):
        self.IDmatch_flag=0
        #打开数据库
        if not db.open():
            QMessageBox.critical(None,  ("无法打开数据库"),
            ( "无法建立到数据库的连接,这个例子需要SQLite 支持，请检查数据库配置。\n\n"
            "点击取消按钮退出应用。"),QMessageBox.Cancel )
            return False
        query=QSqlQuery()
        code_find="select code from people where user='%s'"%user
        if query.exec_(code_find):
            query.next()
            realcode = query.value(0)
            if str(code)==str(realcode):
                self.IDmatch_flag=1
            else:
                QMessageBox.information(self, "登录出错", "用户名或密码错误")
        else:
            QMessageBox.information(self, "登录出错", "用户名或密码错误")
        db.close()
        return self.IDmatch_flag

    def SignIn_user(self):
        user = self.lineEdit.text()
        code = self.lineEdit_2.text()
        flag = self.IDmatch(user, code)
        if flag == 1:
            flag = 0
            self.mainForm.show()
            self.close()

    def SignIn_tour(self):
        self.mainForm.show()
        self.close()

    def SinUp(self):
        self.Sign.show()


class signupForm(QWidget, Ui_signup):
    def __init__(self):
        super(signupForm, self).__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.Sign_Up)
        self.pushButton_2.clicked.connect(self.Sign_back)

    def Sign_Up(self):
        db.open()
        query = QSqlQuery()
        user = self.lineEdit.text()
        user_find = "select user from people where user='%s'" % user
        print(user_find)
        query.exec_(user_find)
        query.next()
        user_have = query.value(0)
        if str(user_have) == str(user):
            self.hint.setText("*该用户名已存在")
        elif not self.lineEdit_2.text() == self.lineEdit_3.text():
            self.hint.setText("*两次密码不一致")
        else:
            self.hint.setText(" ")
            user_code = "insert into people values('%s', '%s')" % (self.lineEdit.text(), self.lineEdit_2.text())
            print(user_code)
            query.exec_(user_code)
            db.close()
            self.close()

    def Sign_back(self):

        self.close()


class MainForm(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainForm, self).__init__()
        self.setupUi(self)
        self.child = ChildrenForm()

        self.gridLayout.addWidget(self.child)

        self.child.show()
        self.F = MyFigure(width=3, height=2, dpi=100)
        self.F1 = MyFigure1(width=3, height=2, dpi=100)
        self.return_ok = 0
        self.pushButton.clicked.connect(self.btn_init)
        self.pushButton_2.clicked.connect(self.gengrate_current_file)
        self.pushButton_3.clicked.connect(self.open_file)
        self.pushButton_4.clicked.connect(self.gengrate_all_file)
        self.pushButton_5.clicked.connect(self.childShow_3)
        self.start_top.triggered.connect(self.start_renew)  # 开始按钮
        self.finish_top.triggered.connect(self.childClose)  # 终止按钮
        self.stop_top.triggered.connect(self.drawText)  # 暂停按钮
        self.step_top.triggered.connect(self.stepOn)  # 步进按钮
        self.item_degree=self.listWidget.item(0)
        self.item_path = self.listWidget.item(1)
        self.item_cluster = self.listWidget.item(2)
        self.item_runtime = self.listWidget.item(3)
        self.item_state = self.listWidget.item(4)
        self.comboBox_2.currentIndexChanged.connect(self.get_way)
        self.comboBox_4.currentIndexChanged.connect(self.get_way_2)
        self.comboBox_6.currentIndexChanged.connect(self.get_way_3)
        self.comboBox.currentIndexChanged.connect(self.get_way_4)

        # 暂停flag
        self.flag_stop = 0
        # 步进flag
        self.flag_step = 0
        # 退出登录flag
        self.return_ok = 0
        # 运行时间
        self.run_time = 0
        # 模式标志
        self.mode = 1
        self.init_flag = 0
        # 设置子窗口定时器
        self.child.widget.mpl.timer = QTimer(self)
        self.child.widget.mpl.timer.timeout.connect(self.child.widget.mpl.operate)  # 与子窗口函数连接
        self.child.widget.mpl.axes.axis('off')  # 关闭子窗口坐标显示
        # 设置定时器
        self.timer_Main = QTimer(self)
        self.timer_Main.timeout.connect(self.operate_Main)

    def gengrate_current_file(self):
        text1 = self.comboBox.currentText()
        text2 = self.comboBox_2.currentText()
        text3 = self.comboBox_3.currentText()
        text4 = self.comboBox_4.currentText()
        text5 = self.comboBox_5.currentText()
        text6 = self.comboBox_6.currentText()
        print("成功")
        if self.tabWidget.currentIndex()==0:
            if text1=='prisonersDilemma' and text2=='squareGrid':
                book = xlwt.Workbook(encoding='utf-8', style_compression=0)
                sheet = book.add_sheet('sheet1', cell_overwrite_ok=True)

                for i in range(0, self.number):
                    sheet.write(0, i, self.child.widget.mpl.node_state_1[0][i])
                savepath = 'D:\program pyqt\exp02/%d.xls'%(self.run_time+1)
                book.save(savepath)



    def gengrate_all_file(self):
        text1 = self.comboBox.currentText()
        text2 = self.comboBox_2.currentText()
        text3 = self.comboBox_3.currentText()
        text4 = self.comboBox_4.currentText()
        text5 = self.comboBox_5.currentText()
        text6 = self.comboBox_6.currentText()
        if self.tabWidget.currentIndex()==0:
            if text1=='prisonersDilemma' and text2=='squareGrid':
                book = xlwt.Workbook(encoding='utf-8', style_compression=0)
                sheet = book.add_sheet('sheet1', cell_overwrite_ok=True)
                for i in range(0,5):
                    self.data=self.child.widget.mpl.node_state_2[i][0]
                    for j in range(0, 49):
                        sheet.write(i, j, self.data[j])
                savepath = 'D:\program pyqt\exp02/all_file.xls'
                book.save(savepath)


    def open_file(self):
        file, ok = QFileDialog.getOpenFileName(self, "打开", "D:\program pyqt\exp02", "ALL Files (*);;Text Files (*.xlsx)")
        #self.statusBar.showMessage(file)
        open_file = file
        open_file = str(open_file.replace('/', '\\'))
        print(open_file)


    def operate_Main(self):
        # self.timer.stop()
        if self.child.widget.mpl.stop_flag == 1:  # 设置博弈次数到了暂停
            self.drawText()


        if self.flag_step == 1:
            # self.flag_step=0
            self.timer_Main.stop()
            self.child.widget.mpl.timer.stop()
        else:
            self.run_time += 1
            self.item_runtime.setText("运行时间：" + str(self.run_time) + "s")


    def closeEvent(self, event):
        '''
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        '''
        print(self.return_ok)
        if self.return_ok == 1:
            reply = QtWidgets.QMessageBox.question(self,
                                                   '退出登录',
                                                   "少侠想回到登录界面？",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)
            self.return_ok == 0
        else:
            reply = QtWidgets.QMessageBox.question(self,
                                                   '退出',
                                                   "确认离开当前界面？",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def drawText(self):
        # 两个定时器暂停计时
        self.child.widget.mpl.timer.stop()
        self.timer_Main.stop()
        # 暂停flag和步进flag设为1
        self.flag_stop = 1
        self.flag_step = 1
        self.item_state.setText("paused")

    def stepOn(self):  # 步进按钮
        print("step:" + str(self.flag_step))
        print("stop:" + str(self.flag_stop))
        if self.flag_step == 1 and self.flag_stop == 1:
            self.timer_Main.start(50)
            self.child.widget.mpl.timer.start(50)



    def get_way_4(self):
        text1=self.comboBox.currentText()
        if text1=='prisonersDilemma':
            self.label_2.setText("S(-1<S<0)")
            self.label_26.setText("T(1<T<2)")

        if text1=='Snowdrift game':
            self.label_2.setText("S(0<S<1)")
            self.label_26.setText("T(1<T<2)")


        if text1=='harmony game':
            self.label_2.setText("S(0<S<1)")
            self.label_26.setText("T(0<T<1)")

        if text1=='stag-hunt game':
            self.label_2.setText("S(-1<S<0)")
            self.label_26.setText("T(0<T<1)")




    def get_way_3(self):

        text1 = self.comboBox_5.currentText()
        text2 = self.comboBox_6.currentText()
        if text1=='SIS' and text2 == 'squareGrid':
            self.label_19.setText("a")
            self.label_22.setText("b")
            self.label_23.setText("height")
            self.label_24.setText("width")
            self.lineEdit_13.setText("0.03")
            self.lineEdit_15.setText("0.03")
            self.lineEdit_16.setText("1")
            self.lineEdit_17.setText("1")
            self.label_19.setAlignment(Qt.AlignCenter)
            self.label_22.setAlignment(Qt.AlignCenter)
            self.mode=10

        if text1=='SI' and text2 == 'squareGrid':
            self.label_19.setText("b")

            self.label_23.setText("height")
            self.label_24.setText("width")
            self.lineEdit_13.setText("0.3")

            self.lineEdit_16.setText("1")
            self.lineEdit_17.setText("1")
            self.label_19.setAlignment(Qt.AlignCenter)
            self.label_22.setAlignment(Qt.AlignCenter)
            self.mode=19

        if text1=='SIR' and text2 == 'squareGrid':
            self.label_19.setText("b")
            self.label_22.setText("y")
            self.label_23.setText("height")
            self.label_24.setText("width")
            self.lineEdit_13.setText("0.03")
            self.lineEdit_15.setText("0.03")
            self.lineEdit_16.setText("1")
            self.lineEdit_17.setText("1")
            self.label_19.setAlignment(Qt.AlignCenter)
            self.label_22.setAlignment(Qt.AlignCenter)
            self.mode=11

        if text1=='SIR' and text2 == 'small world network':
            self.label_19.setText("probability")
            self.label_22.setText("neighbours")
            self.label_23.setText("b")
            self.label_24.setText("y")
            self.lineEdit_13.setText("0.3")
            self.lineEdit_15.setText("2")
            self.lineEdit_16.setText("0.03")
            self.lineEdit_17.setText("0.03")
            self.label_23.setAlignment(Qt.AlignCenter)
            self.label_24.setAlignment(Qt.AlignCenter)
            self.mode=12

        if text1=='SIR' and text2 == 'random network':
            self.label_19.setText("probability")
            self.label_22.setText("neighbours")
            self.label_23.setText("b")
            self.label_24.setText("y")
            self.lineEdit_13.setText("1")
            self.lineEdit_13.setEnabled(False)
            self.lineEdit_15.setText("2")
            self.lineEdit_16.setText("0.03")
            self.lineEdit_17.setText("0.03")
            self.label_23.setAlignment(Qt.AlignCenter)
            self.label_24.setAlignment(Qt.AlignCenter)
            self.mode=25



        if text1=='SIS' and text2 == 'small world network':
            self.label_19.setText("probability")
            self.label_22.setText("neighbours")
            self.label_23.setText("a")
            self.label_24.setText("b")
            self.lineEdit_13.setText("0.3")
            self.lineEdit_15.setText("2")
            self.lineEdit_16.setText("0.03")
            self.lineEdit_17.setText("0.03")
            self.label_23.setAlignment(Qt.AlignCenter)
            self.label_24.setAlignment(Qt.AlignCenter)
            self.mode=13

        if text1=='SIS' and text2 == 'random network':
            self.label_19.setText("probability")
            self.label_22.setText("neighbours")
            self.label_23.setText("a")
            self.label_24.setText("b")
            self.lineEdit_13.setText("1")
            self.lineEdit_13.setEnabled(False)
            self.lineEdit_15.setText("2")
            self.lineEdit_16.setText("0.03")
            self.lineEdit_17.setText("0.03")
            self.label_23.setAlignment(Qt.AlignCenter)
            self.label_24.setAlignment(Qt.AlignCenter)
            self.mode=24

        if text1=='SI' and text2 == 'small world network':
            self.label_19.setText("probability")
            self.label_22.setText("neighbours")
            self.label_23.setText("b")

            self.lineEdit_13.setText("0.3")
            self.lineEdit_15.setText("2")
            self.lineEdit_16.setText("0.3")

            self.label_23.setAlignment(Qt.AlignCenter)
            self.label_24.setAlignment(Qt.AlignCenter)
            self.mode=20

        if text1=='SI' and text2 == 'random network':
            self.label_19.setText("probability")
            self.label_22.setText("neighbours")
            self.label_23.setText("b")

            self.lineEdit_13.setText("1")
            self.lineEdit_13.setEnabled(False)
            self.lineEdit_15.setText("2")
            self.lineEdit_16.setText("0.3")

            self.label_23.setAlignment(Qt.AlignCenter)
            self.label_24.setAlignment(Qt.AlignCenter)
            self.mode=23

        if text1=='SIS' and text2 == 'scale-free network':
            self.label_19.setText("m0")
            self.label_22.setText("m")
            self.label_23.setText("a")
            self.label_24.setText("b")
            self.lineEdit_13.setText("3")
            self.lineEdit_15.setText("3")
            self.lineEdit_16.setText("0.03")
            self.lineEdit_17.setText("0.03")
            self.label_19.setAlignment(Qt.AlignCenter)
            self.label_22.setAlignment(Qt.AlignCenter)
            self.label_23.setAlignment(Qt.AlignCenter)
            self.label_24.setAlignment(Qt.AlignCenter)
            self.mode=14

        if text1=='SI' and text2 == 'scale-free network':
            self.label_19.setText("m0")
            self.label_22.setText("m")
            self.label_23.setText("b")

            self.lineEdit_13.setText("3")
            self.lineEdit_15.setText("3")
            self.lineEdit_16.setText("0.3")

            self.label_19.setAlignment(Qt.AlignCenter)
            self.label_22.setAlignment(Qt.AlignCenter)
            self.label_23.setAlignment(Qt.AlignCenter)
            self.label_24.setAlignment(Qt.AlignCenter)
            self.mode=21

        if text1=='SIR' and text2 == 'scale-free network':
            self.label_19.setText("m0")
            self.label_22.setText("m")
            self.label_23.setText("b")
            self.label_24.setText("y")
            self.lineEdit_13.setText("3")
            self.lineEdit_15.setText("3")
            self.lineEdit_16.setText("0.03")
            self.lineEdit_17.setText("0.03")
            self.label_23.setAlignment(Qt.AlignCenter)
            self.label_24.setAlignment(Qt.AlignCenter)
            self.label_19.setAlignment(Qt.AlignCenter)
            self.label_22.setAlignment(Qt.AlignCenter)
            self.mode=15


    def get_way_2(self):

        text3 = self.comboBox_3.currentText()
        text4 = self.comboBox_4.currentText()
        if text3=='election' and text4 == 'squareGrid':
            self.label_11.setText("temptation")
            self.label_14.setText("neighbours")
            self.lineEdit_7.setEnabled(False)
            self.lineEdit_9.setText("4")
            self.mode=7

        if text3=='Deffuant' and text4 == 'squareGrid':
            self.label_11.setText("temptation")
            self.label_14.setText("neighbours")
            self.lineEdit_7.setEnabled(False)
            self.lineEdit_9.setText("4")
            self.label_15.setText("u")
            self.label_16.setText("d")
            self.lineEdit_10.setText("0.5")
            self.lineEdit_11.setText("0.5")
            self.mode=22

        if text3=='election' and text4 == 'small world network':
            self.label_11.setText("probability")
            self.label_14.setText("neighbours")
            self.lineEdit_7.setText("0.3")
            self.lineEdit_7.setEnabled(True)
            self.lineEdit_9.setText("2")
            self.mode=8

        if text3=='election' and text4 == 'random network':
            self.label_11.setText("probability")
            self.label_14.setText("neighbours")
            self.lineEdit_7.setText("1")
            self.lineEdit_7.setEnabled(False)
            self.lineEdit_9.setText("2")
            self.mode=18
        if text3=='election' and text4 == 'scale-free network':
            self.label_11.setText("m0")
            self.label_14.setText("m")
            self.lineEdit_7.setText("3")
            self.lineEdit_7.setEnabled(True)
            self.lineEdit_9.setText("3")
            self.label_11.setAlignment(Qt.AlignCenter)
            self.label_14.setAlignment(Qt.AlignCenter)
            self.mode=9



    def get_way(self):
        text1 = self.comboBox.currentText()
        text2 = self.comboBox_2.currentText()

        if text1=='Snowdrift game' and text2 == 'squareGrid':
            #self.label_2.setText("S")
            self.label_2.setAlignment(Qt.AlignCenter)
            self.label_26.setAlignment(Qt.AlignCenter)
            self.lineEdit_2.setText("0.5")
            #self.label_26.setText("T")
            self.lineEdit_19.setText("1.5")
            self.label_5.setText("neighbours")
            self.lineEdit_3.setText("4")
            self.label_7.setText("height")
            self.label_8.setText("width")
            self.lineEdit_5.setText("1")
            self.lineEdit_6.setText("1")
            self.mode = 1
        if text1=='prisonersDilemma' and text2 == 'squareGrid':
            #self.label_2.setText("S")
            self.lineEdit_2.setText("-0.5")
            self.label_2.setAlignment(Qt.AlignCenter)
            self.label_26.setAlignment(Qt.AlignCenter)
            #self.label_26.setText("T")
            self.lineEdit_19.setText("1.5")
            self.label_5.setText("neighbours")
            self.lineEdit_3.setText("4")
            self.label_7.setText("height")
            self.label_8.setText("width")
            self.lineEdit_5.setText("1")
            self.lineEdit_6.setText("1")
            self.mode = 4
        if text1=='prisonersDilemma' and text2 == 'small world network':
            self.label_7.setText("probability")
            self.label_5.setText("neighbours")
            self.lineEdit_5.setText("0.3")
            self.lineEdit_3.setText("2")
            self.label_8.setText("width")
            self.lineEdit_6.setText("1")
            self.mode = 2
        if text1=='Snowdrift game' and text2 == 'small world network':
            self.label_7.setText("probability")
            self.label_5.setText("neighbours")
            self.lineEdit_5.setText("0.3")
            self.lineEdit_3.setText("2")
            self.label_8.setText("width")
            self.lineEdit_6.setText("1")
            self.mode = 5
        if text1=='prisonersDilemma' and text2 == 'scale-free network':
            self.label_7.setText("m0")
            self.label_8.setText("m")
            self.lineEdit_5.setText("3")
            self.lineEdit_6.setText("3")
            self.label_7.setAlignment(Qt.AlignCenter)
            self.label_8.setAlignment(Qt.AlignCenter)
            self.mode=3
        if text1=='Snowdrift game' and text2 == 'scale-free network':
            self.label_7.setText("m0")
            self.label_8.setText("m")
            self.lineEdit_5.setText("3")
            self.lineEdit_6.setText("3")
            self.label_7.setAlignment(Qt.AlignCenter)
            self.label_8.setAlignment(Qt.AlignCenter)
            self.mode=6
        if text1=='prisonersDilemma' and text2 == 'random network':
            self.label_7.setText("probability")
            self.label_5.setText("neighbours")
            self.lineEdit_5.setText("1")
            self.lineEdit_5.setEnabled(False)
            self.lineEdit_3.setText("2")
            self.label_8.setText("width")
            self.lineEdit_6.setText("1")
            self.mode = 16
        if text1=='Snowdrift game' and text2 == 'random network':
            self.label_7.setText("probability")
            self.label_5.setText("neighbours")
            self.lineEdit_5.setText("1")
            self.lineEdit_5.setEnabled(False)
            self.lineEdit_3.setText("2")
            self.label_8.setText("width")
            self.lineEdit_6.setText("1")
            self.mode = 17





    def start_renew(self):


        if self.flag_stop == 0:
            self.flag_stop = 1
            self.childShow()
        else:
            self.flag_step = 0
            self.timer_Main.start(1000)
            self.child.widget.mpl.timer.start(1000)
        self.item_state.setText("running")

    def childClose(self):
        self.drawText()
        self.child.widget.mpl.timer.stop()
        self.timer_Main.stop()
        #self.flag_new()
        # self.time_fresh()
        self.child.widget.mpl.axes.plot(1, 1, color='white')
        self.child.widget.mpl.axes.axis('off')
        # self.child.widget.mpl.flag=0
        self.child.widget.mpl.draw()
        print("终止")

        self.init_flag = 0


    def btn_init(self):
        print("初始化")
        self.init_flag = 1
        self.childShow()
        self.childShow_2()

    def flag_new(self):
        self.run_time = 0
        self.flag_stop = 0
        self.flag_step = 0
        self.boyi_times = 0
        self.child.widget.mpl.stop_flag = 0


    def childShow(self):

        text1=self.comboBox.currentText()
        text2= self.comboBox_2.currentText()
        text3=self.comboBox_3.currentText()
        text4=self.comboBox_4.currentText()
        text5=self.comboBox_5.currentText()
        text6 = self.comboBox_6.currentText()

        if self.tabWidget.currentIndex()==0:
            if text1=='Snowdrift game' and text2=='squareGrid':
                self.number=int(self.lineEdit.text())
                self.n = math.sqrt(int(self.number))
                self.n = int(self.n)
                self.boyi_steps = int(self.lineEdit_4.text())
                self.a1=float(self.lineEdit_2.text())
                self.a2=float(self.lineEdit_19.text())
            #self.child.widget.mpl.start_grid(self.n)
                if self.init_flag == 0:
                    QMessageBox.information(self, "操作错误", "请先初始化")
                    return
                self.flag_new()
                if 0 < self.a1 < 1 and 1 < self.a2 < 2:
                    pass
                else:
                    QMessageBox.information(self, "输入错误", "S的取值范围在(0,1),T的取值范围在(1,2)")
                    return

                if not self.init_flag == 2:
                    self.child.widget.mpl.flag = 0
                    self.child.widget.mpl.mode = 1
                    self.child.widget.mpl.grid_snow(self.n, self.boyi_steps,self.a1,self.a2)
                    print("运行")
                if self.init_flag == 2:
                    self.timer_Main.start(1000)
                    self.child.widget.mpl.timer.start(1000)
                self.init_flag = 2

            elif text1=='prisonersDilemma' and text2=='squareGrid':
                self.number = int(self.lineEdit.text())
                self.n = math.sqrt(int(self.number))
                self.n = int(self.n)
                self.boyi_steps = int(self.lineEdit_4.text())
                self.a1 = float(self.lineEdit_2.text())
                self.a2=float(self.lineEdit_19.text())
            # self.child.widget.mpl.start_grid(self.n)
                if self.init_flag == 0:
                    QMessageBox.information(self, "操作错误", "请先初始化")
                    return
                self.flag_new()
                self.item_runtime.setText("runtime：0s")
                self.item_degree.setText("average degree: 4")
                self.item_cluster.setText("cluster coefficient: 0")

                if self.number==self.n*self.n:
                    pass
                else:
                    QMessageBox.information(self, "输入错误", "请输入一个完全平方数")
                    return
                if -1 < self.a1 < 0 and 1 < self.a2 < 2:
                    pass
                else:
                    QMessageBox.information(self, "输入错误", "S的取值范围在(-1,0),T的取值范围在(1,2)")
                    return
                if not self.init_flag == 2:
                    self.child.widget.mpl.flag = 0
                    self.child.widget.mpl.mode = 4
                    self.child.widget.mpl.grid_prisoner(self.n, self.boyi_steps, self.a1,self.a2)

                    self.item_path.setText("average path length:"+str(self.child.widget.mpl.path))
                    print("运行")
                if self.init_flag == 2:
                    self.timer_Main.start(1000)
                    self.child.widget.mpl.timer.start(1000)
                    self.item_state.setText("running")
                self.init_flag = 2

            elif text1=='prisonersDilemma' and text2=='small world network':
                self.number2 = float(self.lineEdit_5.text())  # 第一行输入
                self.number4 = int(self.lineEdit_3.text())  # 第二行输入
                self.number5 = int(self.lineEdit.text())
                self.boyi_steps=int(self.lineEdit_4.text())
                self.a1=float(self.lineEdit_2.text())
                self.a2=float(self.lineEdit_19.text())

                if self.init_flag == 0:
                    QMessageBox.information(self, "操作错误", "请先初始化")
                    return
                self.flag_new()
                self.item_runtime.setText("runtime：0s")
                if -1 < self.a1 < 0 and 1 < self.a2 < 2:
                    pass
                else:
                    QMessageBox.information(self, "输入错误", "S的取值范围在(-1,0),T的取值范围在(1,2)")
                if not self.init_flag == 2:
                    self.child.widget.mpl.flag = 0
                    self.child.widget.mpl.step_time = 0
                    self.child.widget.mpl.mode = 3
                    self.child.widget.mpl.small_world_prisoner(self.number4, self.number2, self.boyi_steps, self.number5,self.a1,self.a2)
                    self.item_cluster.setText("cluster coefficient:"+str(self.child.widget.mpl.cluster))
                    self.item_path.setText("average path length:"+str(self.child.widget.mpl.path))
                    self.item_degree.setText("average degree:"+str(self.child.widget.mpl.ave_degree))



                if self.init_flag == 2:
                    self.timer_Main.start(1000)
                    self.child.widget.mpl.timer.start(1000)

                self.init_flag = 2

            elif text1=='prisonersDilemma' and text2=='random network':

                self.number2 = float(self.lineEdit_5.text())  # 第一行输入
                self.number4 = int(self.lineEdit_3.text())  # 第二行输入
                self.number5 = int(self.lineEdit.text())
                self.boyi_steps = int(self.lineEdit_4.text())
                self.a1 = float(self.lineEdit_2.text())
                self.a2 = float(self.lineEdit_19.text())

                if self.init_flag == 0:
                    QMessageBox.information(self, "操作错误", "请先初始化")
                    return
                self.flag_new()
                if -1 < self.a1 < 0 and 1 < self.a2 < 2:
                    pass
                else:
                    QMessageBox.information(self, "输入错误", "S的取值范围在(-1,0),T的取值范围在(1,2)")
                if not self.init_flag == 2:
                    self.child.widget.mpl.flag = 0
                    self.child.widget.mpl.step_time = 0
                    self.child.widget.mpl.mode = 16
                    self.child.widget.mpl.random_network_prisoner(self.number4, self.number2, self.boyi_steps, self.number5,self.a1,self.a2)


                if self.init_flag == 2:
                    self.timer_Main.start(1000)
                    self.child.widget.mpl.timer.start(1000)

                self.init_flag = 2

            elif text1=='Snowdrift game' and text2=='small world network':
                self.number2 = float(self.lineEdit_5.text())  # 第一行输入
                self.number4 = int(self.lineEdit_3.text())  # 第二行输入
                self.number5 = int(self.lineEdit.text())
                self.boyi_steps=int(self.lineEdit_4.text())
                self.a1 = float(self.lineEdit_2.text())
                self.a2 = float(self.lineEdit_19.text())

                if self.init_flag == 0:
                    QMessageBox.information(self, "操作错误", "请先初始化")
                    return
                self.flag_new()
                if 0<self.a1<1 and 1<self.a2<2:
                    pass
                else:
                    QMessageBox.information(self, "输入错误", "S的取值范围在(0,1),T的取值范围在(1,2)")
                    return
                if not self.init_flag == 2:
                    self.child.widget.mpl.flag = 0
                    self.child.widget.mpl.step_time = 0
                    self.child.widget.mpl.mode = 5
                    self.child.widget.mpl.small_world_snow(self.number4, self.number2, self.boyi_steps, self.number5,self.a1,self.a2)


                if self.init_flag == 2:
                    self.timer_Main.start(1000)
                    self.child.widget.mpl.timer.start(1000)

                self.init_flag = 2

            elif text1=='Snowdrift game' and text2=='random network':
                self.number2 = float(self.lineEdit_5.text())  # 第一行输入
                self.number4 = int(self.lineEdit_3.text())  # 第二行输入
                self.number5 = int(self.lineEdit.text())
                self.boyi_steps = int(self.lineEdit_4.text())
                self.a1 = float(self.lineEdit_2.text())
                self.a2 = float(self.lineEdit_19.text())

                if self.init_flag == 0:
                    QMessageBox.information(self, "操作错误", "请先初始化")
                    return
                self.flag_new()
                if not self.init_flag == 2:
                    self.child.widget.mpl.flag = 0
                    self.child.widget.mpl.step_time = 0
                    self.child.widget.mpl.mode = 17
                    self.child.widget.mpl.random_network_snow(self.number4, self.number2, self.boyi_steps, self.number5,self.a1,self.a2)


                if self.init_flag == 2:
                    self.timer_Main.start(1000)
                    self.child.widget.mpl.timer.start(1000)

                self.init_flag = 2

            elif text1=='prisonersDilemma' and text2 == 'scale-free network':
                self.number2 = int(self.lineEdit_6.text())  # 第一行输入
                self.number4 = int(self.lineEdit_5.text())  # 第二行输入
                self.number5 = int(self.lineEdit.text())
                self.boyi_steps=int(self.lineEdit_4.text())
                self.a1=float(self.lineEdit_2.text())
                self.a2=float(self.lineEdit_19.text())

                if self.init_flag == 0:
                    QMessageBox.information(self, "操作错误", "请先初始化")
                    return
                self.flag_new()
                self.item_runtime.setText("runtime：0s")
                if -1 < self.a1 < 0 and 1 < self.a2 < 2:
                    pass
                else:
                    QMessageBox.information(self, "输入错误", "S的取值范围在(-1,0),T的取值范围在(1,2)")
                if not self.init_flag == 2:
                    self.child.widget.mpl.flag = 0
                    self.child.widget.mpl.step_time = 0
                    self.child.widget.mpl.mode = 3
                    self.child.widget.mpl.scale_free_prisoner(self.number4, self.number2, self.boyi_steps, self.number5,self.a1,self.a2)
                    self.item_cluster.setText("cluster coefficient:" + str(self.child.widget.mpl.cluster))
                    self.item_path.setText("average path length:" + str(self.child.widget.mpl.path))
                    self.item_degree.setText("average degree:" + str(self.child.widget.mpl.ave_degree))


                if self.init_flag == 2:
                    self.timer_Main.start(1000)
                    self.child.widget.mpl.timer.start(1000)

                self.init_flag = 2
            elif text1=='Snowdrift game' and text2 == 'scale-free network':
                self.number2 = int(self.lineEdit_6.text())  # 第一行输入
                self.number4 = int(self.lineEdit_5.text())  # 第二行输入
                self.number5 = int(self.lineEdit.text())
                self.boyi_steps=int(self.lineEdit_4.text())
                self.a1 = float(self.lineEdit_2.text())
                self.a2 = float(self.lineEdit_19.text())

                if self.init_flag == 0:
                    QMessageBox.information(self, "操作错误", "请先初始化")
                    return
                self.flag_new()
                if 0<self.a1<1 and 1<self.a2<2:
                    pass
                else:
                    QMessageBox.information(self, "输入错误", "S的取值范围在(0,1),T的取值范围在(1,2)")
                    return
                if not self.init_flag == 2:
                    self.child.widget.mpl.flag = 0
                    self.child.widget.mpl.step_time = 0
                    self.child.widget.mpl.mode = 6
                    self.child.widget.mpl.scale_free_snow(self.number4, self.number2, self.boyi_steps, self.number5,self.a1,self.a2)


                if self.init_flag == 2:
                    self.timer_Main.start(1000)
                    self.child.widget.mpl.timer.start(1000)

                self.init_flag = 2
        elif self.tabWidget.currentIndex() == 1:
            if text3 == 'election' and text4 == 'squareGrid':
                self.number4 = int(self.lineEdit_8.text())  # 第一行输入
                self.boyi_steps = int(self.lineEdit_12.text())

                if self.init_flag == 0:
                    QMessageBox.information(self, "操作错误", "请先初始化")
                    return
                self.flag_new()
                if not self.init_flag == 2:
                    self.child.widget.mpl.flag = 0
                    self.child.widget.mpl.step_time = 0
                    self.child.widget.mpl.mode = 7
                    self.child.widget.mpl.grid_election(self.number4, self.boyi_steps)

                if self.init_flag == 2:
                    self.timer_Main.start(1000)
                    self.child.widget.mpl.timer.start(1000)

                self.init_flag = 2
            elif text3 == 'Deffuant' and text4 == 'squareGrid':
                self.number4 = int(self.lineEdit_8.text())  # 第一行输入
                self.boyi_steps = int(self.lineEdit_12.text())
                self.a1=float(self.lineEdit_10.text())
                self.a2 = float(self.lineEdit_11.text())

                if self.init_flag == 0:
                    QMessageBox.information(self, "操作错误", "请先初始化")
                    return
                self.flag_new()
                if not self.init_flag == 2:
                    self.child.widget.mpl.flag = 0
                    self.child.widget.mpl.step_time = 0
                    self.child.widget.mpl.mode = 22
                    self.child.widget.mpl.grid_deffuant(self.number4, self.boyi_steps,self.a1,self.a2)

                if self.init_flag == 2:
                    self.timer_Main.start(1000)
                    self.child.widget.mpl.timer.start(1000)

                self.init_flag = 2

            elif text3=='election' and text4=='small world network':
                self.number2 = float(self.lineEdit_7.text())  # 第一行输入
                self.number4 = int(self.lineEdit_9.text())  # 第二行输入
                self.number5 = int(self.lineEdit_8.text())
                self.boyi_steps=int(self.lineEdit_12.text())

                if self.init_flag == 0:
                    QMessageBox.information(self, "操作错误", "请先初始化")
                    return
                self.flag_new()
                if not self.init_flag == 2:
                    self.child.widget.mpl.flag = 0
                    self.child.widget.mpl.step_time = 0
                    self.child.widget.mpl.mode = 8
                    self.child.widget.mpl.small_world_election(self.number4, self.number2, self.boyi_steps, self.number5)


                if self.init_flag == 2:
                    self.timer_Main.start(1000)
                    self.child.widget.mpl.timer.start(1000)

                self.init_flag = 2

            elif text3=='election' and text4 == 'scale-free network':
                self.number2 = int(self.lineEdit_9.text())  # 第一行输入
                self.number4 = int(self.lineEdit_7.text())  # 第二行输入
                self.number5 = int(self.lineEdit_8.text())
                self.boyi_steps=int(self.lineEdit_12.text())

                if self.init_flag == 0:
                    QMessageBox.information(self, "操作错误", "请先初始化")
                    return
                self.flag_new()
                if not self.init_flag == 2:
                    self.child.widget.mpl.flag = 0
                    self.child.widget.mpl.step_time = 0
                    self.child.widget.mpl.mode = 9
                    self.child.widget.mpl.scale_free_election(self.number4, self.number2, self.boyi_steps, self.number5)


                if self.init_flag == 2:
                    self.timer_Main.start(1000)
                    self.child.widget.mpl.timer.start(1000)

                self.init_flag = 2

            elif text3 == 'election' and text4 == 'random network':
                self.number2 = float(self.lineEdit_7.text())  # 第一行输入
                self.number4 = int(self.lineEdit_9.text())  # 第二行输入
                self.number5 = int(self.lineEdit_8.text())
                self.boyi_steps = int(self.lineEdit_12.text())

                if self.init_flag == 0:
                    QMessageBox.information(self, "操作错误", "请先初始化")
                    return
                self.flag_new()
                if not self.init_flag == 2:
                    self.child.widget.mpl.flag = 0
                    self.child.widget.mpl.step_time = 0
                    self.child.widget.mpl.mode = 18
                    self.child.widget.mpl.random_network_election(self.number4, self.number2, self.boyi_steps, self.number5)

                if self.init_flag == 2:
                    self.timer_Main.start(1000)
                    self.child.widget.mpl.timer.start(1000)

                self.init_flag = 2

        elif self.tabWidget.currentIndex() == 2:
            if text5 == 'SIS' and text6 == 'squareGrid':
                self.number1=float(self.lineEdit_13.text())
                self.number2=int(self.lineEdit_14.text())
                self.number3 = float(self.lineEdit_15.text())
                self.boyi_steps = int(self.lineEdit_18.text())

                if self.init_flag == 0:
                    QMessageBox.information(self, "操作错误", "请先初始化")
                    return
                self.flag_new()
                if not self.init_flag == 2:
                    self.child.widget.mpl.flag = 0
                    self.child.widget.mpl.step_time = 0
                    self.child.widget.mpl.mode = 10
                    self.child.widget.mpl.grid_SIS(self.number2, self.number1,self.number3,self.boyi_steps)

                if self.init_flag == 2:
                    self.timer_Main.start(1000)
                    self.child.widget.mpl.timer.start(1000)

                self.init_flag = 2

            elif text5 == 'SIR' and text6 == 'squareGrid':
                self.number1=float(self.lineEdit_13.text())
                self.number2=int(self.lineEdit_14.text())
                self.number3 = float(self.lineEdit_15.text())
                self.boyi_steps = int(self.lineEdit_18.text())

                if self.init_flag == 0:
                    QMessageBox.information(self, "操作错误", "请先初始化")
                    return
                self.flag_new()
                if not self.init_flag == 2:
                    self.child.widget.mpl.flag = 0
                    self.child.widget.mpl.step_time = 0
                    self.child.widget.mpl.mode = 11
                    self.child.widget.mpl.grid_SIR(self.number2, self.number1,self.number3,self.boyi_steps)

                if self.init_flag == 2:
                    self.timer_Main.start(1000)
                    self.child.widget.mpl.timer.start(1000)

                self.init_flag = 2

            elif text5 == 'SI' and text6 == 'squareGrid':
                self.number1=float(self.lineEdit_13.text())
                self.number2=int(self.lineEdit_14.text())

                self.boyi_steps = int(self.lineEdit_18.text())

                if self.init_flag == 0:
                    QMessageBox.information(self, "操作错误", "请先初始化")
                    return
                self.flag_new()
                if not self.init_flag == 2:
                    self.child.widget.mpl.flag = 0
                    self.child.widget.mpl.step_time = 0
                    self.child.widget.mpl.mode = 19
                    self.child.widget.mpl.grid_SI(self.number2, self.number1,self.boyi_steps)

                if self.init_flag == 2:
                    self.timer_Main.start(1000)
                    self.child.widget.mpl.timer.start(1000)

                self.init_flag = 2

            elif text5 == 'SIR' and text6 == 'small world network':
                self.number1=float(self.lineEdit_13.text()) #probability
                self.number2=int(self.lineEdit_14.text()) #总结点数
                self.number3 = int(self.lineEdit_15.text()) #邻居节点
                self.number4 = float(self.lineEdit_16.text()) #a
                self.number5 = float(self.lineEdit_17.text()) #b
                self.boyi_steps = int(self.lineEdit_18.text()) #博弈次数

                if self.init_flag == 0:
                    QMessageBox.information(self, "操作错误", "请先初始化")
                    return
                self.flag_new()
                if not self.init_flag == 2:
                    self.child.widget.mpl.flag = 0
                    self.child.widget.mpl.step_time = 0
                    self.child.widget.mpl.mode = 12
                    self.child.widget.mpl.small_world_SIR(self.number1, self.number3,self.number2,self.number4,self.number5,self.boyi_steps)

                if self.init_flag == 2:
                    self.timer_Main.start(1000)
                    self.child.widget.mpl.timer.start(1000)

                self.init_flag = 2

            elif text5 == 'SIR' and text6 == 'random network':
                self.number1=float(self.lineEdit_13.text()) #probability
                self.number2=int(self.lineEdit_14.text()) #总结点数
                self.number3 = int(self.lineEdit_15.text()) #邻居节点
                self.number4 = float(self.lineEdit_16.text()) #a
                self.number5 = float(self.lineEdit_17.text()) #b
                self.boyi_steps = int(self.lineEdit_18.text()) #博弈次数

                if self.init_flag == 0:
                    QMessageBox.information(self, "操作错误", "请先初始化")
                    return
                self.flag_new()
                if not self.init_flag == 2:
                    self.child.widget.mpl.flag = 0
                    self.child.widget.mpl.step_time = 0
                    self.child.widget.mpl.mode = 25
                    self.child.widget.mpl.random_network_SIR(self.number1, self.number3,self.number2,self.number4,self.number5,self.boyi_steps)

                if self.init_flag == 2:
                    self.timer_Main.start(1000)
                    self.child.widget.mpl.timer.start(1000)

                self.init_flag = 2



            elif text5 == 'SIS' and text6 == 'small world network':
                self.number2=float(self.lineEdit_13.text()) #probability
                self.number5=int(self.lineEdit_14.text()) #总结点数
                self.number4 = int(self.lineEdit_15.text()) #邻居节点
                self.number1 = float(self.lineEdit_16.text()) #a
                self.number3 = float(self.lineEdit_17.text()) #b
                self.boyi_steps = int(self.lineEdit_18.text()) #博弈次数

                if self.init_flag == 0:
                    QMessageBox.information(self, "操作错误", "请先初始化")
                    return
                self.flag_new()
                if not self.init_flag == 2:
                    self.child.widget.mpl.flag = 0
                    self.child.widget.mpl.step_time = 0
                    self.child.widget.mpl.mode = 13
                    self.child.widget.mpl.small_world_SIS(self.number4, self.number2,self.boyi_steps,self.number5,self.number1,self.number3)

                if self.init_flag == 2:
                    self.timer_Main.start(1000)
                    self.child.widget.mpl.timer.start(1000)

                self.init_flag = 2

            elif text5 == 'SIS' and text6 == 'random network':
                self.number2=float(self.lineEdit_13.text()) #probability
                self.number5=int(self.lineEdit_14.text()) #总结点数
                self.number4 = int(self.lineEdit_15.text()) #邻居节点
                self.number1 = float(self.lineEdit_16.text()) #a
                self.number3 = float(self.lineEdit_17.text()) #b
                self.boyi_steps = int(self.lineEdit_18.text()) #博弈次数

                if self.init_flag == 0:
                    QMessageBox.information(self, "操作错误", "请先初始化")
                    return
                self.flag_new()
                if not self.init_flag == 2:
                    self.child.widget.mpl.flag = 0
                    self.child.widget.mpl.step_time = 0
                    self.child.widget.mpl.mode = 24
                    self.child.widget.mpl.random_network_SIS(self.number4, self.number2,self.boyi_steps,self.number5,self.number1,self.number3)

                if self.init_flag == 2:
                    self.timer_Main.start(1000)
                    self.child.widget.mpl.timer.start(1000)

                self.init_flag = 2

            elif text5 == 'SI' and text6 == 'small world network':
                self.number2=float(self.lineEdit_13.text()) #probability
                self.number5=int(self.lineEdit_14.text()) #总结点数
                self.number4 = int(self.lineEdit_15.text()) #邻居节点
                self.number1 = float(self.lineEdit_16.text()) #a

                self.boyi_steps = int(self.lineEdit_18.text()) #博弈次数

                if self.init_flag == 0:
                    QMessageBox.information(self, "操作错误", "请先初始化")
                    return
                self.flag_new()
                if not self.init_flag == 2:
                    self.child.widget.mpl.flag = 0
                    self.child.widget.mpl.step_time = 0
                    self.child.widget.mpl.mode = 20
                    self.child.widget.mpl.small_world_SI(self.number4, self.number2,self.boyi_steps,self.number5,self.number1)

                if self.init_flag == 2:
                    self.timer_Main.start(1000)
                    self.child.widget.mpl.timer.start(1000)

                self.init_flag = 2


            elif text5 == 'SI' and text6 == 'random network':
                self.number2=float(self.lineEdit_13.text()) #probability
                self.number5=int(self.lineEdit_14.text()) #总结点数
                self.number4 = int(self.lineEdit_15.text()) #邻居节点
                self.number1 = float(self.lineEdit_16.text()) #a

                self.boyi_steps = int(self.lineEdit_18.text()) #博弈次数

                if self.init_flag == 0:
                    QMessageBox.information(self, "操作错误", "请先初始化")
                    return
                self.flag_new()
                if not self.init_flag == 2:
                    self.child.widget.mpl.flag = 0
                    self.child.widget.mpl.step_time = 0
                    self.child.widget.mpl.mode = 23
                    self.child.widget.mpl.random_network_SI(self.number4, self.number2,self.boyi_steps,self.number5,self.number1)

                if self.init_flag == 2:
                    self.timer_Main.start(1000)
                    self.child.widget.mpl.timer.start(1000)

                self.init_flag = 2

            elif text5=='SIS' and text6 == 'scale-free network':
                self.number1 = int(self.lineEdit_13.text())  # 第一行输入
                self.number2 = int(self.lineEdit_14.text())  # 第二行输入
                self.number3 = int(self.lineEdit_15.text())
                self.number4 = float(self.lineEdit_16.text())
                self.number5 = float(self.lineEdit_17.text())
                self.boyi_steps=int(self.lineEdit_18.text())

                if self.init_flag == 0:
                    QMessageBox.information(self, "操作错误", "请先初始化")
                    return
                self.flag_new()
                if not self.init_flag == 2:
                    self.child.widget.mpl.flag = 0
                    self.child.widget.mpl.step_time = 0
                    self.child.widget.mpl.mode = 14
                    self.child.widget.mpl.scale_free_SIS(self.number1, self.number3, self.number4,self.number5,self.number2,self.boyi_steps)


                if self.init_flag == 2:
                    self.timer_Main.start(1000)
                    self.child.widget.mpl.timer.start(1000)

                self.init_flag = 2

            elif text5=='SI' and text6 == 'scale-free network':
                self.number1 = int(self.lineEdit_13.text())  # 第一行输入
                self.number2 = int(self.lineEdit_14.text())  # 第二行输入
                self.number3 = int(self.lineEdit_15.text())
                self.number4 = float(self.lineEdit_16.text())

                self.boyi_steps=int(self.lineEdit_18.text())

                if self.init_flag == 0:
                    QMessageBox.information(self, "操作错误", "请先初始化")
                    return
                self.flag_new()
                if not self.init_flag == 2:
                    self.child.widget.mpl.flag = 0
                    self.child.widget.mpl.step_time = 0
                    self.child.widget.mpl.mode = 21
                    self.child.widget.mpl.scale_free_SI(self.number1, self.number3, self.number4,self.number2,self.boyi_steps)


                if self.init_flag == 2:
                    self.timer_Main.start(1000)
                    self.child.widget.mpl.timer.start(1000)

                self.init_flag = 2
            elif text5=='SIR' and text6 == 'scale-free network':
                self.number1 = int(self.lineEdit_13.text())  # 第一行输入
                self.number2 = int(self.lineEdit_14.text())  # 第二行输入
                self.number3 = int(self.lineEdit_15.text())
                self.number4 = float(self.lineEdit_16.text())
                self.number5 = float(self.lineEdit_17.text())
                self.boyi_steps=int(self.lineEdit_18.text())

                if self.init_flag == 0:
                    QMessageBox.information(self, "操作错误", "请先初始化")
                    return
                self.flag_new()
                if not self.init_flag == 2:
                    self.child.widget.mpl.flag = 0
                    self.child.widget.mpl.step_time = 0
                    self.child.widget.mpl.mode = 15
                    self.child.widget.mpl.scale_free_SIR(self.number1, self.number3, self.number4,self.number5, self.number2,self.boyi_steps)


                if self.init_flag == 2:
                    self.timer_Main.start(1000)
                    self.child.widget.mpl.timer.start(1000)

                self.init_flag = 2

    def childShow_2(self):

        text1 = self.comboBox.currentText()
        text2 = self.comboBox_2.currentText()
        text3 = self.comboBox_3.currentText()
        text4 = self.comboBox_4.currentText()
        text5 = self.comboBox_5.currentText()
        text6 = self.comboBox_6.currentText()

        if self.tabWidget.currentIndex() == 0:
            if text1 == 'prisonersDilemma' and text2 == 'squareGrid':
                self.x = list(range(len(self.child.widget.mpl.degree_dis)))
                self.y = [i for i in self.child.widget.mpl.degree_dis]
                # print(self.child.widget.mpl.degree_dis)
                # self.child_2.widget_2.mpl_2.axes.plot(self.x, self.y)  # plot、loglog
                # t = np.arange(0.0, 3.0, 0.01)
                # s = np.sin(2 * np.pi * t)
                self.F.axes.bar(self.x, self.y)
                self.F.axes.hold(False)
                self.gridlayout = QGridLayout(self.widget_2)
                    # 在GUI的widget中添加布局
                self.gridlayout.addWidget(self.F)

                print("hello eveoomm")
            if text1 == 'prisonersDilemma' and text2 == 'scale-free network':
                self.x = list(range(len(self.child.widget.mpl.degree)))
                self.y = [i for i in self.child.widget.mpl.degree]

                self.F.axes.bar(self.x, self.y)
                self.F.axes.hold(False)
                self.gridlayout = QGridLayout(self.widget_2)
                    # 在GUI的widget中添加布局
                self.gridlayout.addWidget(self.F)

    def childShow_3(self):

        text1 = self.comboBox.currentText()
        text2 = self.comboBox_2.currentText()
        text3 = self.comboBox_3.currentText()
        text4 = self.comboBox_4.currentText()
        text5 = self.comboBox_5.currentText()
        text6 = self.comboBox_6.currentText()

        if self.tabWidget.currentIndex() == 0:
            if text1 == 'prisonersDilemma' and text2 == 'squareGrid':
                self.x = list(range(0, self.boyi_steps+1))
                self.y = [i for i in self.child.widget.mpl.cratio]
                # x = list(range(len(degree)))
                # y = [i for i in degree]
                self.F1.axes.plot(self.x, self.y)

                self.gridlayout = QGridLayout(self.widget_3)
                # 在GUI的widget中添加布局
                self.gridlayout.addWidget(self.F1)
            if text1 == 'prisonersDilemma' and text2 == 'scale-free network':
                self.x = list(range(0, self.boyi_steps))
                self.y = [i for i in self.child.widget.mpl.cratio]

                self.F1.axes.plot(self.x, self.y)
                self.F1.axes.set_ylim(0, 1)

                self.gridlayout = QGridLayout(self.widget_3)
                # 在GUI的widget中添加布局
                self.gridlayout.addWidget(self.F1)












class ChildrenForm(QWidget, Ui_Form):
    def __init__(self):
        super(ChildrenForm, self).__init__()
        self.setupUi(self)





if __name__=="__main__":
    app=QApplication(sys.argv)
    Mainwin=MainForm()
    win=SignForm()
    Signwin=signupForm()
    win.show()
    sys.exit(app.exec_())
