"""
抽卡记录统计
1、操作截图类，生成截图
2、图形处理类：处理图像，生产数据
3、数据处理类，计算数据，
4、绘图统计
"""
import os
import shutil
import time

import cv2

from ControlEngine import controlengine
from ImgHandler import imghandler
from Record import *

type_names = ['Begin', 'SpecialLimitedRole', 'SpecialLimitedWeapon', 'LimitedRole', 'LimitedWeapon', 'NormalRole',
              'NormalWeapon']
type_names_ch = ["新手池", "限定角色不歪池", "限定武器不歪池", "限定角色池", "限定武器池", "常驻角色池", "常驻武器池"]


g_backup_flag: bool = False  # 是否备份文件

def cleanfiles(path):
    """清理文件"""
    if not os.path.exists(path):
        os.makedirs(path)
    filenum = 0
    dirnum = 0
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            filenum += 1
            os.remove(os.path.join(root, name))
        for name in dirs:
            dirnum += 1
            os.rmdir(os.path.join(root, name))
    print(f"清理{path}，共清理{filenum}个文件，{dirnum}个文件夹。")


def generateRecordByType(name):
    """
    获取并更新保存指定类型抽卡记录
    :param name: 类型名称 type_names[index]
    :return:
    """

    # 入参校验
    for index in range(len(type_names)):
        if name == type_names[index] or name == type_names_ch[index]:
            name = type_names[index]
            break
    else:
        print("未找到对应记录类型" + name)
        return 1

    # 前置窗口
    controlengine.preWindow()

    # 进入抽卡记录界面
    for i in range(3):
        ret = controlengine.goPoolRecord(name)
        if ret == 0:
            print(f"进入抽卡记录界面")
            break
        elif ret == 1:
            print(f"第{i+1}次尝试进入抽卡记录界面失败，请检查是否在抽卡界面")
            continue
        else:
            print(f"第{i+1}次尝试进入抽卡记录界面失败，请检查是否在抽卡界面")
            return 1


    # 对抽卡记录进行保存截图
    # 1.先清空图片文件夹
    # 2.进入抽卡记录界面
    # 3.保存截图
    # 4.处理图片内容
    # 5.保存数据文件
    img_abspath = os.path.join(os.path.abspath('./pic'), name)  # 图片保存路径
    cleanfiles(img_abspath)
    picnum = controlengine.saveRecordImg(name)
    print(f"保存{picnum}张{name}记录截图。")
    controlengine.goHome()

    # 备份并清空数据文件
    data_abspath = os.path.join(os.path.abspath('./data'), f'{name}.txt')
    global g_backup_flag
    if g_backup_flag is False:  # 第一次备份对应记录
        bakfile(data_abspath, "./data/bak/")
        g_backup_flag = True
    record_list_old_all = rh.getfromtxtfile(data_abspath)  # 读取旧数据
    cleanfiles(data_abspath)  # 清空数据文件
    # with open(data_abspath,"w", encoding='utf-8') as f:
    #     f.write('')

    # 处理图片内容
    print("开始处理图片" + img_abspath)
    dirlist = os.listdir(img_abspath)
    record_list_new_all = []
    for filename in dirlist:
        pic_path = os.path.join(img_abspath, filename)
        print('pic_path:', pic_path)
        img = cv2.imread(pic_path)
        ocr_list, level_list = imghandler.getlist(img)
        record_list_temp = imghandler.convert2record(ocr_list, level_list)
        record_list_new_all.extend(record_list_temp)
        record_list_temp.clear()

    print(f"处理图片{img_abspath}完成，共得到{len(record_list_new_all)}条记录。")

    record_list = rh.mergeRecord(record_list_new_all, record_list_old_all)
    imghandler.saverecored(record_list, data_abspath, 'w')

    # 清空图片文件夹
    cleanfiles(img_abspath)
    print(f"完成处理{name}记录的获取。")

    return 0


def bakfile(srcfile, bakpath):
    """
    备份文件
    :param srcfile: 源文件
    :param bakpath: 备份路径
    :return:
    """
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(srcfile)  # 分离文件名和路径
        fname, ext = os.path.splitext(fname)
        if not os.path.exists(bakpath):
            os.makedirs(bakpath)  # 创建路径
        timestr = time.strftime('%Y%m%d%H%M%S', time.localtime())
        fname = fname + timestr + ext
        shutil.copy(srcfile, bakpath + fname)  # 复制文件
        print("备份文件记录 %s -> %s" % (srcfile, bakpath + fname))


def getstrfromfile(filename):
    """
    获取要显示的字符串内容
    :param filename: 文件名
    :return:
    """
    rlist = rh.getfromtxtfile(filename)
    info = rh.collectInfofromRecord(rlist)
    list1 = info['start_5_details']
    list1 = sorted(list1, key=lambda x: x[0], reverse=False)
    # print(list1)
    sum = info['total_num']
    sum5 = info['start_5_num']
    sum4 = info['start_4_num']
    sum3 = info['start_3_num']

    str1 = ""
    if sum == 0:
        str1 = "暂无抽卡记录"
    else:
        str1 = f"总计{sum}抽\n"
        str1 += f"五星数量：{sum5}\t概率：{sum5 / sum:.2%}\n"
        str1 += f"四星数量：{sum4}\t概率：{sum4 / sum:.2%}\n"
        str1 += f"三星数量：{sum3}\n"
    str2 = ""
    for i in list1:
        str2 += f"第{sum - i[0] + 1}抽：{i[1]}\n"
    print("获取记录截图完成。")
    return str1, str2


if __name__ == '__main__':
    pass


def getPoolInfoByIndex(index):
    """
    获取指定池子的信息
    :param index: 索引
    :return:info 信息字典
    """
    if index < 0 or index >= len(type_names):
        print("索引超出范围")
        return None
    type_name = type_names[index]
    filename = f"./data/{type_name}.txt"
    rlist = rh.getfromtxtfile(filename)
    info = rh.collectInfofromRecord(rlist)
    return info
