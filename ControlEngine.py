import time
import win32gui
import pyautogui
import os

def auto_click(var_avg, t=1.0):
    pyautogui.click(var_avg[0], var_avg[1], button='left')
    if t != 0:
        time.sleep(t)
    return


def get_img_box(image, confidence=0.9, box=None):
    try:
        if box is not None:
            box = pyautogui.locateOnScreen(image, confidence, region=(box[0], box[1], box[2], box[3]))
        else:
            box = pyautogui.locateOnScreen(image, confidence)
    except Exception as e:
        print(f"图像未识别({image})", box)
        return None
    else:
        return box


def auto_click(var_avg, t=1.0):
    """自动点击指定坐标，并可选择性延迟"""
    pyautogui.click(var_avg[0], var_avg[1], button='left')
    if t != 0:
        time.sleep(t)
    return


def get_img_box(image, confidence=1.0, box=None):
    """根据图像和置信度查找屏幕上的图像位置，可指定区域"""
    try:
        if box is not None:
            box = pyautogui.locateOnScreen(image, confidence, region=(box[0], box[1], box[2], box[3]))
        else:
            box = pyautogui.locateOnScreen(image, confidence)
    except Exception as e:
        print(f"图像未识别({image})", box)
        return None
    else:
        return box





class ControlEngine:
    """控制引擎类，用于执行各种自动化操作"""

    def __init__(self):
        self.type_names = ['Begin', 'SpecialLimitedRole', 'SpecialLimitedWeapon', 'LimitedRole', 'LimitedWeapon',
                           'NormalRole', 'NormalWeapon']
        pass

    def __isHome(self):
        """判断是否在主界面"""
        if get_img_box('./template/setting.png', 0.8) is not None:
            return True
        else:
            return False

    # 前置尘白禁区窗口
    def preWindow(self):
        """前置尘白禁区窗口，将其置于前台"""
        hwnd = win32gui.FindWindow(None, "尘白禁区")
        if not hwnd:
            print("no windows")
        else:
            win32gui.SetForegroundWindow(hwnd)
        time.sleep(1)
        return

    # 回到主界面
    def goHome(self):
        """通过识别图像和按键操作返回主界面"""
        count = 1
        while True:
            count += 1
            print('正在返回主界面，第%d次尝试' % count)
            if self.__isHome():
                break

            # 键盘esc返回主界面
            pyautogui.press('esc', interval=0.1)
            time.sleep(1)
            # 判断是否是基地返回
            pos3 = get_img_box('./template/exitBase.png', box=(2000, 0, 560, 200))
            if pos3 is not None:
                auto_click(pyautogui.center(pos3))
                time.sleep(3)
            if count > 5:
                print('返回主界面失败')
                return 1
        print('返回主界面成功')
        return 0

    # (200, 260)
    # (200, 380)
    # (200, 460)
    #
    # (200, 360)
    # (200, 480)
    # (200, 560)
    def selectPool(self, name):
        """根据名称选择相应的卡池"""
        if name == self.type_names[0]:
            pass
        if name == self.type_names[1]:
            auto_click((200, 260))
            auto_click((200, 380))
        if name == self.type_names[2]:
            auto_click((200, 260))
            auto_click((200, 460))

        if name == self.type_names[3]:
            auto_click((200, 360))
            auto_click((200, 480))
        if name == self.type_names[4]:
            auto_click((200, 360))
            auto_click((200, 560))

        if name == self.type_names[5]:
            auto_click((200, 480))
        if name == self.type_names[6]:
            auto_click((200, 580))
        print("已选择", name)
        return name

    def goPoolRecord(self, name):
        """进入卡池记录界面"""
        if not self.__isHome():
            ret = self.goHome()
            if ret != 0:
                return ret
        # 点击共鸣
        auto_click([2200, 800], 1.5)
        # 选择池子
        self.selectPool(name)
        # 点击卡池介绍
        time.sleep(1)
        auto_click([2500, 190])
        # pos = get_img_box('./template/bannarparticular.png', box=(2460, 133, 100, 120))
        # if pos is not None:
        #     auto_click(pyautogui.center(pos), 1)
        #     print('点击记录')
        # else:
        #     return 1
        pos2 = get_img_box('./template/viewrecord.png', box=(1347, 72, 270, 80))
        if pos2 is not None:
            auto_click(pyautogui.center(pos2))
            print('查看记录')
        else:
            return 1
        count = 0
        while True:
            pos3 = get_img_box('./template/wp.png', box=(1157, 270, 100, 60))
            if pos3 is not None:
                print('发现武器记录')
                break
            pos4 = get_img_box('./template/role.png', box=(1157, 270, 100, 60))
            if pos4 is not None:
                print('发现角色记录')
                break
            time.sleep(0.5)
            count += 1
            if count > 20:
                print('未发现抽取记录')
                return 1
            print('等待记录更新')
        return 0

    def saveRecordImg(self, name='Default') -> int:
        """
        保存记录界面的截图，并处理翻页
        :param name: 保存的文件夹名称
        :return: 保存的截图数量
        """
        i = 1
        while i <= 20:
            cur_save_path = './pic/%s/%s_%02d.png' % (name, name, i)
            pyautogui.screenshot().save(cur_save_path)

            # 保存当前页码图片，判断是否翻页或退出
            # time.sleep(1)
            slippage_box = (2170, 642, 100, 100)
            pyautogui.screenshot('./pic/temp/cur_number_%02d.png' % i, region=slippage_box)

            # 定位向下按钮，点击翻页
            pos = get_img_box('./template/down.png', 1, (2179, 752, 86, 100))
            if pos is not None:
                auto_click(pyautogui.center(pos), 0.2)

            # 判断是否继续还是退出
            pos1 = get_img_box('./pic/temp/cur_number_%02d.png' % i, 1, (2170, 642, 100, 100))
            if pos1 is not None:
                print('共保存截图%d张，路径：./pic/%s' % (i, name))
                break
            else:
                time.sleep(0.1)
            i += 1
        # 清理临时截图按钮图片
        abspath = os.path.abspath("./pic/temp")
        dirlist = os.listdir(abspath)
        for filename in dirlist:
            print("清理临时截图按钮图片：", os.path.join(abspath, filename))
            os.remove(os.path.join(abspath, filename))
        return i

    def esc(self):
        """按下ESC键"""
        pyautogui.press('esc', 1)
        # keyboard.press(27)
        # keyboard.release(27)
        return


controlengine = ControlEngine()
