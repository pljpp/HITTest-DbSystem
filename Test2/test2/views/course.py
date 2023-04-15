# @PydevCodeAnalysisIgnore
from django.shortcuts import render, redirect
from test2 import models

# 大学机构数据库系统管理首页
def list(request):
    course_list = models.Course.objects.all()
    return render(request, "course.html", {"course_list": course_list})
