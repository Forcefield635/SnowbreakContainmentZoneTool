from Record import *
import copy

class PoolInfo:
    name = ""
    total_num = 0
    alrady_drawn_num = 0
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
        info = RecordHandler.collectInfofromRecord(self.records)
        self.total_num = info['total_num']
        self.alrady_drawn_num = info['alrady_drawn_num']
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
    pass