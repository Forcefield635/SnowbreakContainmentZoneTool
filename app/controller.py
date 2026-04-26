import time
import win32gui
import pyautogui
import os

from app.types import PoolType


def auto_click(var_avg, t=1.0, isdouble=False):
    if isdouble:
        pyautogui.doubleClick(var_avg[0], var_avg[1], button='left')
    else:
        pyautogui.click(var_avg[0], var_avg[1], button='left')
    if t != 0:
        time.sleep(t)


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


class ControlEngine:
    def __init__(self):
        self.type_names = ['Begin', 'SpecialLimitedRole', 'SpecialLimitedWeapon', 'LimitedRole', 'LimitedWeapon',
                           'NormalRole', 'NormalWeapon']

    def __isHome(self):
        if get_img_box('./resources/template/setting.png', 0.8) is not None:
            return True
        else:
            return False

    def preWindow(self):
        hwnd = win32gui.FindWindow(None, "尘白禁区")
        if not hwnd:
            print("未识别到尘白禁区窗口")
            return -1
        else:
            win32gui.SetForegroundWindow(hwnd)
        time.sleep(1)
        return 0

    def goHome(self):
        count = 1
        while True:
            count += 1
            print('正在返回主界面，第%d次尝试' % count)
            if self.__isHome():
                break
            pyautogui.press('esc', interval=0.1)
            time.sleep(1)
            pos3 = get_img_box('./resources/template/exitBase.png', box=(2000, 0, 560, 200))
            if pos3 is not None:
                auto_click(pyautogui.center(pos3))
                time.sleep(3)
            if count > 5:
                print('返回主界面失败')
                return 1
        print('返回主界面成功')
        return 0

    def selectPool(self, name, BGFlag=True):
        if not self.__isHome():
            return 1
        auto_click([2200, 800], 2, isdouble=True)
        pos = get_img_box('./resources/template/pool_store.png')
        if pos is None:
            print('未进入卡池商店')
            return 2
        if BGFlag:
            add_pos = 100
        else:
            add_pos = 0
        pool_click_positions = {
            PoolType.BG.en_name: [(200, 60 + add_pos), (200, 60 + add_pos)],
            PoolType.SLR.en_name: [(200, 160 + add_pos), (200, 280 + add_pos)],
            PoolType.SLW.en_name: [(200, 160 + add_pos), (200, 360 + add_pos)],
            PoolType.LR.en_name: [(200, 260 + add_pos), (200, 380 + add_pos)],
            PoolType.LW.en_name: [(200, 260 + add_pos), (200, 460 + add_pos)],
            PoolType.NR.en_name: [(200, 360 + add_pos), (200, 360 + add_pos)],
            PoolType.NW.en_name: [(200, 460 + add_pos), (200, 460 + add_pos)]
        }
        if name in pool_click_positions:
            for pos in pool_click_positions[name]:
                auto_click(pos, 2)
        else:
            print(f"未知的卡池名称: {name}")
            return 1
        print(f"已点击卡池名称: {name}")
        return 0

    def goPoolRecord(self, name):
        if not self.__isHome():
            ret = self.goHome()
            if ret != 0:
                return ret
        ret = self.selectPool(name)
        if ret != 0:
            print(f'选择卡池失败{name}')
            return ret
        auto_click([2500, 190], 2, isdouble=True)
        pos2 = get_img_box('./resources/template/viewrecord.png', box=(1347, 72, 270, 80))
        if pos2 is not None:
            auto_click(pyautogui.center(pos2), 2, isdouble=True)
            print('点击查看记录')
        else:
            return 1
        count = 0
        while True:
            pos3 = get_img_box('./resources/template/wp.png', box=(1157, 270, 100, 60))
            if pos3 is not None:
                print('发现武器记录')
                break
            pos4 = get_img_box('./resources/template/role.png', box=(1157, 270, 100, 60))
            if pos4 is not None:
                print('发现角色记录')
                break
            time.sleep(0.5)
            count += 1
            if count > 10:
                print('未发现抽取记录')
                return 2
            print('等待记录更新')
        return 0

    def saveRecordImg(self, name='Default') -> int:
        i = 1
        while i <= 20:
            cur_save_path = './pic/%s/%s_%02d.png' % (name, name, i)
            pyautogui.screenshot().save(cur_save_path)
            slippage_box = (2170, 642, 100, 100)
            pyautogui.screenshot('./pic/temp/cur_number_%02d.png' % i, region=slippage_box)
            pos = get_img_box('./resources/template/down3.png', 0.8, (2179, 752, 100, 150))
            if pos is not None:
                auto_click(pyautogui.center(pos), 0.2)
            pos1 = get_img_box('./pic/temp/cur_number_%02d.png' % i, 1, (2170, 642, 100, 100))
            if pos1 is not None:
                print('共保存截图%d张，路径：./pic/%s' % (i, name))
                break
            else:
                time.sleep(0.1)
            i += 1
        abspath = os.path.abspath("./pic/temp")
        dirlist = os.listdir(abspath)
        for filename in dirlist:
            print("清理临时截图按钮图片：", os.path.join(abspath, filename))
            os.remove(os.path.join(abspath, filename))
        return i

    def esc(self):
        pyautogui.press('esc', 1)


controlengine = ControlEngine()
