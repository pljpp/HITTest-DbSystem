# @PydevCodeAnalysisIgnore
from django.shortcuts import render, redirect
from test2 import models
from test2.utils import checknone
import pymysql
import re

# 大学机构数据库系统管理首页
def college_home(request):
    sql_carry = {'sql_carry': '', 'error': ''}
    if request.method == 'GET':
        return render(request, "college_home.html", {'sql_carry': sql_carry})
    
    sentence = request.POST.get('sentence')
    print(sentence)
    check_none = checknone.CheckNone({'sql_carry': sentence})
    sql_carry = check_none.getCheck()
    if sql_carry is not None:
        return render(request, "college_home.html", {'sql_carry': sql_carry})
    
    try:
        connect = pymysql.connect(host = "127.0.0.1", port = 3306, user = "root", password = "318414275", charset = "utf8", db = "test_database_2")
        test_database = connect.cursor(cursor = pymysql.cursors.DictCursor)
        test_database.execute(sentence)
        match_result = match_select(sentence)
        if match_result:
            select = test_database.fetchall()
            return render(request, 'college_result.html', {'select': select})
        else:
            connect.commit()
    except Exception as e:
        sql_carry = {'sql_carry': sentence, 'error': str(e)}
        return render(request, "college_home.html", {'sql_carry': sql_carry})
    finally:
        test_database.close()
        connect.close()
    return redirect(to = "/college/")

def match_select(sentence):
    template_re = r'^[\s]*select'
    match_re = re.match(template_re, sentence, re.M | re.I)
    if match_re is None:
        return False
    else:
        return True
