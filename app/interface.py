import os
from typing import Dict, List, Optional, Tuple
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QListWidgetItem, QComboBox

from qfluentwidgets import ListWidget, PushButton, CheckBox

import app.pipeline as pl
import app.pool_info
from app.types import PoolType, type_names, type_names_zh


class PoolBox(QFrame):
    POOL_THRESHOLDS = {
        0: 100,
        1: 80,
        2: 80,
        3: 60,
        4: 80,
        5: 60,
        6: 50
    }
    signal_update_info = pyqtSignal(int)

    def __init__(self, parent=None, text: str = 'default', index: int = 0):
        super().__init__(parent=parent)
        self.setObjectName('poolbox-' + text)
        self.name = text
        self.index = index
        self.name_ch = AppInterface.choices_zh[index]
        self.showInitInfo()
        self.updateInfo_start(self.index)

    def showInitInfo(self):
        print('show init info')
        self.labelTitle = QLabel(self.name_ch, self)
        self.labelTitle.setObjectName('title')
        self.labelTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelTitle.setFont(QFont('微软雅黑', 17))
        self.labelTotalNum = QLabel(parent=self, objectName='total-num', text='总计抽卡数量:')
        self.labelTotalNum_value = QLabel(parent=self, objectName='total-num-value', text='0')
        self.labelAlreadyNum = QLabel(parent=self, objectName='already-num', text='已垫抽卡数量:')
        self.labelAlreadyNum_value = QLabel(parent=self, objectName='already-num-value', text='0')
        self.label5Num = QLabel(parent=self, objectName='5-num', text='5星共计:')
        self.label5Num_value = QLabel(parent=self, objectName='5-num-value', text='0')
        self.label5Avg = QLabel(parent=self, objectName='5-avg', text='5星平均抽数:')
        self.label5Avg_value = QLabel(parent=self, objectName='5-avg-value', text='0')
        self.label4Num = QLabel(parent=self, objectName='4-num', text='4星共计:')
        self.label4Num_value = QLabel(parent=self, objectName='4-num-value', text='0')
        self.vBoxLayout_box2_left = QVBoxLayout()
        self.vBoxLayout_box2_left.addWidget(self.labelTotalNum)
        self.vBoxLayout_box2_left.addWidget(self.labelAlreadyNum)
        self.vBoxLayout_box2_left.addWidget(self.label5Num)
        self.vBoxLayout_box2_left.addWidget(self.label5Avg)
        self.vBoxLayout_box2_left.addWidget(self.label4Num)
        self.vBoxLayout_box2_right = QVBoxLayout()
        self.vBoxLayout_box2_right.addWidget(self.labelTotalNum_value)
        self.vBoxLayout_box2_right.addWidget(self.labelAlreadyNum_value)
        self.vBoxLayout_box2_right.addWidget(self.label5Num_value)
        self.vBoxLayout_box2_right.addWidget(self.label5Avg_value)
        self.vBoxLayout_box2_right.addWidget(self.label4Num_value)
        self.conLayout = QHBoxLayout()
        self.conLayout.addLayout(self.vBoxLayout_box2_left)
        self.conLayout.addLayout(self.vBoxLayout_box2_right)
        self.listWidget = ListWidget(self)
        self.listWidget.setObjectName('stands-list')
        self.listWidget.setMinimumWidth(200)
        self.listWidget.setAlternatingRowColors(True)
        self.topBoxLayout = QVBoxLayout(self)
        self.topBoxLayout.addWidget(self.labelTitle)
        self.topBoxLayout.addLayout(self.conLayout)
        self.topBoxLayout.addWidget(self.listWidget)
        self.setLayout(self.topBoxLayout)

    def updateInfo_start(self, index: int = 0):
        print(f"updatePoolInfo_start: {index}")
        self.updataBoxThd = UpdataBoxThread(pool=self)
        self.updataBoxThd.t_finished.connect(self.updateInfo_finish)
        self.updataBoxThd.start()
        print(f"开始更新卡池{index}的信息")

    def updateInfo_finish(self, ret: int):
        self.updataBoxThd.deleteLater()
        if ret != 0:
            print(f"更新失败 ret:{ret}")
            return -1
        print(f"更新成功")
        return 0

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
            font.setBold(True)
            item.setFont(font)
            self.listWidget.addItem(item)
        return 1


class QueryBoxThread(QThread):
    t_finished = pyqtSignal(int)
    boxtype = "默认"
    query_type = 1

    def __init__(self, parent=None, boxtype="默认", query_type=1):
        super().__init__(parent=parent)
        self.boxtype = boxtype
        self.query_type = query_type

    def run(self):
        print(f'QueryBox线程 开始执行Type:{self.boxtype} 查询方式：{self.query_type}')
        index = PoolType.get_index_by_zh_name(self.boxtype)
        if index is None:
            print(f"未找到对应记录类型 Type: {self.boxtype}")
            self.t_finished.emit(-1)
            return
        print(f"QueryBox线程 开始查询({type_names[index]})的记录")
        if self.query_type == 1:
            ret = pl.generateRecordByEnType(type_names[index])
        elif self.query_type == 0:
            ret = pl.generateRecordDict(type_names[index])
        else:
            print(f"QueryBox线程 未知查询方式 {self.query_type}")
            ret = -1
        if ret != 0:
            print(f"QueryBox线程 查询({type_names[index]})抽卡记录失败 ret:{ret}")
            self.t_finished.emit(ret)
            return
        print(f"QueryBox线程 ({type_names[index]})查询成功")
        self.t_finished.emit(ret)


