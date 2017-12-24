#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2017-12-24,15:52"

import xadmin
from xadmin.views import BaseAdminPlugin,CreateAdminView,ModelFormAdminView,UpdateAdminView
from DjangoUeditor.models import UEditorField
from DjangoUeditor.widgets import UEditorWidget
from django.conf import settings

class XAdminUEditorWidget(UEditorWidget):
    def __init__(self,**kwargs):
        self.ueditor_options = kwargs
        self.Media.js  = None
        super(XAdminUEditorWidget,self).__init__(kwargs)
class UEditorPlugin(BaseAdminPlugin):
    def get_field_style(self,attrs,db_field,style,**kwargs):
        if style == "ueditor":
            if isinstance(db_field,UEditorField):
                widget = db_field.formfield().widget
                param = {}
                param.update(widget.ueditor_settings)
                param.update(widget.attrs)
                return {"widget":XAdminUEditorWidget(**param)}
        return attrs
    def block_extrahead(self,context,nodes):
        js = "<script type='text/javascript' src = '%s'></script>"%(settings.STATIC_URL+"ueditor/ueditor.config.js")
        js += "<script type='text/javascript' src = '%s'></script>"%(settings.STATIC_URL+"ueditor/ueditor.all.min.js")
        nodes.append(js)
xadmin.site.register_plugin(UEditorPlugin,UpdateAdminView)
xadmin.site.register_plugin(UEditorPlugin,CreateAdminView)