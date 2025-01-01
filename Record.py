import copy
import json


class Record:
    name: str  # 名称
    type: str  # 类型 [武器, 角色]
    date: str  # 日期
    rarity: int  # 星级： [3, 4, 5]

    def __init__(self, name="Null", type="Null", date="Null", rarity=0):
        self.name = name  # 名称
        self.type = type  # 类型 [武器, 角色]
        self.date = date  # 日期
        self.rarity = rarity  # 星级： [3, 4, 5]

    def __str__(self):
        return f'{self.name},{self.type},{self.date},{self.rarity}'

    def __eq__(self, other):
        if isinstance(other, Record):
            return self.name == other.name and self.type == other.type and self.date == other.date and self.rarity == other.rarity
        else:
            return False

    def __hash__(self):
        return hash((self.name, self.type, self.date, self.rarity))


class RecordHandler:
    _instance = None # 单例模式
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RecordHandler, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        pass

    def getfromtxtfile(self, filename) -> list[Record]:
        """
        从txt文件中读取记录
        :param filename:
        :return: list[Record]
        """
        record_list = []
        with open(filename, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                line = line.strip()
                item = line.split(',')
                record = Record(item[0], item[1], item[2], int(item[3]))
                record_list.append(record)
        return record_list

    def getfromjsonfile(self, filename) -> list:
        """
        从json文件中读取记录
        :param filename:
        :return: list[Record]
        """
        record_list = []
        with open(filename, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                line = line.strip()
                item = json.loads(line)
                record = Record(item['name'], item['type'], item['date'], item['rarity'])
                record_list.append(record)
        return record_list

    def correctcontent(self, record):
        """
        修正记录内容
        :param record:
        :return:
        """
        # 2024-04-2000:54 15长度 异常
        # 2024-04-20 00:54 正常16长度
        if len(record.date) == 15:
            record.date = f'{record.date[:10]} {record.date[10:]}'
        if record.name == "芙提雅-默":
            record.name = "芙提雅-缄默"
        elif record.name == "琴诺-谬":
            record.name = "琴诺-悖谬"
        return record

    def savetotxtfile(self, record_list: list, output_path: str, mode: str = 'a'):
        """
        txt文件输出
        :param record_list: 记录列表
        :param output_path: 保存路径
        :param mode: 写入模式
        :return:
        """
        with open(output_path, mode, encoding='utf-8') as f:
            for record in record_list:
                f.write(str(record))
                f.write('\n')
        print(f'({len(record_list)}) record were written txt file')

    def savetojsonfile(self, record_list: list, output_path: str, mode: str = 'a'):
        """
        json文件输出
        :param record_list: 记录列表
        :param output_path: 保存路径
        :param mode: 写入模式
        :return:
        """
        with open(output_path, mode, encoding='utf-8') as f:
            for record in record_list:
                f.write(json.dumps(record.__dict__, ensure_ascii=False))
                f.write('\n')
        print(f'({len(record_list)}) record were written json file')

    def collectInfofromRecord(self, record_list: list):
        """
        获取记录数量
        :param record_list:
        :return :info 字典:
            total_num: 总记录数
            already_drawn_num: 已垫抽数
            start_5_num: 星级5记录数
            start_4_num: 星级4记录数
            start_3_num: 星级3记录数
            start_5_details: 星级5记录详情 [index, record] index从1开始
            start_4_details: 星级4记录详情 [index, record] index从1开始
        """
        info = {}
        total_num = len(record_list)
        already_drawn_num = -1  # 已垫抽数
        start_3_num = 0
        start_4_num = 0
        start_5_num = 0
        start_4_details = []
        start_5_details = []
        for index, record in enumerate(record_list):
            if record.rarity == 3:
                start_3_num += 1
            elif record.rarity == 4:
                start_4_num += 1
                start_4_details.append([index + 1, str(record)])
            elif record.rarity == 5:
                start_5_num += 1
                start_5_details.append([index + 1, str(record)])
                if already_drawn_num == -1:
                    already_drawn_num = index

        info['total_num'] = total_num
        info['already_drawn_num'] = already_drawn_num
        info['start_5_num'] = start_5_num
        info['start_4_num'] = start_4_num
        info['start_3_num'] = start_3_num
        info['start_5_details'] = copy.deepcopy(start_5_details)
        info['start_4_details'] = copy.deepcopy(start_4_details)

        print(f'总记录数：{total_num}，星级5：{start_5_num}，星级4：{start_4_num}，星级3：{start_3_num}, 已垫抽数：{already_drawn_num}')
        # print(f'星级4记录：{record_4}')
        # print(f'星级5记录：{start_5_details}')

        return info

    def mergeRecord(self, record_list_new: list, record_list_old: list):
        """
        合并两个记录列表，剔除重复记录
        :param record_list_new:新列表
        :param record_list_old:老列表
        :return:合并后的列表
        """
        if len(record_list_old) == 0 or len(record_list_new) == 0:
            print(f"输入列表有空，newlistlen({len(record_list_new)}) or oldlistlen({len(record_list_old)})")
            return record_list_new + record_list_old

        # new_list的最后一条记录时间大于old_list的最后一条记录时间，则直接合并
        # new_list的最后一条记录时间小于old_list的最后一条记录时间，则直接返回new_list
        if record_list_new[-1].date > record_list_old[0].date:
            print("新列表和老列表时间段不重叠，直接返回和")
            return record_list_new + record_list_old
        elif record_list_new[-1].date < record_list_new[-1].date:
            print("新列表已覆盖老列表时间段记录，请检查输入")
            return record_list_new

        # 预期可以在list1中找到list2的第一条记录，然后将list2的记录插入到list1的对应位置
        index = 0xffff
        mate_index = 0
        mate_count = 4
        for i, record in enumerate(record_list_new):
            if record == record_list_old[mate_index]:
                mate_index += 1
                if mate_index >= mate_count:
                    index = i
                    break
            else:
                mate_index = 0
                if record == record_list_old[mate_index]:
                    mate_index += 1

        if index != 0xffff:
            record_list = record_list_new[:index - mate_index + 1] + record_list_old
            print(f"合并成功，从新列表第{index + 1}条开始重复，合并后有{len(record_list)}条记录")
            return record_list
        elif mate_index == 0:
            print("未找到匹配的记录, 请检查输入")
            return None
        elif index == 0xffff and mate_index <= mate_count:
            record_list = record_list_new[:-mate_index] + record_list_old
            print(f"合并成功，从新列表倒数第{mate_index}条开始重复，合并后有{len(record_list)}条记录")
            return record_list
        else:
            print("输入列表有误")
        return None



if __name__ == '__main__':

    rh  = RecordHandler()
    rh2 = RecordHandler()
    if rh == rh2:
        print("单例模式测试成功")
    else:
        print("单例模式测试失败")

