from entity.model import CurrentSituation
from utils.JsonUtils import get_class_one, get_class_list
from utils.PageUtils import get_page_start, PageData
from utils.Result import Result
from utils.SySQL import SQLManager

"""
全国区域渔场数据相关业务逻辑服务�?
"""


# 根据渔场名称查询最新数�?
def select_current_situation_by_fishery(fishery):
    sql = "SELECT * FROM currentsituation WHERE fishery_name=%s order by create_time desc limit 1"
    sqlManager = SQLManager()
    data = sqlManager.get_one(sql, fishery)
    sqlManager.close()
    return data


# 根据ID查询数据
def select_current_situation_by_id(id):
    sql = "SELECT * FROM CurrentSituation WHERE id=%s"
    sqlManager = SQLManager()
    data = sqlManager.get_one(sql, id)
    current_situation = get_class_one(data, CurrentSituation)
    sqlManager.close()
    return current_situation


# 当前情况列表
def select_current_situation_list(page, limit, where):
    page, limit, where = get_page_start(int(page), int(limit), where)
    params_sql = get_search_params(where)
    data_sql = "SELECT * FROM CurrentSituation WHERE 1=1 " + params_sql + " ORDER BY id DESC LIMIT %s,%s"
    count_sql = "SELECT COUNT(id) as i FROM CurrentSituation WHERE 1=1 " + params_sql
    sqlManager = SQLManager()
    data = sqlManager.get_list(data_sql, (page, limit))  # 获取分页数据
    count = sqlManager.get_one(count_sql)['i']  # 获取数据总数
    current_situation = get_class_list(data, CurrentSituation)
    page_result = PageData(count, current_situation)
    return page_result


# 查询条件处理
def get_search_params(where):
    sql = ''
    if where:
        if where['fishery_name'] and len(where['fishery_name']) > 0:
            sql = sql + " AND fishery_name like '%%" + where['fishery_name'] + "%%' "
        if where['record_date'] and len(where['record_date']) > 0:
            sql = sql + " AND record_date = '" + where['record_date'] + "' "
    return sql


# 鱼的种类列表
def get_fish_list():
    sql = "SELECT fish_name FROM CurrentSituation GROUP BY fish_name"
    sqlManager = SQLManager()
    fish_list = []
    data = sqlManager.get_list(sql)
    for i in data:
        fish_list.append(i['fish_name'])
    sqlManager.close()
    return fish_list


# 获取水质信息
def get_water_list():
    sql = "SELECT water_quality FROM CurrentSituation GROUP BY water_quality"
    sqlManager = SQLManager()
    water_list = []
    data = sqlManager.get_list(sql)
    for i in data:
        water_list.append(i['water_quality'])
    sqlManager.close()
    return water_list


# 获取渔场列表
def get_fishery_list():
    sql = "SELECT fishery_name FROM CurrentSituation GROUP BY fishery_name"
    sqlManager = SQLManager()
    fishery_list = []
    data = sqlManager.get_list(sql)
    for i in data:
        fishery_list.append(i['fishery_name'])
    sqlManager.close()
    return fishery_list


# 插入渔场实时数据
def insert_current_situation(data):
    sqlManager = SQLManager()
    check_sql = "SELECT COUNT(id) as `i` FROM `CurrentSituation` WHERE fishery_name=%s AND record_date=%s AND record_time=%s"
    count = sqlManager.get_one(check_sql, (data['fishery_name'], data['record_date'], data['record_time']))['i']
    if count > 0:
        return Result(False, "数据重复")
    sql = "INSERT INTO CurrentSituation (province, fishery_name, record_date, record_time, water_temp, water_quality, ph_value, dissolved_oxygen, turbidity, fish_name, fish_count) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    sqlManager.insert(sql, (
        data['province'], data['fishery_name'], data['record_date'], data['record_time'], data['water_temp'], data['water_quality'], data['ph_value'], data['dissolved_oxygen'], data['turbidity'], data['fish_name'], data['fish_count']))
    sqlManager.close()
    return Result(True, "添加成功")


# 修改渔场实时数据
def edit_current_situation(data):
    sqlManager = SQLManager()
    sql = "UPDATE CurrentSituation SET water_temp=%s, water_quality=%s, ph_value=%s, dissolved_oxygen=%s, turbidity=%s, fish_name=%s, fish_count=%s WHERE id=%s"
    sqlManager.moddify(sql, (
        data['water_temp'], data['water_quality'], data['ph_value'], data['dissolved_oxygen'], data['turbidity'], data['fish_name'], data['fish_count'], data['id']))
    sqlManager.close()
    return Result(True, "修改成功")


# 删除渔场实时数据
def del_current_situation(id):
    sqlManager = SQLManager()
    sql = "DELETE FROM CurrentSituation WHERE id=%s"
    sqlManager.moddify(sql, id)
    sqlManager.close()
    return Result(True, "删除成功")


# 批量删除渔场实时数据
def del_current_situation_list(ids):
    sqlManager = SQLManager()
    sql = "DELETE FROM CurrentSituation WHERE id IN (" + ids + ")"
    sqlManager.moddify(sql)
    sqlManager.close()
    return Result(True, "删除成功")


# 根据id获取渔场情况
def get_current_situation(id):
    sqlManager = SQLManager()
    sql = "SELECT * FROM `CurrentSituation` WHERE id=%s"
    data = sqlManager.get_one(sql, id)
    sqlManager.close()
    return data

