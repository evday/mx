#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Author:沈中秋
#date:"2017-11-03,18:49"
from random import choice
from users.models import EmailVerifyRecord
from django.core.mail import send_mail
from mxonline.settings import EMAIL_FROM

def random_str(random_length=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'

    for i in range(random_length):
        str+= choice(chars)
    return str

def send_register_email(email,send_type='register'):


    email_recode = EmailVerifyRecord()
    if send_type == 'update_email':

        code=random_str(4)

    else:
        code = random_str(16)

    email_recode.code = code

    email_recode.email = email
    email_recode.send_type = send_type

    email_recode.save()
    print('+++++++++++++++++')


    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = "幕学在线网在线注册激活链接"
        email_body = '请点击下面的链接激活你的账号：http://127.0.0.1:8000/active/{0}'.format(code)

        send_status =send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass
    elif send_type == 'forget':
        email_title = '重置密码链接'
        email_body = '请点击下面的链接重置你的密码：http://127.0.0.1:8000/reset/{0}'.format(code)
        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass

    elif send_type == 'update_email':
        email_title = '修改邮箱链接'
        email_body = '你的邮箱验证码为：{0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass