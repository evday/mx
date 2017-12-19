#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2017-12-17,22:35"

from django.conf.urls import url
from users.views import UserInfoView,UploadImageView,UpdatePwdView,SendEmailView,UpdateEmailView

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





]