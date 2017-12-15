#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2017-12-15,20:14"

from django.conf.urls import url

from courses.views import CourseListView,CourseDetailView

urlpatterns = [
    #课程列表页面
    url(r'^list/$',CourseListView.as_view(),name='org_list'),

    #课程详情页面
    url(r'^detail/(?P<course_id>\d+)/$',CourseDetailView.as_view(),name='course_detail'),

]