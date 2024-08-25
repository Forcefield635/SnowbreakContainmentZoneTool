# coding:utf-8
import sys

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QIcon, QDesktopServices
from PyQt6.QtWidgets import QApplication, QFrame, QHBoxLayout, QPushButton, QWidget, QVBoxLayout, QComboBox, QLabel
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, MSFluentWindow,
                            NavigationAvatarWidget, qrouter, SubtitleLabel, setFont, PushButton, DisplayLabel)
from qfluentwidgets import FluentIcon as FIF
import Main as ma
import PoolInfo


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

class PoolBox(QWidget):
    name: str = 'unknown'
    name_ch: str = '未知'
    index: int = 0
    def __init__(self, parent=None, text: str = 'default', index: int = 0):
        super().__init__(parent=parent)

        self.name = text
        self.index = index
        self.name_ch = ma.type_names_ch[index]
        self.setObjectName('obj-'+text)
        self.showInitInfo()
        for i in range(0, 6):
            self.updateInfo(i)

    def showInitInfo(self):
        print('show init info')
        self.topBoxLayout = QVBoxLayout(self)
        self.labelTitle = QLabel(self.name_ch, self)
        self.labelTitle.setObjectName('title')

        self.labelTotalNum = QLabel(parent=self, objectName='total-num', text='总计抽卡数量:')
        self.labelTotalNum_value = QLabel(parent=self, objectName='total-num-value', text='0')
        self.label5Num = QLabel(parent=self, objectName='5-num', text='5星数量:')
        self.label5Num_value = QLabel(parent=self, objectName='5-num-value', text='0')
        self.label5Avg = QLabel(parent=self, objectName='5-avg', text='5星平均:')
        self.label5Avg_value = QLabel(parent=self, objectName='5-avg-value', text='0')
        self.label4Num = QLabel(parent=self, objectName='4-num', text='4星数量:')
        self.label4Num_value = QLabel(parent=self, objectName='4-num-value', text='0')
        self.label4Avg = QLabel(parent=self, objectName='4-avg', text='4星平均:')
        self.label4Avg_value = QLabel(parent=self, objectName='4-avg-value', text='0')

        self.listlist = QLabel(parent=self, objectName='listlist', text='列表列表:'+self.name)

        self.vBoxLayout_box2_left = QVBoxLayout()
        self.vBoxLayout_box2_left.addWidget(self.labelTotalNum)
        self.vBoxLayout_box2_left.addWidget(self.label5Num)
        self.vBoxLayout_box2_left.addWidget(self.label5Avg)
        self.vBoxLayout_box2_left.addWidget(self.label4Num)
        self.vBoxLayout_box2_left.addWidget(self.label4Avg)

        self.vBoxLayout_box2_right = QVBoxLayout()
        self.vBoxLayout_box2_right.addWidget(self.labelTotalNum_value)
        self.vBoxLayout_box2_right.addWidget(self.label5Num_value)
        self.vBoxLayout_box2_right.addWidget(self.label5Avg_value)
        self.vBoxLayout_box2_right.addWidget(self.label4Num_value)
        self.vBoxLayout_box2_right.addWidget(self.label4Avg_value)

        self.conLayout = QHBoxLayout()
        self.conLayout.addLayout(self.vBoxLayout_box2_left)
        self.conLayout.addLayout(self.vBoxLayout_box2_right)

        # 设置整体布局
        self.topBoxLayout.addWidget(self.labelTitle)
        self.topBoxLayout.addLayout(self.conLayout)
        self.topBoxLayout.addWidget(self.listlist)
        self.setLayout(self.topBoxLayout)


    def updateInfo(self, index: int = 0):
        print(f'update info index:{index}')
        info = ma.getPoolInfoByIndex(self.index)
        self.labelTotalNum_value.setText(str(info['total_num']))
        self.label5Num_value.setText(str(info['start_5_num']))
        self.label5Avg_value.setText(str(int(info['total_num']/info['start_5_num'])))
        self.label4Num_value.setText(str(info['start_4_num']))
        self.label4Avg_value.setText(str(int(info['total_num']/info['start_4_num'])))


