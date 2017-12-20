# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.core.urlresolvers import reverse
from django.shortcuts import HttpResponse,HttpResponseRedirect


from .models import UserProfile,EmailVerifyRecord
from operation.models import UserMessage
from users.forms import LoginForm,RegisterForm,ForgetForm,ModifyPwdForm,UploadImageForm,UserForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse,UserFavorite,Course,UserMessage
from organization.models import CourseOrg,Teacher


from pure_pagination import Paginator, EmptyPage, PageNotAnInteger



class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username = username)|Q(email = username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class ActiveUserView(View):
    def get(self,request,active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request,'active_file.html')
        return render(request, 'login.html')


class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request, 'register.html', {"register_form":register_form})
    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email','')

            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {"register_form": register_form,'msg':'用户名已存在'})

            pass_word = request.POST.get('password','')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            # 填写欢迎注册信息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = '欢迎注册慕学在线网'
            user_message.save()


            send_register_email(user_name,'register')
            return render(request, 'login.html')
        else:
            return render(request,'register.html',{"register_form":register_form})
class LogoutView(View):
    '''
    用户登出
    '''
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class LoginView(View):
    def get(self,request):
        return render(request, 'login.html', {})
    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():

            user_name = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=user_name, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {"msg": u"用户未激活"})
            else:
                return render(request, 'login.html', {"msg": u"用户名或密码错误"})

        else:
            return render(request, 'login.html', {"login_form":login_form})


class ForgetPwdView(View):
    def get(self,request):
        forget_form = ForgetForm()
        return render(request,'forgetpwd.html',{"forget_form":forget_form})

    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email",'')
            send_register_email(email,"forget")
            return render(request,"send_success.html")
        else:
            return render(request, 'forgetpwd.html', {"forget_form": forget_form})




class ResetView(View):
    def get(self,request,active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request,'password_reset.html',{"email":email})
        else:
            return render(request,'active_file.html')
        return render(request, 'login.html')

class ModifyPwdView(View):
    '''
    修改用户密码
    '''
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1","")
            pwd2 = request.POST.get("password2","")
            email = request.POST.get("email","")
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {"email": email,"msg":"密码不一致"})
            user= UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()

            return render(request,'login.html')
        else:
            email = request.POST.get("email", "")
            return render(request, 'password_reset.html', {"email": email, "modify_form": modify_form})

class UserInfoView(LoginRequiredMixin, View):
    '''
    用户个人信息
    '''
    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    def post(self,request):
        form = UserForm(data=request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse(json.dumps(form.errors), content_type="application/json")


class UploadImageView(LoginRequiredMixin, View):
    '''
    用户修改头像
    '''
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES,instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"fail"}', content_type="application/json")

class UpdatePwdView(View):
    '''
    修改个人中心密码
    '''
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1","")
            pwd2 = request.POST.get("password2","")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"两次密码不一致"}', content_type="application/json")
            user= request.user
            user.password = make_password(pwd1)
            user.save()

            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:

            return HttpResponse(json.dumps(modify_form.errors), content_type="application/json")


class SendEmailView(LoginRequiredMixin,View):
    '''
    发送邮箱验证码
    '''
    def get(self,request):

        email = request.GET.get("email",'')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已存在"}', content_type="application/json")

        send_register_email(email,"update_email")
        return HttpResponse('{"status":"success"}', content_type="application/json")

class UpdateEmailView(LoginRequiredMixin,View):
    '''
    修改个人邮箱
    '''
    def post(self,request):
        email = request.POST.get("email",'')
        code = request.POST.get("code",'')

        existed_code = EmailVerifyRecord.objects.filter(email=email,code=code,send_type="update_email")
        if existed_code:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse('{"email":"验证码错误"}', content_type="application/json")


class MyCourseView(LoginRequiredMixin,View):
    '''
    我的课程
    '''

    def get(self,request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request,'usercenter-mycourse.html',{
            "user_courses":user_courses
        })


class MyOrgFivView(LoginRequiredMixin,View):
    '''
    我的课程
    '''

    def get(self,request):
        org_list = []
        my_favs = UserFavorite.objects.filter(user=request.user,fav_type=2)
        for my_fav in my_favs:
            org_id = my_fav.fav_id

            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request,'usercenter-fav-org.html',{
            "org_list":org_list
        })

class MyTeacherFivView(LoginRequiredMixin,View):
    '''
    我的课程
    '''

    def get(self,request):
        teacher_list = []
        my_favs = UserFavorite.objects.filter(user=request.user,fav_type=3)
        for my_fav in my_favs:
            teacher_id = my_fav.fav_id

            org = Teacher.objects.get(id=teacher_id)
            teacher_list.append(org)
        return render(request,'usercenter-fav-teacher.html',{
            "teacher_list":teacher_list
        })

class MyCourseFivView(LoginRequiredMixin,View):
    '''
    我的课程
    '''

    def get(self,request):
        course_list = []
        my_favs = UserFavorite.objects.filter(user=request.user,fav_type=1)
        for my_fav in my_favs:
            course_id = my_fav.fav_id

            org =Course.objects.get(id=course_id)
            course_list.append(org)
        return render(request,'usercenter-fav-course.html',{
            "teacher_list":course_list
        })

class MyMessageView(LoginRequiredMixin,View):
    '''
    我的消息
    '''
    def get(self,request):
        all_message = UserMessage.objects.filter(user = request.user.id)
        # 对消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_message, 5, request=request)

        all_messages = p.page(page)
        return render(request,'usercenter-message.html',{"all_message":all_messages})