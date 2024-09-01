from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPaintEvent, QPainter, QFont, QColor
from PyQt6.QtWidgets import QWidget, QStyleOption, QStyle, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QComboBox, QListWidgetItem

from qfluentwidgets import ListWidget, PushButton, CheckBox

import Main as ma
import PoolInfo


class PoolBox(QFrame):
    name: str = 'unknown'
    name_ch: str = '未知'
    index: int = 0
    stands: list = []
    signal_update_info = pyqtSignal(int)
    def __init__(self, parent=None, text: str = 'default', index: int = 0):
        super().__init__(parent=parent)
        self.setObjectName('poolbox-' + text)

        self.name = text
        self.index = index
        self.name_ch = AppInterface.choices_zh[index]

        self.showInitInfo()
        self.updateInfo(self.index)

    def showInitInfo(self):
        print('show init info')
        self.topBoxLayout = QVBoxLayout(self)
        self.labelTitle = QLabel(self.name_ch, self)
        self.labelTitle.setObjectName('title')
        self.labelTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelTitle.setFont(QFont('微软雅黑', 17))

        self.labelTotalNum = QLabel(parent=self, objectName='total-num', text='总计抽卡数量:')
        self.labelTotalNum_value = QLabel(parent=self, objectName='total-num-value', text='0')
        self.label5Num = QLabel(parent=self, objectName='5-num', text='5星共计:')
        self.label5Num_value = QLabel(parent=self, objectName='5-num-value', text='0')
        self.label5Avg = QLabel(parent=self, objectName='5-avg', text='5星平均抽数:')
        self.label5Avg_value = QLabel(parent=self, objectName='5-avg-value', text='0')
        self.label4Num = QLabel(parent=self, objectName='4-num', text='4星共计:')
        self.label4Num_value = QLabel(parent=self, objectName='4-num-value', text='0')
        # self.label4Avg = QLabel(parent=self, objectName='4-avg', text='4星平均抽数:')
        # self.label4Avg_value = QLabel(parent=self, objectName='4-avg-value', text='0')

        self.listWidget = ListWidget(self)
        # self.listWidget = QListWidget(self)
        self.listWidget.setObjectName('stands-list')
        # self.listWidget.setFixedWidth(170)
        self.listWidget.setMinimumWidth(200)
        self.listWidget.setAlternatingRowColors(True)  # 设置交替行颜色

        # 先暂时不初始化
        # for stand in self.stands:
        #     item = QListWidgetItem(stand)
        #     item.setIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        #     # item.setIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        #     # item.setCheckState(Qt.CheckState.Unchecked)
        #     self.listWidget.addItem(item)

        self.vBoxLayout_box2_left = QVBoxLayout()
        self.vBoxLayout_box2_left.addWidget(self.labelTotalNum)
        self.vBoxLayout_box2_left.addWidget(self.label5Num)
        self.vBoxLayout_box2_left.addWidget(self.label5Avg)
        self.vBoxLayout_box2_left.addWidget(self.label4Num)
        # self.vBoxLayout_box2_left.addWidget(self.label4Avg)

        self.vBoxLayout_box2_right = QVBoxLayout()
        self.vBoxLayout_box2_right.addWidget(self.labelTotalNum_value)
        self.vBoxLayout_box2_right.addWidget(self.label5Num_value)
        self.vBoxLayout_box2_right.addWidget(self.label5Avg_value)
        self.vBoxLayout_box2_right.addWidget(self.label4Num_value)
        # self.vBoxLayout_box2_right.addWidget(self.label4Avg_value)

        self.conLayout = QHBoxLayout()
        self.conLayout.addLayout(self.vBoxLayout_box2_left)
        self.conLayout.addLayout(self.vBoxLayout_box2_right)

        # 设置整体布局
        self.topBoxLayout.addWidget(self.labelTitle)
        self.topBoxLayout.addLayout(self.conLayout)
        self.topBoxLayout.addWidget(self.listWidget)
        self.setLayout(self.topBoxLayout)

    def updateInfo(self, index: int = 0):
        # todo: 加个index的判断，确保卡池正确
        print(f'PoolBox 更新信息 index:{index}')
        info = ma.getPoolInfoByIndex(self.index)
        self.labelTotalNum_value.setText(str(info['total_num']))
        self.label5Num_value.setText(str(info['start_5_num']))
        self.label5Avg_value.setText(str(int(info['total_num'] / info['start_5_num'])))
        self.label4Num_value.setText(str(info['start_4_num']))
        # self.label4Avg_value.setText(str(int(info['total_num'] / info['start_4_num'])))
        # 更新5星记录详情
        self.updataInfoStands(info)

    def updataInfoStands(self, info: dict):
        if 'start_5_details' not in info:
            print('start_5_details not in info')
            return -1
        start5List = info['start_5_details']
        totalNum = info['total_num']
        standNames = []
        standCosts = []
        stands = []
        for index, item in enumerate(start5List):
            cost = totalNum + 1 - item[0]
            standCosts.append(cost)
            name = str(item[1]).split(',')[0]
            standNames.append(name)
            if index > 0:
                standCosts[index - 1] -= standCosts[index]
        for i in range(len(standNames)):
            stands.append(standNames[i] + ' ' + str(standCosts[i]))

        self.stands = stands
        self.listWidget.clear()
        for stand in self.stands:
            item = QListWidgetItem(stand)
            item.setForeground(QColor(233, 155, 55))
            font = QFont('楷体', 13)
            font.setBold(True)  # 设置字体加粗
            item.setFont(font)
            # item.setIcon(QIcon(':/qfluentwidgets/images/logo.png'))
            # item.setCheckState(Qt.CheckState.Unchecked)
            self.listWidget.addItem(item)
        return 1

        # 外部信号连接
    def update_info(index: int):
        self.updateInfo(index)
