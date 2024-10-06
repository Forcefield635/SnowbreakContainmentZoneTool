"""
图片处理类
1. 识别等级
2. 识别ocr
"""

import cv2
from paddleocr import PaddleOCR
from Record import Record,rh

class LevelHandle():
    """
    等级识别类
    """
    # RGB标识
    # (55, 98, 242)     #3762f2     蓝色3星
    # (192, 105, 214)   #c069d6     紫色4星
    # (233, 155, 55)    #e99b37     橙色5星
    # (225, 226, 239)   #e1e2ef     无，接近白色
    # opencv中是BGR排列
    level_color_list = [[0, (239, 226, 225)], [3, (242, 98, 55)], [4, (214, 105, 192)], [5, (55, 155, 233)]]

    def __init__(self):
        self.level_list = []
        self.threshold = 10

    def calc_diff(self, pixel, bg_color):
        # 计算pixel与背景的离差平方和，作为当前像素点与背景相似程度的度量
        return (pixel[0] - bg_color[0]) ** 2 + (pixel[1] - bg_color[1]) ** 2 + (pixel[2] - bg_color[2]) ** 2

    def get_level(self, img_1k) -> list:
        """
        识别1080P图片的[180:860, 344:360]区域的等级
        img_1k
        :param img_1k:
        :return:
        """
        # 识别图片是16*680大小，第一行距离图片下标中心点为12+(68/2) = 46 像素
        # 中心点坐标(46+68*n ,8)
        color_img = img_1k[180:860, 344:360]
        img_a = cv2.cvtColor(color_img, cv2.COLOR_BGR2BGRA)
        height = img_a.shape[0]
        width = img_a.shape[1]
        level_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(0, 10):
            center_point = (int(46 + (height / 10) * i), int(width / 2))
            for k in range(len(self.level_color_list)):
                if self.calc_diff(img_a[center_point[0]][center_point[1]], self.level_color_list[k][1]) < self.threshold:
                    level_list[i] = self.level_color_list[k][0]
                    break
        print(f'level_list:{level_list}')
        return level_list


class ImgHandler:
    """
    图片处理类
    """

    def __init__(self, ):
        self.__ocr_engine = PaddleOCR(lang='ch', show_log=False, use_gpu=False, drop_score=0.7, use_angle_cls=False)
        self.lh = LevelHandle()

    def getlist(self, img) -> (list, list):
        """
        获取ocr识别后的list
        :param img:
        :return:
        """
        if img is None:
            print('ERROR: img is None')
            return []
        img_1k = cv2.resize(img, (1920, 1080))

        # 统计稀有度处理
        # 中心点坐标(46+68*n ,8)
        level_list = self.lh.get_level(img_1k)

        # ocr 表格识别
        table_img = img_1k[180:860, 360:1560]
        table_img = cv2.cvtColor(table_img, cv2.COLOR_BGR2GRAY)

        # 二值化处理
        ret, img = cv2.threshold(table_img, 190, 255, cv2.THRESH_BINARY)
        # ocr识别输出列表格式 [ [[[左上坐标],[右上坐标],[右下坐标],[左下坐标]], ('识别内容', 置信度)], ... ]
        # [[[2432.0, 74.0], [2509.0, 74.0], [2509.0, 148.0], [2432.0, 148.0]], ('α', 0.5288054943084717)]
        ocr_lists = self.__ocr_engine.ocr(table_img)[0]

        print(f'img handle finished. ocr list len:{len(ocr_lists)}')
        return ocr_lists, level_list

    def convert2record(self, ocr_lists=None, level_list=None) -> list[Record]:
        """
        转换ocrlist和levellist为Record记录列表
        :param ocr_lists: ocr识别返回的记录列表
        :param level_list: ocr识别返回的等级列表
        :return: list[Record]
        """
        record_list = []
        if ocr_lists is None:
            return record_list

        if level_list is None:
            _level_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        else:
            _level_list = level_list

        length = len(ocr_lists)
        if length % 3 != 0:
            print(f'ocr list length({length}) error', )
            print(f'error lists:{ocr_lists}')
            return []
        count = int(length / 3)
        record_list = []
        for i in range(0, count):
            name = ocr_lists[i * 3][1][0]
            type = ocr_lists[i * 3 + 1][1][0]
            date = ocr_lists[i * 3 + 2][1][0]
            level = level_list[i]
            record = Record(name, type, date, level)
            record = rh.correctcontent(record)
            record_list.append(record)

        print(f'data handle finished. record list len:{len(record_list)}')
        return record_list

    def saverecored(self, record_list: list, output_path, file_type='a'):
        """
        文件输出
        :param record_list:
        :param output_path:
        :param file_type:
        :return:
        """
        if record_list is None or len(record_list) == 0:
            print('record_list is empty')
            return 1
        file = open(output_path, file_type, encoding='utf-8')
        for record in record_list:
            file.writelines(str(record) + '\n')
        print(f'({len(record_list)}) record were written this time')
        file.close()
        return 0

imghandler = ImgHandler()