# 定义一个抽卡详情界面
class AppInterface(QFrame):
    spr: PoolInfo = None
    choices_zh = ["新手池", "限定角色特选", "限定武器特选", "限定角色", "限定武器", "常驻角色", "常驻武器"]
    choices_en = ['Begin', 'SpecialLimitedRole', 'SpecialLimitedWeapon', 'LimitedRole', 'LimitedWeapon', 'NormalRole', 'NormalWeapon']
    poolboxlist = []
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('app-interface')
        self.all_h_layout = QHBoxLayout(self)
        self.all_h_layout.setContentsMargins(20, 20, 20, 20)
        self.all_h_layout.setSpacing(20)
        self.all_h_layout.setObjectName("all_h_layout")

        self.commoninit(text)
        self.poolinit(text)


    def commoninit(self, text: str):

        self.combobox = QComboBox(self)
        self.combobox.addItems(self.choices_zh)

        self.button_queryRecord = PushButton('查询记录', self)
        self.button_queryRecord.clicked.connect(self.queryRecords)
        self.button_exportRecord = PushButton('导出记录', self)
        self.button_exportRecord.clicked.connect(lambda: testPrint('导出记录'))

        self.hBoxLayout_button = QHBoxLayout(self)
        self.hBoxLayout_button.addWidget(self.combobox)
        self.hBoxLayout_button.addWidget(self.button_queryRecord)
        self.hBoxLayout_button.addWidget(self.button_exportRecord)

        self.all_h_layout.addLayout(self.hBoxLayout_button)


    def poolinit(self, text: str):
        for index, item in enumerate(self.choices_en):
            poolbox = PoolBox(self, item, index)
            self.poolboxlist.append(poolbox)
            print(f"pool_init: {item}")
            self.all_h_layout.addWidget(self.poolboxlist[index])
            # self.all_h_layout.addLayout(box.conLayout)



    def queryRecords(self):
        curType = self.combobox.currentText()
        print('query record:' + curType)

        for index, item in enumerate(self.choices_zh):
            if curType == item:
                break
        else:
            print("未找到对应记录类型 " + curType)
            return
        print(f"开始查询{self.choices_en[index]}的记录")
        ret = ma.generateRecordByType(ma.type_names[index])
        if ret != 0:
            print("查询失败")
            return
        print(f"查询{self.choices_en[index]}的记录成功")
        self.updateInfo(index)


    def updateInfo(self, index: int = 0):
        print(f'update info index:{index}')
        self.poolboxlist[index].updateInfo(index)


def testPrint(str):
    print('test print:' + str)


class HomeInterface(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('home-interface')
        self.label = SubtitleLabel('Home Interface', self)
        self.button = PushButton('测试按钮', self)
        self.button.clicked.connect(testButtonClicked)
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.addWidget(self.label)
        self.vBoxLayout.addWidget(self.button)


# 主窗口类，继承自MSFluentWindow
class Window(MSFluentWindow):

    def __init__(self):
        super().__init__()

        # create sub interface
        # self.homeInterface = HomeInterface('主页 Interface', self)
        self.appInterface = AppInterface('抽卡详情 Interface', self)
        self.videoInterface = Widget('没啥用 Interface', self)
        self.settingInterface = Widget('设置 Interface', self)

        self.initNavigation()
        self.initWindow()

    # 初始化导航栏
    def initNavigation(self):
        # self.addSubInterface(self.homeInterface, FIF.HOME, '主页', FIF.HOME_FILL)
        self.addSubInterface(self.appInterface, FIF.CALENDAR, '记录')
        self.addSubInterface(self.videoInterface, FIF.VIDEO, '不知道干啥')

        self.addSubInterface(self.settingInterface, FIF.SETTING, '设置', FIF.SETTING, NavigationItemPosition.BOTTOM)

    # 初始化窗口设置
    def initWindow(self):
        self.resize(900, 700)
        # self.setWindowIcon(QIcon(':/src/无能力者娜娜右.png'))
        self.setWindowTitle('SFWidgets Demo')

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    # 测试按钮点击事件处理函数


def testButtonClicked(self):
    print('test button clicked')
    pass


if __name__ == '__main__':
    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()
