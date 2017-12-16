# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import render
from django.views.generic.base import View

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course,CourseResource
from operation.models import UserFavorite

class CourseListView(View):
    def get(self,request):
        all_courses = Course.objects.all().order_by("-add_time") #减号表示降序排列
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]
        sort = request.GET.get("sort", '')
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 6, request=request)

        courses = p.page(page)

        return render(request,'course-list.html',{
            "all_courses":courses,
            "sort":sort,
            "hot_courses":hot_courses,
        })


class CourseDetailView(View):
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))

        #增加课程点击数
        course.click_nums += 1
        course.save()

        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=course_id,fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True




        tag = course.tag
        if tag:
            related_courses = Course.objects.filter(tag=tag)[:2]
        else:
            related_courses = []
        return render(request,'course-detail.html',{
            "course":course,
            "related_courses":related_courses,
            "has_fav_course":has_fav_course,
            "has_fav_org":has_fav_org,
        })

class CourseInfoView(View):
    '''
    课程章节信息
    '''
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resource = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', {
            "course": course,
            "course_resources":all_resource

        })