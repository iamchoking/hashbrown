from ._FunctionBasic import *
from ._DataH import *

# I will die for a hot and crispy strip of hashbrown

class DiffFuncError(Exception):
    pass

def mapF(ts,te,step,f,name = 'Function'): #maps a function with respect to time #f takes a tuple of functions
    """
    genertates a (class Result) taking output of each function in f.

    Parameters
    ----------
    ts,te (num): start and end time

    step (num): timestep

    f (iterable): iterable of (class Function) objects

    name (string): name of resulting (class Result) object

    Notes
    -----
    unlike rk4, each (class Function) object must only have one input (f[i].var == 1).
    """
    values = []
    varName = []
    for i in f:
        varName.append(i.name)
    for i in np.arange(ts,te,step):
        temp = [0 for k in f]
        for j in range(len(f)):
            temp[j] = f[j].f(i)
        values.append((i,tuple(temp)))
    return Result(values,varName,name)

def _genK(t,step,s): #s contains two tuples of n elements ((values),(functions))
    """
    [internal function] does all the magic

    Parameters
    ----------
    t (num): current time
    
    step (num): timestep
    
    s (tuple): s contains two tuples of n elements ((values),(functions)) which are current values, and the iterable of (class Function) objects

    Notes
    -----
    a very convoluted function that is specifically for rk4 and rk4R. don't mess with this unless you are quite sure of what you are doing.
    """
    #init
    v = list(s[0])
    f = s[1]
    k1 = [0.0 for i in s[0]]
    k2 = [0.0 for i in s[0]]
    k3 = [0.0 for i in s[0]]
    k4 = [0.0 for i in s[0]]
    #step01
    cR = range(len(s[0]))
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

def rk4(ts,te,step,s,name = 'rkResult',ti = None): #s contains two tuples of n elements ((values),(functions))
    """
    uses Runge-Kutta 4th order with fixed timestep to generate a (class Result) object for a given differential equation.

    Parameters
    ----------
    ts, te (num): start and end time
    
    step (num): timestep. used as fixed timestep for the Runge-Kutta method
    
    s (tuple): s contains two tuples of n elements ((values),(functions))
    
        values (tuple): intitial values
        functions (tuple): iterable of (class Function) objects that govern the differential equation.

    name (string): name of resulting (class Result) object

    ti (num or None): option to constrain initial value at some other time than ts.

    Notes
    -----
    if you are looking at this before the documentation, please see the documentation first at:
    
        https://github.com/iamchoking/Hashbrown/blob/master/Hashbrown_Program_Documentation.pdf
    """
    v = s[0]
    f = s[1]
    varName = []
    #print f
    print('[hashbrown] rk4 >> Computation Started  : %s'%(name))
    if ti != None:
        print ('[hashbrown] rk4 >> Dual-Direction Solve Initialized')
        return (rk4R(ti,ts,step,s,name).attach(rk4(ti,te,step,s,name)))
    if ts>te:
        return rk4R(ts,te,step,s,name = name)
    
    for i in f:
        varName.append(i.name)
    for i in f:
        if i.var-1 != len(f):
            raise DiffFuncError('[hashbrown] ERR>> Invalid Function Set')
    values = []
    values.append((ts,list(v))) #the v here used to be copy.deepcopy(v)
    t = ts
    while t <= te:
        v =  _genK(t,step,(v,f))
        t += step
        values.append((t,v))
        #print '%f finished (out of %f)' %(t,te)

        
    print ('[hashbrown] rk4 >> Computation Finished : %s\n'%(name))
    return Result(values,varName,name)

def rk4R(ts,te,step,s,name = 'rkResultR',discr = True): #a reverse version of rk4
    """
    Reverse version of rk4. see rk4 for more info.

    Notes
    -----
    recommeded to unify interface by using rk4 with ti = te, rather than this method.
    """
    v = s[0]
    f = invSign(s[1])
    varName = []
    #print f
    
    for i in f:
        varName.append(i.name)
    for i in f:
        if i.var-1 != len(f):
            raise DiffFuncError('[hashbrown] REVERSE >> ERR>> Invalid Function Set')
    values = []
    values.append((ts,v)) #the v here used to be copy.deepcopy(v)
    t = ts
    while t >= te:
        v =  _genK(t,step,(v,f))
        t -= step
        values.append((t,list(v)))
    values.reverse()
    #print (values[:10])
    print ('[hashbrown] REVERSE: Computation Finished')
    if discr:
        name = name + '(to %s)'%(str(ts)[:3])
    # print (name)
    return Result(values,varName,name)