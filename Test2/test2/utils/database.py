import pymysql

# 教室信息
class Classroom:
    classroom = []
    
    def __init__(self):
        connect = pymysql.connect(host = "127.0.0.1", port = 3306, user = "root", password = "318414275", charset = "utf8", db = "test_database_2")
        test_database = connect.cursor(cursor = pymysql.cursors.DictCursor)
        sql = 'select * from classroom'
        test_database.execute(sql)
        self.classroom = test_database.fetchall()
        test_database.close()
        connect.close()
    
    def getClassroom(self):
        return self.classroom

# 课程段信息
class Section:
    section = []
    
    def __init__(self):
        connect = pymysql.connect(host = "127.0.0.1", port = 3306, user = "root", password = "318414275", charset = "utf8", db = "test_database_2")
        test_database = connect.cursor(cursor = pymysql.cursors.DictCursor)
        sql = 'select * from section order by year, semester'
        test_database.execute(sql)
        self.section = test_database.fetchall()
        test_database.close()
        connect.close()
    
    def getSection(self):
        return self.section
    
    def add(self, cid, section, semester, year):
        connect = pymysql.connect(host = "127.0.0.1", port = 3306, user = "root", password = "318414275", charset = "utf8", db = "test_database_2")
        test_database = connect.cursor(cursor = pymysql.cursors.DictCursor)
        param_sql = [cid, section, semester, year]
        sql = 'insert into section(cid, section, semester, year) values(%s, %s, %s, %s)'
        test_database.execute(sql, param_sql)
        connect.commit()
        test_database.close()
        connect.close()
    
    def delete(self, cid, section, semester, year):
        connect = pymysql.connect(host = "127.0.0.1", port = 3306, user = "root", password = "318414275", charset = "utf8", db = "test_database_2")
        test_database = connect.cursor(cursor = pymysql.cursors.DictCursor)
        param_sql = [cid, section, semester, year]
        sql = 'delete from section where cid = %s and section = %s and semester = %s and year = %s'
        test_database.execute(sql, param_sql)
        connect.commit()
        test_database.close()
        connect.close()

# 课程实验信息
class Need:
    need = []
    
    def __init__(self):
        connect = pymysql.connect(host = "127.0.0.1", port = 3306, user = "root", password = "318414275", charset = "utf8", db = "test_database_2")
        test_database = connect.cursor(cursor = pymysql.cursors.DictCursor)
        sql = 'select * from need'
        test_database.execute(sql)
        self.need = test_database.fetchall()
        test_database.close()
        connect.close()
    
    def getNeed(self):
        return self.need

# 学生选课信息
class Takes:
    takes = []
    
    def __init__(self):
        connect = pymysql.connect(host = "127.0.0.1", port = 3306, user = "root", password = "318414275", charset = "utf8", db = "test_database_2")
        test_database = connect.cursor(cursor = pymysql.cursors.DictCursor)
        sql = 'select * from takes order by sid'
        test_database.execute(sql)
        self.takes = test_database.fetchall()
        test_database.close()
        connect.close()
        
    def getTakes(self):
        return self.takes
    
    def add(self, sid, cid, section, semester, year, grade):
        connect = pymysql.connect(host = "127.0.0.1", port = 3306, user = "root", password = "318414275", charset = "utf8", db = "test_database_2")
        test_database = connect.cursor(cursor = pymysql.cursors.DictCursor)
        grade = int(grade)
        param_sql = [sid, cid, section, semester, year, grade]
        sql = 'insert into takes(sid, cid, section, semester, year, grade) values(%s, %s, %s, %s, %s, %s)'
        test_database.execute(sql, param_sql)
        connect.commit()
        test_database.close()
        connect.close()
    
    def modify(self, sid, cid, section, semester, year, grade):
        connect = pymysql.connect(host = "127.0.0.1", port = 3306, user = "root", password = "318414275", charset = "utf8", db = "test_database_2")
        test_database = connect.cursor(cursor = pymysql.cursors.DictCursor)
        grade = int(grade)
        param_sql = [grade, sid, cid, section, semester, year]
        sql = 'update takes set grade = %s where sid = %s and cid = %s and section = %s and semester = %s and year = %s'
        test_database.execute(sql, param_sql)
        connect.commit()
        test_database.close()
        connect.close()
    
    def delete(self, sid, cid, section, semester, year):
        connect = pymysql.connect(host = "127.0.0.1", port = 3306, user = "root", password = "318414275", charset = "utf8", db = "test_database_2")
        test_database = connect.cursor(cursor = pymysql.cursors.DictCursor)
        param_sql = [sid, cid, section, semester, year]
        sql = 'delete from takes where sid = %s and cid = %s and section = %s and semester = %s and year = %s'
        test_database.execute(sql, param_sql)
        connect.commit()
        test_database.close()
        connect.close()
    
# 教师授课信息
class Teaches:
    teaches = []
    
    def __init__(self):
        connect = pymysql.connect(host = "127.0.0.1", port = 3306, user = "root", password = "318414275", charset = "utf8", db = "test_database_2")
        test_database = connect.cursor(cursor = pymysql.cursors.DictCursor)
        sql = 'select * from teaches order by iid'
        test_database.execute(sql)
        self.teaches = test_database.fetchall()
        test_database.close()
        connect.close()
        
    def getTeaches(self):
        return self.teaches

# 系与学生信息
class Stud_dept:
    stud_dept = []
    
    def __init__(self):
        connect = pymysql.connect(host = "127.0.0.1", port = 3306, user = "root", password = "318414275", charset = "utf8", db = "test_database_2")
        test_database = connect.cursor(cursor = pymysql.cursors.DictCursor)
        sql = 'select * from stud_dept order by did'
        test_database.execute(sql)
        self.stud_dept = test_database.fetchall()
        test_database.close()
        connect.close()
        
    def getStud_dept(self):
        return self.stud_dept
    
# 系与教师信息
class Inst_dept:
    inst_dept = []
    
    def __init__(self):
        connect = pymysql.connect(host = "127.0.0.1", port = 3306, user = "root", password = "318414275", charset = "utf8", db = "test_database_2")
        test_database = connect.cursor(cursor = pymysql.cursors.DictCursor)
        sql = 'select * from inst_dept order by did'
        test_database.execute(sql)
        self.inst_dept = test_database.fetchall() 
        test_database.close()
        connect.close()
    
    def getInst_dept(self):
        return self.inst_dept

# 教室与课程段信息
class Sec_class:
    sec_class = []
    
    def __init__(self):
        connect = pymysql.connect(host = "127.0.0.1", port = 3306, user = "root", password = "318414275", charset = "utf8", db = "test_database_2")
        test_database = connect.cursor(cursor = pymysql.cursors.DictCursor)
        sql = 'select * from sec_class order by rid'
        test_database.execute(sql)
        self.sec_class = test_database.fetchall()
        test_database.close()
        connect.close()
    
    def getSec_class(self):
        return self.sec_class

# 时段与课程段信息
class Sec_time:
    sec_time = []
    
    def __init__(self):
        connect = pymysql.connect(host = "127.0.0.1", port = 3306, user = "root", password = "318414275", charset = "utf8", db = "test_database_2")
        test_database = connect.cursor(cursor = pymysql.cursors.DictCursor)
        sql = 'select * from sec_time order by section'
        test_database.execute(sql)
        self.sec_time = test_database.fetchall() 
        test_database.close()
        connect.close()
    
    def getSec_time(self):
        return self.sec_time
