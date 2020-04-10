from _RungeKutta import *

def candle(c = 2500, p = 900, tm = 80, tr = 23, R = 0.03, ql = 2100,n = 10,v = 0.000003, L = 0.02,duration = 100000,step = 1): #n: lambda
    k1 = (p/2*(ql+(1/3*c*(tm-tr))))
    k2 = p/6*c*R*(tm-tr)
    d0 = 0.00000001
    
    def dp(t,d):
        return n*(atan(v*t/d)-atan((v*t - L)/d))/(2*d*k1 + k2)
    
    F1 = Function(dp,2,'disc hole')
    
    D = rk4(0,duration,step,((d0,),(F1,)),'candle test')
    

def rocketN(kl = 0.01,kq = 0.0001,x0 = 0,v0 = 1000,g = 9.8,duration=250): #gravity is considered constant
    def m(t):
        return 1 + 2.0*exp(-t)
    
    def mp(t):
        return -2.0*exp(-t)
    
    def f(t):
        return 5000*exp(-t)
    
    def xp(t,x,v):
        return v
    
    def vp(t,x,v):
        return -mp(t)/m(t)*v - kl/m(t)*v - kq/m(t)*v*abs(v) + f(t)/m(t) - g
    
    F1 = Function(xp,3,'position')
    F2 = Function(vp,3,'velocity')
    
    rk4(0,duration,0.001,((x0,v0),(F1,F2)),'rocket(normal)')


if __name__ == '__main__':
    rocketN()