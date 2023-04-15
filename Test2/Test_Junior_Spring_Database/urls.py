from django.contrib import admin
from django.urls import path
from test2.views import test_home
from test2.views import department
from test2.views import test
from test2.views import student
from test2.views import instructor
from test2.views import course
from test2.views import section
from test2.views import classroom
from test2.views import contact
from test2.views import view

urlpatterns = [
    path('admin/', admin.site.urls),
    # 实验首页
    path('college/', test_home.college_home),
    # 系信息
    path('department/list/', department.list),
    # 学生信息
    path('student/list/', student.list),
    # 教师信息
    path('instructor/list/', instructor.list),
    # 课程信息
    path('course/list/', course.list),
    # 教室信息
    path('classroom/list/', classroom.list),
    # 课程段信息
    path('section/list/', section.list),
    # 实验信息
    path('test/list/', test.list),
    
    # 增加学生
    path('student/add/', student.add),
    # 修改学生
    path('student/modify/', student.modify),
    # 删除学生
    path('student/delete/', student.delete),
    
    # 增加课程段
    path('section/add/', section.add),
    # 删除课程段
    path('section/delete/', section.delete),
    
    # 课程实验信息
    path('need/list/', contact.need_list),
    # 学生选课信息
    path('takes/list/', contact.takes_list),
    # 教师授课信息
    path('teaches/list/', contact.teaches_list),
    # 系与学生信息
    path('stud_dept/list/', contact.stud_dept_list),
    # 系与教师信息
    path('inst_dept/list/', contact.inst_dept_list),
    # 教室与课程段信息
    path('sec_class/list/', contact.sec_class_list),
    # 时段与课程段信息
    path('sec_time/list/', contact.sec_time_list),
    
    # 增加选课信息
    path('takes/add/', contact.takes_add),
    # 修改选课信息
    path('takes/modify/', contact.takes_modify),
    # 删除选课信息
    path('takes/delete/', contact.takes_delete),
    
    # 视图：教师授课
    path('view/instructorteaches/', view.instructor_teaches),
    # 视图：学生选课
    path('view/studenttakes/', view.student_takes),
    # 视图：系中教师
    path('view/instructorindepartment/', view.instructor_in_department),
    # 视图：系中学生
    path('view/studentindepartment/', view.student_in_department),
]