class SummaryBox(QFrame):
    summary_signal = pyqtSignal(list)
    update_poolbox_signal = pyqtSignal(int)
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('summarybox')
        self.setFixedWidth(220)
        self.initInfo()

    def initInfo(self):
        # 设置查询框
        self.combobox = QComboBox(self)
        self.combobox.addItems(AppInterface.choices_zh)
        self.combobox.setCurrentIndex(0)
        self.button_queryRecord = PushButton('查询记录', self)
        self.button_queryRecord.clicked.connect(self.queryRecords)
        self.selectLayout = QHBoxLayout()
        self.selectLayout.addWidget(self.combobox)
        self.selectLayout.addWidget(self.button_queryRecord)

        # 设置checkBox
        self.checkboxes = [
            CheckBox("限定角色特选", parent=self),
            CheckBox("限定武器特选", parent=self),
            CheckBox("限定角色", parent=self),
            CheckBox("限定武器", parent=self),
            CheckBox("常驻角色", parent=self),
            CheckBox("常驻武器", parent=self),
            CheckBox("新手池", parent=self)
        ]
        self.checkBox_All = CheckBox("全部", parent=self)

        # 设置初始值
        for checkbox in self.checkboxes:
            checkbox.setChecked(True)
        self.checkboxes[6].setChecked(False)  # 新手池默认不选中
        self.checkBox_All.setTristate(True)
        self.checkBox_All.setCheckState(Qt.CheckState.PartiallyChecked)

        # 连接方法
        for checkbox in self.checkboxes:
            checkbox.stateChanged.connect(self.changecheckboxstatus)
        self.checkBox_All.stateChanged.connect(self.selectAll)

        # checkbox设置布局
        self.checkboxLeftLayout = QVBoxLayout()
        self.checkboxRightLayout = QVBoxLayout()
        for i, checkbox in enumerate(self.checkboxes):
            (self.checkboxLeftLayout if i < 4 else self.checkboxRightLayout).addWidget(checkbox)
        self.checkboxRightLayout.addWidget(self.checkBox_All)
        self.checkboxLayout = QHBoxLayout()
        self.checkboxLayout.addLayout(self.checkboxLeftLayout)
        self.checkboxLayout.addLayout(self.checkboxRightLayout)

        # 设置整体布局
        self.summaryVBoxLayout = QVBoxLayout(self)
        self.summaryVBoxLayout.addLayout(self.selectLayout)
        self.summaryVBoxLayout.addLayout(self.checkboxLayout)
        self.setLayout(self.summaryVBoxLayout)

    def selectAll(self, state):
        print(f"selectAll: {state}")
        if state == 2:
            for checkbox in self.checkboxes:
                checkbox.blockSignals(True)
                checkbox.setChecked(True)
                checkbox.blockSignals(False)
        elif state == 0:
            for checkbox in self.checkboxes:
                checkbox.blockSignals(True)
                checkbox.setChecked(False)
                checkbox.blockSignals(False)
        self.send_checked_list()

    def changecheckboxstatus(self, index):
        print(f"checkSelectAll: {index}")
        # 检查是否所有复选框都被选中
        allChecked = all(checkbox.isChecked() for checkbox in self.checkboxes)
        anyChecked = any(checkbox.isChecked() for checkbox in self.checkboxes)
        self.checkBox_All.blockSignals(True)
        if allChecked:
            self.checkBox_All.setCheckState(Qt.CheckState.Checked)
        elif anyChecked:
            self.checkBox_All.setCheckState(Qt.CheckState.PartiallyChecked)
        else:
            self.checkBox_All.setCheckState(Qt.CheckState.Unchecked)
        self.checkBox_All.blockSignals(False)
        self.send_checked_list()

    def queryRecords(self):
        curType = self.combobox.currentText()
        print('query record:' + curType)
        index = ma.PoolType.get_index_by_zh_name(curType)
        print(f'index:{index}')
        if index is None:
            print("未找到对应记录类型 Type: %s" % curType)
            return

        print(f"开始查询({index})的记录")
        ret = ma.generateRecordByEnType(ma.type_names[index])
        if ret != 0:
            print(f"查询失败ret:{ret}")
            return
        print(f"查询{AppInterface.choices_en[index]}的记录成功")
        self.update_poolbox_signal.emit(index)

    def send_checked_list(self):
        checked_list = []
        for checkbox in self.checkboxes:
            checked_list.append((checkbox.text(), int(checkbox.isChecked())))
        self.summary_signal.emit(checked_list)


