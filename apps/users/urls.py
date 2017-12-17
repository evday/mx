#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2017-12-17,22:35"

from django.conf.urls import url
from users.views import UserInfoView

urlpatterns = [
    #用户信息
    url(r'^info/$',UserInfoView.as_view(),name='user_info'),


]