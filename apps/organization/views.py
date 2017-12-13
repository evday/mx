# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic.base import View
from django.shortcuts import render

from .models import CourseOrg,CityDict
from operation.models import UserFavorite
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserAskForm
from django.http import HttpResponse

# Create your views here.
class OrgView(View):
    def get(self,request):
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        all_citys = CityDict.objects.all()
        #取出筛选城市
        city_id = request.GET.get("city",'')
        if city_id:
            all_orgs = all_orgs.filter(city_id = int(city_id))

        #类别筛选
        category = request.GET.get("ct", '')
        if category:
            all_orgs = all_orgs.filter(category=category)
        org_nums = all_orgs.count()
        sort = request.GET.get("sort", '')
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_num")
        #对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs,5,request=request)

        orgs = p.page(page)
        return render(request,'org-list.html',{
            "all_orgs":orgs,
            "all_citys":all_citys,
            "org_nums":org_nums,
            "city_id":city_id,
            "category":category,
            "hot_orgs":hot_orgs,
            "sort":sort,

        })


class AddUserAskView(View):
    '''
    用户添加咨询
    '''
    def post(self,request):
        user_ask_form = UserAskForm(request.POST)
        if user_ask_form.is_valid():
            user_ask = user_ask_form.save(commit=True)#可以直接保存到数据库，commit不指定的话就不保存
            return HttpResponse('{"status":"success"}',content_type="application/json")
        else:
            return HttpResponse('{"status":"fail","msg":"添加出错"}',content_type="application/json")

class OrgHomeView(View):
    '''
    机构首页
    '''
    def get(self,request,org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id = int(org_id))
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request,'org-detail-homepage.html',{
            "all_courses":all_courses,
            "all_teachers":all_teachers,
            "course_org":course_org,
            "current_page" : current_page,
        })

class OrgCourseView(View):
    '''
    机构课程页
    '''
    def get(self,request,org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id = int(org_id))
        all_courses = course_org.course_set.all()
        return render(request,'org-detail-course.html',{
            "all_courses":all_courses,
            "course_org":course_org,
            "current_page":current_page,
        })
class OrgDescView(View):
    '''
    机构描述页
    '''
    def get(self,request,org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id = int(org_id))
        return render(request,'org-detail-desc.html',{
            "course_org":course_org,
            "current_page":current_page,
        })

class OrgTeacherView(View):
    '''
    机构教师页
    '''
    def get(self,request,org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id = int(org_id))
        all_teachers = course_org.teacher_set.all()
        return render(request,'org-detail-teachers.html',{
            "all_teachers":all_teachers,
            "course_org":course_org,
            "current_page":current_page,
        })

class AddFavView(View):
    '''
    用户收藏和取消收藏
    '''
    def post(self,request):
        fav_id = request.POST.get("fav_id",0)
        fav_type = request.POST.get("fav_type",0)

        #判断用户是否登录
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"收藏"}', content_type="application/json")

        exist_records = UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=int(fav_type))
        if exist_records:
            #如果已经存在，则表示用户取消收藏
            exist_records.delete()
        else:
            user_fav = UserFavorite()
            if int(fav_id)>0 and int(fav_type)>0:
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type="application/json")
            else:
                return HttpResponse('{"status":"fail","msg":"收藏出错"}', content_type="application/json")