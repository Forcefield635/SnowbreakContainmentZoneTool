import json


class Record:
    name: str
    type: str
    date: str
    rarity: int

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
    def __init__(self):
        pass

    def getfromtxtfile(self, filename) -> list:
        record_list = []
        with open(filename, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                line = line.strip()
                item = line.split(',')
                record = Record(item[0], item[1], item[2], int(item[3]))
                record_list.append(record)
        return record_list

    def getfromjsonfile(self, filename) -> list:
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
        文件输出
        :param record_list:
        :param output_path:
        :param mode:
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
        :param record_list:
        :param output_path:
        :param mode:
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
        :return:[[sum, sum_5, sum_4, sum_3], [record_5, record_4]]
        """
        sum = len(record_list)
        sum_3 = 0
        sum_4 = 0
        sum_5 = 0
        record_4 = []
        record_5 = []
        for index, record in enumerate(record_list):
            if record.rarity == 3:
                sum_3 += 1
            elif record.rarity == 4:
                sum_4 += 1
                record_4.append([index + 1, str(record)])
            elif record.rarity == 5:
                sum_5 += 1
                record_5.append([index + 1, str(record)])
        allinfo = [[sum, sum_5, sum_4, sum_3], [record_5, record_4]]
        print(f'总记录数：{sum}，星级5：{sum_5}，星级4：{sum_4}，星级3：{sum_3}')
        print(f'星级4记录：{record_4}')
        print(f'星级5记录：{record_5}')
        return allinfo

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
            return record_list_new +record_list_old
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
            record_list = record_list_new[:index-mate_index+1] + record_list_old
            print(f"合并成功，从新列表第{index+1}条开始重复，合并后有{len(record_list)}条记录")
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

rh = RecordHandler()

if __name__ == '__main__':
    record1 = Record('琴诺-悖谬', '角色', '2024-04-20 00:54', 5)
    # print(record1.__dict__)
    rh = RecordHandler()
    rh.savetojsonfile([record1], 'testtest.json')
