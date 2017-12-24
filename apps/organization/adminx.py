#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Author:沈中秋
#date:"2017-10-30,15:40"

import xadmin

from .models import CityDict,CourseOrg,Teacher

class CityDictAdmin(object):


    list_display = ['name', 'desc','add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc','add_time']


class CourseOrgAdmin(object):


    list_display = ['name', 'desc','click_nums','fav_nums','image','address','city','add_time']
    search_fields = ['name', 'desc','click_nums','fav_nums','image','address','city',]
    list_filter = ['name', 'desc','click_nums','fav_nums','image','address','city__name','add_time']
    relfield_style = 'fk-ajax'


class TeacherAdmin(object):


    list_display = ['org','name', 'work_year', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'add_time']
    search_fields = ['org','name', 'work_year', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'add_time']
    list_filter = ['org__name','name', 'work_year', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'add_time']


xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(Teacher,TeacherAdmin)