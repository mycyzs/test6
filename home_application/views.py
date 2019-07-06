# -*- coding: utf-8 -*-

from common.mymako import render_mako_context
from home_application.sysinfo import *
from home_application.all_api import *
def home(request):
    """
    首页
    """
    return render_mako_context(request, '/home_application/js_factory.html')


