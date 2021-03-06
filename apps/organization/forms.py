#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Author:沈中秋
#date:"2017-12-04,9:17"
import re

from django import forms

from operation.models import UserAsk

class UserAskForm(forms.ModelForm): #django 的modelform 方法
    class Meta:
        model = UserAsk  #关联的model对象
        fields = ["name","mobile","course_name"]

    def clean_mobile(self):
        mobile = self.cleaned_data["mobile"]
        REGEX_MOBILE= "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号非法",code="mobile_invalid")

