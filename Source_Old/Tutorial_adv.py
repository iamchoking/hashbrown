from hashbrown_d import *

def interruptedForcedOsc(b,m,k,F0,w,tf,ts,te,name = 'ForceInt',dev = 0.0001,init = (0,0),ti = None):
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

    return rk4(ts,te,dev,(init,(F1,F2)),name,ti)

R = interruptedForcedOsc(1,1,1,10,10,5,0,10,name = 'ForceInt1',dev = 0.0001)

#R.writePLOT()

R1 = interruptedForcedOsc(1,1,1,10,10,5,0,10,name = 'ForceInt2',dev = 0.0001,init = (-0.09131260928062768, 0.0193951948001254),ti = 3)
print (R1.get(3))
X = R.merge(R1)
X.writePLOT()