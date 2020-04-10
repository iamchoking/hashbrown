from _FunctionBasic import *
from _DataH import *

class DiffFuncError(Exception):
    pass

def genK(t,step,s): #s contains two tuples of n elements ((values),(functions))
    #init
    v = list(s[0])
    f = s[1]
    cR = range(len(v))
    k1 = [0.0 for i in cR]
    k2 = [0.0 for i in cR]
    k3 = [0.0 for i in cR]
    k4 = [0.0 for i in cR]
    #step01
    for i in cR:
        k1[i] = float(f[i].f(float(t),*v))
    
    #print f[1].f(float(t),*v),v
    
    #step02
    t = t + 0.5*step
    for i in cR:
        v[i] = v[i] + 0.5*k1[i]*step
    for i in cR:
        k2[i] = (f[i].f(t,*v))

    #step03
    for i in cR:
        v[i] = v[i] + 0.5*(k2[i]-k1[i])*step
    for i in cR:
        k3[i] = (f[i].f(t,*v))
    
    #step04
    t = t + 0.5*step
    for i in cR:
        v[i] = v[i] + 0.5*(2*k3[i]-k2[i])*step
    for i in cR:
        k4[i] = (f[i].f(t,*v))
    
    #final
    for i in cR:
        v[i] = v[i] +(-k3[i]+ 1.0/6*(k1[i]+2*k2[i]+2*k3[i]+k4[i]))*step
        
    #print (t,k1,k2,k3,k4,v)    
    
    return v



def rk4(ts,te,step,s,name = 'rkResult',wCmd = ()): #s contains two tuples of n elements ((values),(functions))
    v = s[0]
    f = s[1]
    varName = []
    #print f
    for i in f:
        varName.append(i.name)
    for i in f:
        if i.var-1 != len(f):
            raise DiffFuncError('Invalid Function Set')
    values = []
    values.append((ts,copy.deepcopy(v)))
    t = ts
    while t <= te:
        v =  genK(t,step,(v,f))
        t += step
        values.append((t,v))
        #print '%f finished (out of %f)' %(t,te)

        
    print ('Computation Finished')
    write(values,varName,name,wCmd)
    return (values,varName,name)