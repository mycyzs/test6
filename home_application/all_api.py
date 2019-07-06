# -*- coding:utf-8 -*-
import copy
import datetime
import json

from blueking.component.shortcuts import get_client_by_request, get_client_by_user
from common.log import logger
from common.mymako import render_json
from conf.default import APP_ID, APP_TOKEN


# 获取平台所有模型
def search_init(request):
    try:
        client = get_client_by_user(request.user.username)
        param = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": 'admin'
        }
        result = client.cc.search_classifications(param)
        data_list = []
        if result['result']:
            for i in result['data']:
                data_list.append({
                    "id": i['bk_classification_id'],
                    "text": i['bk_classification_name']
                })
        return render_json({'result':True,'data':data_list})
    except Exception as e:
        logger.error(e)


# 获取该模型分类下的所有模型
def search_objects(request):
    try:
        client = get_client_by_user(request.user.username)
        param = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": 'admin',
            'bk_classification_id':'database'
        }
        result = client.cc.search_all_objects(param)
        data_list = []
        if result['result']:
            for i in result['data']:
                data_list.append({
                    "id": i['bk_obj_id'],
                    "text": i['bk_obj_name']
                })
        return render_json({'result':True,'data':data_list})
    except Exception as e:
        logger.error(e)


# 获取该模型下所有的实例
def search_inst(request):
    try:
        client = get_client_by_user(request.user.username)
        param = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": 'admin',
            'bk_obj_id':'mssql',
            'condition':{},
            'bk_supplier_account':'0'
        }
        result = client.cc.search_inst(param)
        inst_data = {}
        if result['result']:
            inst_data = {'inst_id':result['data']['info'][0]['bk_inst_id']}
        return render_json({'result':True,'data':inst_data})
    except Exception as e:
        logger.error(e)


# 根据实例名获取实例详情
def search_inst_detail(request):
    try:
        client = get_client_by_user(request.user.username)
        param = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": 'admin',
            "bk_obj_id": "mssql",
            "page": {"start": 0, "limit": 0, "sort": "-bk_inst_id"},
            "fields": {},
            "condition": {'bk_inst_name': 'mssql-192.168.169.22'}
        }
        result = client.cc.search_inst_by_object(param)
        inst_data = {}
        if result['result']:
            inst_data = {'inst_id':result['data']['info'][0]['bk_inst_id']}
        return render_json({'result':True,'data':inst_data})
    except Exception as e:
        logger.error(e)


# 查询所有的业务
def search_buseness(request):
    try:
        client = get_client_by_user(request.user.username)
        param = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": 'admin'
        }
        result = client.cc.search_business(param)
        user_business_list = []
        if result["result"]:
            user_business_list = [
                {"id": i["bk_biz_id"], "text": i["bk_biz_name"]} for i in result["data"]["info"]

            ]
        return render_json({"result": True, "data": user_business_list})
    except Exception as e:
        logger.error(e)


# 查询业务下的所有主机
def search_app_host(request):
    try:
        client = get_client_by_user(request.user.username)
        kwargs = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": 'admin',
            "ip" : {"flag": "bk_host_innerip|bk_host_outerip","exact": 1,"data": []},

            "condition": [
            {
                "bk_obj_id": "biz",
                "fields": [
                    "default",
                    "bk_biz_id",
                    "bk_biz_name",
                ],
                # 根据业务ID查询主机
                "condition": [
                    {
                        "field": "bk_biz_id",
                        "operator": "$eq",
                        "value": 2
                    }
                ]
            }
        ]
        }
        result = client.cc.search_host(kwargs)
        host_list = []
        if result["result"]:
            for i in result['data']['info']:
                host_list.append({
                    'id':i['host']['bk_host_id'],
                    'text':i['host']['bk_host_innerip'],
                    'app_id': i['biz'][0]['bk_biz_id'],
                    'cloud_id': i['host']['bk_cloud_id'][0]['id']
                })
        return render_json({"result": True, "data": host_list})
    except Exception as e:
        logger.error(e)


# 根据查询条件查询主机
def select_search_host(request):
    try:
        requst_data = json.loads(request.body)
        select_value = requst_data['select_value']
        if requst_data['select_o'] == 'operator':
            select_value = [requst_data['select_value']]
        client = get_client_by_user(request.user.username)
        kwargs = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": 'admin',
            "ip" : {"flag": "bk_host_innerip|bk_host_outerip","exact": 1,"data": []},
            'bk_biz_id': int(requst_data['biz']),
            "condition": [
            {
                "bk_obj_id": "biz",
                "fields": [],
                # 根据业务ID查询主机
                "condition": []
            },
            {
                "bk_obj_id": "host",
                "fields": [],
                "condition": [{"field": requst_data['select_o'],"operator": "$regex","value": select_value}]
            },

            {
            "bk_obj_id": "module",
            "fields": [],
            "condition": []
        },
        {
            "bk_obj_id": "set",
            "fields": [],
            "condition": []
        },
        ]
        }
        result = client.cc.search_host(kwargs)
        host_list = []
        if result["result"]:
            for i in result['data']['info']:
                host_list.append({
                    'id':i['host']['bk_host_id'],
                    'bk_host_innerip':i['host']['bk_host_innerip'],
                    'area': i['host']['bk_cloud_id'][0]['bk_inst_name'],
                    'module': [j['bk_module_name'] for j in i['module']][0] if [j['bk_module_name'] for j in i['module']] else '',
                    'agent_status': ''
                })
        return render_json({"result": True, "data": host_list})
    except Exception as e:
        logger.error(e)



