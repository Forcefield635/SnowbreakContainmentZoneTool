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
from ImgHandle import imghandler
from Record import rh
type_names = ['Begin', 'SpecialLimitedRole', 'SpecialLimitedWeapon', 'LimitedRole', 'LimitedWeapon', 'NormalRole',
              'NormalWeapon']
type_names_ch = ["新手池", "限定角色不歪池", "限定武器不歪池", "限定角色池", "限定武器池", "常驻角色池", "常驻武器池"]

def cleanfiles(path):
    """清理文件"""
    if not os.path.exists(path):
        os.makedirs(path)
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            print("清理文件：",os.path.join(root, name))
            os.remove(os.path.join(root, name))
        for name in dirs:
            print(os.path.join(root, name))
            os.rmdir(os.path.join(root, name))


def generateRecordByType(name):
    """
    获取指定类型抽卡记录
    :param name: 类型名称
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

    # 进入抽卡界面
    controlengine.preWindow()
    time.sleep(2)
    ret = controlengine.goPoolRecord(name)
    if ret != 0:
        print("进入抽卡记录页面失败")
        return 1

    # 保存截图
    img_abspath = os.path.join(os.path.abspath('../pic'), name)
    cleanfiles(img_abspath)
    controlengine.saveRecordImg(name)
    controlengine.goHome()

    # 备份并清空数据文件
    data_abspath = os.path.join(os.path.abspath('../data'), f'{name}.txt')
    cleanfiles(data_abspath)
    bakfile(data_abspath,"../data/bak/")
    with open(data_abspath,"w", encoding='utf-8') as f:
        f.write('')
    # 处理图片内容
    print("开始处理图片"+img_abspath)
    dirlist = os.listdir(img_abspath)
    for filename in dirlist:
        pic_path = os.path.join(img_abspath, filename)
        print('pic_path:', pic_path)
        img = cv2.imread(pic_path)
        ocr_list, level_list = imghandler.getlist(img)
        record_list = imghandler.convert2record(ocr_list, level_list)
        imghandler.saverecored(record_list, data_abspath, 'a')

    print(f"完成处理{name}")
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
        print("bak %s -> %s" % (srcfile, bakpath + fname))

def test1(filename):
    """
    测试函数
    :param filename: 文件名
    :return:
    """
    rlist = rh.generateRecordlistfromfile(filename)
    info = rh.collectInfofromRecord(rlist)
    list1 = info[1][0]+info[1][1]
    list1 = sorted(list1, key=lambda x: x[0], reverse=False)
    print(list1)
    sum,sum5,sum4,sum3 = info[0]
    str =f"总计{sum}抽\n"
    str +=f"五星数量：{sum5}\t概率：{sum5/sum:.2%}\n"
    str +=f"四星数量：{sum4}\t概率：{sum4/sum:.2%}\n"
    str +=f"三星数量：{sum3}\n"
    str2 = ""
    for i in list1:
        str2 += f"第{sum-i[0]+1}抽：{i[1]}\n"
    print("maintest1")
    return str,str2

if __name__ == '__main__':

    pass
