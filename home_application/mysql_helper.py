# -*- coding:utf-8 -*-

import pymysql
from common.log import logger


# 验证数据库可否连接
from common.mymako import render_json


def connect_mysql(mysql_server):
    try:
        connect = pymysql.connect(**mysql_server)
        connect.close()
        return True
    except Exception, e:
        print e
        return False


# 执行sql
def execute_mysql_sql(sql, server):
    try:
        server["autocommit"] = True
        connection = pymysql.connect(**server)
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        connection.commit()
        connection.close()
        return {'result':True, 'data':result}
    except Exception,e:
        logger.exception(e)
        return {'result':False, 'message':e}


# 获取MySQL实例信息
def get_mysql_db_info(server):
    sql1 = '''show VARIABLES WHERE variable_name LIKE "character_set_database" 
OR variable_name LIKE "slow_query_log"
OR variable_name LIKE "datadir"
OR variable_name LIKE "basedir" 
OR variable_name LIKE "version"
OR variable_name LIKE "port"
or variable_name LIKE "log_bin" 
or variable_name LIKE "innodb_buffer_pool_size" 
or variable_name LIKE "innodb_buffer_pool_instances" 
or variable_name LIKE "innodb_log_file_size" 
or variable_name LIKE "innodb_log_files_in_group" 
or variable_name LIKE "max_connections" 
'''
    sql2 = '''show variables LIKE "read_only"'''
    sql3 = 'show slave status'
    sql4 = "select concat(round((sum(data_length)+sum(index_length))/1024/1024,2),'MB') as data from information_schema.tables"
    sql5 = 'SHOW VARIABLES WHERE variable_name ="default_storage_engine"'
    sql6 = "show databases"
    is_read = execute_mysql_sql(sql2, server)
    role = execute_mysql_sql(sql3, server)
    base_info = execute_mysql_sql(sql1, server)
    database = execute_mysql_sql(sql6, server)
    db_name = []
    for db in database['data']:
        db_name.append(db['Database'])
    res_data = {
        "mysql_version": base_info['data'][11]["Value"],
        "base_dir": base_info['data'][0]["Value"],
        "data_dir": base_info['data'][2]["Value"],
        "is_read_only": is_read['data'][0]["Value"],
        "role": type(role['data']) == type([]),
        "mysql_size": execute_mysql_sql(sql4, server)['data'][0]["data"],
        "charset": base_info['data'][1]["Value"],
        "mysql_engine": execute_mysql_sql(sql5, server)['data'][0]["Value"],
        "is_binlog": base_info['data'][7]["Value"],
        "is_slow_query_log": base_info['data'][10]["Value"],
        "innodb_buffer_pool_size": base_info['data'][4]["Value"],
        "innodb_buffer_pool_instances": base_info['data'][3]["Value"],
        "innodb_log_file_size": base_info['data'][5]["Value"],
        "innodb_log_files_in_group": base_info['data'][6]["Value"],
        "max_connections": base_info['data'][8]["Value"],
        "db_name": str(db_name)
    }
    return res_data


def get_mysql_info(request):
    mysql_server = {"user": 'username', "password": 'password', "port": 3306, "host": 'ip'}
    res = connect_mysql(mysql_server)
    if not res:  # 判断连接是否正常
        return render_json({"result": False, "msg": "数据库连接异常"})

    mysql_server['charset'] = 'utf8'
    mysql_server['cursorclass'] = pymysql.cursors.DictCursor
    result = get_mysql_db_info(mysql_server)