# 查询业务下的所有主机,显示集群、模块信息
def search_all_host(request):
    try:
        requst_data = json.loads(request.body)
        client = get_client_by_user(request.user.username)
        kwargs = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": 'admin',
            "ip" : {"flag": "bk_host_innerip|bk_host_outerip","exact": 1,"data": []},

            "condition": [
            {
                "bk_obj_id": "biz",
                "fields": [
                    "default",
                    "bk_biz_id",
                    "bk_biz_name",
                ],
                # 根据业务ID查询主机
                "condition": [
                    {
                        "field": "bk_biz_id",
                        "operator": "$eq",
                        "value": int(requst_data['biz'])
                    }
                ]
            },

            {
            "bk_obj_id": "module",
            "fields": [],
            "condition": []
        },
        {
            "bk_obj_id": "set",
            "fields": [],
            "condition": []
        },
        ]
        }
        result = client.cc.search_host(kwargs)
        host_list = []
        if result["result"]:
            for i in result['data']['info']:
                host_list.append({
                    'id':i['host']['bk_host_id'],
                    'bk_host_innerip':i['host']['bk_host_innerip'],
                    'area': i['host']['bk_cloud_id'][0]['bk_inst_name'],
                    'module': [j['bk_module_name'] for j in i['module']][0] if [j['bk_module_name'] for j in i['module']] else '',
                    #'agent_status': u'正常' if get_host_agent(request.user.username, i['host']['bk_host_innerip'], i['host']['bk_cloud_id'][0]['bk_inst_id']) else u'异常',
                })
        return render_json({"result": True, "data": host_list})
    except Exception as e:
        logger.error(e)


# 查询不属于该业务下所有主机
def search_all_host_by_biz(request):
    try:
        client = get_client_by_user(request.user.username)
        kwargs = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": 'admin',
            "ip" : {"flag": "bk_host_innerip|bk_host_outerip","exact": 1,"data": []},
            "condition": [
                {
                    "bk_obj_id": "biz",
                    "fields": [
                        "default",
                        "bk_biz_id",
                        "bk_biz_name",
                    ],
                    # 根据业务ID查询主机
                    "condition": [{"field":"bk_biz_id","operator":"$nin","value":6}]
                }
            ]
        }
        result = client.cc.search_host(kwargs)
        host_list = []
        if result["result"]:
            for i in result['data']['info']:
                host_list.append({
                    'id':i['host']['bk_host_id'],
                    'text':i['host']['bk_host_innerip']
                })
        return render_json({"result": True, "data": host_list})
    except Exception as e:
        logger.error(e)

os_type = {'1':'Linux','2':'Windows'}


# 根据ip查询主机信息
def search_host_by_ip(request):
    try:
        client = get_client_by_user(request.user.username)
        kwargs = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": 'admin',
            "ip" : {"flag": "bk_host_innerip|bk_host_outerip","exact": 1,"data": ['192.168.165.51']},
            "condition": [
                {
                    "bk_obj_id": "biz",
                    "fields": [
                        "default",
                        "bk_biz_id",
                        "bk_biz_name",
                    ],
                    "condition": []
                }
            ]
        }
        result = client.cc.search_host(kwargs)
        d={}
        if result["result"]:
            d = {}

        return render_json({"result": True, "data": d})
    except Exception as e:
        logger.error(e)


# 饼图
def get_count_obj(request):
    data_list = [
        {'name':"test1",'y':10},
        {'name':"test2",'y':20}
    ]

    return render_json({'result':True,'data':data_list})


# 折线图
def get_count(request):
    date_now = datetime.datetime.now() + datetime.timedelta(hours=-1)
    time_now = datetime.datetime.now()
    when_created__gt = str(date_now).split(".")[0]
    time_n = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    # 存的时候
    # when_created = str(datetime.datetime.now()).split(".")[0]
    # 数据库读取的时候
    # when_created__gt = str(date_now).split(".")[0]

    install_list = [
        {"name": u"本月MySQL新增数", "data": [3,6,8,9]},
        {"name": u"本月Oracle新增数", "data": [1,4,7,10]}
    ]
    return render_json({'result':True,'data':install_list,'cat':['1','2','3','4']})



def get_count_zhu(request):
    data = [
        {'name': 'Windows服务器', 'data': [1]},
        {'name': 'AD服务器', 'data': [3], 'color': "#4cb5b0"},
        {'name': 'TEST服务器', 'data': [5]}
    ]

    return render_json({'result':True,'data':data})



