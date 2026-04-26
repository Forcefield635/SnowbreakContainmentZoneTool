from enum import Enum

type_names = ['SpecialLimitedRole', 'SpecialLimitedWeapon', 'LimitedRole', 'LimitedWeapon', 'NormalRole',
              'NormalWeapon', 'Begin']
type_names_zh = ["限定角色特选", "限定武器特选", "限定角色", "限定武器", "常驻角色", "常驻武器", "新手池"]


class PoolType(Enum):
    SLR = 0, "SpecialLimitedRole", "限定角色特选"
    SLW = 1, "SpecialLimitedWeapon", "限定武器特选"
    LR = 2, "LimitedRole", "限定角色"
    LW = 3, "LimitedWeapon", "限定武器"
    NR = 4, "NormalRole", "常驻角色"
    NW = 5, "NormalWeapon", "常驻武器"
    BG = 6, "Begin", "新手池"

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    def __init__(self, index, en_name, zh_name):
        self._value_ = index
        self.en_name = en_name
        self.zh_name = zh_name

    @classmethod
    def get_en_name(cls, index):
        for name, member in cls.__members__.items():
            if member.value == index:
                return member.en_name
        return None

    @classmethod
    def get_zh_name(cls, index):
        for name, member in cls.__members__.items():
            if member.value == index:
                return member.zh_name
        return None

    @classmethod
    def get_index_by_en_name(cls, en_name):
        for index in range(len(PoolType)):
            if PoolType(index).en_name == en_name:
                return index
        return None

    @classmethod
    def get_index_by_zh_name(cls, zh_name):
        for index in range(len(PoolType)):
            if PoolType(index).zh_name == zh_name:
                return index
        return None
