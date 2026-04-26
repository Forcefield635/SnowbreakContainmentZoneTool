import sys
from typing import Optional

from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtWidgets import QApplication, QFrame, QHBoxLayout, QWidget
from qfluentwidgets import (
    NavigationItemPosition, MSFluentWindow, SubtitleLabel, setFont,
    NavigationAvatarWidget, qrouter, setTheme, Theme,
    FluentIcon as FIF
)

from app.interface import AppInterface

WINDOW_TITLE = "SFWidgets Demo"
INITIAL_SIZE = (900, 700)
POSITION_OFFSET = (500, 500)


class BaseWidget(QFrame):
    def __init__(self, text: str, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self._init_ui(text)
        self._setup_layout()

    def _init_ui(self, text: str) -> None:
        self.label = SubtitleLabel(text, self)
        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))

    def _setup_layout(self) -> None:
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)


class MainWindow(MSFluentWindow):
    def __init__(self):
        super().__init__()
        self._init_interfaces()
        self._init_navigation()
        self._configure_window()

    def _init_interfaces(self) -> None:
        self.app_interface = AppInterface('抽卡详情 Interface', self)
        self.settings_interface = BaseWidget('设置 Interface', self)

    def _init_navigation(self) -> None:
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
        self.setWindowTitle(WINDOW_TITLE)
        self.resize(*INITIAL_SIZE)
        self._center_window()

    def _center_window(self) -> None:
        screen_geometry = QGuiApplication.primaryScreen().availableGeometry()
        x = (screen_geometry.width() - self.width()) // 3
        y = (screen_geometry.height() - self.height()) // 3
        self.move(x, y)


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
