services = angular.module('webApiService', ['ngResource', 'utilServices']);

//生产代码
var POST = "POST";
var GET = "GET";

//测试代码
//var sourceRoute = "./Client/MockData";
//var fileType = ".html";
//var POST = "GET";
//var GET = "GET";
services.factory('sysService', ['$resource', function ($resource) {
    return $resource(site_url + ':actionName/', {},
        {
            search_sys_info: {method: POST, params: {actionName: 'search_sys_info'}, isArray: false},
            add_sys: {method: POST, params: {actionName: 'add_sys'}, isArray: false},
            modify_sys: {method: POST, params: {actionName: 'modify_sys'}, isArray: false},
            delete_sys: {method: POST, params: {actionName: 'delete_sys'}, isArray: false},
            search_init: {method: POST, params: {actionName: 'search_init'}, isArray: false},
            get_count_obj: {method: POST, params: {actionName: 'get_count_obj'}, isArray: false},
            get_count: {method: POST, params: {actionName: 'get_count'}, isArray: false},
            get_count_zhu: {method: POST, params: {actionName: 'get_count_zhu'}, isArray: false},
            up_csv: {method: POST, params: {actionName: 'up_csv'}, isArray: false},
            search_topo: {method: POST, params: {actionName: 'search_topo'}, isArray: false},
            search_host_by_node: {method: POST, params: {actionName: 'search_host_by_node'}, isArray: false},
        });
}])


;//这是结束符，请勿删除