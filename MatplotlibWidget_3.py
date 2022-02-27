import sys
import matplotlib
matplotlib.use("Qt5Agg")
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QSizePolicy, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
class MyFigure1(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        plt.rcParams['font.family'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        self.F1 = Figure(figsize=(width, height), dpi=100)
        #self.F.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)
        self.axes = self.F1.add_subplot(111)
        #self.axes1 = self.fig.add_subplot(2, 1, 2)
        self.axes.hold(False)

        FigureCanvas.__init__(self, self.F1)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plotcos(self):
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2 * np.pi * t)
        self.F1.axes.plot(t, s)
        self.gridlayout = QGridLayout(self.widget_3)  # 继承容器widget
        # 在布局中添加F这个实例
        self.gridlayout.addWidget(self.F1)

