from entity.model import Notice
from utils.JsonUtils import get_class_one, get_class_list
from utils.PageUtils import get_page_start, PageData
from utils.Result import Result
from utils.SySQL import SQLManager
import logging
from datetime import datetime
"""
日志数据相关业务逻辑服务层
"""


# 根据ID查询数据
def select_slog_by_id(id):
    sql = "SELECT * FROM slog WHERE id=%s"
    sqlManager = SQLManager()
    data = sqlManager.get_one(sql, id)
    slog = get_class_one(data, Notice)
    sqlManager.close()
    return slog


# 分页数据
def select_slog_list(page, limit, where):
    page, limit, where = get_page_start(int(page), int(limit), where)
    params_sql = get_search_params(where)
    logging.debug(f"Page: {page}, Limit: {limit}, Where: {where}")
    logging.debug(f"Params SQL: {params_sql}")

    data_sql = "SELECT * FROM slog WHERE 1=1 " + params_sql + " ORDER BY id DESC LIMIT %s,%s"
    count_sql = "SELECT COUNT(id) as i FROM slog WHERE 1=1 " + params_sql
    logging.debug(f"Data SQL: {data_sql}")
    logging.debug(f"Count SQL: {count_sql}")

    sqlManager = SQLManager()
    try:
        data = sqlManager.get_list(data_sql, (page, limit))  # 获取分页数据
        count = sqlManager.get_one(count_sql)['i']  # 获取数据总数
    except Exception as e:
        logging.error(f"Database query error: {e}")
        return Result(False, "数据库查询错误: " + str(e))

    slog = get_class_list(data, Notice)

    page_result = PageData(count, slog)
    return page_result


def insert_slog(data):
    # 获取当前时间并格式化
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sqlManager = SQLManager()

    # 修改SQL语句，添加时间字段
    sql = "INSERT INTO slog (log, create_time) VALUES (%s, %s)"

    # 执行插入操作时，传入log数据和时间
    sqlManager.insert(sql, (data['log'], current_time))

    sqlManager.close()
    return Result(True, "添加成功")


# 删除数据
def del_slog(id):
    sqlManager = SQLManager()
    sql = "DELETE FROM slog where id=%s"
    sqlManager.moddify(sql, id)
    sqlManager.close()
    return Result(True, "删除成功")


# 批量删除
def del_slog_list(ids):
    sqlManager = SQLManager()
    sql = "DELETE FROM slog where id in (" + ids + ")"
    sqlManager.moddify(sql)
    sqlManager.close()
    return Result(True, "删除成功")


# 获取单个数据
def get_slog(id):
    sqlManager = SQLManager()
    sql = "select * from `slog` where id=%s "
    data = sqlManager.get_one(sql, id)
    sqlManager.close()
    return data


# 查询条件处理
def get_search_params(where):
    sql = ''
    if where:
        if where['log'] and len(where['log']) > 0:
            sql = sql + " AND log like '%%" + where['log'] + "%%' "
    return sql