class UpdataBoxThread(QThread):
    t_finished = pyqtSignal(int)

    def __init__(self, parent=None, pool: PoolBox = None):
        super().__init__(parent=parent)
        self.pool = pool

    def run(self):
        if self.pool is None:
            print(f"UpdataBox线程 卡池为空")
            self.t_finished.emit(-1)
            return
        pool = self.pool
        print(f'UpdataBox线程 开始执行 index:{pool.index}')
        info = pl.getPoolInfoByIndex(pool.index)
        if info is None:
            print(f"PoolBox 更新卡池信息失败 index:{pool.index}")
            self.t_finished.emit(-2)
            return
        pool.labelTotalNum_value.setText(str(info['total_num']))
        self.setAlreadyDrawnNum(pool, info['already_drawn_num'], pool.index)
        pool.label5Num_value.setText(str(info['start_5_num']))
        if info['start_5_num'] != 0:
            pool.label5Avg_value.setText(str(int(info['total_num'] / info['start_5_num'])))
        pool.label4Num_value.setText(str(info['start_4_num']))
        pool.updataInfoStands(info)
        self.t_finished.emit(0)

    def setAlreadyDrawnNum(self, pool: PoolBox, num: int, index: int):
        thresholds = {0: "/100", 1: "/80", 2: "/80", 3: "/60", 4: "/80", 5: "/60", 6: "/50"}
        suffix = thresholds.get(index, "")
        pool.labelAlreadyNum_value.setText(str(num) + suffix)
        return 0


class SummaryBox(QFrame):
    summary_signal = pyqtSignal(list)
    update_poolbox_signal = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.queryBoxThd = None
        self.setObjectName('summarybox')
        self.setFixedWidth(220)
        self.initInfo()

    def initInfo(self):
        self.combobox = QComboBox(self)
        self.combobox.addItems(AppInterface.choices_zh)
        self.combobox.setCurrentIndex(0)
        self.button_queryRecord = PushButton('查询记录', self)
        self.button_queryRecord.clicked.connect(self.queryRecords_start)
        self.checkbox_query_type = CheckBox("查询方式", parent=self)
        self.checkbox_query_type.setChecked(False)
        self.selectLayout = QHBoxLayout()
        self.selectLayout.addWidget(self.combobox)
        self.selectLayout.addWidget(self.button_queryRecord)
        self.selectLayout.addWidget(self.checkbox_query_type)
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
        for checkbox in self.checkboxes:
            checkbox.setChecked(True)
        self.checkboxes[6].setChecked(False)
        self.checkBox_All.setTristate(True)
        self.checkBox_All.setCheckState(Qt.CheckState.PartiallyChecked)
        for checkbox in self.checkboxes:
            checkbox.stateChanged.connect(self.changecheckboxstatus)
        self.checkBox_All.stateChanged.connect(self.selectAll)
        self.checkboxLeftLayout = QVBoxLayout()
        self.checkboxRightLayout = QVBoxLayout()
        for i, checkbox in enumerate(self.checkboxes):
            (self.checkboxLeftLayout if i < 4 else self.checkboxRightLayout).addWidget(checkbox)
        self.checkboxRightLayout.addWidget(self.checkBox_All)
        self.checkboxLayout = QHBoxLayout()
        self.checkboxLayout.addLayout(self.checkboxLeftLayout)
        self.checkboxLayout.addLayout(self.checkboxRightLayout)
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

    def send_checked_list(self):
        checked_list = []
        for checkbox in self.checkboxes:
            checked_list.append((checkbox.text(), int(checkbox.isChecked())))
        self.summary_signal.emit(checked_list)

    def queryRecords_start(self):
        curType = self.combobox.currentText()
        print('query record:' + curType)
        self.button_queryRecord.setEnabled(False)
        self.queryBoxThd = QueryBoxThread(boxtype=curType, query_type=int(self.checkbox_query_type.isChecked()))
        self.queryBoxThd.t_finished.connect(self.queryRecords_finish)
        self.queryBoxThd.start()
        print(f"开始查询{curType}的记录")

    def queryRecords_finish(self, ret: int):
        self.button_queryRecord.setEnabled(True)
        self.queryBoxThd.deleteLater()
        if ret != 0:
            print(f"查询失败 ret:{ret}")
            return -1
        print(f"queryRecords_finish 查询成功")
        index = PoolType.get_index_by_zh_name(self.combobox.currentText())
        print(f"发送信号给 AppInterface的更新方法 index:{index}")
        self.update_poolbox_signal.emit(index)
        return 0


class AppInterface(QFrame):
    spr: app.pool_info.PoolInfo = None
    choices_zh = type_names_zh
    choices_en = type_names
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
        qss_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'style.qss')
        with open(qss_path, 'r', encoding='utf-8') as f:
            style = f.read()
            print(style)
            self.setStyleSheet(style)

    def summaryInit(self, text: str):
        self.summaryBox = SummaryBox(self)
        self.all_h_layout.addWidget(self.summaryBox)
        self.summaryBox.summary_signal.connect(self.showorhidePoolBox)
        self.summaryBox.update_poolbox_signal.connect(self.updateAppPoolInfo)

    def poolInit(self, text: str):
        for index, item in enumerate(self.choices_en):
            poolBox = PoolBox(self, item, index)
            self.poolboxlist.append(poolBox)
            print(f"pool_init: {item}")
            self.all_h_layout.addWidget(self.poolboxlist[index])
            if item == 'Begin':
                self.poolboxlist[index].hide()

    def updateAppPoolInfo(self, index: int = 0):
        print(f'App更新记录信息 index:{index}')
        self.poolboxlist[index].updateInfo_start(index)

    def showorhidePoolBox(self, checked_list: list):
        print(f"print_signal: {checked_list}")
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
