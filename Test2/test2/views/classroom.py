# @PydevCodeAnalysisIgnore
from django.shortcuts import render, redirect
from test2.utils import database

# 教室信息
def list(request):
    classroom_list = database.Classroom().getClassroom()
    return render(request, "classroom.html", {"classroom_list": classroom_list})
