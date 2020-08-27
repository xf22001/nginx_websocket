# -*- coding: utf-8 -*-
#!/usr/bin/env python
#================================================================
#   
#   
#   文件名称：urls.py
#   创 建 者：肖飞
#   创建日期：2020年08月26日 星期三 13时39分24秒
#   修改日期：2020年08月26日 星期三 14时24分46秒
#   描    述：
#
#================================================================
import sys
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index$', views.index, name='index'),
    url(r'^(?P<page>\w+)/$', views.index, name='page'),
]

def main(argv):
    pass

if '__main__' == __name__:
    main(sys.argv[1:])
