import sys
from typing import Optional

from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtWidgets import QApplication, QFrame, QHBoxLayout, QWidget
from qfluentwidgets import (
    NavigationItemPosition, MSFluentWindow, SubtitleLabel, setFont,
    NavigationAvatarWidget, qrouter, setTheme, Theme,  # 实际需要保留的qfluentwidgets组件
    FluentIcon as FIF
)

from AppInterface import AppInterface  # 假设这是自定义模块

# 常量定义
WINDOW_TITLE = "SFWidgets Demo"
INITIAL_SIZE = (900, 700)
POSITION_OFFSET = (500, 500)


class BaseWidget(QFrame):
    """基础带标题的展示组件"""

    def __init__(self, text: str, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self._init_ui(text)
        self._setup_layout()

    def _init_ui(self, text: str) -> None:
        """初始化界面元素"""
        self.label = SubtitleLabel(text, self)
        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))

    def _setup_layout(self) -> None:
        """配置布局管理器"""
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)


class MainWindow(MSFluentWindow):
    """应用程序主窗口"""

    def __init__(self):
        super().__init__()
        self._init_interfaces()
        self._init_navigation()
        self._configure_window()

    def _init_interfaces(self) -> None:
        """初始化子界面"""
        self.app_interface = AppInterface('抽卡详情 Interface', self)
        self.settings_interface = BaseWidget('设置 Interface', self)

    def _init_navigation(self) -> None:
        """初始化导航栏"""
        navigation_items = [
            (self.app_interface, FIF.CALENDAR, '记录'),
            (self.settings_interface, FIF.SETTING, '设置', FIF.SETTING, NavigationItemPosition.BOTTOM)
        ]

        for item in navigation_items:
            if len(item) == 3:
                self.addSubInterface(*item)
            else:
                self.addSubInterface(*item[:-1], position=item[-1])

    def _configure_window(self) -> None:
        """配置窗口属性"""
        self.setWindowTitle(WINDOW_TITLE)
        self.resize(*INITIAL_SIZE)

        # 设置窗口图标（需要确保资源存在）
        # self.setWindowIcon(QIcon(':/src/无能力者娜娜右.png'))

        # 居中显示窗口
        self._center_window()

    def _center_window(self) -> None:
        """将窗口居中显示"""
        screen_geometry = QGuiApplication.primaryScreen().availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)


def main() -> None:
    """应用程序入口点"""
    # 启用暗黑主题（按需开启）
    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()