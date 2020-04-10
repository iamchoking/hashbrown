#-*-coding:utf-8-*-

import numpy as np
from openpyxl import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import copy

outs = 10
# outs denotes how many actual data is recorded as the output (10 means every 10th step is recorded

def rectXLSX(ws,rect):
    for i in range(len(rect)):
        for j in range(len(rect[i])):
            ws.cell(row=1+i,column=1+j).value=rect[i][j]
    return ws


class Result():
    def __init__(self,values,varName,name):
        self.values = values
        self.varName = varName
        self.name = name
        self.timestepR = values[1][0]-values[0][0] #timestep for inherent value dataset

    def __str__(self):
        S = ''
        for i in self.varName:
            S += '%s\t'%i
        S+= '\n'
        for j in self.values:
            S+= '\n%f' %(j[0])
            for k in j[1]:
                S+='\t%f' %(k)
        return S

    def get(self,t,varN = ''):
        if varN == '':
            return self.values[int(t/self.timestepR)]
        return self.values[int(t/self.timestepR)][1][self.varName.index(varN)]

    def write(self,wCmd=()):
        print ('Initiate Output Module ...\n')
        if 'csv' in wCmd:
            writeCSV(values,varName,name,s=outs)
        if 'xlsx' in wCmd:
            writeXLSX(values,varName,name,s=outs)
        if 'plot' in wCmd:
            writePLOT(values,varName,name,s=outs)
        if 'animate' in wCmd:
            animateF(values,varName,name,s=outs)
        return values

    def writeCSV(self,s=1):
        print ('Writing CSV file...\n')
        S = 't'
        for i in self.varName:
            S += ',%s'%(i)
        
        for i in self.values[::s]:
            S+= '\n'+str(i[0])
            for j in i[1]:
                S += ','+str(j)
        f = open(self.name+'.csv','w')
        f.write(S)
        f.close()
        #print values
        print ('\nCSV Output Successful\nName >> %s'%(self.name+'.csv'))        


    def spl(self,s=1,incT=0): #incT denotes the new desired timestep
        if incT !=0:
            s = int(incT/(self.timestepR))
        L = dict()
        L['t'] = []
        for i in self.varName:
            L[i] = []
        for i in self.values[::s]:
            L['t'].append(i[0])
            for j in range(len(i[1])):
                L[self.varName[j]].append(i[1][j])
        timestep = L['t'][1]-L['t'][0]
        return (L,timestep,)
    
    def rect(self,s=1,incT=0,incN=True): #incN determines to include the name or not
        X = [tuple(['t']+list(self.varName))]
        if incT !=0:
            s = int(incT/(self.timestepR))
        for i in self.values[::s]:
            temp = []
            temp.append(i[0])
            for j in i[1]:
                temp.append(j)
            X.append(temp)
        return X


    def writeXLSX(self,s=1):
        print ('Writing XLSX file...\n')
        wb = Workbook()
        ws = wb.active
        ws.title = self.name[:30] #worksheet title cannot be longer than 31 characters!
        rectXLSX(ws,self.rect(s))
        wb.save(self.name+'.xlsx')
        print ('\nEXCEL Output Successful\nName >> %s'%(self.name+'.xlsx'))
        return wb

    def writePLOT(self,points = 1000,s=1,subj = False):
        print ('Plotting Result...\n')
        if points == 0:
            D = self.spl(s)[0]
        else:
            D = self.spl(incT = self.values[-1][0]/points)[0]
            
        #print (self.varName)
        #print ('top',subj)
        if subj == False:
            subj = []
            for i in self.varName:
                subj.append(('t',i))
        
        xlab,ylab = '',''
        for i in subj:
            xlab += '%s, ' %(i[0])
            ylab += '%s, ' %(i[1])
        plt.xlabel(xlab[:-2])
        plt.ylabel(ylab[:-2])

        for i in subj:
            #print (i)
            plt.plot(D[i[0]],D[i[1]],label = '%s - %s' %(i[0],i[1]) )
        t = ''
        #print (self.name)
        t += self.name+'\n'

        for i in subj:
            t += i[1] + ', '
        t = t[:-2] + ' - '
        for j in subj:
            t += i[0] + ', '
        plt.title(t[:-2] + ' graph')
        plt.grid(b=None, which='major', axis='both')
        plt.legend()
        plt.show()
        subj = []
        #print ('bottom',subj)
        print ('Plotting Complete')

    def animateF(self,subj = [],scale = 1, tail = 1,conS = ()): 
        print ('Prepairing Animation...\n')
    
        #scale governs the scale ratio between the real and animated time, and tail governs the 'time length' of tail
        #subj governs the things to plot ex) (('x','y'),('t','x')) versus time
        #conn connects the respective places. (putting 'O' includes the origin as the starting point) (putting 'L' forms a loop)
        
        #default subject graphs everything agianst time with respect to time
        if subj == []:
            for i in self.varName:
                subj.append(('t',i))
        
        # initialize object necessary
        L,timestep = self.spl(incT = 0.01*scale)
        #print (timestep)
        #initialize matplotlib objects
        fig = plt.figure()
        axes = plt.gca()
        
        # initialize line variables
        Lines = []
        con = False
        coz = False
        coL = False
        if conS != ():
            con = True
            if '0' in conS:
                coz = True
            if 'L' in conS:
                coL = True
            link, = axes.plot([],[],label = 'link')
        for i in subj:
            Lines.append(axes.plot([], [], label = '(%s,%s)vs Time'%(i[0],i[1])))
    #    line, = Lines[0]
    #    print (type(line))
        
        if tail == 0:
            #print ('tail zero')
            def ani(t):
                for i in range(len(Lines)):
                    line, = Lines[i]
                    line.set_xdata(L[subj[i][0]][:int(t/timestep)])
                    line.set_ydata(L[subj[i][1]][:int(t/timestep)])
                # Set up the links
                if con:
                    x,y = [],[]
                    if coz:
                        x,y = [0],[0]
                    for i in conS:
                        if type(i) == int:
                            x.append(L[subj[i][0]][int(t/timestep)])
                            y.append(L[subj[i][1]][int(t/timestep)])
                    if coL:
                        x.append(x[0])
                        y.append(y[0])
                    link.set_xdata(x)
                    link.set_ydata(y)
    
        else:
            def ani(t):
                x = t-tail
                if x<0:
                    x = 0
                for i in range(len(Lines)):
                    line, = Lines[i]
                    line.set_xdata(L[subj[i][0]][int(x/timestep):int(t/timestep)])
                    line.set_ydata(L[subj[i][1]][int(x/timestep):int(t/timestep)])
                #Set up the links
                if con:
                    x,y = [],[]
                    if coz:
                        x,y = [0],[0]
                    for i in conS:
                        if type(i) == int:
                            x.append(L[subj[i][0]][int(t/timestep)])
                            y.append(L[subj[i][1]][int(t/timestep)])
                    if coL:
                        x.append(x[0])
                        y.append(y[0])
                    link.set_xdata(x)
                    link.set_ydata(y)
        
        # determines proper x, y lim
        axes.set_autoscale_on(False)
        X = []
        Y = []
        #for i in L.keys():
        #    print (i,L[i][:10])
        #print (subj)
        for i in subj:
            X += L[i[0]]
            Y += L[i[1]]
        minX,minY,maxX,maxY = min(X),min(Y),max(X),max(Y)
        if subj[0][0] == 't':
            axes.set_xlim(min(L['t']),max(L['t']))
            axes.set_ylim(minY-abs(minY*0.05),maxY+abs(maxY*0.05))
        else:
            axes.set_xlim(minX-abs(minX*0.05),maxX+abs(maxX*0.05))
            axes.set_ylim(minY-abs(minY*0.05),maxY+abs(maxY*0.05))
    
        # the initialization and formats are in place. now for the animation.
        quality = 10/scale
        anchor = np.arange(0,L['t'][-1],1/quality)
        intV = 0.01
        plt.show()
        plt.title(self.name+'\nAnimation %s vs time'%(str(subj)))
        plt.legend()

        for i in anchor:
            ani(i)
            plt.draw()
            plt.pause(1e-17)
            time.sleep(intV)
        time.sleep(2)
        plt.close(fig)
        print ('Animation Finished\n')
    

   
if __name__ == '__main__':
    pass