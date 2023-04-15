# @PydevCodeAnalysisIgnore
from django.shortcuts import render, redirect
from test2.utils import database
from test2.utils import checknone

# 课程实验信息
def need_list(request):
    need_list = database.Need().getNeed()
    return render(request, "need.html", {"need_list": need_list})

# 学生与系
def stud_dept_list(request):
    stud_dept_list = database.Stud_dept().getStud_dept()
    return render(request, 'stud_dept.html', {'stud_dept_list': stud_dept_list})

# 教师与系
def inst_dept_list(request):
    inst_dept_list = database.Inst_dept().getInst_dept()
    return render(request, 'inst_dept.html', {'inst_dept_list': inst_dept_list})

# 教室与课程段
def sec_class_list(request):
    sec_class_list = database.Sec_class().getSec_class()
    return render(request, 'sec_class.html', {'sec_class_list': sec_class_list})

# 时段与课程段
def sec_time_list(request):
    sec_time_list = database.Sec_time().getSec_time()
    return render(request, 'sec_time.html', {'sec_time_list': sec_time_list})

# 教师授课
def teaches_list(request):
    teaches_list = database.Teaches().getTeaches()
    return render(request, 'teaches.html', {'teaches_list': teaches_list})

# 学生选课
def takes_list(request):
    takes_list = database.Takes().getTakes()
    return render(request, 'takes.html', {'takes_list': takes_list})

# 增加选课信息
def takes_add(request):
    add = {'sid': '', 'cid': '', 'section': '', 'semester': '', 'year': '', 'grade': '0', 'error': ''}
    if request.method == "GET":
        return render(request, 'takes_add.html', {'add': add})
    
    sid = request.POST.get('sid')
    cid = request.POST.get('cid')
    section = request.POST.get('section')
    semester = request.POST.get('semester')
    year = request.POST.get('year')
    grade = request.POST.get('grade')
    check_none = checknone.CheckNone({'sid': sid, 'cid': cid, 'section': section, 'semester': semester, 'year': year, 'grade': grade})
    add = check_none.getCheck()
    if add is not None:
        return render(request, 'takes_add.html', {'add': add})
    
    try:
        database.Takes().add(sid, cid, section, semester, year, grade)
    except Exception as e:
        add = {'sid': sid, 'cid': cid, 'section': section, 'semester': semester, 'year': year, 'grade': grade, 'error': str(e)}
        return render(request, "takes_add.html", {'add': add})
    return redirect(to = "/takes/list/")

# 修改学生成绩
def takes_modify(request):
    if request.method == "GET":
        sid = request.GET.get("sid")
        cid = request.GET.get("cid")
        section = request.GET.get("section")
        semester = request.GET.get("semester")
        year = request.GET.get("year")
        grade = request.GET.get("grade")
        modify = {'sid': sid, 'cid': cid, 'section': section, 'semester': semester, 'year': year, 'grade': grade, 'error':''}
        return render(request, 'takes_modify.html', {'modify': modify})
    
    sid = request.POST.get('sid')
    cid = request.POST.get('cid')
    section = request.POST.get('section')
    semester = request.POST.get('semester')
    year = request.POST.get('year')
    grade = request.POST.get('grade')
    check_none = checknone.CheckNone({'sid': sid, 'cid': cid, 'section': section, 'semester': semester, 'year': year, 'grade': grade})
    modify = check_none.getCheck()
    if modify is not None:
        return render(request, 'takes_modify.html', {'modify': modify})
    
    try:
        database.Takes().modify(sid, cid, section, semester, year, grade)
    except Exception as e:
        modify = {'sid': sid, 'cid': cid, 'section': section, 'semester': semester, 'year': year, 'grade': grade, 'error': str(e)}
        return render(request, "takes_modify.html", {'modify': modify})
    return redirect(to = "/takes/list/")

# 删除选课信息
def takes_delete(request):
    sid = request.GET.get("sid")
    cid = request.GET.get("cid")
    section = request.GET.get("section")
    semester = request.GET.get("semester")
    year = request.GET.get("year")
    database.Takes().delete(sid, cid, section, semester, year)
    return redirect(to = "/takes/list/")
