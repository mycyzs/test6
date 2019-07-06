# -*- coding: utf-8 -*-
from common.log import logger
import json
from conf.default import APP_ID, OWNER_ID, cmdb_host
import requests
import ssl


ssl._create_default_https_context = ssl._create_unverified_context

def http_request(url, j_data, method):
    rs = requests.session()
    rs.headers['Content-Type'] = 'application/json'
    rs.headers['HTTP_BlUEKING_SUPPLIER_ID'] = 0
    rs.headers['BK_USER'] = APP_ID

    rp = rs.request(method, url, data=j_data)

    try:
        return json.loads(rp.content)
    except Exception as e:
        logger.exception("json loads error!, url: %s , rq_data: %s , rp_content: %s" % (url, j_data, rp.content))
        return {"result": False, "bk_error_msg": "请求外部接口失败，详情请查看APP日志"}


def is_host(obj_id):
    return obj_id == "Linux" or obj_id == "Windows" or obj_id == "AIX"


# post请求cmdb api_server接口
def http_post(url, data):
    json_data = json.dumps(data)
    headers = {
        "Content-Type": "application/json",
        "HTTP_BlUEKING_SUPPLIER_ID": OWNER_ID,
        "BK_USER": "admin"
    }
    rp = requests.post(url=url, data=json_data, headers=headers,verify=False)
    if rp.status_code != 200:
        logger.error("http_post error, url:{0}, request_data:{1}, status_code:{2}, content: {3}".format(
            url, data, rp.status_code, rp.content))
        try:
            message = json.loads(rp.content)['bk_error_msg']
        except:
            message = rp.content
        return {"result": False, "message": message}
    try:
        result = json.loads(rp.content)
        return result
    except:
        return {"result": False, "message": rp.content}


# 查询实例
def search_inst(bk_inst_name, BK_OBJ_ID):
    data = {
        "condition": {
            BK_OBJ_ID: [{
                "field": "bk_inst_name",
                "operator": "$eq",
                "value": bk_inst_name
            }]
        }
    }
    url = cmdb_host + '/api/v3/inst/association/search/owner/{0}/object/{1}'.format(OWNER_ID, BK_OBJ_ID)
    res = http_post(url, data)
    if not res["result"]:
        return []
    return res["data"]["info"]


# 添加实例
def create_inst(BK_OBJ_ID, data):
    url = cmdb_host + "/api/v3/inst/{0}/{1}".format(OWNER_ID, BK_OBJ_ID)
    return http_post(url, data)


def http_cmdb_post(data, url):
    is_connect = check_cmdb_status()
    if not is_connect:
        return {"result": False, "bk_error_msg": "cmdb is not connect"}
    res = http_post(url, data)
    return res


# 检验cmdb连通性
def check_cmdb_status():
    url = cmdb_host + "/api/v3/biz/search/" + str(OWNER_ID)
    res = http_post(url, {})
    if not res['result']:
        return False
    return True
