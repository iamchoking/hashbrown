#-*-coding:utf-8-*-

from _RungeKutta import *

######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################


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

def rocketR(kl = 0.01,kq = 0.0001,x0 = 0,v0 = 0,g = 9.8,duration=250,Re = 6400000): #gravity depends on position
    def m(t):
        return 1 + 2.0*exp(-t)
    
    def mp(t):
        return -2.0*exp(-t)
    
    def f(t):
        return 5000*exp(-t)
    
    def xp(t,x,v):
        return v
    
    def vp(t,x,v):
        #print (-kq/m(t)*v*abs(v))
        return -mp(t)/m(t)*v - kl/m(t)*v - kq/m(t)*v*abs(v) + f(t)/m(t) - g*((Re*Re)/((Re+x)*(float(Re)+x)))
    
    F1 = Function(xp,3,'position')
    F2 = Function(vp,3,'velocity')
    
    rk4(0,duration,0.001,((x0,v0),(F1,F2)),'rocket(radial),v0=%d'%v0)


######################################################################################################
######################################################################################################
######################################################################################################

def catch(va = 0,vb = 0, vc = 0, A0 = (0,0), B0 = (300,0),C0 = (150,180),duration = 20,step = 0.0001):
    def axp(t,ax,ay,bx,by,cx,cy):
        return (bx-ax)/pow((ax-bx)*(ax-bx)+(ay-by)*(ay-by),0.5)*va
    def ayp(t,ax,ay,bx,by,cx,cy):
        return (by-ay)/pow((ax-bx)*(ax-bx)+(ay-by)*(ay-by),0.5)*va
    
    def bxp(t,ax,ay,bx,by,cx,cy):
            return (cx-bx)/pow((cx-bx)*(cx-bx)+(cy-by)*(cy-by),0.5)*vb
    def byp(t,ax,ay,bx,by,cx,cy):
            return (cy-by)/pow((cx-bx)*(cx-bx)+(cy-by)*(cy-by),0.5)*vb    

    def cxp(t,ax,ay,bx,by,cx,cy):
            return (ax-cx)/pow((cx-ax)*(cx-ax)+(cy-ay)*(cy-ay),0.5)*vc
    def cyp(t,ax,ay,bx,by,cx,cy):
            return (ay-cy)/pow((cx-ax)*(cx-ax)+(cy-ay)*(cy-ay),0.5)*vc

    Ax = Function(axp,7,'Ax')
    Ay = Function(ayp,7,'Ay')
    Bx = Function(bxp,7,'Bx')
    By = Function(byp,7,'By')
    Cx = Function(cxp,7,'Cx')
    Cy = Function(cyp,7,'Cy')

    D = rk4(0,duration,step,((A0[0],A0[1],B0[0],B0[1],C0[0],C0[1]),(Ax,Ay,Bx,By,Cx,Cy)),'Catch_Va %d_Vb %d_Vc %d'%(va,vb,vc),wCmd=('csv'))
    D1 = D[0]
    animateF(D[0],D[1],D[2],subj=[('Ax','Ay'),('Bx','By'),('Cx','Cy')],tail = 0)
    '''
    D2 = []
    for i,j in D1:
        ax = j[0]
        ay = j[1]
        bx = j[2]
        by = j[3]
        cx = j[4]
        cy = j[5]
        dab = pow((ax-bx)*(ax-bx)+(ay-by)*(ay-by),0.5)
        dbc = pow((cx-bx)*(cx-bx)+(cy-by)*(cy-by),0.5)
        dca = pow((cx-ax)*(cx-ax)+(cy-ay)*(cy-ay),0.5)
        D2.append((i,(dab,dbc,dca)))
    writeCSV(D2,('Dab','Dbc','Dca'),'Catch_Va %d_Vb %d_Vc %d _ Distances'%(va,vb,vc),s = 10)
    '''


