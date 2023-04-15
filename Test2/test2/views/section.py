# @PydevCodeAnalysisIgnore
from django.shortcuts import render, redirect
from test2.utils import database
from test2.utils import checknone

# 课程段信息
def list(request):
    section_list = database.Section().getSection()
    return render(request, "section.html", {"section_list": section_list})

# 增加课程段
def add(request):
    add = {'cid': '', 'section': '', 'semester': '', 'year': '', 'grade': '0', 'error': ''}
    if request.method == "GET":
        return render(request, 'section_add.html', {'add': add})
    
    cid = request.POST.get('cid')
    section = request.POST.get('section')
    semester = request.POST.get('semester')
    year = request.POST.get('year')
    check_none = checknone.CheckNone({'cid': cid, 'section': section, 'semester': semester, 'year': year})
    add = check_none.getCheck()
    if add is not None:
        return render(request, 'section_add.html', {'add': add})
    
    try:
        database.Section().add(cid, section, semester, year)
    except Exception as e:
        add = {'cid': cid, 'section': section, 'semester': semester, 'year': year, 'error': str(e)}
        return render(request, "section_add.html", {'add': add})
    return redirect(to = "/section/list/")

# 删除课程段
def delete(request):
    cid = request.GET.get("cid")
    section = request.GET.get("section")
    semester = request.GET.get("semester")
    year = request.GET.get("year")
    database.Section().delete(cid, section, semester, year)
    return redirect(to = "/section/list/")
