import pymysql

# 教师授课视图
class InstructorTeaches:
    studenttakes = []
    
    def __init__(self):
        connect = pymysql.connect(host = '', port = , user = '', password = '', charset = "utf8", db = '')
        test_database = connect.cursor(cursor = pymysql.cursors.DictCursor)
        sql = 'select * from instructorteaches'
        test_database.execute(sql)
        self.studenttakes = test_database.fetchall()
        test_database.close()
        connect.close()
    
    def getStudentTakes(self):
        return self.studenttakes

# 学生选课视图
class StudentTakes:
    studenttakes = []
    
    def __init__(self):
        connect = pymysql.connect(host = '', port = , user = '', password = '', charset = "utf8", db = '')
        test_database = connect.cursor(cursor = pymysql.cursors.DictCursor)
        sql = 'select * from studenttakes'
        test_database.execute(sql)
        self.studenttakes = test_database.fetchall()
        test_database.close()
        connect.close()
    
    def getStudentTakes(self):
        return self.studenttakes

# 系中教师视图
class InstructorInDepartment:
    instructorindepartment = []
    
    def __init__(self):
        connect = pymysql.connect(host = '', port = , user = '', password = '', charset = "utf8", db = '')
        test_database = connect.cursor(cursor = pymysql.cursors.DictCursor)
        sql = 'select * from instructorindepartment'
        test_database.execute(sql)
        self.instructorindepartment = test_database.fetchall()
        test_database.close()
        connect.close()
    
    def getInstructorInDepartment(self):
        return self.instructorindepartment

# 系中学生视图
class StudentInDepartment:
    studentindepartment = []
    
    def __init__(self):
        connect = pymysql.connect(host = '', port = , user = '', password = '', charset = "utf8", db = '')
        test_database = connect.cursor(cursor = pymysql.cursors.DictCursor)
        sql = 'select * from studentindepartment'
        test_database.execute(sql)
        self.studentindepartment = test_database.fetchall()
        test_database.close()
        connect.close()
    
    def getStudentInDepartment(self):
        return self.studentindepartment
