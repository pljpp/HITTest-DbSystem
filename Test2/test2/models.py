from django.db import models

# 系department
class Department(models.Model):
    did = models.CharField(verbose_name = '系编号', max_length = 20, primary_key = True)
    dname = models.CharField(verbose_name = '系名称', max_length = 20)
    building = models.CharField(verbose_name = '楼', max_length = 20)
    class Meta:
        db_table = "department"

# 学生student
class Student(models.Model):
    sid = models.CharField(verbose_name = '学生编号', max_length = 20, primary_key = True)
    sname = models.CharField(verbose_name = '学生姓名', max_length = 20)
    points = models.IntegerField(verbose_name = '学分')
    class Meta:
        db_table = 'student'

# 教师instructor
class Instructor(models.Model):
    iid = models.CharField(verbose_name = '教师编号', max_length = 20, primary_key = True)
    iname = models.CharField(verbose_name = '教师姓名', max_length = 20)
    salary = models.IntegerField(verbose_name = '薪水')
    class Meta:
        db_table = 'instructor'

# 教室classroom

# 课程course
class Course(models.Model):
    cid = models.CharField(verbose_name = '课程编号', max_length = 20, primary_key = True)
    cname = models.CharField(verbose_name = '课程姓名', max_length = 20)
    credits = models.IntegerField(verbose_name = '学分')
    class Meta:
        db_table = 'course'

# 课程段section

# 实验test
class Test(models.Model):
    tid = models.CharField(verbose_name = '实验编号', max_length = 20, primary_key = True)
    tname = models.CharField(verbose_name = '实验名称', max_length = 20)
    groups = models.IntegerField(verbose_name = '分组人数')
    class Meta:
        db_table = 'test'
