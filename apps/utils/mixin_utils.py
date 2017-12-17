#!/usr/bin/env python
#-*- coding:utf-8 -*-
#date:"2017-12-17,14:57"
#基础类
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):
    @method_decorator(login_required(login_url="/login/"))
    def dispatch(self,request,*args,**kwargs):
        return super(LoginRequiredMixin,self).dispatch(request,*args,**kwargs)