# 获取topo树，展示所有的业务，只显示集群和模块
def search_topo(request):
    try:
        request_data = json.loads(request.body)

        client = get_client_by_user(request.user.username)


        topo = []
        for k in request_data['biz_list']:

            kwargs = {
                "bk_app_code": APP_ID,
                "bk_app_secret": APP_TOKEN,
                "bk_username": 'admin',
                "bk_biz_id": int(k['id'])
            }
            result = client.cc.search_biz_inst_topo(kwargs)

            if result["result"]:
                global topo_list
                topo_list = []
                # need_data = []
                # for child in result['data']:
                #     if
                get_inst_of_same_level(result['data'])
                topo.append({"id": int(k['id']), "name": k['text'], "bk_obj_id": "biz","isParent": 'true', 'children': copy.deepcopy(topo_list)})

        return render_json({"result": True, "data": topo})
    except Exception as e:
        logger.error(e)


def get_inst_of_same_level(children):
    """获取所有的层级"""

    for child in children:
        child["id"] = child['bk_inst_id']
        child.pop("bk_inst_id", None)
        child['name'] = child['bk_inst_name']
        child.pop("bk_inst_name")
        child.pop('bk_obj_name')
        child.pop('default')
        child['children'] = child['child']
        child.pop("child")
        if child['children']:
            child['isParent'] = 'true'
        else:
            child['isParent'] = 'false'
        if child['bk_obj_id'] == 'set':
            topo_list.append(child)
        get_inst_of_same_level(child['children'])


#根据业务展示该业务topo树
def search_topo_by_biz(request):
    try:
        request_data = json.loads(request.body)

        client = get_client_by_user(request.user.username)

        kwargs = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": 'admin',
            "bk_biz_id": int(request_data['biz_id'])
        }
        result = client.cc.search_biz_inst_topo(kwargs)

        if result["result"]:
            get_inst_of_same_level_biz(result['data'])

        return render_json({"result": True, "data": result['data']})
    except Exception as e:
        logger.error(e)


def get_inst_of_same_level_biz(children):
    """获取所有的层级"""

    for child in children:
        child["id"] = child['bk_inst_id']
        child.pop("bk_inst_id", None)
        child['name'] = child['bk_inst_name']
        child.pop("bk_inst_name")
        child.pop('bk_obj_name')
        child.pop('default')
        child['children'] = child['child']
        child.pop("child")
        if child['children']:
            child['isParent'] = 'true'
        else:
            child['isParent'] = 'false'
        get_inst_of_same_level_biz(child['children'])


#获取节点下的所有主机
def search_host_by_node(request):
    try:
        requst_data = json.loads(request.body)
        select_value = requst_data['select_value']
        # if requst_data['select_o'] == 'operator':
        #     select_value = [requst_data['select_value']]
        client = get_client_by_user(request.user.username)
        kwargs = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": 'admin',
            "ip" : {"flag": "bk_host_innerip|bk_host_outerip","exact": 1,"data": []},
            'bk_biz_id': int(requst_data['biz']),
            "condition": [
            {
                "bk_obj_id": "biz",
                "fields": [],
                # 根据业务ID查询主机
                "condition": []
            },
            {
                "bk_obj_id": "host",
                "fields": [],
                # "condition": [{"field": requst_data['select_o'],"operator": SELECT_TYPE.get(requst_data['select_o'], "$regex"),"value": select_value}] if requst_data['select_o'] else []
            },

            {
            "bk_obj_id": "module",
            "fields": [],
            "condition": []
        },
        {
            "bk_obj_id": "set",
            "fields": [],
            "condition": []
        },
        ]
        }

        if requst_data['bk_obj_id']:
            if requst_data['bk_obj_id'] == 'module':
                kwargs['condition'][2]['condition'].append({'field': "bk_module_id", 'operator': "$eq", 'value': int(requst_data['value'])})

            elif requst_data['bk_obj_id'] == 'set':
                kwargs['condition'][3]['condition'].append(
                    {'field': "bk_set_id", 'operator': "$eq", 'value': int(requst_data['value'])})
            elif requst_data['bk_obj_id'] == 'biz':
                pass
            else:
                kwargs['condition'].append({'bk_obj_id': "object", 'condition': [{'field': "bk_inst_id", 'operator': "$eq", 'value': int(requst_data['value'])}], 'fields': []})
        result = client.cc.search_host(kwargs)
        host_list = []
        if result["result"]:
            for i in result['data']['info']:
                host_list.append({
                    'id':i['host']['bk_host_id'],
                    'bk_host_innerip':i['host']['bk_host_innerip'],
                    'area': i['host']['bk_cloud_id'][0]['bk_inst_name'],
                    'module': [j['bk_module_name'] for j in i['module']][0] if [j['bk_module_name'] for j in i['module']] else '',
                    # 'agent_status': u'正常' if get_host_agent(request.user.username, i['host']['bk_host_innerip'],
                    #                                         i['host']['bk_cloud_id'][0]['bk_inst_id']) else u'异常',
                })
        return render_json({"result": True, "data": host_list})
    except Exception as e:
        logger.error(e)







