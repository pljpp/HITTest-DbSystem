'''
关系R和S
'''
class R:
    A = 1
    B = 1
    def __init__(self, a, b):
        assert isinstance(a, int)
        assert isinstance(b, int)
        assert 1 <= a <= 40
        assert 1 <= a <= 1000
        self.A = a
        self.B = b
    
    def __eq__(self, other):
        assert isinstance(other, R)
        if self.A == other.A and self.B == other.B:
            return True
        else:
            return False
        
class S:
    C = 20
    D = 1
    def __init__(self, c, d):
        assert 20 <= c <= 60
        assert 1 <= d <= 1000
        self.C = c
        self.D = d
    
    def __eq__(self, other):
        assert isinstance(other, S)
        if self.C == other.C and self.D == other.D:
            return True
        else:
            return False
