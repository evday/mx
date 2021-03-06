# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import render
from django.views.generic.base import View
from django.shortcuts import HttpResponse

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course,CourseResource,Video
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserFavorite,CourseComments,UserCourse

class CourseListView(View):
    def get(self,request):
        all_courses = Course.objects.all().order_by("-add_time") #减号表示降序排列
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]

        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|Q(detail__icontains=search_keywords))



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

class CourseInfoView(LoginRequiredMixin, View):
    '''
    课程章节信息
    '''
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()
        #给用户和课程绑定关系
        user_courses = UserCourse.objects.filter(user=request.user,course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user,course=course)
            user_course.save()


        #取出学过该课程的所有信息
        users_course  = UserCourse.objects.filter(course=course)
        #取出所有的user id
        users_id = [user_course.user_id for user_course in users_course]
        #取出这些用户学过的所有课程
        all_user_courses = UserCourse.objects.filter(user_id__in=users_id)
        # 取出所有课程ID
        courses_ids = [user_course.course_id for user_course in all_user_courses]

        #从所有课程中过滤出id 在course_ids中的所有课程
        related_courses = Course.objects.filter(id__in=courses_ids).order_by("-click_nums")[:3]
        all_resource = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', {
            "course": course,
            "course_resources":all_resource,

            "related_courses":related_courses

        })
class CommentView(LoginRequiredMixin, View):
    '''
     课程评论信息
     '''

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 取出该课程所有的所有学生
        user_courses = UserCourse.objects.filter(course=course)

        # 取出所有课程ID
        course_ids = [user_course.course_id for user_course in user_courses]
        # 获取该用户学过的其它所有课程
        related_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:3]
        all_resource = CourseResource.objects.filter(course=course)
        all_comment = CourseComments.objects.filter(course_id=course_id)
        return render(request, 'course-comment.html', {
            "course": course,
            "course_resources": all_resource,
            "course_comments":all_comment,
            "user_courses": user_courses,
            "related_courses": related_courses
        })

class AddComments(View):
    def post(self,request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type="application/json")

        course_id = request.POST.get("course_id",0)
        comments = request.POST.get("comments",'')
        if course_id > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id = int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success","msg":"评论成功"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"fail","msg":"评论失败"}', content_type="application/json")

class VideoPlayView(View):

       def get(self, request, video_id):
           video = Video.objects.get(id=int(video_id))
           course = video.lesson.course
           #给用户和课程绑定关系
           user_courses = UserCourse.objects.filter(user=request.user,course=course)
           if not user_courses:
               user_course = UserCourse(user=request.user,course=course)
               user_course.save()


           #取出学过该课程的所有信息
           users_course  = UserCourse.objects.filter(course=course)
           #取出所有的user id
           users_id = [user_course.user_id for user_course in users_course]
           #取出这些用户学过的所有课程
           all_user_courses = UserCourse.objects.filter(user_id__in=users_id)
           # 取出所有课程ID
           courses_ids = [user_course.course_id for user_course in all_user_courses]

           #从所有课程中过滤出id 在course_ids中的所有课程
           related_courses = Course.objects.filter(id__in=courses_ids).order_by("-click_nums")[:3]
           all_resource = CourseResource.objects.filter(course=course)
           return render(request, 'course-play.html', {
               "course": course,
               "course_resources":all_resource,
                "video":video,
               "related_courses":related_courses

           })