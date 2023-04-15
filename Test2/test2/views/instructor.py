# @PydevCodeAnalysisIgnore
from django.shortcuts import render, redirect
from test2 import models

# 大学机构数据库系统管理首页
def list(request):
    instructor_list = models.Instructor.objects.all()
    return render(request, "instructor.html", {"instructor_list": instructor_list})
