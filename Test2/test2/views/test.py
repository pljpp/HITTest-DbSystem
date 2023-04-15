# @PydevCodeAnalysisIgnore
from django.shortcuts import render, redirect
from test2 import models

# 大学机构数据库系统管理首页
def list(request):
    test_list = models.Test.objects.all()
    return render(request, "test.html", {"test_list": test_list})
