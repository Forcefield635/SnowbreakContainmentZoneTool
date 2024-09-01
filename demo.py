# coding:utf-8
import sys

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QIcon, QDesktopServices, QFont, QColor, QPaintEvent, QPainter
from PyQt6.QtWidgets import QApplication, QFrame, QHBoxLayout, QPushButton, QWidget, QVBoxLayout, QComboBox, QLabel, QListWidgetItem, QStyleOption, QStyle, QListWidget

from AppInterface import AppInterface
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, MSFluentWindow,
                            NavigationAvatarWidget, qrouter, SubtitleLabel, setFont, PushButton, DisplayLabel, ListWidget)
from qfluentwidgets import FluentIcon as FIF



# 定义一个简单的QFrame子类，用于显示文本
class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))



def testPrint(str):
    print('test print:' + str)



# 主窗口类，继承自MSFluentWindow
class Window(MSFluentWindow):

    def __init__(self):
        super().__init__()

        # create sub interface
        self.appInterface = AppInterface('抽卡详情 Interface', self)
        # self.videoInterface = Widget('没啥用 Interface', self)
        self.settingInterface = Widget('设置 Interface', self)

        self.initNavigation()
        self.initWindow()

    # 初始化导航栏
    def initNavigation(self):
        self.addSubInterface(self.appInterface, FIF.CALENDAR, '记录')
        # self.addSubInterface(self.videoInterface, FIF.VIDEO, '不知道干啥')

        self.addSubInterface(self.settingInterface, FIF.SETTING, '设置', FIF.SETTING, NavigationItemPosition.BOTTOM)

    # 初始化窗口设置
    def initWindow(self):
        self.resize(900, 700)
        # self.setWindowIcon(QIcon(':/src/无能力者娜娜右.png'))
        self.setWindowTitle('SFWidgets Demo')

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(500, 500)




if __name__ == '__main__':
    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()
