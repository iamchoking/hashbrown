from _HashBrown import *

def interruptedForcedOsc(b,m,k,F0,w,tf,ts,te):
    def F(t):
        if t>=tf:
            return 0
        return F0
    
    def xp(t,x,y):
        return y
    def yp(t,x,y):
        return -(b/m)*y - (k/m)*x - (F(t)/m)*sin(w*t)
    
    F1 = Function(xp,3,'Displacement')
    F2 = Function(yp,3,'Speed')

    return rk4(ts,te,0.0001,((0,0),(F1,F2)),'Forced Oscillation')