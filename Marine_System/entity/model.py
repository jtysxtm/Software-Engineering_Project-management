# 全国渔场数据
class CurrentSituation:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


# 特殊渔场数据
class SpecialFishery:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


# 系统用户数据
class User:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


# 渔场数据
class Fishery:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


# 公告数据
class Notice:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


# 日志数据
class Slog:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


# 水产数据
class Fish:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
