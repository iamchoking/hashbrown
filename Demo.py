#-*-coding:utf-8-*-
from hashbrown import *

def catch(va = 0,vb = 0, vc = 0, A0 = (0,0), B0 = (300,0),C0 = (150,180),duration = 20,step = 0.001):
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

    D = rk4(0,duration,step,((A0[0],A0[1],B0[0],B0[1],C0[0],C0[1]),(Ax,Ay,Bx,By,Cx,Cy)),'Catch_Va %d_Vb %d_Vc %d'%(va,vb,vc))
    D.animateF(subj=[('Ax','Ay'),('Bx','By'),('Cx','Cy')],tail = 0,scale = 3,conS = (0,1,2,'L'))

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
    
    X = rk4(0,20,0.0001,((x0,v0),(F1,F2)),'DampOsc c_%.1f,m_%.1f,k_%.1f'%(c,m,k))
    X.writePLOT()
    X.writeCSV(10)
    X.writeXLSX(10)
    #print(X.get(1))
    #print(X.get(1,'f1'))

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

    D = rk4(0,time,step,((a0,b0,wa0,wb0),(F1,F2,F3,F4)),'Double Pendulum wa0_%d wb0_%d timestep_%fs'%(wa0,wb0,step))
    D1 = D.values
    D2 = []
    for i,j in D1: #Changing the set of angles into rectangular coordinates
        a = j[0]
        b = j[1]
        x1 = l1*sin(a)
        y1 = -l1*cos(a)
        x2 = l1*sin(a)+l2*sin(b)
        y2 = -(l1*cos(a)+l2*cos(b))
        D2.append((i,(x1,y1,x2,y2)))
    Dp = Result(D2,('x1','y1','x2','y2'),'Double Pendulum')
    
    #writeCSV(D2,('x1','y1','x2','y2'),'Double Pendulum_Processed wa0_%d wb0_%d timestep_%fs'%(wa0,wb0,step))
    Dp.animateF(subj = [('x1','y1'),('x2','y2')],conS=('0',0,1),tail = 0)
    Dp.animateF(subj = [('x1','y1'),('x2','y2')],conS=('0',0,1),tail = 1)
    ######################################################################################################
    ######################################################################################################
    ######################################################################################################
    
    
def nature(k1,k2,c1,c2,a1,a2,p0,q0,typ = 'comp',duration = 10,step = 0.0001):
    def pp(t,p,q):
        return  k1 * float(p) * (1.0 - float(p)/c1)+(-1.0*                   a1*p*q)
    def qp(t,p,q):
        return  k2 * float(q) * (1.0 - float(q)/c2)+(1.0-2*(typ == 'comp'))*(a2*p*q)

    #print (1.0-2*(typ == 'comp'))
    
    P = Function(pp,3,'P')
    Q = Function(qp,3,'Q')
    
    D = rk4(0,duration,step,((p0,q0),(P,Q)),'Nature_%s'%(typ))
    #print (D.varName)
    D.writePLOT()
    input('continue')
    D.writePLOT(subj = [('P','Q')])

def natural2(x0=1200,y0=450,z0=60,duration = 150,step = 0.001):
    def xp(t,x,y,z):
        return x*(1.0-x/3000.0-2*y/1500.0)
    def yp(t,x,y,z):
        return y*(1-x/3000.0-y/1500.0-z/300.0)
    def zp(t,x,y,z):
        return z*(-1+y/500.0)
    
    X = Function(xp,4,'x')
    Y = Function(yp,4,'y')
    Z = Function(zp,4,'z')
    D = rk4(0,duration,step,((x0,y0,z0),(X,Y,Z)),'natural2')
    #writeCSV(*D,s=10)
    #writeXLSX(*D,s=50)
    D.writePLOT()
    input('continue')
    D.writePLOT(subj = [('x','y')])
    input('continue')
    D.animateF(subj=[('x','y')],tail = 0,scale = 10)
    input('continue')
    D.writePLOT(subj=[('x','y','z')])
    input('continue')
    D.animateF(subj=[('x','y','z')],tail = 0,scale = 10)


def showcase():
    dampOsc()
    input ('continue')    
    nature(k1 = 10,k2 = 20,c1 = 1000,c2 = 100,a1 = 1.0/20,a2 = 1.0/100,p0 = 800, q0 = 50,step = 0.0001,typ = 'comp')
    input ('continue')
    natural2()
    input ('continue')
    catch(va = 12,vb = 13,vc = 15)
    input ('continue')
    catch(va = 20,vb = 30, vc = 50, A0 = (0,0), B0 = (700,0),C0 = (1500,800),duration = 40,step = 0.001)
    input ('continue')
    doublePendulum(step = 0.0001,m1 = 1,m2=1,l1=3,l2=3,a0=1,b0=1.4,wa0=0,wb0=4)
    input ('continue')
    doublePendulum(step = 0.0001,m1 = 1,m2=1,l1=3,l2=3,a0=1,b0=1.4,wa0=-2,wb0=8)

if __name__ == '__main__':
    showcase()