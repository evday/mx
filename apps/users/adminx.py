#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Author:沈中秋
#date:"2017-10-27,19:35"
import xadmin

from xadmin import views
from xadmin.plugins.auth import UserAdmin
from xadmin.layout import Fieldset,Main,Side,Row

from .models import EmailVerifyRecord,Banner,UserProfile




class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = '后台管理系统'
    site_footer = '幕学在线网'
    menu_style = 'accordion'

class EmailVerifyRecordAdmin(object):
    list_display = ['code','email','send_type','send_time']
    search_fields = ['code','email','send_type']
    list_filter = ['code','email','send_type','send_time']
    model_icon = 'fa fa-envelope'

class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index','add_time']
    search_fields =  ['title', 'image', 'url', 'index']
    list_filter =  ['title', 'image', 'url', 'index','add_time']

xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)

xadmin.site.register(views.BaseAdminView,BaseSettings)
xadmin.site.register(views.CommAdminView,GlobalSettings)