def catch4 (va = 0,vb = 0, vc = 0, vd = 0, A0 = (0,0), B0 = (100,0),C0 = (100,100),D0 = (0,100),duration = 20,step = 0.0001):
    def axp(t,ax,ay,bx,by,cx,cy,dx,dy):
        return (bx-ax)/pow((ax-bx)*(ax-bx)+(ay-by)*(ay-by),0.5)*va
    def ayp(t,ax,ay,bx,by,cx,cy,dx,dy):
        return (by-ay)/pow((ax-bx)*(ax-bx)+(ay-by)*(ay-by),0.5)*va
    
    def bxp(t,ax,ay,bx,by,cx,cy,dx,dy):
        return (cx-bx)/pow((cx-bx)*(cx-bx)+(cy-by)*(cy-by),0.5)*vb
    def byp(t,ax,ay,bx,by,cx,cy,dx,dy):
        return (cy-by)/pow((cx-bx)*(cx-bx)+(cy-by)*(cy-by),0.5)*vb    

    def cxp(t,ax,ay,bx,by,cx,cy,dx,dy):
        return (dx-cx)/pow((cx-dx)*(cx-dx)+(cy-dy)*(cy-dy),0.5)*vc


    def cyp(t,ax,ay,bx,by,cx,cy,dx,dy):
        try:
            return (dy-cy)/pow((cx-dx)*(cx-ax)+(cy-dy)*(cy-dy),0.5)*vc
        except:
            print ('error')
            return -vc
        
    def dxp(t,ax,ay,bx,by,cx,cy,dx,dy):
        return (ax-dx)/pow((ax-dx)*(ax-dx)+(ay-dy)*(ay-dy),0.5)*vd
    def dyp(t,ax,ay,bx,by,cx,cy,dx,dy):
        return (ay-dy)/pow((ax-dx)*(ax-dx)+(ay-dy)*(ay-dy),0.5)*vd

    Ax = Function(axp,9,'Ax')
    Ay = Function(ayp,9,'Ay')
    Bx = Function(bxp,9,'Bx')
    By = Function(byp,9,'By')
    Cx = Function(cxp,9,'Cx')
    Cy = Function(cyp,9,'Cy')
    Dx = Function(dxp,9,'Dx')
    Dy = Function(dyp,9,'Dy')

    D1 = rk4(0,duration,step,((A0[0],A0[1],B0[0],B0[1],C0[0],C0[1],D0[0],D0[1]),(Ax,Ay,Bx,By,Cx,Cy,Dx,Dy)),'Catch4_Va %d_Vb %d_Vc %d_Vd %d'%(va,vb,vc,vd))[0]
    D2 = []
    for i,j in D1:
        ax = j[0]
        ay = j[1]
        bx = j[2]
        by = j[3]
        cx = j[4]
        cy = j[5]
        dx = j[6]
        dy = j[7]
        dab = pow((ax-bx)*(ax-bx)+(ay-by)*(ay-by),0.5)
        dbc = pow((cx-bx)*(cx-bx)+(cy-by)*(cy-by),0.5)
        dcd = pow((cx-dx)*(cx-dx)+(cy-dy)*(cy-dy),0.5)
        dda = pow((ax-dx)*(ax-dx)+(ay-dy)*(ay-dy),0.5)
        D2.append((i,(dab,dbc,dcd,dda)))
    writeCSV(D2,('Dab','Dbc','Dcd','Dda'),'Catch_Va %d_Vb %d_Vc %d_Vd %d _ Distances'%(va,vb,vc,vd),s = 10)

######################################################################################################
######################################################################################################
######################################################################################################


def nature(k1,k2,c1,c2,a1,a2,p0,q0,typ = 'comp',duration = 10,step = 0.0001):
    def pp(t,p,q):
        return  k1 * float(p) * (1.0 - float(p)/c1)+(-1.0*                   a1*p*q)
    def qp(t,p,q):
        return  k2 * float(q) * (1.0 - float(q)/c2)+(1.0-2*(typ == 'comp'))*(a2*p*q)

    print (1.0-2*(typ == 'comp'))
    
    P = Function(pp,3,'P')
    Q = Function(qp,3,'Q')
    
    rk4(0,duration,step,((p0,q0),(P,Q)),'Nature_%s'%(typ))
    


######################################################################################################
######################################################################################################
######################################################################################################

def dampOsc(c = 0.1,m = 0.2,k = 20.0,x0 = 100,v0 = 0): #Example of Damped Oscillation
    
    def f1(t,x,y):
        return y
    
    def f2(t,x,y):
        return -k/m*x-c/m*y
    
    F1 = Function(f1,3,'f1')
    F2 = Function(f2,3,'f2')
    
    X = rk4(0,10,0.0001,((x0,v0),(F1,F2)),'DampOsc c_%.1f,m_%.1f,k_%.1f'%(c,m,k),wCmd=())
    animateF(X[0],X[1],X[2],subj=[('t','f1'),('t','f2')],tail = 0)
    #animateF(X[0],X[1],X[2],subj=[('f1','f2')])
    writePLOT(X[0],X[1],X[2])

######################################################################################################
######################################################################################################
######################################################################################################


