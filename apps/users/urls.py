#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2017-12-17,22:35"

from django.conf.urls import url
from users.views import UserInfoView,UploadImageView,UpdatePwdView,SendEmailView,UpdateEmailView,MyCourseView,MyOrgFivView,MyTeacherFivView,MyCourseFivView,MyMessageView

urlpatterns = [
    #用户信息
    url(r'^info/$',UserInfoView.as_view(),name='user_info'),

    # 用户头像上传
    url(r'^image/upload/$', UploadImageView.as_view(), name='image_upload'),
    #用户个人中心密码修改
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),
    #发送邮箱验证码

    url(r'^sendemail_code/$', SendEmailView.as_view(), name='sendemail_code'),
    #修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),

    #我的课程
    url(r'^my_course/$', MyCourseView.as_view(), name='my_course'),

    #课程收藏
    url(r'^my_fav/$', MyOrgFivView.as_view(), name='my_fav'),

    #讲师收藏
    url(r'^my_fav_teacher/$', MyTeacherFivView.as_view(), name='my_fav_teacher'),
    #课程收藏
    url(r'^my_fav_course/$', MyCourseFivView.as_view(), name='my_fav_course'),
    #我的消息
    url(r'^my_message/$', MyMessageView.as_view(), name='my_message'),



]