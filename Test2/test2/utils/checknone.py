# 检查用户输入是否为空（html将空转换为空格）
class CheckNone:
    # 用户输入
    form_input = {}
    # 错误标记
    have_none = 0
    
    def __init__(self, form_input):
        self.form_input = form_input
        for item in self.form_input:
            if self.form_input[item] == None or self.form_input[item] == '':
                self.form_input['error'] = '请输入完整'
                self.have_none = 1
                break
    
    def getCheck(self):
        if self.have_none == 1:
            return self.form_input
        else:
            return None
