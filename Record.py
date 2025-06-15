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
    _initialized = False
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RecordHandler, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not RecordHandler._initialized:
            super().__init__()
            RecordHandler._initialized = True

    def getfromtxtfile(self, filename: str):
        """从txt文件中读取记录"""
        record_list = []
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    items = line.split(',')
                    if len(items) != 4:
                        print(f"Invalid line format: {line}")
                        continue
                    record = Record(items[0], items[1], items[2], int(items[3]))
                    record = self.correctcontent(record)
                    record_list.append(record)
        except FileNotFoundError:
            print(f"文件 {filename} 不存在")
        except Exception as e:
            print(f"读取文件时发生错误：{e}")
        return record_list

    def getfromjsonfile(self, filename: str):
        """从json文件中读取记录"""
        record_list = []
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        item = json.loads(line)
                        record = Record(item['name'], item['type'], item['date'], item['rarity'])
                        record = self.correctcontent(record)
                        record_list.append(record)
                    except json.JSONDecodeError:
                        print(f"JSON解析失败: {line}")
        except FileNotFoundError:
            print(f"文件 {filename} 不存在")
        except Exception as e:
            print(f"读取文件时发生错误：{e}")
        return record_list

    @staticmethod
    def correctcontent(record: Record) -> Record:
        """
        修正记录内容
        :param record:
        :return:
        """
        # 2024-04-2000:54 15长度 异常
        # 2024-04-20 00:54 正常16长度
        if len(record.date) == 15:
            record.date = f'{record.date[:10]} {record.date[10:]}'
        # 使用字典进行名称修正
        name_corrections = {
            "芙提雅-默": "芙提雅-缄默",
            "琴诺-谬": "琴诺-悖谬"
        }
        record.name = name_corrections.get(record.name, record.name)
        return record

    def savetotxtfile(self, record_list: list, output_path: str, mode: str = 'a') -> None:
        """保存到txt文件"""
        try:
            with open(output_path, mode, encoding='utf-8') as f:
                for record in record_list:
                    f.write(f"{record}\n")
            print(f"成功写入 {len(record_list)} 条记录到 {output_path}")
        except Exception as e:
            print(f"写入文件时发生错误：{e}")


    def savetojsonfile(self, record_list: list[Record], output_path: str, mode: str = 'a') -> None:
        """保存到json文件"""
        try:
            with open(output_path, mode, encoding='utf-8') as f:
                for record in record_list:
                    json_line = json.dumps(record.__dict__, ensure_ascii=False)
                    f.write(f"{json_line}\n")
            print(f"成功写入 {len(record_list)} 条记录到 {output_path}")
        except Exception as e:
            print(f"写入文件时发生错误：{e}")

    def collectInfofromRecord(self, record_list: list[Record]) -> dict:
        """收集统计信息"""
        info = {
            'total_num': len(record_list),
            'already_drawn_num': 0,
            'start_5_num': 0,
            'start_4_num': 0,
            'start_3_num': 0,
            'start_5_details': [],
            'start_4_details': [],
        }
        already_drawn_num = -1 # 记录是从新往旧排列，所以到第一个五星记录时，是已垫的记录数
        last_5_index = -1
        for idx, record in enumerate(record_list):
            if record.rarity == 5:
                info['start_5_num'] += 1
                info['start_5_details'].append([idx + 1, str(record)])
                last_5_index = idx
                if already_drawn_num == -1:
                    already_drawn_num = idx
            elif record.rarity == 4:
                info['start_4_num'] += 1
                info['start_4_details'].append([idx + 1, str(record)])
            else:
                info['start_3_num'] += 1

        info['already_drawn_num'] = already_drawn_num
        print(
            f"总记录数：{info['total_num']}，五星：{info['start_5_num']}，四星：{info['start_4_num']}，"
            f"三星：{info['start_3_num']}，已垫抽数：{info['already_drawn_num']}"
        )
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
        mate_count = 1 # 需要匹配的记录数
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

