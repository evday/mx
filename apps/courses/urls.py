#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2017-12-15,20:14"

from django.conf.urls import url

from courses.views import CourseListView,CourseDetailView,CourseInfoView,CommentView,AddComments,VideoPlayView

urlpatterns = [
    #课程列表页面
    url(r'^list/$',CourseListView.as_view(),name='org_list'),

    #课程详情页面
    url(r'^detail/(?P<course_id>\d+)/$',CourseDetailView.as_view(),name='course_detail'),


    url(r'^info/(?P<course_id>\d+)/$',CourseInfoView.as_view(),name='course_info'),

    #课程评论
    url(r'^comment/(?P<course_id>\d+)/$',CommentView.as_view(),name='course_comments'),
    #添加课程评论
    url(r'^add_comment/$',AddComments.as_view(),name='add_comment'),

    #课程视频
    url(r'^video/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name='video_play'),

]