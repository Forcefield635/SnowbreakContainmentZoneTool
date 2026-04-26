import os
import shutil
import time

import cv2

from app.types import type_names
from app.controller import controlengine
from app.record import RecordHandler
from app.ocr_engine import ImgHandler

g_record_handler = RecordHandler()
g_img_handler = ImgHandler()
g_backup_flag: bool = False


def cleanfiles(path):
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


def generateRecordByEnType(name):
    from app.types import PoolType
    index = PoolType.get_index_by_en_name(name)
    if index is None:
        print(f"类型名称{name}不正确，请检查。")
        return 1
    ret = controlengine.preWindow()
    if ret != 0:
        print("前置窗口操作失败，请检查是否已打开抽卡窗口")
        return ret
    for i in range(3):
        ret = controlengine.goPoolRecord(name)
        if ret == 0:
            print(f"进入抽卡记录界面")
            break
        elif ret == 1:
            print(f"第{i + 1}次尝试进入抽卡记录界面失败，请检查是否在抽卡界面")
            continue
        else:
            print(f"第{i + 1}次尝试进入抽卡记录界面失败，请检查是否在抽卡界面")
            return 1
    img_abspath = os.path.join(os.path.abspath('./pic'), name)
    cleanfiles(img_abspath)
    picnum = controlengine.saveRecordImg(name)
    print(f"保存{picnum}张{name}记录截图。")
    controlengine.goHome()
    data_abspath = os.path.join(os.path.abspath('./data'), f'{name}.txt')
    global g_backup_flag
    if g_backup_flag is False:
        bakfile(data_abspath, "./data/bak/")
        g_backup_flag = True
    record_list_old_all = g_record_handler.getfromtxtfile(data_abspath)
    cleanfiles(data_abspath)
    print("main.py 开始处理图片" + img_abspath)
    dirlist = os.listdir(img_abspath)
    record_list_new_all = []
    for filename in dirlist:
        pic_path = os.path.join(img_abspath, filename)
        print('main.py 处理图片:', pic_path)
        img = cv2.imread(pic_path)
        ocr_list, level_list = g_img_handler.getlist(img)
        record_list_temp = g_img_handler.convert2record(ocr_list, level_list)
        record_list_new_all.extend(record_list_temp)
        record_list_temp.clear()
    print(f"main.py 处理图片{img_abspath}完成，共得到{len(record_list_new_all)}条记录。")
    record_list = g_record_handler.mergeRecord(record_list_new_all, record_list_old_all)
    ret = g_img_handler.saverecored(record_list, data_abspath, 'w')
    if ret == 0:
        print(f"保存{name}记录数据文件成功。")
    else:
        print(f"保存{name}记录数据文件失败。")
    cleanfiles(img_abspath)
    print(f"完成处理{name}记录的获取。")
    return ret


def generateRecordDict(name):
    from app.types import PoolType
    index = PoolType.get_index_by_en_name(name)
    if index is None:
        print(f"类型名称{name}不正确，请检查。")
        return 1
    img_abspath = os.path.join(os.path.abspath('./pic'), name)
    cleanfiles(img_abspath)
    picnum = controlengine.saveRecordImg(name)
    print(f"保存{picnum}张{name}记录截图。")
    data_abspath = os.path.join(os.path.abspath('./data'), f'{name}.txt')
    global g_backup_flag
    if g_backup_flag is False:
        bakfile(data_abspath, "./data/bak/")
        g_backup_flag = True
    record_list_old_all = g_record_handler.getfromtxtfile(data_abspath)
    cleanfiles(data_abspath)
    print("main.py 开始处理图片" + img_abspath)
    dirlist = os.listdir(img_abspath)
    record_list_new_all = []
    for filename in dirlist:
        pic_path = os.path.join(img_abspath, filename)
        print('main.py 处理图片:', pic_path)
        img = cv2.imread(pic_path)
        ocr_list, level_list = g_img_handler.getlist(img)
        record_list_temp = g_img_handler.convert2record(ocr_list, level_list)
        record_list_new_all.extend(record_list_temp)
        record_list_temp.clear()
    print(f"main.py 处理图片{img_abspath}完成，共得到{len(record_list_new_all)}条记录。")
    record_list = g_record_handler.mergeRecord(record_list_new_all, record_list_old_all)
    if record_list is None or len(record_list) == 0:
        print(f"合并失败 没有新的{name}记录。")
        cleanfiles(img_abspath)
        return 2
    ret = g_img_handler.saverecored(record_list, data_abspath, 'w')
    if ret == 0:
        print(f"保存{name}记录数据文件成功。")
    else:
        print(f"保存{name}记录数据文件失败。")
    cleanfiles(img_abspath)
    print(f"完成处理{name}记录的获取。")
    return ret


def bakfile(srcfile, bakpath):
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(srcfile)
        fname, ext = os.path.splitext(fname)
        if not os.path.exists(bakpath):
            os.makedirs(bakpath)
        timestr = time.strftime('%Y%m%d%H%M%S', time.localtime())
        fname = fname + timestr + ext
        shutil.copy(srcfile, bakpath + fname)
        print("备份文件记录 %s -> %s" % (srcfile, bakpath + fname))


def getstrfromfile(filename):
    rlist = g_record_handler.getfromtxtfile(filename)
    info = g_record_handler.collectInfofromRecord(rlist)
    list1 = info['start_5_details']
    list1 = sorted(list1, key=lambda x: x[0], reverse=False)
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


def getPoolInfoByIndex(index):
    if index < 0 or index >= len(type_names):
        print("索引超出范围")
        return None
    type_name = type_names[index]
    filename = f"./data/{type_name}.txt"
    rlist = g_record_handler.getfromtxtfile(filename)
    info = g_record_handler.collectInfofromRecord(rlist)
    return info
