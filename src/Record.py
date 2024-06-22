


class Record:
    name: str
    type: str
    date: str
    rarity: int

    def __init__(self, name="", type="", date="", rarity=0):
        self.name = name  # 名称
        self.type = type  # 类型 [武器, 角色]
        self.date = date  # 日期
        self.rarity = rarity  # 星级： [3, 4, 5]

    def __str__(self):
        return f'{self.name},{self.type},{self.date},{self.rarity}'


class RecordHandler:
    def __init__(self):
        pass

    def generateRecordlistfromfile(self, filename) -> list:
        record_list = []
        with open(filename, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                line = line.strip()
                item = line.split(',')
                record = Record(item[0], item[1], item[2], int(item[3]))
                record_list.append(record)
        return record_list

    def filterRecordlistbyRarity(self, record_list: list, rarity: int) -> list:
        """
        过滤星级
        :param record_list:
        :param rarity:
        :return:
        """
        return [record for record in record_list if record.rarity == rarity]

    def filterRecordlistbyType(self, record_list: list, type: str) -> list:
        """
        过滤类型
        :param record_list:
        :param type:
        :return:
        """
        return [record for record in record_list if record.type == type]



    def formatDate(self, record):
        """
        修正记录内容
        :param record:
        :return:
        """
        # 2024-04-2000:54 15长度
        # 2024-04-20 00:54 正常16长度
        if len(record.date) == 15:
            record.date = f'{record.date[:10]} {record.date[10:]}'
        if record.name == "芙提雅-默":
            record.name = "芙提雅-缄默"
        elif record.name == "琴诺-谬":
            record.name = "琴诺-悖谬"
        return record

    def savetotxt(self, record_list: list, output_path, file_type='a'):
        """
        文件输出
        :param record_list:
        :param output_path:
        :param file_type:
        :return:
        """
        file = open(output_path, file_type, encoding='utf-8')
        for record in record_list:
            file.writelines(str(record) + '\n')
        print(f'({len(record_list)}) record were written this time')
        file.close()

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
                record_4.append([index+1, str(record)])
            elif record.rarity == 5:
                sum_5 += 1
                record_5.append([index+1, str(record)])
        allinfo = [[sum, sum_5, sum_4, sum_3], [record_5, record_4]]
        print(f'总记录数：{sum}，星级5：{sum_5}，星级4：{sum_4}，星级3：{sum_3}')

        print(f'星级4记录：{record_4}')
        print(f'星级5记录：{record_5}')
        return allinfo

rh = RecordHandler()