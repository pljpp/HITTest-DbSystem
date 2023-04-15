# @PydevCodeAnalysisIgnore
from django.shortcuts import render, redirect
from test2.utils import view

# 教师授课视图
def instructor_teaches(request):
    instructor_teaches_list = view.InstructorTeaches().getStudentTakes()
    return render(request, "instructor_teaches.html", {"instructor_teaches_list": instructor_teaches_list})

# 学生选课视图
def student_takes(request):
    student_takes_list = view.StudentTakes().getStudentTakes()
    return render(request, 'student_takes.html', {'student_takes_list': student_takes_list})

# 系中教师视图
def instructor_in_department(request):
    instructor_in_department_list = view.InstructorInDepartment().getInstructorInDepartment()
    return render(request, 'instructor_in_department.html', {'instructor_in_department_list': instructor_in_department_list})

# 系中学生视图
def student_in_department(request):
    student_in_department_list = view.StudentInDepartment().getStudentInDepartment()
    return render(request, 'student_in_department.html', {'student_in_department_list': student_in_department_list})
