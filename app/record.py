import copy
import json


class Record:
    name: str
    type: str
    date: str
    rarity: int

    def __init__(self, name="Null", type="Null", date="Null", rarity=0):
        self.name = name
        self.type = type
        self.date = date
        self.rarity = rarity

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
    _instance = None
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
                    record_list.append(record)
        except FileNotFoundError:
            print(f"文件 {filename} 不存在")
        except Exception as e:
            print(f"读取文件时发生错误：{e}")
        return record_list

    def getfromjsonfile(self, filename: str):
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
        if len(record.date) == 15:
            record.date = f'{record.date[:10]} {record.date[10:]}'
        name_corrections = {
            "芙提雅-默": "芙提雅-缄默",
            "琴诺-谬": "琴诺-悖谬"
        }
        record.name = name_corrections.get(record.name, record.name)
        return record

    def savetotxtfile(self, record_list: list, output_path: str, mode: str = 'a') -> None:
        try:
            with open(output_path, mode, encoding='utf-8') as f:
                for record in record_list:
                    f.write(f"{record}\n")
            print(f"成功写入 {len(record_list)} 条记录到 {output_path}")
        except Exception as e:
            print(f"写入文件时发生错误：{e}")

    def savetojsonfile(self, record_list: list[Record], output_path: str, mode: str = 'a') -> None:
        try:
            with open(output_path, mode, encoding='utf-8') as f:
                for record in record_list:
                    json_line = json.dumps(record.__dict__, ensure_ascii=False)
                    f.write(f"{json_line}\n")
            print(f"成功写入 {len(record_list)} 条记录到 {output_path}")
        except Exception as e:
            print(f"写入文件时发生错误：{e}")

    def collectInfofromRecord(self, record_list: list[Record]) -> dict:
        info = {
            'total_num': len(record_list),
            'already_drawn_num': 0,
            'start_5_num': 0,
            'start_4_num': 0,
            'start_3_num': 0,
            'start_5_details': [],
            'start_4_details': [],
        }
        already_drawn_num = -1
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
        if len(record_list_old) == 0 or len(record_list_new) == 0:
            print(f"输入列表有空，newlistlen({len(record_list_new)}) or oldlistlen({len(record_list_old)})")
            return record_list_new + record_list_old
        if record_list_new[-1].date > record_list_old[0].date:
            print("新列表和老列表时间段不重叠，直接返回合并后的列表")
            return record_list_new + record_list_old
        record_list_new = copy.deepcopy(record_list_new)
        record_list_old = copy.deepcopy(record_list_old)
        record_list_new.reverse()
        record_list_old.reverse()
        record_list = []
        record_list += record_list_old
        idx = 0
        for record, index in zip(record_list_new, range(len(record_list_new))):
            if record not in record_list_old:
                record_list.append(record)
            else:
                idx = index
        print(f"合并成功，新列表有{len(record_list_new)}条记录，老列表有{len(record_list_old)}条记录，从新列表第{idx + 1}条开始重复，合并后有{len(record_list)}条记录")
        record_list.reverse()
        return record_list