# 定义一个抽卡详情界面
class AppInterface(QFrame):
    spr: PoolInfo = None
    choices_zh = ["限定角色特选", "限定武器特选", "限定角色", "限定武器", "常驻角色", "常驻武器", "新手池"]
    choices_en = ['SpecialLimitedRole', 'SpecialLimitedWeapon', 'LimitedRole', 'LimitedWeapon', 'NormalRole', 'NormalWeapon', 'Begin']
    poolboxlist = []

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('app-interface')
        self.all_h_layout = QHBoxLayout(self)
        self.all_h_layout.setContentsMargins(20, 20, 20, 20)
        self.all_h_layout.setSpacing(20)
        self.all_h_layout.setObjectName("all_h_layout")

        self.summaryInit(text)
        self.poolInit(text)
        # 设置样式
        with open('style.qss', 'r', encoding='utf-8') as f:
            style = f.read()
            print(style)
            self.setStyleSheet(style)
        # self.setStyleSheet('border: 10px solid #000000;')

    def summaryInit(self, text: str):
        self.summaryBox = SummaryBox(self)
        self.all_h_layout.addWidget(self.summaryBox)
        self.summaryBox.summary_signal.connect(self.showorhidePoolBox)
        self.summaryBox.update_poolbox_signal.connect(self.updatePoolInfo)

    def poolInit(self, text: str):
        for index, item in enumerate(self.choices_en):
            poolBox = PoolBox(self, item, index)
            # poolbox.setStyleSheet('border: 1px solid #EDEDED;')
            self.poolboxlist.append(poolBox)
            print(f"pool_init: {item}")
            self.all_h_layout.addWidget(self.poolboxlist[index])
            if item == 'Begin':
                self.poolboxlist[index].hide()
            # self.all_h_layout.addLayout(box.conLayout)

    def updatePoolInfo(self, index: int = 0):
        print(f'App更新记录信息 index:{index}')
        self.poolboxlist[index].updateInfo(index)

    def showorhidePoolBox(self, checked_list: list):
        print(f"print_signal: {checked_list}")
        # 显示隐藏对应poolbox
        for index, item in enumerate(self.choices_zh):
            for index_c, item_c in enumerate(checked_list):
                if item == item_c[0]:
                    if item_c[1] == 1:
                        print(f"显示{index}de {item}的记录")
                        self.poolboxlist[index_c].show()
                    else:
                        print(f"隐藏{index}de {item}的记录")
                        self.poolboxlist[index_c].hide()
                    break