def doublePendulum(m1=1,m2=1,l1=1,l2=1,a0=0,b0=0,wa0=0,wb0=10,g=9.8,time = 15,step = 0.0013):
    
    def f1_a(t,a,b,wa,wb):
        return wa
    
    def f2_b(t,a,b,wa,wb):
        return wb
    
    def f3_wa(t,a,b,wa,wb):
        return -1*(m1*g*sin(a)+m2*sin(a-b)*(g*cos(b)+l1*cos(a-b)*(pow(wa,2)) + l2*(pow(wb,2))))/(l1*(m1+m2*(pow((sin(a-b)),2))))

    def f4_wb(t,a,b,wa,wb):
        return (sin(a-b)*((m1+m2)*g*cos(a)+(m1+m2)*l1*(pow(wa,2))+m2*l2*cos(a-b)*(pow(wb,2))))/(l1*(m1+m2*(pow((sin(a-b)),2))))
    
    F1 = Function(f1_a,5,'alpha')
    F2 = Function(f2_b,5,'beta')
    F3 = Function(f3_wa,5,'wa')
    F4 = Function(f4_wb,5,'wb')

    D1 = rk4(0,time,step,((a0,b0,wa0,wb0),(F1,F2,F3,F4)),'Double Pendulum wa0_%d wb0_%d timestep_%fs'%(wa0,wb0,step))[0]
    D2 = []
    for i,j in D1: #Changing the set of angles into rectangular coordinates
        a = j[0]
        b = j[1]
        x1 = l1*sin(a)
        y1 = -l1*cos(a)
        x2 = l1*sin(a)+l2*sin(b)
        y2 = -(l1*cos(a)+l2*cos(b))
        D2.append((i,(x1,y1,x2,y2)))
    
    #writeCSV(D2,('x1','y1','x2','y2'),'Double Pendulum_Processed wa0_%d wb0_%d timestep_%fs'%(wa0,wb0,step))
    animateF(D2,('x1','y1','x2','y2'),'Double Pendulum',subj = [('x1','y1'),('x2','y2')],conS=('0',0,1),tail = 0)
    animateF(D2,('x1','y1','x2','y2'),'Double Pendulum',subj = [('x1','y1'),('x2','y2')],conS=('0',0,1),tail = 1)



def chemical(e,d,q,x0,y0,z0,duration = 100,step = 0.0001):
    def xp(t,x,y,z):
        return (1.0/e)*(q*y-x*y+x*(1.0-x))
    
    def yp(t,x,y,z):
        return (1.0/d)*(-q*y-x*y+pow(z,2))
    
    def zp(t,x,y,z):
        return float(x)-float(z)
    
    X = Function(xp,4,'x')
    Y = Function(yp,4,'y')
    Z = Function(zp,4,'z')

    rk4(0,duration,step,((x0,y0,z0),(X,Y,Z)),'Chemical reaction _ e = %f_2'%e)
    

def natural2(x0=1200,y0=450,z0=60,duration = 1000,step = 0.001):
    def xp(t,x,y,z):
        return x*(1.0-x/3000.0-2*y/1500.0)
    def yp(t,x,y,z):
        return y*(1-x/3000.0-y/1500.0-z/300.0)
    def zp(t,x,y,z):
        return z*(-1+y/500.0)
    
    X = Function(xp,4,'x')
    Y = Function(yp,4,'y')
    Z = Function(zp,4,'z')
    rk4(0,duration,step,((x0,y0,z0),(X,Y,Z)),'natural2')


    #(1)
    #nature (k1 = 10,k2 = 20,c1 = 1000,c2 = 100,a1 = 1.0/20,a2 = 1.0/100,p0 = 800, q0 = 50,step = 0.0001,typ = 'comp')
    #nature (20,30,1500,500,1.0/100,1.0/20,1000,300,typ = 'pp')

    #(2)
    #rocketN(v0=1000)
    #rocketR(v0=10000)
    #rocketR(v0=60000000)
    

    #(4)
    #catch(va = 12,vb = 13,vc = 15)
    #catch(va = 10,vb = 10,vc = 10)
    
    #dampOsc()
    #doublePendulum(step = 0.0001,m1 = 1,m2=1,l1=3,l2=3,a0=1,b0=1.4,wa0=0,wb0=4)
    #chemical(e=1.0/100,d=1.0/3,q=1.0/200,x0=1.0,y0=0.1,z0=0.09,duration = 100,step = 0.0001)
    #natural2()
    #catch4(va = 10,vb = 10,vc = 10,vd = 10,duration = 15)

def showcase():
    catch(va = 12,vb = 13,vc = 15)
    doublePendulum(step = 0.0001,m1 = 1,m2=1,l1=3,l2=3,a0=1,b0=1.4,wa0=0,wb0=4)
    dampOsc()
showcase()