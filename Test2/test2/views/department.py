# @PydevCodeAnalysisIgnore
from django.shortcuts import render, redirect
from test2 import models

# 系信息
def list(request):
    department_list = models.Department.objects.all()
    return render(request, "department.html", {"department_list": department_list})
