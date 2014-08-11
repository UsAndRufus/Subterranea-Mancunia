class Bezier(object):
    def __init__(self, start, control1, control2, end):
        self.p0 = start
        self.p1 = control1
        self.p2 = control2
        self.p3 = end
    def __call__(self, t):
        #[x,y] = (1-t)^3*P0 +
        #       3(1-t)^2*t*P1 +
        #       3(1-t)*t^2*P2 +
        #       t^3*P3
        # 1-t = u

        assert 0 <= t <= 1
        
        u = 1 - t

        #list comprehension multiplies each term in tuple
        term1 = tuple([u*u*u*i for i in self.p0])
        term2 = tuple([3*u*u*t*i for i in self.p1])
        term3 = tuple([3*u*t*t*i for i in self.p2])
        term4 = tuple([t*t*t*i for i in self.p3])

        result = (term1[0] + term2[0] + term3[0] + term4[0]), (term1[1] + term2[1] + term3[1] + term4[1])

        return result

        
