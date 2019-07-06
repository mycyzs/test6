# -*-coding:utf-8-*-
import json

import httplib2
import requests
from common.log import logger
from common.mymako import render_json
from conf.default import BK_PAAS_HOST, APP_ID, APP_TOKEN, cmdb_host
# 获取模型分类
from home_application import utils




# 匹配中英文字段
def map_json(obj_id):
    try:
        url = cmdb_host + '/api/v3/object/attr/search'
        post_data = {"bk_obj_id": obj_id, "bk_supplier_account": "0"}
        j_data = json.dumps(post_data)
        d_result = utils.http_request(url, j_data, 'POST')
        if not d_result['result']:
            return False, {}
        data_mapping = {}
        for i in d_result['data']:
            if (i['bk_property_type'] == i['bk_property_type'] == "singleasst" or i['bk_property_type']=="multiasst"):
                continue
            data_mapping[i['bk_property_id']] = i['bk_property_name']
        return True, data_mapping
    except Exception as e:
        logger.exception("error:{0}".format(e.message))
        return False, {}



def get_config_class(request):
    try:
        http = httplib2.Http()
        url = BK_PAAS_HOST + "/api/c/compapi/v2/cc/search_classifications/"
        param = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": 'admin'
        }
        headers = {'Content-type': 'application/json'}
        response, content = http.request(url, 'POST', headers=headers, body=json.dumps(param))
        if response['status'] == "200":
            res_data = json.loads(content)
            class_list = [{'name': i['bk_classification_name'], 'value': i['bk_classification_id']} for i in
                             res_data['data']]
            # name_list = [i['bk_classification_name'] for i in res_data['data']]
            class_list = class_list[3:]
            class_list.insert(0,{"name": "主机管理", "value": "bk_host_manage"})
            return render_json({"result": True, "data": class_list})
        else:
            return render_json({"result": False, "msg": 'error'})
    except Exception as e:
        logger.exception("error:{0}".format(e.message))
        return render_json({"result": False, "msg": 'error'})


# 获取该分类下的所有模型
def get_config_item(request):
    req_data = json.loads(request.body)
    try:
        class_id = req_data['class_id']
        http = httplib2.Http()
        url = BK_PAAS_HOST + "/api/c/compapi/v2/cc/search_objects/"
        param = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": "admin",
            "bk_classification_id": class_id
        }
        headers = {'Content-type': 'application/json'}
        response, content = http.request(url, 'POST', headers=headers, body=json.dumps(param))
        if response['status'] == "200":
            res_data = json.loads(content)
            item_list = [{'name': i['bk_obj_name'], 'value': i['bk_obj_id']} for i in
                        res_data['data']]
            if class_id == 'bk_host_manage':
                item_list = item_list[0:1]
                item_list[0]['name'] = "主机"
            return render_json({"result": True, "data": item_list})
        else:
            return render_json({"result": False, "msg": 'error'})
    except Exception as e:
        logger.exception("error:{0}".format(e.message))
        return render_json({"result": False, "msg": 'error'})


# def jj():
#     if obj_id == 'host':
#         ip = re_data['ip']
#         url = cmdb_host + '/api/v3/hosts/search'
#         post_data = {"page": {"start": 0, "limit": 0, "sort": "bk_host_id"}, "pattern": "",
#                      "ip": {"flag": "bk_host_innerip", "exact": 0, "data": [ip]},
#                      "condition": [{"bk_obj_id": "host", "fields": [], "condition": []},
#                                    {"bk_obj_id": "module", "fields": [], "condition": []},
#                                    {"bk_obj_id": "set", "fields": [], "condition": []},
#                                    {"bk_obj_id": "biz", "fields": [], "condition": []}]}
#         j_data = json.dumps(post_data)
#         d_result = utils.http_request(url, j_data, 'POST')
#         search_list = []
#         if not d_result['result']:
#             return render_json({'result': False, 'msg': "search error！{0}".format(d_result['message'])})
#         else:
#             info = d_result['data']['info']
#         search_list = [{'host_id': i['host']["bk_host_id"], 'obj_id': 'host', "ip": i['host']['bk_host_innerip'],
#                         'name': i['host']['bk_host_name'],
#                         'biz': ','.join([j['bk_biz_name'] for j in i['biz']])} for i in info]


# 获取该模型下所有的实例
def get_config_inst(request):
    try:
        re_data = json.loads(request.body)
        item_id = re_data['item_id']
        url = cmdb_host + '/api/v3/inst/association/search/owner/0/object/{0}'.format(item_id)
        post_data = {
            "page": {"start": 0, "limit": 0, "sort": "-bk_inst_id"},
            "fields": {},
            "condition": {}
        }
        j_data = json.dumps(post_data)
        d_result = utils.http_request(url, j_data, 'POST')
        if not d_result['result']:
            return render_json({"result": False, "msg": 'error'})
        else:
            info = d_result['data']['info']
            if item_id == 'host':
                inst_list = [{"name": i['bk_host_innerip'], "value": i['bk_host_innerip']} for i in info]
            else:
                inst_list = [{'value': i['bk_inst_name'], 'inst_id': i['bk_inst_id'], 'name': i["bk_inst_name"]} for i in info]
        return render_json({"result": True, "data": inst_list})
    except Exception as e:
        logger.exception("get host list error:{0}".format(e.message))
        return render_json({"result": False, "msg": 'error'})


