# @PydevCodeAnalysisIgnore
from django.shortcuts import render, redirect
from test2 import models
from test2.utils import checknone

# 学生信息
def list(request):
    student_list = models.Student.objects.all()
    return render(request, "student.html", {"student_list": student_list})

# 增加学生
def add(request):
    add = {'sid': '', 'sname': '', 'error': ''}
    if request.method == "GET":
        return render(request, "student_add.html", {'add': add})
    sid = request.POST.get("sid")
    sname = request.POST.get("sname")
    check_none = checknone.CheckNone({'sid': sid, 'sname': sname})
    add = check_none.getCheck()
    if add is not None:
        return render(request, "student_add.html", {'add': add})
    points = 0
    try:
        models.Student.objects.create(sid = sid, sname = sname, points = points)
    except Exception as e:
        add = {'sid': sid, 'sname': sname, 'error': str(e)}
        return render(request, "student_add.html", {'add': add})
    return redirect(to = "/student/list/")

# 修改学生
def modify(request):
    modify = {'sid': '', 'sname': '', 'points': '', 'error': ''}
    if request.method == 'GET':
        return render(request, 'student_modify.html', {'modify': modify})
    
    sid = request.POST.get('sid')
    sname = request.POST.get('sname')
    points = request.POST.get('points')
    check_none = checknone.CheckNone({'sid': sid, 'sname': sname, 'points': points})
    modify = check_none.getCheck()
    if modify is not None:
        return render(request, 'student_modify.html', {'modify': modify})
    
    try:
        models.Student.objects.filter(sid = sid).update(sname = sname, points = int(points))
    except Exception as e:
        modify = {'sid': sid, 'sname': sname, 'points': points, 'error': str(e)}
        return render(request, "student_modify.html", {'modify': modify})
    return redirect(to = "/student/list/")

# 删除学生
def delete(request):
    delete = {'sid': '', 'error': ''}
    if request.method == 'GET':
        return render(request, 'student_delete.html', {'delete': delete})
    
    sid = request.POST.get('sid')
    check_none = checknone.CheckNone({'sid': sid})
    delete = check_none.getCheck()
    if delete is not None:
        return render(request, 'student_delete.html', {'delete': delete})
    
    try:
        models.Student.objects.filter(sid = sid).delete()
    except Exception as e:
        delete = {'sid': sid, 'error': str(e)}
        return render(request, 'student_delete.html', {'delete': delete})
    return redirect(to = '/student/list/')
