# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'home_application.views',
    (r'^$', 'home'),
    (r'^api/test$', 'test'),
    (r'^search_sys_info$', 'search_sys_info'),
    (r'^add_sys$', 'add_sys'),
    (r'^modify_sys$', 'modify_sys'),
    (r'^delete_sys$', 'delete_sys'),
    (r'^search_init$', 'search_buseness'),
    (r'^get_count_obj$', 'get_count_obj'),  # 圆饼图
    (r'^get_count$', 'get_count'),   # 折线图
    (r'^get_count_zhu$', 'get_count_zhu'),  # 柱状图



    # 额外的路由
    (r'^upload_pic/$', 'upload_pic'),
    (r'^upload_info/$', 'upload_info'),
    (r'^down_load_field/$', 'down_load_field'),
    (r'^up_excel/$', 'up_excel'),
    (r'^down_excel/$', 'down_excel'),
    (r'^down_csv/$', 'down_csv'),
    (r'^up_csv$', 'up_csv'),
    (r'^search_topo$', 'search_topo_by_biz'),
    (r'^search_host_by_node$', 'search_host_by_node'),

)
