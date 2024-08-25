from Record import *
import copy

class PoolInfo:
    name = ""
    total_num = 0
    start_5_num = 0
    start_4_num = 0
    start_3_num = 0
    records: list[Record] = []
    start_5_details: list[Record] = []
    start_4_details: list[Record] = []
    def __init__(self, name: str, records = None):
        self.name = name
        if records is None:
            self.records = []
        else:
            self.records = copy.deepcopy(records)

    def initInfo(self):
        info = rh.collectInfofromRecord(self.records)
        self.total_num = info['total_num']
        self.start_5_num = info['start_5_num']
        self.start_4_num = info['start_4_num']
        self.start_3_num = info['start_3_num']
        self.start_5_details = copy.deepcopy(info['start_5_details'])
        self.start_4_details = copy.deepcopy(info['start_4_details'])


    def add_record(self, record):
        self.records.append(record)

    def get_records(self):
        return self.records

    def get_name(self):
        return self.name

if __name__ == '__main__':
    # Test code
    record1 = Record('name1', '角色', '2024-04-20 00:54', 5)

    record2 = Record('name2', '武器', '2024-04-20 00:54', 4)

    record3 = Record('name3', '卡牌', '2024-04-20 00:54', 5)

    records = [record1, record2, record3]
    print(str(record1))
    pool_info = PoolInfo('test_pool', 100, 50, 30, 20, records)

    print(pool_info.get_records())
    print(str(pool_info.start_5_records[0]))
    print(str(pool_info.start_5_records[1]))
    record3.name = 'name3_new'
    print(str(pool_info.start_5_records[1]))
    pool_info.records[2].name = 'name3_new2'
    print(str(pool_info.start_5_records[1]))
    pass