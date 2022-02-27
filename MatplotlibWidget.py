import sys
import random
import matplotlib
import math
import time
import os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
matplotlib.use("Qt5Agg")
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import sqlite3

from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication,QVBoxLayout, QSizePolicy, QWidget,QGridLayout
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

#from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
#from PyQt5.QtCore import QTimer
from ctypes import *
class MyMplCanvas(FigureCanvas):
    """FigureCanvas的最终的父类其实是QWidget。"""

    def operate(self):
        self.flag = 1
        # self.backend.start()
        print('self.mode=' + str(self.mode))
        if self.mode == 1:
            self.grid_snow(self.n, self.steps,self.a1,self.a2)
        elif self.mode == 2:
            self.small_world_prisoner(self.number1, self.number2, self.steps, self.number5,self.a1,self.a2)
        elif self.mode == 3:
            self.scale_free_prisoner(self.number1, self.number2, self.steps, self.number5,self.a1,self.a2)
        elif self.mode==4:
            self.grid_prisoner(self.n, self.steps,self.a1,self.a2)
        elif self.mode == 5:
            self.small_world_snow(self.number1, self.number2, self.steps, self.number5,self.a1,self.a2)
        elif self.mode == 6:
            self.scale_free_snow(self.number1, self.number2, self.steps, self.number5,self.a1,self.a2)
        elif self.mode == 7:
            self.grid_election(self.n, self.steps)
        elif self.mode==8:
            self.small_world_election(self.number1, self.number2, self.steps, self.number5)
        elif self.mode==9:
            self.scale_free_election(self.number1, self.number2, self.steps, self.number5)
        elif self.mode==10:
            self.grid_SIS(self.n,self.number1, self.number2, self.steps)
        elif self.mode==11:
            self.grid_SIR(self.n,self.number1, self.number2, self.steps)
        elif self.mode==12:
            self.small_world_SIR(self.number1, self.number2, self.number3, self.number4,self.number5,self.steps)
        elif self.mode==13:
            self.small_world_SIS(self.number1, self.number2, self.steps, self.number5,self.number3,self.number4)
        elif self.mode==14:
            self.scale_free_SIS(self.number1,self.number2,self.number3,self.number4,self.number5,self.steps)
        elif self.mode==15:
            self.scale_free_SIR(self.number1, self.number2, self.number3, self.number4, self.number5, self.steps)
        elif self.mode == 16:
            self.random_network_prisoner(self.number1, self.number2, self.steps, self.number5,self.a1,self.a2)
        elif self.mode == 17:
            self.random_network_snow(self.number1, self.number2, self.steps, self.number5,self.a1,self.a2)
        elif self.mode==18:
            self.random_network_election(self.number1, self.number2, self.steps, self.number5)
        elif self.mode==19:
            self.grid_SI(self.n,self.number1, self.steps)
        elif self.mode==20:
            self.small_world_SI(self.number1, self.number2, self.steps, self.number5, self.number3)
        elif self.mode==21:
            self.scale_free_SI(self.number1, self.number2, self.number3, self.number5, self.steps)
        elif self.mode==22:
            self.grid_deffuant(self.n, self.steps,self.a1,self.a2)
        elif self.mode==23:
            self.random_network_SI(self.number1, self.number2, self.steps, self.number5, self.number3)
        elif self.mode==24:
            self.random_network_SIS(self.number1, self.number2, self.steps, self.number5,self.number3,self.number4)
        elif self.mode==25:
            self.random_network_SIR(self.number1, self.number2, self.number3, self.number4,self.number5,self.steps)


    def __init__(self, parent=None, width=5, height=5, dpi=100):
        self.flag = 0
        self.stop_flag = 0
        self.mode = 1
        self.n = 0
        self.betry = 0
        self.flag_out = 0
        self.steps = 0
        self.step_time = 0
        self.flag_openFile = 0  # 打开文件标识
        self.node_state_2 = []
        self.cratio=[]



        # 配置中文显示
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        # 新建一个figure
        self.fig = Figure(figsize=(width, height), dpi=100)
        # 去除留白
        self.fig.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)
        self.axes = self.fig.add_subplot(111)  # 建立一个子图，如果要建立复合图，可以在这里修改

        self.axes.hold(False) # 每次绘图的时候不保留上一次绘图的结果

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        self.fig.canvas.mpl_connect('button_press_event', self.onClick)
        #######
        #self.fig.canvas.mpl_connect('button_press_event', self.onClick)
        #self.axes.set_xlim(-1.1, +1.1)
        #self.axes.set_ylim(-1.1, +1.1)
        ##############
        '''定义FigureCanvas的尺寸策略，这部分的意思是设置FigureCanvas，使之尽可能的向外填充空间。'''
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)



    def grid_snow(self, n,step_times,a1,a2):
        self.n = n  # 单行节点数
        self.M=n*n
        self.steps = step_times
        self.a1=a1
        self.a2=a2
        self.dll_41 = cdll.LoadLibrary('grid-evolutionary.dll')
        if self.step_time == step_times:
            self.stop_flag = 1
            return
        self.b = ['blue'] * self.n * n
        self.a = [1] * self.n * n
        if self.flag == 0:
            self.dll_41.main(n * n)  # 运行dll初始化程序
            self.dll_41.run_over(n * n, step_times+1,c_double(a1),c_double(a2))  # 运行dll博弈程序

            self.my_file = 'grid-evolutionary-1.csv'
            self.df = pd.DataFrame(pd.read_csv(self.my_file))
            self.G = nx.from_pandas_edgelist(self.df)
            self.pos_round = nx.spring_layout(self.G)
            #self.n3 = int(math.sqrt(self.number))
            for i in range(self.n):  # x坐标
                for j in range(self.n):
                    self.pos_round[i * self.n + j][0] = j
            for i in range(self.n):  # y坐标
                for j in range(self.n):
                    self.pos_round[i + j * self.n][1] = self.n - j
            con = sqlite3.connect("grid-evolutionary.db")
            dff = pd.read_csv('grid-evolutionary-2.csv')
            cursor = con.cursor()
            con.row_factory = sqlite3.Row  # 访问列信息
            dff.to_sql('some_table', con, if_exists='append')
            con.execute("delete from some_table")
            dff.to_sql('some_table', con, if_exists='append')
            cursor.execute("select * from some_table where ROWID=1")
            node_state = cursor.fetchall()
            for i in range(self.n*n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i] = 'red'
        else:
            self.step_time += 1
            con = sqlite3.connect("grid-evolutionary.db")
            dff = pd.read_csv('grid-evolutionary-2.csv')
            cursor = con.cursor()
            con.row_factory = sqlite3.Row  # 访问列信息
            dff.to_sql('some_table', con, if_exists='append')
            con.execute("delete from some_table")
            dff.to_sql('some_table', con, if_exists='append')
            cursor.execute("select * from some_table where ROWID=%d"%(self.step_time+1))
            node_state = cursor.fetchall()
            for i in range(self.n*n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i] = 'red'

        for i in range(self.n*n):
             self.a[i] = self.G.degree(i) * 70  # 度大小设置

        if self.flag == 0:
            self.flag = 1
            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b,node_size=self.a, ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
            nx.draw_networkx_edges(self.G, pos=self.pos_round, ax=self.axes, alpha=0.4)  # 生成边
        else:
            self.axes.hold(True)
            xx = nx.draw_networkx_nodes(self.G,pos=self.pos_round,node_color=self.b,node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框


        self.flag_out = 1
        self.axes.axis('off')
        self.draw()
        self.axes.hold(False)

    def grid_prisoner(self, n,step_times,a1,a2):
        self.n = n  # 单行节点数
        self.M=n*n
        self.steps = step_times
        self.a1=a1
        self.a2=a2
        self.dll_41 = cdll.LoadLibrary('grid-evolutionary.dll')
        if self.step_time == step_times:
            self.stop_flag = 1
            return
        self.b = ['blue'] * self.n * n
        self.a = [1] * self.n * n
        self.count=0

        if self.flag == 0:
            self.dll_41.main(n * n)  # 运行dll初始化程序
            self.dll_41.run_over(n * n, step_times+1,c_double(a1),c_double(a2))  # 运行dll博弈程序

            self.my_file = 'grid-evolutionary-1.csv'
            self.df = pd.DataFrame(pd.read_csv(self.my_file))
            self.G = nx.from_pandas_edgelist(self.df)
            self.pos_round = nx.spring_layout(self.G)
            self.path=nx.average_shortest_path_length(self.G)
            self.degree_dis = nx.degree_histogram(self.G)
            #self.n3 = int(math.sqrt(self.number))
            for i in range(self.n):  # x坐标
                for j in range(self.n):
                    self.pos_round[i * self.n + j][0] = j
            for i in range(self.n):  # y坐标
                for j in range(self.n):
                    self.pos_round[i + j * self.n][1] = self.n - j
            con = sqlite3.connect("grid-evolutionary.db")
            dff = pd.read_csv('grid-evolutionary-2.csv')
            cursor = con.cursor()
            con.row_factory = sqlite3.Row  # 访问列信息
            dff.to_sql('some_table', con, if_exists='append')
            con.execute("delete from some_table")
            dff.to_sql('some_table', con, if_exists='append')
            cursor.execute("select * from some_table where ROWID=1")
            node_state = cursor.fetchall()
            self.node_state_1=node_state
            self.node_state_2.append(node_state)
            con.close()

            for i in range(self.n*n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                    self.count+=1
                else:
                    self.b[i] = 'red'
            self.cratio.append(self.count/self.M)
        else:
            self.step_time += 1
            con = sqlite3.connect("grid-evolutionary.db")
            dff = pd.read_csv('grid-evolutionary-2.csv')
            cursor = con.cursor()
            con.row_factory = sqlite3.Row  # 访问列信息
            dff.to_sql('some_table', con, if_exists='append')
            con.execute("delete from some_table")
            dff.to_sql('some_table', con, if_exists='append')
            cursor.execute("select * from some_table where ROWID=%d"%(self.step_time+1))
            node_state = cursor.fetchall()
            self.node_state_1=node_state
            self.node_state_2.append(node_state)
            con.close()


            for i in range(self.n*n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                    self.count+=1
                else:
                    self.b[i] = 'red'

            self.cratio.append(self.count/100)

        for i in range(self.n*n):
            self.grid_node=510/self.n
            self.a[i]=self.grid_node*self.grid_node
            print(self.a[i])
            # if self.n==6:
            #     self.a[i] = self.G.degree(i) * 750 # 度大小设置
            # if self.n==7:
            #     self.a[i] = self.G.degree(i) * 650
            # if self.n==8:
            #     self.a[i] = self.G.degree(i) * 500
            # if self.n==9:
            #     self.a[i] = self.G.degree(i) * 400
            # if self.n==10:
            #     self.a[i] = self.G.degree(i) * 350
            # if self.n==11:
            #     self.a[i] = self.G.degree(i) * 350
            # if self.n==12:
            #     self.a[i] = self.G.degree(i) * 250
            # if self.n==13:
            #     self.a[i] = self.G.degree(i) * 250
            # if self.n==14:
            #     self.a[i] = self.G.degree(i) * 200



        if self.flag == 0:
            self.flag = 1
            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b,node_size=self.a, ax=self.axes,node_shape='s')  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
            #nx.draw_networkx_edges(self.G, pos=self.pos_round, ax=self.axes, alpha=0.4)  # 生成边
        else:
            self.axes.hold(True)
            xx = nx.draw_networkx_nodes(self.G,pos=self.pos_round,node_color=self.b,node_size=self.a,ax=self.axes,node_shape='s')  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框


        self.flag_out = 1
        self.axes.axis('off')
        self.draw()
        self.axes.hold(False)

    def scale_free_prisoner(self, m1, m2, step_times, N1,a1,a2):
        self.mode = 3  # 网络类型
        self.n = N1  # 节点个数
        self.number1 = m1  # 初始节点数
        self.number2 = m2  # 新加入节点的度大小
        self.number5 = N1
        self.steps = step_times  # 单步博弈次数
        self.a1=a1
        self.a2=a2
        self.dll_21 = cdll.LoadLibrary('scale-free-evolutionary.dll')
        node_change = [0] * N1
        change_flag = 0
        if self.step_time == step_times:
            self.stop_flag = 1
            return
        self.b = ['blue'] * self.n
        self.a=[1]*self.n
        self.count=0
        #print(1)
        if self.flag == 0:
            if self.flag_openFile == 0:
                self.dll_21.main(m1, m2, N1)  # dll初始化
                self.my_file = 'scale-free-evolutionary-1.csv'
                print(2)
                self.df = pd.DataFrame(pd.read_csv(self.my_file))
            else:
                self.flag_openFile = 0
            self.G = nx.from_pandas_edgelist(self.df, edge_attr=True)  # 读取csv表格数据赋值到self.G
            self.pos_round = nx.spring_layout(self.G)  # 生成每个节点的坐标位置
            self.path=nx.average_shortest_path_length(self.G)
            self.cluster=nx.average_clustering(self.G)
            self.degree = nx.degree_histogram(self.G)
            self.sum = 0
            for i in range(len(self.degree)):
                self.sum = self.sum + i * self.degree[i]
            self.ave_degree = self.sum / nx.number_of_nodes(self.G)
            # self.flag=1
            #print(3)
            self.dll_21.run_over(N1, step_times + 1,c_double(a1),c_double(a2))  # 执行博弈，时间步为1000
            # 获取数据，读取当前目录下的CSV文件

            #print('complete')
            # 数据库
            self.dll_sql = sqlite3.connect("scale-free-evolutionary.db")
            dff = pd.DataFrame(pd.read_csv('scale-free-evolutionary-2.csv'))  # , sep='\t'
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            self.dll_sql.execute("delete from some_table")
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            cursor.execute("select * from some_table where ROWID=1")
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                    self.count += 1
                else:
                    self.b[i] = 'red'

        else:
            self.step_time += 1
            #print('第' + str(self.step_time) + '步')
            self.dll_sql = sqlite3.connect("scale-free-evolutionary.db")
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            cursor.execute("select * from some_table where ROWID=%d" % (self.step_time + 1))
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                    self.count += 1
                else:
                    self.b[i] = 'red'
            self.cratio.append(self.count/self.n)



        # self.b = ['blue'] * self.n
        # self.a = [1] * self.n
        for i in range(self.n):
            self.a[i] = self.G.degree(i + 1) * 50 + 10  # 度大小设置


        if self.flag == 0:
            self.flag = 1
            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b, node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
            nx.draw_networkx_edges(self.G, pos=self.pos_round, ax=self.axes, alpha=0.4)  # 生成边
        else:
            self.axes.hold(True)

            xx = nx.draw_networkx_nodes(self.G,  pos=self.pos_round, node_color=self.b, node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
        self.flag_out = 1
        self.axes.axis('off')
        self.draw()
        self.axes.hold(False)

    def scale_free_snow(self, m1, m2, step_times, N1,a1,a2):
        self.mode = 3  # 网络类型
        self.n = N1  # 节点个数
        self.number1 = m1  # 初始节点数
        self.number2 = m2  # 新加入节点的度大小
        self.number5 = N1
        self.steps = step_times  # 单步博弈次数
        self.a1=a1
        self.a2=a2
        self.dll_21 = cdll.LoadLibrary('scale-free-evolutionary.dll')
        node_change = [0] * N1
        change_flag = 0
        if self.step_time == step_times:
            self.stop_flag = 1
            return
        self.b = ['blue'] * self.n
        self.a=[1]*self.n
        print(1)
        if self.flag == 0:
            if self.flag_openFile == 0:
                self.dll_21.main(m1, m2, N1)  # dll初始化
                self.my_file = 'scale-free-evolutionary-1.csv'
                print(2)
                self.df = pd.DataFrame(pd.read_csv(self.my_file))
            else:
                self.flag_openFile = 0
            self.G = nx.from_pandas_edgelist(self.df, edge_attr=True)  # 读取csv表格数据赋值到self.G
            self.pos_round = nx.spring_layout(self.G)  # 生成每个节点的坐标位置
            # self.flag=1
            print(3)
            self.dll_21.run_over(N1, step_times + 1,c_double(a1),c_double(a2))  # 执行博弈，时间步为1000
            # 获取数据，读取当前目录下的CSV文件

            print('complete')
            # 数据库
            self.dll_sql = sqlite3.connect("scale-free-evolutionary.db")
            dff = pd.DataFrame(pd.read_csv('scale-free-evolutionary-2.csv'))  # , sep='\t'
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            self.dll_sql.execute("delete from some_table")
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            cursor.execute("select * from some_table where ROWID=1")
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i] = 'red'



        else:
            self.step_time += 1
            print('第' + str(self.step_time) + '步')
            self.dll_sql = sqlite3.connect("scale-free-evolutionary.db")
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            cursor.execute("select * from some_table where ROWID=%d" % (self.step_time + 1))
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i] = 'red'


            print('run')
        print(node_state[0])
        print(3)
        # self.b = ['blue'] * self.n
        # self.a = [1] * self.n
        for i in range(self.n):
            self.a[i] = self.G.degree(i + 1) * 50 + 10  # 度大小设置


        if self.flag == 0:
            self.flag = 1
            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b, node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
            nx.draw_networkx_edges(self.G, pos=self.pos_round, ax=self.axes, alpha=0.4)  # 生成边
        else:
            self.axes.hold(True)
            # if change_flag == 0:
            #     return
            xx = nx.draw_networkx_nodes(self.G,  pos=self.pos_round, node_color=self.b, node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
        self.flag_out = 1
        self.axes.axis('off')
        self.draw()
        self.axes.hold(False)

    def scale_free_SIS(self, m1, m2, a1,a2,N1,step_times):
        self.mode = 14  # 网络类型
        self.n = N1  # 节点个数
        self.number1 = m1  # 初始节点数
        self.number2 = m2  # 新加入节点的度大小
        self.number3=a1
        self.number4=a2
        self.number5 = N1
        self.steps = step_times  # 单步博弈次数
        self.dll_21 = cdll.LoadLibrary('scale-free-SIS.dll')
        node_change = [0] * N1
        change_flag = 0
        if self.step_time == step_times:
            self.stop_flag = 1
            return
        self.b = ['blue'] * self.n
        self.a=[1]*self.n
        print(1)
        if self.flag == 0:
            if self.flag_openFile == 0:
                self.dll_21.main(m1, m2, N1)  # dll初始化
                self.my_file = 'scale-free-SIS-1.csv'
                print(2)
                self.df = pd.DataFrame(pd.read_csv(self.my_file))
            else:
                self.flag_openFile = 0
            self.G = nx.from_pandas_edgelist(self.df, edge_attr=True)  # 读取csv表格数据赋值到self.G
            self.pos_round = nx.spring_layout(self.G)  # 生成每个节点的坐标位置
            # self.flag=1
            print(3)
            self.dll_21.run_over(N1, step_times + 1,c_double(a1),c_double(a2))  # 执行博弈，时间步为1000
            # 获取数据，读取当前目录下的CSV文件

            print('complete')
            # 数据库
            self.dll_sql = sqlite3.connect("scale-free-SIS.db")
            dff = pd.DataFrame(pd.read_csv('scale-free-SIS-2.csv'))  # , sep='\t'
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            self.dll_sql.execute("delete from some_table")
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            cursor.execute("select * from some_table where ROWID=1")
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i] = 'red'



        else:
            self.step_time += 1
            print('第' + str(self.step_time) + '步')
            self.dll_sql = sqlite3.connect("scale-free-SIS.db")
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            cursor.execute("select * from some_table where ROWID=%d" % (self.step_time + 1))
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i] = 'red'


            print('run')
        print(node_state[0])
        print(3)
        # self.b = ['blue'] * self.n
        # self.a = [1] * self.n
        for i in range(self.n):
            self.a[i] = self.G.degree(i + 1) * 50 + 10  # 度大小设置


        if self.flag == 0:
            self.flag = 1
            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b, node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
            nx.draw_networkx_edges(self.G, pos=self.pos_round, ax=self.axes, alpha=0.4)  # 生成边
        else:
            self.axes.hold(True)

            xx = nx.draw_networkx_nodes(self.G,  pos=self.pos_round, node_color=self.b, node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
        self.flag_out = 1
        self.axes.axis('off')
        self.draw()
        self.axes.hold(False)

    def scale_free_SI(self, m1, m2, a1,N1,step_times):
        self.mode = 21  # 网络类型
        self.n = N1  # 节点个数
        self.number1 = m1  # 初始节点数
        self.number2 = m2  # 新加入节点的度大小
        self.number3=a1

        self.number5 = N1
        self.steps = step_times  # 单步博弈次数
        self.dll_21 = cdll.LoadLibrary('scale-free-SI.dll')
        node_change = [0] * N1
        change_flag = 0
        if self.step_time == step_times:
            self.stop_flag = 1
            return
        self.b = ['blue'] * self.n
        self.a=[1]*self.n
        print(1)
        if self.flag == 0:
            if self.flag_openFile == 0:
                self.dll_21.main(m1, m2, N1)  # dll初始化
                self.my_file = 'scale-free-SI-1.csv'
                print(2)
                self.df = pd.DataFrame(pd.read_csv(self.my_file))
            else:
                self.flag_openFile = 0
            self.G = nx.from_pandas_edgelist(self.df, edge_attr=True)  # 读取csv表格数据赋值到self.G
            self.pos_round = nx.spring_layout(self.G)  # 生成每个节点的坐标位置
            # self.flag=1
            print(3)
            self.dll_21.run_over(N1, step_times + 1,c_double(a1))  # 执行博弈，时间步为1000
            # 获取数据，读取当前目录下的CSV文件

            print('complete')
            # 数据库
            self.dll_sql = sqlite3.connect("scale-free-SI.db")
            dff = pd.DataFrame(pd.read_csv('scale-free-SI-2.csv'))  # , sep='\t'
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            self.dll_sql.execute("delete from some_table")
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            cursor.execute("select * from some_table where ROWID=1")
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i] = 'red'



        else:
            self.step_time += 1
            print('第' + str(self.step_time) + '步')
            self.dll_sql = sqlite3.connect("scale-free-SI.db")
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            cursor.execute("select * from some_table where ROWID=%d" % (self.step_time + 1))
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i] = 'red'


            print('run')
        print(node_state[0])
        print(3)
        # self.b = ['blue'] * self.n
        # self.a = [1] * self.n
        for i in range(self.n):
            self.a[i] = self.G.degree(i + 1) * 50 + 10  # 度大小设置


        if self.flag == 0:
            self.flag = 1
            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b, node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
            nx.draw_networkx_edges(self.G, pos=self.pos_round, ax=self.axes, alpha=0.4)  # 生成边
        else:
            self.axes.hold(True)

            xx = nx.draw_networkx_nodes(self.G,  pos=self.pos_round, node_color=self.b, node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
        self.flag_out = 1
        self.axes.axis('off')
        self.draw()
        self.axes.hold(False)

    def scale_free_SIR(self, m1, m2, a1,a2,N1,step_times):
        self.mode = 15  # 网络类型
        self.n = N1  # 节点个数
        self.number1 = m1  # 初始节点数
        self.number2 = m2  # 新加入节点的度大小
        self.number3=a1
        self.number4=a2
        self.number5 = N1
        self.steps = step_times  # 单步博弈次数
        self.dll_21 = cdll.LoadLibrary('scale-free-SIR.dll')
        node_change = [0] * N1
        change_flag = 0
        if self.step_time == step_times:
            self.stop_flag = 1
            return
        self.b = ['blue'] * self.n
        self.a=[1]*self.n
        print(1)
        if self.flag == 0:
            if self.flag_openFile == 0:
                self.dll_21.main(m1, m2, N1)  # dll初始化
                self.my_file = 'scale-free-SIR-1.csv'
                print(2)
                self.df = pd.DataFrame(pd.read_csv(self.my_file))
            else:
                self.flag_openFile = 0
            self.G = nx.from_pandas_edgelist(self.df, edge_attr=True)  # 读取csv表格数据赋值到self.G
            self.pos_round = nx.spring_layout(self.G)  # 生成每个节点的坐标位置
            # self.flag=1
            print(3)
            self.dll_21.run_over(N1, step_times ,c_double(a1),c_double(a2))  # 执行博弈，时间步为1000
            # 获取数据，读取当前目录下的CSV文件

            print('complete')
            # 数据库
            self.dll_sql = sqlite3.connect("scale-free-SIR.db")
            dff = pd.DataFrame(pd.read_csv('scale-free-SIR-2.csv'))  # , sep='\t'
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            self.dll_sql.execute("delete from some_table")
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            cursor.execute("select * from some_table where ROWID=1")
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                elif node_state[0][i+1] == 0:
                    self.b[i] = 'red'
                else:
                    self.b[i] = 'yellow'



        else:
            self.step_time += 1
            print('第' + str(self.step_time) + '步')
            self.dll_sql = sqlite3.connect("scale-free-SIR.db")
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            cursor.execute("select * from some_table where ROWID=%d" % (self.step_time + 1))
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                elif node_state[0][i + 1] == 0:
                    self.b[i] = 'red'
                else:
                    self.b[i] = 'yellow'


            print('run')
        print(node_state[0])
        print(3)
        # self.b = ['blue'] * self.n
        # self.a = [1] * self.n
        for i in range(self.n):
            self.a[i] = self.G.degree(i + 1) * 50 + 10  # 度大小设置


        if self.flag == 0:
            self.flag = 1
            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b, node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
            nx.draw_networkx_edges(self.G, pos=self.pos_round, ax=self.axes, alpha=0.4)  # 生成边
        else:
            self.axes.hold(True)
            # if change_flag == 0:
            #     return
            xx = nx.draw_networkx_nodes(self.G,  pos=self.pos_round, node_color=self.b, node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
        self.flag_out = 1
        self.axes.axis('off')
        self.draw()
        self.axes.hold(False)

    def scale_free_election(self, m1, m2, step_times, N1):
        self.mode = 9  # 网络类型
        self.n = N1  # 节点个数
        self.number1 = m1  # 初始节点数
        self.number2 = m2  # 新加入节点的度大小
        self.number5 = N1
        self.steps = step_times  # 单步博弈次数
        self.dll_21 = cdll.LoadLibrary('scale-free-election.dll')
        node_change = [0] * N1
        change_flag = 0
        if self.step_time == step_times:
            self.stop_flag = 1
            return
        self.b = ['blue'] * self.n
        self.a=[1]*self.n
        print(1)
        if self.flag == 0:
            if self.flag_openFile == 0:
                self.dll_21.main(m1, m2, N1)  # dll初始化
                self.my_file = 'scale-free-election-1.csv'
                print(2)
                self.df = pd.DataFrame(pd.read_csv(self.my_file))
            else:
                self.flag_openFile = 0
            self.G = nx.from_pandas_edgelist(self.df, edge_attr=True)  # 读取csv表格数据赋值到self.G
            self.pos_round = nx.spring_layout(self.G)  # 生成每个节点的坐标位置
            # self.flag=1
            print(3)
            self.dll_21.run_over(N1, step_times + 1)  # 执行博弈，时间步为1000
            # 获取数据，读取当前目录下的CSV文件

            print('complete')
            # 数据库
            self.dll_sql = sqlite3.connect("scale-free-election.db")
            dff = pd.DataFrame(pd.read_csv('scale-free-election-2.csv'))  # , sep='\t'
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            self.dll_sql.execute("delete from some_table")
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            cursor.execute("select * from some_table where ROWID=1")
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i] = 'red'



        else:
            self.step_time += 1
            print('第' + str(self.step_time) + '步')
            self.dll_sql = sqlite3.connect("scale-free-election.db")
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            cursor.execute("select * from some_table where ROWID=%d" % (self.step_time + 1))
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i] = 'red'


            print('run')
        print(node_state[0])
        print(3)
        # self.b = ['blue'] * self.n
        # self.a = [1] * self.n
        for i in range(self.n):
            self.a[i] = self.G.degree(i + 1) * 50 + 10  # 度大小设置


        if self.flag == 0:
            self.flag = 1
            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b, node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
            nx.draw_networkx_edges(self.G, pos=self.pos_round, ax=self.axes, alpha=0.4)  # 生成边
        else:
            self.axes.hold(True)

            xx = nx.draw_networkx_nodes(self.G,  pos=self.pos_round, node_color=self.b, node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
        self.flag_out = 1
        self.axes.axis('off')
        self.draw()
        self.axes.hold(False)

    def grid_SIS(self, N,m1, m2, step_times):
        self.mode = 10  # 网络类型
        self.n = N  # 节点个数
        self.n1=int(math.sqrt(N))
        self.number1 = m1  # 传染率
        self.number2 = m2  # 恢复率
        self.steps = step_times  # 单步博弈次数
        self.dll_21 = cdll.LoadLibrary('grid-SIS.dll')

        if self.step_time == step_times:
            self.stop_flag = 1
            return
        self.b = ['blue'] * self.n
        self.a=[1]*self.n
        print(1)
        if self.flag == 0:
            if self.flag_openFile == 0:
                self.dll_21.main(N)  # dll初始化
                self.my_file = 'grid-SIS-1.csv'
                print(2)
                self.df = pd.DataFrame(pd.read_csv(self.my_file))
            else:
                self.flag_openFile = 0
            self.G = nx.from_pandas_edgelist(self.df, edge_attr=True)  # 读取csv表格数据赋值到self.G
            self.pos_round = nx.spring_layout(self.G)  # 生成每个节点的坐标位置
            # self.flag=1
            print(3)
            self.dll_21.run_over(N,step_times + 1,c_double(m1),c_double(m2))  # 执行博弈，时间步为1000
            # 获取数据，读取当前目录下的CSV文件
            for i in range(self.n1):  # x坐标
                for j in range(self.n1):
                    self.pos_round[i * self.n1 + j][0] = j
            for i in range(self.n1):  # y坐标
                for j in range(self.n1):
                    self.pos_round[i + j * self.n1][1] = self.n1 - j

            print('complete')
            # 数据库
            self.dll_sql = sqlite3.connect("grid-SIS.db")
            dff = pd.DataFrame(pd.read_csv('grid-SIS-2.csv'))  # , sep='\t'
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            self.dll_sql.execute("delete from some_table")
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            cursor.execute("select * from some_table where ROWID=1")
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i] = 'red'



        else:
            self.step_time += 1
            print('第' + str(self.step_time) + '步')
            self.dll_sql = sqlite3.connect("grid-SIS.db")
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            cursor.execute("select * from some_table where ROWID=%d" % (self.step_time + 1))
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i] = 'red'


            print('run')
        print(node_state[0])
        print(3)
        # self.b = ['blue'] * self.n
        # self.a = [1] * self.n
        for i in range(self.n):
            self.a[i] = self.G.degree(i)*70  # 度大小设置


        if self.flag == 0:
            self.flag = 1
            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b, node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
            nx.draw_networkx_edges(self.G, pos=self.pos_round, ax=self.axes, alpha=0.4)  # 生成边
        else:
            self.axes.hold(True)
            # if change_flag == 0:
            #     return
            xx = nx.draw_networkx_nodes(self.G,  pos=self.pos_round, node_color=self.b, node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
        self.flag_out = 1
        self.axes.axis('off')
        self.draw()
        self.axes.hold(False)

    def grid_SI(self, N,m1,step_times):
        self.mode = 19  # 网络类型
        self.n = N  # 节点个数
        self.n1=int(math.sqrt(N))
        self.number1 = m1  # 传染率
        self.steps = step_times  # 单步博弈次数
        self.dll_21 = cdll.LoadLibrary('grid-SI.dll')

        if self.step_time == step_times:
            self.stop_flag = 1
            return
        self.b = ['blue'] * self.n
        self.a=[1]*self.n
        print(1)
        if self.flag == 0:
            if self.flag_openFile == 0:
                self.dll_21.main(N)  # dll初始化
                self.my_file = 'grid-SI-1.csv'
                print(2)
                self.df = pd.DataFrame(pd.read_csv(self.my_file))
            else:
                self.flag_openFile = 0
            self.G = nx.from_pandas_edgelist(self.df, edge_attr=True)  # 读取csv表格数据赋值到self.G
            self.pos_round = nx.spring_layout(self.G)  # 生成每个节点的坐标位置
            # self.flag=1
            print(3)
            self.dll_21.run_over(N,step_times + 1,c_double(m1))  # 执行博弈，时间步为1000
            # 获取数据，读取当前目录下的CSV文件
            for i in range(self.n1):  # x坐标
                for j in range(self.n1):
                    self.pos_round[i * self.n1 + j][0] = j
            for i in range(self.n1):  # y坐标
                for j in range(self.n1):
                    self.pos_round[i + j * self.n1][1] = self.n1 - j

            print('complete')
            # 数据库
            self.dll_sql = sqlite3.connect("grid-SI.db")
            dff = pd.DataFrame(pd.read_csv('grid-SI-2.csv'))  # , sep='\t'
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            self.dll_sql.execute("delete from some_table")
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            cursor.execute("select * from some_table where ROWID=1")
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i] = 'red'



        else:
            self.step_time += 1
            print('第' + str(self.step_time) + '步')
            self.dll_sql = sqlite3.connect("grid-SI.db")
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            cursor.execute("select * from some_table where ROWID=%d" % (self.step_time + 1))
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i] = 'red'


            print('run')
        print(node_state[0])
        print(3)
        # self.b = ['blue'] * self.n
        # self.a = [1] * self.n
        for i in range(self.n):
            self.a[i] = self.G.degree(i)*70  # 度大小设置


        if self.flag == 0:
            self.flag = 1
            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b, node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
            nx.draw_networkx_edges(self.G, pos=self.pos_round, ax=self.axes, alpha=0.4)  # 生成边
        else:
            self.axes.hold(True)
            # if change_flag == 0:
            #     return
            xx = nx.draw_networkx_nodes(self.G,  pos=self.pos_round, node_color=self.b, node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
        self.flag_out = 1
        self.axes.axis('off')
        self.draw()
        self.axes.hold(False)

    def grid_SIR(self, N,m1, m2, step_times):
        self.mode = 11  # 网络类型
        self.n = N  # 节点个数
        self.n1 = int(math.sqrt(N))
        self.number1 = m1  # 传染率
        self.number2 = m2  # 恢复率
        self.steps = step_times  # 单步博弈次数
        self.dll_21 = cdll.LoadLibrary('grid-SIR.dll')

        if self.step_time == step_times:
            self.stop_flag = 1
            return
        self.b = ['blue'] * self.n
        self.a=[1]*self.n
        print(1)
        if self.flag == 0:
            if self.flag_openFile == 0:
                self.dll_21.main(N)  # dll初始化
                self.my_file = 'grid-SIR-1.csv'
                print(2)
                self.df = pd.DataFrame(pd.read_csv(self.my_file))
            else:
                self.flag_openFile = 0
            self.G = nx.from_pandas_edgelist(self.df, edge_attr=True)  # 读取csv表格数据赋值到self.G
            self.pos_round = nx.spring_layout(self.G)  # 生成每个节点的坐标位置
            # self.flag=1
            print(3)
            self.dll_21.run_over(N,step_times,c_double(m1),c_double(m2))  # 执行博弈，时间步为1000
            # 获取数据，读取当前目录下的CSV文件

            for i in range(self.n1):  # x坐标
                for j in range(self.n1):
                    self.pos_round[i * self.n1 + j][0] = j
            for i in range(self.n1):  # y坐标
                for j in range(self.n1):
                    self.pos_round[i + j * self.n1][1] = self.n1 - j

            print('complete')


            # 数据库
            self.dll_sql = sqlite3.connect("grid-SIR.db")
            dff = pd.DataFrame(pd.read_csv('grid-SIR-2.csv'))  # , sep='\t'
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            self.dll_sql.execute("delete from some_table")
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            cursor.execute("select * from some_table where ROWID=1")
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                elif node_state[0][i+1] == 0:
                    self.b[i] = 'red'
                else:
                    self.b[i] = 'yellow'



        else:
            self.step_time += 1
            print('第' + str(self.step_time) + '步')
            self.dll_sql = sqlite3.connect("grid-SIR.db")
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            cursor.execute("select * from some_table where ROWID=%d" % (self.step_time + 1))
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                elif node_state[0][i + 1] == 0:
                    self.b[i] = 'red'
                else:
                    self.b[i] = 'yellow'


            print('run')
        print(node_state[0])
        print(3)
        # self.b = ['blue'] * self.n
        # self.a = [1] * self.n
        for i in range(self.n):
            self.a[i] = self.G.degree(i)*70  # 度大小设置


        if self.flag == 0:
            self.flag = 1
            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b, node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
            nx.draw_networkx_edges(self.G, pos=self.pos_round, ax=self.axes, alpha=0.4)  # 生成边
        else:
            self.axes.hold(True)
            # if change_flag == 0:
            #     return
            xx = nx.draw_networkx_nodes(self.G,  pos=self.pos_round, node_color=self.b, node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
        self.flag_out = 1
        self.axes.axis('off')
        self.draw()
        self.axes.hold(False)

    def grid_election(self, n, step_times):
        self.mode = 7  # 网络类型
        self.M=n
        self.n = n  # 节点个数
        self.n1=int(math.sqrt(n))
        self.steps = step_times  # 单步博弈次数
        self.dll_21 = cdll.LoadLibrary('grid-election.dll')

        if self.step_time == step_times:
            self.stop_flag = 1
            return
        self.b = ['blue'] * self.n
        self.a=[1]*self.n
        print(1)
        if self.flag == 0:
            if self.flag_openFile == 0:
                self.dll_21.main(n)  # dll初始化
                self.my_file = 'grid-election-1.csv'
                print(2)
                self.df = pd.DataFrame(pd.read_csv(self.my_file))
            else:
                self.flag_openFile = 0
            self.G = nx.from_pandas_edgelist(self.df, edge_attr=True)  # 读取csv表格数据赋值到self.G
            self.pos_round = nx.spring_layout(self.G)  # 生成每个节点的坐标位置
            # self.flag=1
            print(3)
            self.dll_21.run_over(n, step_times + 1)  # 执行博弈，时间步为1000
            # 获取数据，读取当前目录下的CSV文件
            for i in range(self.n1):  # x坐标
                for j in range(self.n1):
                    self.pos_round[i * self.n1 + j][0] = j
            for i in range(self.n1):  # y坐标
                for j in range(self.n1):
                    self.pos_round[i + j * self.n1][1] = self.n1 - j


            print('complete')
            # 数据库
            self.dll_sql = sqlite3.connect("grid-election.db")
            dff = pd.DataFrame(pd.read_csv('grid-election-2.csv'))  # , sep='\t'
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            self.dll_sql.execute("delete from some_table")
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            cursor.execute("select * from some_table where ROWID=1")
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i] = 'red'



        else:
            self.step_time += 1
            print('第' + str(self.step_time) + '步')
            self.dll_sql = sqlite3.connect("grid-election.db")
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            cursor.execute("select * from some_table where ROWID=%d" % (self.step_time + 1))
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i] = 'red'


            print('run')
        for i in range(self.n):
            self.a[i] = self.G.degree(i) * 70  # 度大小设置


        if self.flag == 0:
            self.flag = 1
            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b, node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
            nx.draw_networkx_edges(self.G, pos=self.pos_round, ax=self.axes, alpha=0.4)  # 生成边
        else:
            self.axes.hold(True)

            xx = nx.draw_networkx_nodes(self.G,  pos=self.pos_round, node_color=self.b, node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
        self.flag_out = 1
        self.axes.axis('off')
        self.draw()
        self.axes.hold(False)

    def grid_deffuant(self, n, step_times,a1,a2):
        self.mode = 22  # 网络类型
        self.M=n
        self.n = n  # 节点个数
        self.n1=int(math.sqrt(n))
        self.steps = step_times  # 单步博弈次数
        self.a1=a1
        self.a2=a2
        self.dll_21 = cdll.LoadLibrary('grid-deffuant.dll')

        if self.step_time == step_times:
            self.stop_flag = 1
            return
        self.b = ['blue'] * self.n
        self.a=[1]*self.n
        print(1)
        if self.flag == 0:
            if self.flag_openFile == 0:
                self.dll_21.main(n)  # dll初始化
                self.my_file = 'grid-deffuant-1.csv'
                print(2)
                self.df = pd.DataFrame(pd.read_csv(self.my_file))
            else:
                self.flag_openFile = 0
            self.G = nx.from_pandas_edgelist(self.df, edge_attr=True)  # 读取csv表格数据赋值到self.G
            self.pos_round = nx.spring_layout(self.G)  # 生成每个节点的坐标位置
            # self.flag=1
            print(3)
            self.dll_21.run_over(n, step_times + 1,c_double(a1),c_double(a2))  # 执行博弈，时间步为1000
            # 获取数据，读取当前目录下的CSV文件
            for i in range(self.n1):  # x坐标
                for j in range(self.n1):
                    self.pos_round[i * self.n1 + j][0] = j
            for i in range(self.n1):  # y坐标
                for j in range(self.n1):
                    self.pos_round[i + j * self.n1][1] = self.n1 - j


            print('complete')
            # 数据库
            self.dll_sql = sqlite3.connect("grid-deffuant.db")
            dff = pd.DataFrame(pd.read_csv('grid-deffuant-2.csv'))  # , sep='\t'
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            self.dll_sql.execute("delete from some_table")
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            cursor.execute("select * from some_table where ROWID=1")
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] <0.1:
                    self.b[i] = 'mediumblue'
                elif node_state[0][i+1] <0.2:
                    self.b[i] = 'blue'
                elif node_state[0][i + 1] < 0.3:
                    self.b[i]='royalblue'
                elif node_state[0][i + 1] < 0.4:
                    self.b[i]='cornflowerblue'
                elif node_state[0][i + 1] < 0.5:
                    self.b[i]='turquoise'
                elif node_state[0][i + 1] < 0.6:
                    self.b[i]='lime'
                elif node_state[0][i + 1] < 0.7:
                    self.b[i]='chartreuse'
                elif node_state[0][i + 1] < 0.8:
                    self.b[i]='tomato'
                elif node_state[0][i + 1] < 0.9:
                    self.b[i]='orangered'
                elif node_state[0][i + 1] < 1:
                    self.b[i]='red'






        else:
            self.step_time += 1
            print('第' + str(self.step_time) + '步')
            self.dll_sql = sqlite3.connect("grid-deffuant.db")
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            cursor.execute("select * from some_table where ROWID=%d" % (self.step_time + 1))
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i + 1] < 0.1:
                    self.b[i] = 'mediumblue'
                elif node_state[0][i + 1] < 0.2:
                    self.b[i] = 'blue'
                elif node_state[0][i + 1] < 0.3:
                    self.b[i] = 'royalblue'
                elif node_state[0][i + 1] < 0.4:
                    self.b[i] = 'cornflowerblue'
                elif node_state[0][i + 1] < 0.5:
                    self.b[i] = 'turquoise'
                elif node_state[0][i + 1] < 0.6:
                    self.b[i] = 'lime'
                elif node_state[0][i + 1] < 0.7:
                    self.b[i] = 'chartreuse'
                elif node_state[0][i + 1] < 0.8:
                    self.b[i] = 'tomato'
                elif node_state[0][i + 1] < 0.9:
                    self.b[i] = 'orangered'
                elif node_state[0][i + 1] < 1:
                    self.b[i] = 'red'


            print('run')
        for i in range(self.n):
            self.a[i] = self.G.degree(i) * 70  # 度大小设置


        if self.flag == 0:
            self.flag = 1
            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b, node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
            nx.draw_networkx_edges(self.G, pos=self.pos_round, ax=self.axes, alpha=0.4)  # 生成边
        else:
            self.axes.hold(True)

            xx = nx.draw_networkx_nodes(self.G,  pos=self.pos_round, node_color=self.b, node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
        self.flag_out = 1
        self.axes.axis('off')
        self.draw()
        self.axes.hold(False)


    def small_world_prisoner(self, number, p, step_times, N2,a1,a2):
        self.mode = 2  # 网络类型
        self.n = N2  # 节点个数
        self.number1 = number  # 邻居节点数
        self.number2 = p  # 概率
        self.number5 = N2
        self.steps = step_times  # 单步博弈次数
        self.a1=a1
        self.a2=a2
        self.dll_21 = cdll.LoadLibrary('small-world-evolutionary.dll')
        node_change = [0] * N2
        change_flag = 0
        if self.step_time == step_times:
            self.stop_flag = 1
            return
        self.b = ['blue'] * self.n
        self.a = [1] * self.n
        print(1)
        if self.flag == 0:
            if self.flag_openFile == 0:
                self.dll_21.main(number, c_double(p), N2)  # dll初始化
                self.my_file = 'small-world-evolutionary-1.csv'
                print(2)
                self.df = pd.DataFrame(pd.read_csv(self.my_file))
            else:
                self.flag_openFile = 0
            self.G = nx.from_pandas_edgelist(self.df, edge_attr=True)  # 读取csv表格数据赋值到self.G
            self.pos_round = nx.spring_layout(self.G)  # 生成每个节点的坐标位置
            self.path=nx.average_shortest_path_length(self.G)
            self.cluster=nx.average_clustering(self.G)
            self.degree=nx.degree_histogram(self.G)
            self.sum=0
            for i in range(len(self.degree)):
                self.sum=self.sum+i*self.degree[i]
            self.ave_degree=self.sum/nx.number_of_nodes(self.G)


            # self.flag=1
            print(3)
            self.dll_21.run_over(N2, step_times + 1,c_double(a1),c_double(a2))  # 执行博弈，时间步为1000
            # 获取数据，读取当前目录下的CSV文件

            print('complete')
            # 数据库
            self.dll_sql = sqlite3.connect("small-world-evolutionary.db")
            dff = pd.DataFrame(pd.read_csv('small-world-evolutionary-2.csv'))  # , sep='\t'
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            self.dll_sql.execute("delete from some_table")
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            cursor.execute("select * from some_table where ROWID=1")
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i] = 'red'

        else:
            self.step_time += 1
            #print('第' + str(self.step_time) + '步')
            self.dll_sql = sqlite3.connect("small-world-evolutionary.db")
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            cursor.execute("select * from some_table where ROWID=%d" % (self.step_time + 1))
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i] = 'red'


            print('run')
        print(node_state[0])
        print(3)

        # self.b = ['blue'] * self.n
        #self.a=[1]*self.n
        for i in range(self.n):

            self.a[i] = self.G.degree(i) * 30  # 度大小设置

        if self.flag == 0:
            self.flag = 1
            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b,node_size=self.a, ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
            nx.draw_networkx_edges(self.G, pos=self.pos_round, ax=self.axes, alpha=0.4)  # 生成边
        else:
            self.axes.hold(True)

            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b,node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
        self.flag_out = 1

        self.axes.axis('off')
        self.draw()
        self.axes.hold(False)

    def random_network_prisoner(self, number, p, step_times, N2,a1,a2):
        self.mode = 16  # 网络类型
        self.n = N2  # 节点个数
        self.number1 = number  # 邻居节点数
        self.number2 = p  # 概率
        self.number5 = N2
        self.steps = step_times  # 单步博弈次数
        self.a1=a1
        self.a2=a2
        self.dll_21 = cdll.LoadLibrary('random-network-evolutionary.dll')
        node_change = [0] * N2
        change_flag = 0
        if self.step_time == step_times:
            self.stop_flag = 1
            return
        self.b = ['blue'] * self.n
        self.a = [1] * self.n
        print(1)
        if self.flag == 0:
            if self.flag_openFile == 0:
                self.dll_21.main(number, c_double(p), N2)  # dll初始化
                self.my_file = 'random-network-evolutionary-1.csv'
                print(2)
                self.df = pd.DataFrame(pd.read_csv(self.my_file))
            else:
                self.flag_openFile = 0
            self.G = nx.from_pandas_edgelist(self.df, edge_attr=True)  # 读取csv表格数据赋值到self.G
            self.pos_round = nx.spring_layout(self.G)  # 生成每个节点的坐标位置
            # self.flag=1
            print(3)
            self.dll_21.run_over(N2, step_times + 1,c_double(a1),c_double(a2))  # 执行博弈，时间步为1000
            # 获取数据，读取当前目录下的CSV文件

            print('complete')
            # 数据库
            self.dll_sql = sqlite3.connect("random-network-evolutionary.db")
            dff = pd.DataFrame(pd.read_csv('random-network-evolutionary-2.csv'))  # , sep='\t'
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            self.dll_sql.execute("delete from some_table")
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            cursor.execute("select * from some_table where ROWID=1")
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i] = 'red'

        else:
            self.step_time += 1
            #print('第' + str(self.step_time) + '步')
            self.dll_sql = sqlite3.connect("random-network-evolutionary.db")
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            cursor.execute("select * from some_table where ROWID=%d" % (self.step_time + 1))
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i] = 'red'


            print('run')
        print(node_state[0])
        print(3)

        # self.b = ['blue'] * self.n
        #self.a=[1]*self.n
        for i in range(self.n):

            self.a[i] = self.G.degree(i) * 30  # 度大小设置

        if self.flag == 0:
            self.flag = 1
            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b,node_size=self.a, ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
            nx.draw_networkx_edges(self.G, pos=self.pos_round, ax=self.axes, alpha=0.4)  # 生成边
        else:
            self.axes.hold(True)

            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b,node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
        self.flag_out = 1

        self.axes.axis('off')
        self.draw()
        self.axes.hold(False)

    def small_world_snow(self, number, p, step_times, N2,a1,a2):
        self.mode = 2  # 网络类型
        self.n = N2  # 节点个数
        self.number1 = number  # 邻居节点数
        self.number2 = p  # 概率
        self.number5 = N2
        self.steps = step_times  # 单步博弈次数
        self.a1=a1
        self.a2=a2
        self.dll_21 = cdll.LoadLibrary('small-world-evolutionary.dll')
        node_change = [0] * N2
        change_flag = 0
        if self.step_time == step_times:
            self.stop_flag = 1
            return
        self.b = ['blue'] * self.n
        self.a = [1] * self.n
        print(1)
        if self.flag == 0:
            if self.flag_openFile == 0:
                self.dll_21.main(number, c_double(p), N2)  # dll初始化
                self.my_file = 'small-world-evolutionary-1.csv'
                print(2)
                self.df = pd.DataFrame(pd.read_csv(self.my_file))
            else:
                self.flag_openFile = 0
            self.G = nx.from_pandas_edgelist(self.df, edge_attr=True)  # 读取csv表格数据赋值到self.G
            self.pos_round = nx.spring_layout(self.G)  # 生成每个节点的坐标位置
            # self.flag=1
            print(3)
            self.dll_21.run_over(N2, step_times + 1,c_double(a1),c_double(a2))  # 执行博弈，时间步为1000
            # 获取数据，读取当前目录下的CSV文件

            print('complete')
            # 数据库
            self.dll_sql = sqlite3.connect("small-world-evolutionary.db")
            dff = pd.DataFrame(pd.read_csv('small-world-evolutionary-2.csv'))  # , sep='\t'
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            self.dll_sql.execute("delete from some_table")
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            cursor.execute("select * from some_table where ROWID=1")
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i] = 'red'

        else:
            self.step_time += 1
            #print('第' + str(self.step_time) + '步')
            self.dll_sql = sqlite3.connect("small-world-evolutionary.db")
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            cursor.execute("select * from some_table where ROWID=%d" % (self.step_time + 1))
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i] = 'red'


            print('run')
        print(node_state[0])
        print(3)

        # self.b = ['blue'] * self.n
        #self.a=[1]*self.n
        for i in range(self.n):

            self.a[i] = self.G.degree(i) * 30  # 度大小设置

        if self.flag == 0:
            self.flag = 1
            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b,node_size=self.a, ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
            nx.draw_networkx_edges(self.G, pos=self.pos_round, ax=self.axes, alpha=0.4)  # 生成边
        else:
            self.axes.hold(True)

            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b,node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
        self.flag_out = 1

        self.axes.axis('off')
        self.draw()
        self.axes.hold(False)

    def random_network_snow(self, number, p, step_times, N2,a1,a2):
        self.mode = 17  # 网络类型
        self.n = N2  # 节点个数
        self.number1 = number  # 邻居节点数
        self.number2 = p  # 概率
        self.number5 = N2
        self.steps = step_times  # 单步博弈次数
        self.a1=a1
        self.a2=a2
        self.dll_21 = cdll.LoadLibrary('random-network-evolutionary.dll')
        node_change = [0] * N2
        change_flag = 0
        if self.step_time == step_times:
            self.stop_flag = 1
            return
        self.b = ['blue'] * self.n
        self.a = [1] * self.n
        print(1)
        if self.flag == 0:
            if self.flag_openFile == 0:
                self.dll_21.main(number, c_double(p), N2)  # dll初始化
                self.my_file = 'random-network-evolutionary-1.csv'
                print(2)
                self.df = pd.DataFrame(pd.read_csv(self.my_file))
            else:
                self.flag_openFile = 0
            self.G = nx.from_pandas_edgelist(self.df, edge_attr=True)  # 读取csv表格数据赋值到self.G
            self.pos_round = nx.spring_layout(self.G)  # 生成每个节点的坐标位置
            # self.flag=1
            print(3)
            self.dll_21.run_over(N2, step_times + 1,c_double(a1),c_double(a2))  # 执行博弈，时间步为1000
            # 获取数据，读取当前目录下的CSV文件

            print('complete')
            # 数据库
            self.dll_sql = sqlite3.connect("random-network-evolutionary.db")
            dff = pd.DataFrame(pd.read_csv('random-network-evolutionary-2.csv'))  # , sep='\t'
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            self.dll_sql.execute("delete from some_table")
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            cursor.execute("select * from some_table where ROWID=1")
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i] = 'red'

        else:
            self.step_time += 1
            #print('第' + str(self.step_time) + '步')
            self.dll_sql = sqlite3.connect("random-network-evolutionary.db")
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            cursor.execute("select * from some_table where ROWID=%d" % (self.step_time + 1))
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i] = 'red'


            print('run')
        print(node_state[0])
        print(3)

        # self.b = ['blue'] * self.n
        #self.a=[1]*self.n
        for i in range(self.n):

            self.a[i] = self.G.degree(i) * 30  # 度大小设置

        if self.flag == 0:
            self.flag = 1
            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b,node_size=self.a, ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
            nx.draw_networkx_edges(self.G, pos=self.pos_round, ax=self.axes, alpha=0.4)  # 生成边
        else:
            self.axes.hold(True)

            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b,node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
        self.flag_out = 1

        self.axes.axis('off')
        self.draw()
        self.axes.hold(False)

    def small_world_SIR(self, p,number,N2,a1,a2,step_times):
        self.mode = 12  # 网络类型
        self.n=N2
        self.number1 = p # 概率
        self.number2 = number  # 邻居节点数
        self.number3 = N2
        self.number4=a1
        self.number5=a2
        self.steps = step_times  # 单步博弈次数
        self.dll_21 = cdll.LoadLibrary('small-world-SIR.dll')

        if self.step_time == step_times:
            self.stop_flag = 1
            return
        self.b = ['blue'] * self.n
        self.a = [1] * self.n
        print(1)
        if self.flag == 0:
            if self.flag_openFile == 0:
                self.dll_21.main(number, c_double(p), N2)  # dll初始化
                self.my_file = 'small-world-SIR-1.csv'
                print(2)
                self.df = pd.DataFrame(pd.read_csv(self.my_file))
            else:
                self.flag_openFile = 0
            self.G = nx.from_pandas_edgelist(self.df, edge_attr=True)  # 读取csv表格数据赋值到self.G
            self.pos_round = nx.spring_layout(self.G)  # 生成每个节点的坐标位置
            # self.flag=1
            print(3)
            self.dll_21.run_over(N2, step_times ,c_double(a1),c_double(a2))  # 执行博弈，时间步为1000
            # 获取数据，读取当前目录下的CSV文件

            print('complete')
            # 数据库
            self.dll_sql = sqlite3.connect("small-world-SIR.db")
            dff = pd.DataFrame(pd.read_csv('small-world-SIR-2.csv'))  # , sep='\t'
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            self.dll_sql.execute("delete from some_table")
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            cursor.execute("select * from some_table where ROWID=1")
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                elif node_state[0][i + 1] == 0:
                    self.b[i] = 'red'
                else:
                    self.b[i]='yellow'

        else:
            self.step_time += 1
            #print('第' + str(self.step_time) + '步')
            self.dll_sql = sqlite3.connect("small-world-SIR.db")
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            cursor.execute("select * from some_table where ROWID=%d" % (self.step_time + 1))
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                elif node_state[0][i+1] == 0:
                    self.b[i] = 'red'
                else:
                    self.b[i]='yellow'


            print('run')
        print(node_state[0])
        print(3)

        # self.b = ['blue'] * self.n
        #self.a=[1]*self.n
        for i in range(self.n):

            self.a[i] = self.G.degree(i) * 30  # 度大小设置

        if self.flag == 0:
            self.flag = 1
            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b,node_size=self.a, ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
            nx.draw_networkx_edges(self.G, pos=self.pos_round, ax=self.axes, alpha=0.4)  # 生成边
        else:
            self.axes.hold(True)

            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b,node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
        self.flag_out = 1

        self.axes.axis('off')
        self.draw()
        self.axes.hold(False)

    def random_network_SIR(self, p,number,N2,a1,a2,step_times):
        self.mode = 25  # 网络类型
        self.n=N2
        self.number1 = p # 概率
        self.number2 = number  # 邻居节点数
        self.number3 = N2
        self.number4=a1
        self.number5=a2
        self.steps = step_times  # 单步博弈次数
        self.dll_21 = cdll.LoadLibrary('random-network-SIR.dll')

        if self.step_time == step_times:
            self.stop_flag = 1
            return
        self.b = ['blue'] * self.n
        self.a = [1] * self.n
        print(1)
        if self.flag == 0:
            if self.flag_openFile == 0:
                self.dll_21.main(number, c_double(p), N2)  # dll初始化
                self.my_file = 'random-network-SIR-1.csv'
                print(2)
                self.df = pd.DataFrame(pd.read_csv(self.my_file))
            else:
                self.flag_openFile = 0
            self.G = nx.from_pandas_edgelist(self.df, edge_attr=True)  # 读取csv表格数据赋值到self.G
            self.pos_round = nx.spring_layout(self.G)  # 生成每个节点的坐标位置
            # self.flag=1
            print(3)
            self.dll_21.run_over(N2, step_times ,c_double(a1),c_double(a2))  # 执行博弈，时间步为1000
            # 获取数据，读取当前目录下的CSV文件

            print('complete')
            # 数据库
            self.dll_sql = sqlite3.connect("random-network-SIR.db")
            dff = pd.DataFrame(pd.read_csv('random-network-SIR-2.csv'))  # , sep='\t'
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            self.dll_sql.execute("delete from some_table")
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            cursor.execute("select * from some_table where ROWID=1")
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                elif node_state[0][i + 1] == 0:
                    self.b[i] = 'red'
                else:
                    self.b[i]='yellow'

        else:
            self.step_time += 1
            #print('第' + str(self.step_time) + '步')
            self.dll_sql = sqlite3.connect("random-network-SIR.db")
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            cursor.execute("select * from some_table where ROWID=%d" % (self.step_time + 1))
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                elif node_state[0][i+1] == 0:
                    self.b[i] = 'red'
                else:
                    self.b[i]='yellow'


            print('run')
        print(node_state[0])
        print(3)

        # self.b = ['blue'] * self.n
        #self.a=[1]*self.n
        for i in range(self.n):

            self.a[i] = self.G.degree(i) * 30  # 度大小设置

        if self.flag == 0:
            self.flag = 1
            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b,node_size=self.a, ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
            nx.draw_networkx_edges(self.G, pos=self.pos_round, ax=self.axes, alpha=0.4)  # 生成边
        else:
            self.axes.hold(True)

            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b,node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
        self.flag_out = 1

        self.axes.axis('off')
        self.draw()
        self.axes.hold(False)

    def small_world_SIS(self,number,p,step_times,N2,a1,a2):
        self.mode = 13  # 网络类型
        self.n = N2  # 节点个数
        self.number1 = number  # 邻居节点数
        self.number2 = p  # 概率
        self.number5 = N2
        self.number3=a1
        self.number4=a2


        #self.number4=a1 #传染率
        #self.number5=a2 #恢复率
        self.steps = step_times  # 单步博弈次数
        self.dll_21 = cdll.LoadLibrary('small-world-SIS.dll')

        if self.step_time == step_times:
            self.stop_flag = 1
            return
        self.b = ['blue'] * self.n
        self.a = [1] * self.n
        print(1)
        if self.flag == 0:
            if self.flag_openFile == 0:
                self.dll_21.main(number,c_double(p),N2)  # dll初始化
                self.my_file = 'small-world-SIS-1.csv'
                print(2)
                self.df = pd.DataFrame(pd.read_csv(self.my_file))
            else:
                self.flag_openFile = 0
            self.G = nx.from_pandas_edgelist(self.df, edge_attr=True)  # 读取csv表格数据赋值到self.G
            self.pos_round = nx.spring_layout(self.G)  # 生成每个节点的坐标位置
            # self.flag=1
            print(3)
            self.dll_21.run_over(N2, step_times + 1,c_double(a1),c_double(a2))  # 执行博弈，时间步为1000
            # 获取数据，读取当前目录下的CSV文件

            print('complete')
            # 数据库
            self.dll_sql = sqlite3.connect("small-world-SIS.db")
            dff = pd.DataFrame(pd.read_csv('small-world-SIS-2.csv'))  # , sep='\t'
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            self.dll_sql.execute("delete from some_table")
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            cursor.execute("select * from some_table where ROWID=1")
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i]='red'

        else:
            self.step_time += 1
            #print('第' + str(self.step_time) + '步')
            self.dll_sql = sqlite3.connect("small-world-SIS.db")
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            cursor.execute("select * from some_table where ROWID=%d" % (self.step_time + 1))
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i]='red'


            print('run')
        print(node_state[0])
        print(3)

        # self.b = ['blue'] * self.n
        #self.a=[1]*self.n
        for i in range(self.n):

            self.a[i] = self.G.degree(i) * 30  # 度大小设置

        if self.flag == 0:
            self.flag = 1
            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b,node_size=self.a, ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
            nx.draw_networkx_edges(self.G, pos=self.pos_round, ax=self.axes, alpha=0.4)  # 生成边
        else:
            self.axes.hold(True)
            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b,node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
        self.flag_out = 1

        self.axes.axis('off')
        self.draw()
        self.axes.hold(False)

    def random_network_SIS(self,number,p,step_times,N2,a1,a2):
        self.mode = 24  # 网络类型
        self.n = N2  # 节点个数
        self.number1 = number  # 邻居节点数
        self.number2 = p  # 概率
        self.number5 = N2
        self.number3=a1
        self.number4=a2


        #self.number4=a1 #传染率
        #self.number5=a2 #恢复率
        self.steps = step_times  # 单步博弈次数
        self.dll_21 = cdll.LoadLibrary('random-network-SIS.dll')

        if self.step_time == step_times:
            self.stop_flag = 1
            return
        self.b = ['blue'] * self.n
        self.a = [1] * self.n
        print(1)
        if self.flag == 0:
            if self.flag_openFile == 0:
                self.dll_21.main(number,c_double(p),N2)  # dll初始化
                self.my_file = 'random-network-SIS-1.csv'
                print(2)
                self.df = pd.DataFrame(pd.read_csv(self.my_file))
            else:
                self.flag_openFile = 0
            self.G = nx.from_pandas_edgelist(self.df, edge_attr=True)  # 读取csv表格数据赋值到self.G
            self.pos_round = nx.spring_layout(self.G)  # 生成每个节点的坐标位置
            # self.flag=1
            print(3)
            self.dll_21.run_over(N2, step_times + 1,c_double(a1),c_double(a2))  # 执行博弈，时间步为1000
            # 获取数据，读取当前目录下的CSV文件

            print('complete')
            # 数据库
            self.dll_sql = sqlite3.connect("random-network-SIS.db")
            dff = pd.DataFrame(pd.read_csv('random-network-SIS-2.csv'))  # , sep='\t'
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            self.dll_sql.execute("delete from some_table")
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            cursor.execute("select * from some_table where ROWID=1")
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i]='red'

        else:
            self.step_time += 1
            #print('第' + str(self.step_time) + '步')
            self.dll_sql = sqlite3.connect("random-network-SIS.db")
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            cursor.execute("select * from some_table where ROWID=%d" % (self.step_time + 1))
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i]='red'


            print('run')
        print(node_state[0])
        print(3)

        # self.b = ['blue'] * self.n
        #self.a=[1]*self.n
        for i in range(self.n):

            self.a[i] = self.G.degree(i) * 30  # 度大小设置

        if self.flag == 0:
            self.flag = 1
            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b,node_size=self.a, ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
            nx.draw_networkx_edges(self.G, pos=self.pos_round, ax=self.axes, alpha=0.4)  # 生成边
        else:
            self.axes.hold(True)
            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b,node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
        self.flag_out = 1

        self.axes.axis('off')
        self.draw()
        self.axes.hold(False)

    def small_world_SI(self,number,p,step_times,N2,a1):
        self.mode = 20  # 网络类型
        self.n = N2  # 节点个数
        self.number1 = number  # 邻居节点数
        self.number2 = p  # 概率
        self.number5 = N2
        self.number3=a1



        #self.number4=a1 #传染率
        #self.number5=a2 #恢复率
        self.steps = step_times  # 单步博弈次数
        self.dll_21 = cdll.LoadLibrary('small-world-SI.dll')

        if self.step_time == step_times:
            self.stop_flag = 1
            return
        self.b = ['blue'] * self.n
        self.a = [1] * self.n
        print(1)
        if self.flag == 0:
            if self.flag_openFile == 0:
                self.dll_21.main(number,c_double(p),N2)  # dll初始化
                self.my_file = 'small-world-SI-1.csv'
                print(2)
                self.df = pd.DataFrame(pd.read_csv(self.my_file))
            else:
                self.flag_openFile = 0
            self.G = nx.from_pandas_edgelist(self.df, edge_attr=True)  # 读取csv表格数据赋值到self.G
            self.pos_round = nx.spring_layout(self.G)  # 生成每个节点的坐标位置
            # self.flag=1
            print(3)
            self.dll_21.run_over(N2, step_times + 1,c_double(a1))  # 执行博弈，时间步为1000
            # 获取数据，读取当前目录下的CSV文件

            print('complete')
            # 数据库
            self.dll_sql = sqlite3.connect("small-world-SI.db")
            dff = pd.DataFrame(pd.read_csv('small-world-SI-2.csv'))  # , sep='\t'
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            self.dll_sql.execute("delete from some_table")
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            cursor.execute("select * from some_table where ROWID=1")
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i]='red'

        else:
            self.step_time += 1
            #print('第' + str(self.step_time) + '步')
            self.dll_sql = sqlite3.connect("small-world-SI.db")
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            cursor.execute("select * from some_table where ROWID=%d" % (self.step_time + 1))
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i]='red'


            print('run')
        print(node_state[0])
        print(3)

        # self.b = ['blue'] * self.n
        #self.a=[1]*self.n
        for i in range(self.n):

            self.a[i] = self.G.degree(i) * 30  # 度大小设置

        if self.flag == 0:
            self.flag = 1
            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b,node_size=self.a, ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
            nx.draw_networkx_edges(self.G, pos=self.pos_round, ax=self.axes, alpha=0.4)  # 生成边
        else:
            self.axes.hold(True)
            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b,node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
        self.flag_out = 1

        self.axes.axis('off')
        self.draw()
        self.axes.hold(False)

    def random_network_SI(self,number,p,step_times,N2,a1):
        self.mode = 23  # 网络类型
        self.n = N2  # 节点个数
        self.number1 = number  # 邻居节点数
        self.number2 = p  # 概率
        self.number5 = N2
        self.number3=a1



        #self.number4=a1 #传染率
        #self.number5=a2 #恢复率
        self.steps = step_times  # 单步博弈次数
        self.dll_21 = cdll.LoadLibrary('random-network-SI.dll')

        if self.step_time == step_times:
            self.stop_flag = 1
            return
        self.b = ['blue'] * self.n
        self.a = [1] * self.n
        print(1)
        if self.flag == 0:
            if self.flag_openFile == 0:
                self.dll_21.main(number,c_double(p),N2)  # dll初始化
                self.my_file = 'random-network-SI-1.csv'
                print(2)
                self.df = pd.DataFrame(pd.read_csv(self.my_file))
            else:
                self.flag_openFile = 0
            self.G = nx.from_pandas_edgelist(self.df, edge_attr=True)  # 读取csv表格数据赋值到self.G
            self.pos_round = nx.spring_layout(self.G)  # 生成每个节点的坐标位置
            # self.flag=1
            print(3)
            self.dll_21.run_over(N2, step_times + 1,c_double(a1))  # 执行博弈，时间步为1000
            # 获取数据，读取当前目录下的CSV文件

            print('complete')
            # 数据库
            self.dll_sql = sqlite3.connect("random-network-SI.db")
            dff = pd.DataFrame(pd.read_csv('random-network-SI-2.csv'))  # , sep='\t'
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            self.dll_sql.execute("delete from some_table")
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            cursor.execute("select * from some_table where ROWID=1")
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i]='red'

        else:
            self.step_time += 1
            #print('第' + str(self.step_time) + '步')
            self.dll_sql = sqlite3.connect("random-network-SI.db")
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            cursor.execute("select * from some_table where ROWID=%d" % (self.step_time + 1))
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i]='red'


            print('run')
        print(node_state[0])
        print(3)

        # self.b = ['blue'] * self.n
        #self.a=[1]*self.n
        for i in range(self.n):

            self.a[i] = self.G.degree(i) * 30  # 度大小设置

        if self.flag == 0:
            self.flag = 1
            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b,node_size=self.a, ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
            nx.draw_networkx_edges(self.G, pos=self.pos_round, ax=self.axes, alpha=0.4)  # 生成边
        else:
            self.axes.hold(True)
            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b,node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
        self.flag_out = 1

        self.axes.axis('off')
        self.draw()
        self.axes.hold(False)

    def small_world_election(self, number, p, step_times, N2):
        self.mode = 8  # 网络类型
        self.n = N2  # 节点个数
        self.number1 = number  # 邻居节点数
        self.number2 = p  # 概率
        self.number5 = N2
        self.steps = step_times  # 单步博弈次数
        self.dll_21 = cdll.LoadLibrary('small-world-election.dll')
        node_change = [0] * N2
        change_flag = 0
        if self.step_time == step_times:
            self.stop_flag = 1
            return
        self.b = ['blue'] * self.n
        self.a = [1] * self.n
        print(1)
        if self.flag == 0:
            if self.flag_openFile == 0:
                self.dll_21.main(number, c_double(p), N2)  # dll初始化
                self.my_file = 'small-world-election-1.csv'
                print(2)
                self.df = pd.DataFrame(pd.read_csv(self.my_file))
            else:
                self.flag_openFile = 0
            self.G = nx.from_pandas_edgelist(self.df, edge_attr=True)  # 读取csv表格数据赋值到self.G
            self.pos_round = nx.spring_layout(self.G)  # 生成每个节点的坐标位置
            # self.flag=1
            print(3)
            self.dll_21.run_over(N2, step_times + 1)  # 执行博弈，时间步为1000
            # 获取数据，读取当前目录下的CSV文件

            print('complete')
            # 数据库
            self.dll_sql = sqlite3.connect("small-world-election.db")
            dff = pd.DataFrame(pd.read_csv('small-world-election-2.csv'))  # , sep='\t'
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            self.dll_sql.execute("delete from some_table")
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            cursor.execute("select * from some_table where ROWID=1")
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i] = 'red'

        else:
            self.step_time += 1
            #print('第' + str(self.step_time) + '步')
            self.dll_sql = sqlite3.connect("small-world-election.db")
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            cursor.execute("select * from some_table where ROWID=%d" % (self.step_time + 1))
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i] = 'red'


            print('run')
        print(node_state[0])
        print(3)

        # self.b = ['blue'] * self.n
        #self.a=[1]*self.n
        for i in range(self.n):

            self.a[i] = self.G.degree(i) * 30  # 度大小设置

        if self.flag == 0:
            self.flag = 1
            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b,node_size=self.a, ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
            nx.draw_networkx_edges(self.G, pos=self.pos_round, ax=self.axes, alpha=0.4)  # 生成边
        else:
            self.axes.hold(True)

            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b,node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
        self.flag_out = 1

        self.axes.axis('off')
        self.draw()
        self.axes.hold(False)

    def random_network_election(self, number, p, step_times, N2):
        self.mode = 18  # 网络类型
        self.n = N2  # 节点个数
        self.number1 = number  # 邻居节点数
        self.number2 = p  # 概率
        self.number5 = N2
        self.steps = step_times  # 单步博弈次数
        self.dll_21 = cdll.LoadLibrary('random-network-election.dll')
        node_change = [0] * N2
        change_flag = 0
        if self.step_time == step_times:
            self.stop_flag = 1
            return
        self.b = ['blue'] * self.n
        self.a = [1] * self.n
        print(1)
        if self.flag == 0:
            if self.flag_openFile == 0:
                self.dll_21.main(number, c_double(p), N2)  # dll初始化
                self.my_file = 'random-network-election-1.csv'
                print(2)
                self.df = pd.DataFrame(pd.read_csv(self.my_file))
            else:
                self.flag_openFile = 0
            self.G = nx.from_pandas_edgelist(self.df, edge_attr=True)  # 读取csv表格数据赋值到self.G
            self.pos_round = nx.spring_layout(self.G)  # 生成每个节点的坐标位置
            # self.flag=1
            print(3)
            self.dll_21.run_over(N2, step_times + 1)  # 执行博弈，时间步为1000
            # 获取数据，读取当前目录下的CSV文件

            print('complete')
            # 数据库
            self.dll_sql = sqlite3.connect("random-network-election.db")
            dff = pd.DataFrame(pd.read_csv('random-network-election-2.csv'))  # , sep='\t'
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            self.dll_sql.execute("delete from some_table")
            dff.to_sql('some_table', self.dll_sql, if_exists='append')  # index=False
            cursor.execute("select * from some_table where ROWID=1")
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i] = 'red'

        else:
            self.step_time += 1
            #print('第' + str(self.step_time) + '步')
            self.dll_sql = sqlite3.connect("random-network-election.db")
            cursor = self.dll_sql.cursor()  # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
            self.dll_sql.row_factory = sqlite3.Row  # 可访问列信息
            cursor.execute("select * from some_table where ROWID=%d" % (self.step_time + 1))
            node_state = cursor.fetchall()
            self.dll_sql.close()
            for i in range(self.n):

                if node_state[0][i+1] == 1:
                    self.b[i] = 'blue'
                else:
                    self.b[i] = 'red'


            print('run')
        print(node_state[0])
        print(3)

        # self.b = ['blue'] * self.n
        #self.a=[1]*self.n
        for i in range(self.n):

            self.a[i] = self.G.degree(i) * 30  # 度大小设置

        if self.flag == 0:
            self.flag = 1
            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b,node_size=self.a, ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
            nx.draw_networkx_edges(self.G, pos=self.pos_round, ax=self.axes, alpha=0.4)  # 生成边
        else:
            self.axes.hold(True)

            xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round, node_color=self.b,node_size=self.a,ax=self.axes)  # 生成节点
            xx.set_edgecolor('black')  # 设置节点边框
        self.flag_out = 1

        self.axes.axis('off')
        self.draw()
        self.axes.hold(False)

    def onClick(self, event):
        (x, y) = (event.xdata, event.ydata)
        print(x, y)
        self.click_roundchange(x, y)




    def click_roundchange(self, x, y):
        print('ready')
        # print(self.pos_round)
        if self.mode==2 or self.mode==5:
            for i in range(self.n):
                print('run-clickchange:' + str(i + 1))
                node = self.pos_round[i ]
                distance = math.sqrt(pow(x - node[0], 2) + pow(y - node[1], 2)) * 550 / 2.2  # 图坐标与像素坐标的转换
                # print(x, y)
                node_r = math.sqrt(self.a[i] / math.pi)
                # print(distance, self.a[i], node_r)
                if distance < node_r:
                    print('find')
                    # print('点坐标', node)
                    # print('与点的距离', distance)
                    # print('该点的面积')
                    # print('该点的半径', node_r)
                    # self.b[1]='red'
                    # print('change', i+1)
                    # self.b[i]='red'
                    nodd = [i]
                    self.axes.hold(True)
                    if self.b[i] == 'red':
                        self.b[i] = 'blue'
                    else:
                        self.b[i] = 'red'
                    xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round,nodelist=nodd,node_color=self.b[i],
                                                node_size=self.a[i], ax=self.axes)
                    xx.set_edgecolor('black')
                    print('complete')
                    self.axes.axis('off')
                    self.draw()
                    self.axes.hold(False)
                    break
        elif self.mode==3 or self.mode==6 or self.mode==9:
            for i in range(self.n):
                print('run-clickchange:' + str(i + 1))
                node = self.pos_round[i+1]
                distance = math.sqrt(pow(x - node[0], 2) + pow(y - node[1], 2)) * 550 / 2.2  # 图坐标与像素坐标的转换
                # print(x, y)
                node_r = math.sqrt(self.a[i] / math.pi)
                # print(distance, self.a[i], node_r)
                if distance < node_r:
                    print('find')
                    # print('点坐标', node)
                    # print('与点的距离', distance)
                    # print('该点的面积')
                    # print('该点的半径', node_r)
                    # self.b[1]='red'
                    # print('change', i+1)
                    # self.b[i]='red'
                    nodd = [i+1]
                    self.axes.hold(True)
                    if self.b[i] == 'red':
                        self.b[i] = 'blue'
                    else:
                        self.b[i] = 'red'
                    xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round,nodelist=nodd,node_color=self.b[i],
                                                node_size=self.a[i], ax=self.axes)
                    xx.set_edgecolor('black')
                    print('complete')
                    self.axes.axis('off')
                    self.draw()
                    self.axes.hold(False)
                    break

        elif self.mode==1 or self.mode==4 or self.mode==7:
            for i in range(self.M):
                print('run-clickchange:' + str(i + 1))
                node = self.pos_round[i ]
                distance = math.sqrt(pow(x - node[0], 2) + pow(y - node[1], 2)) * 550 / 2.2  # 图坐标与像素坐标的转换
                # print(x, y)
                node_r = math.sqrt(self.a[i] / math.pi)
                # print(distance, self.a[i], node_r)
                if distance < node_r:
                    print('find')
                    # print('点坐标', node)
                    # print('与点的距离', distance)
                    # print('该点的面积')
                    # print('该点的半径', node_r)
                    # self.b[1]='red'
                    # print('change', i+1)
                    # self.b[i]='red'
                    nodd = [i]
                    self.axes.hold(True)
                    if self.b[i] == 'red':
                        self.b[i] = 'blue'
                    else:
                        self.b[i] = 'red'
                    xx = nx.draw_networkx_nodes(self.G, pos=self.pos_round,nodelist=nodd,node_color=self.b[i],
                                                node_size=self.a[i], ax=self.axes,node_shape='s')
                    xx.set_edgecolor('black')
                    print('complete')
                    self.axes.axis('off')
                    self.draw()
                    self.axes.hold(False)
                    break








class MatplotlibWidget(QWidget):
    def __init__(self,parent=None):
        super(MatplotlibWidget, self).__init__(parent)
        self.initUi()


    def initUi(self):
        self.layout = QVBoxLayout(self)
        self.mpl = MyMplCanvas(self, width=7, height=10.4, dpi=100)

        self.layout.addWidget(self.mpl)







if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MatplotlibWidget()
    #ui.mpl.plotsin()

    ui.mpl.grid_snow(49,4,0.3,0.3)# 方格网
    #ui.mpl.start_world(2, 50, 1000)#小世界
    ui.show()
    #ui.mpl.start_static_plot()
    sys.exit(app.exec_())