# 获取实例详情
def get_inst_detail(request):
    try:
        re_data = json.loads(request.body)
        obj_id = re_data['obj_id']
        url = cmdb_host + '/api/v3/inst/association/search/owner/0/object/{0}'.format(obj_id)
        inst_name = re_data['inst_name']
        post_data = {
            "page": {"start": 0, "limit": 0, "sort": "-bk_inst_id"},
            "fields": {},
            "condition": {obj_id: [{"field": "bk_inst_name", "operator": "$regex", "value": inst_name}]}
        }
        j_data = json.dumps(post_data)
        d_result = utils.http_request(url, j_data, 'POST')
        if not d_result['result']:
            return render_json({'result': False, 'msg': "search error！{0}".format(d_result['message'])})
        else:
            info = d_result['data']['info']
        search_list = [{'inst_id': i['bk_inst_id'], 'obj_id': i['bk_obj_id'], 'inst_name': i["bk_inst_name"]} for i in
                       info]
        return render_json({'result': True, 'data': search_list})

    except Exception as e:
        logger.exception("get host list error:{0}".format(e.message))
        return render_json({'result': False, 'msg': "系统异常！"})


# 获取对象属性
def get_obj_field(request):
    try:
        re_data = json.loads(request.body)
        item_id = re_data['item_id']
        http = httplib2.Http()
        url = BK_PAAS_HOST + '/api/c/compapi/v2/cc/search_object_attribute/'
        param = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": "admin",
            "bk_supplier_account": "0",
            "bk_obj_id": item_id,
        }
        headers = {'Content-type': 'application/json'}
        response, content = http.request(url, 'POST', headers=headers, body=json.dumps(param))
        if response['status'] == "200":
            res_data = json.loads(content)
            field_list = []
            data_dict = {}
            for i in res_data['data']:
                if i['bk_property_type'] == "singleasst" or i['bk_property_type'] == "multiasst":
                    continue
                data_dict[i['bk_property_id']] = i['bk_property_name']
            res, mapping = map_json(item_id)
            if res:
                for k, v in data_dict.items():
                    if k not in mapping:
                        continue
                field_list.append({'name': mapping[k], 'value': k})
            else:
                for k, v in data_dict.items():
                    field_list.append({"name": v, "value": k})
            return render_json({"result": True, "data": field_list})
        else:
            return render_json({"result": False, "msg": 'error'})
    except Exception as e:
        logger.exception("get field list error:{0}".format(e.message))
        return render_json({"result": False, "msg": 'error'})


# 获取实例详情
def get_data(config_kv):
    try:
        obj_id = config_kv['config_item']
        inst_name = config_kv['config_inst']
        if obj_id == '' or inst_name == '':
            return False, '缺少obj_id或者inst_name'

        if obj_id == 'host':
            url = cmdb_host + '/api/v3/hosts/search'
            post_data = {"page": {"start": 0, "limit": 0, "sort": "bk_host_id"}, "pattern": "",
                         "ip": {"flag": "bk_host_innerip|bk_host_outerip", "exact": 1, "data": [inst_name]},
                         "condition": [{"bk_obj_id": "host", "fields": [], "condition": []},
                                       {"bk_obj_id": "module", "fields": [], "condition": []},
                                       {"bk_obj_id": "set", "fields": [], "condition": []},
                                       {"bk_obj_id": "biz", "fields": [], "condition": []}]}

            j_data = json.dumps(post_data)
            d_result = utils.http_request(url, j_data, 'POST')
            if not d_result['result']:
                return False, "search host detail error！{0}".format(d_result['message'])
            detail = []
            obj = d_result['data']['info'][0]
            res, mappings = map_json(obj_id)
            if res:
                for (k, v) in obj['host'].items():
                    if k not in mappings:
                        continue
                    detail.append({
                        "value": str(v) if v else "",
                        "name": mappings[k]
                    })
            else:
                for k, v in obj['host'].items():
                    detail.append({
                        "name": 'error',
                        "value": str(v) if v else ""
                    })
            detail_dict = {
                "name": inst_name,
                "brief": "",
                "detail": detail
            }
        else:
            url = cmdb_host + '/api/v3/inst/association/search/owner/0/object/{0}'.format(obj_id)
            post_data = {
                "page": {"start": 0, "limit": 0, "sort": "-bk_inst_id"},
                "fields": {},
                "condition": {obj_id: [{"field": "bk_inst_name", "operator": "$regex", "value": inst_name}]}
            }
            j_data = json.dumps(post_data)
            d_result = utils.http_request(url, j_data, 'POST')
            if not d_result['result']:
                return False, "search inst detail error！{0}".format(d_result['message'])
            detail = []
            info = d_result['data']['info'][0]
            res, mappings = map_json(obj_id)
            if res:
                for (k, v) in info.items():
                    if k not in mappings:
                        continue
                    detail.append({
                        "value": str(v) if v else "",
                        "name": mappings[k]
                    })
            else:
                for k, v in info.items():
                    detail.append({
                        "name": 'error',
                        "value": str(v) if v else ""
                    })
            detail_dict = {
                "name": inst_name,
                "brief": "",
                "detail": detail
            }
        return True, detail_dict
    except Exception as e:
        logger.exception("get inst detail error:{0}".format(e.message))
        return False, e.message