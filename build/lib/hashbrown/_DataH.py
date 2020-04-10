#-*-coding:utf-8-*-

import numpy as np
from openpyxl import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import mpl_toolkits.mplot3d.axes3d as p3

outs = 10
# outs denotes how many actual data is recorded as the output (10 means every 10th step is recorded

class InvalidAttach(Exception):
    pass

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
        #print (name,values)
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
    
    def __len__(self):
        return len(self.varName)

    def get(self,t,varN = ''):
        if varN == '':
            if t <= self.values[0][0]:
                return self.values[0]
            if t >= self.values[-1][0]:
                return self.values[-1]
            return self.values[int((t-self.values[0][0])/self.timestepR)]
        if t <= self.values[0][0]:
            return self.values[0][1][self.varName.index(varN)]
        if t >= self.values[-1][0]:
            return self.values[-1][1][self.varName.index(varN)]
        return self.values[int((t-self.values[0][0])/self.timestepR)][1][self.varName.index(varN)]

    def merge(self,R,name = None,varMerge = False):
        newVal = []
        if varMerge:
            newvarName = self.varName+R.varName
        else:
            tsv = []
            trv = []
            for i in self.varName:
                if '_' in i:
                    tsv.append(i)
                    continue
                tsv.append('%s_%s'%(self.name,i))
            for i in R.varName:
                if '_' in i:
                    tsv.append(i)
                    continue                    
                trv.append('%s_%s'%(R.name,i))
            newvarName = tsv+trv
        if name == None:
            newname = self.name+', '+R.name
        else:
            newname = name
        ts = min(R.values[0][0],self.values[0][0])
        te = max(R.values[-1][0],self.values[-1][0])
        step = max(R.timestepR,self.timestepR)
        for i in np.arange(ts,te,step):
            #print (self.get(i)[1] , R.get(i)[1])
            try:
                newVal.append((i,self.get(i)[1] + R.get(i)[1]))
            except:
                print (self.get(i)[1] , R.get(i)[1])
                newVal.append((i,list(self.get(i)[1]) + list(R.get(i)[1])))                
        return Result(newVal,newvarName,newname)
    
    def attach(self,R):
        if R.varName != self.varName:
            raise InvalidAttach('Attachment not compatible (varName different)')
        elif self.values[-1][0] - R.values[0][0] >= self.timestepR:
            raise InvalidAttach('Attachment not compatible (time incompatible)')
        elif self.timestepR - R.timestepR >= self.timestepR*0.01:
            raise InvalidAttach('Attachment not compatible (timestep incompatible)')
        return Result(self.values+R.values[1:],self.varName,self.name)

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

    def plot3d(self,D,subj): #only invoke from writePLOT
        fig = plt.figure()
        ax1 = p3.Axes3D(fig)
        
        xlab,ylab,zlab = '','',''
        for i in subj:
            xlab += '%s, ' %(i[0])
            ylab += '%s, ' %(i[1])
            zlab += '%s, ' %(i[2])
        ax1.set_xlabel(xlab[:-2])
        ax1.set_ylabel(ylab[:-2])
        ax1.set_zlabel(zlab[:-2])
        
        for i in subj:
            ax1.plot(D[i[0]],D[i[1]],D[i[2]], label = '%s - %s - %s' %(i[0],i[1],i[2]))
        t = ''
        #print (self.name)
        t += self.name+'\n'
        for i in subj:
            t += i[0] + ', '
        t = t[:-2] + ' - '
        for i in subj:
            t += i[1] + ', '
        t = t[:-2] + ' - '
        for i in subj:
            t += i[2] + ', '
        plt.title(t[:-2] + ' graph')
        plt.legend()
        plt.ion()
        plt.show()
        subj = []
        #print ('bottom',subj)
        print ('Plotting Complete')      
    
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

        if len(subj[0]) == 3:
            self.plot3d(D,subj)
            return

        xlab,ylab = '',''
        for i in subj:
            xlab += '%s, ' %(i[0])
            ylab += '%s, ' %(i[1])
        plt.xlabel(xlab[:-2])
        plt.ylabel(ylab[:-2])
        
        #print (subj)

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
        plt.ion()
        plt.show()
        subj = []
        #print ('bottom',subj)
        print ('Plotting Complete')

    def animate3d(self,L,subj,scale,tail,timestep): #only invoke frome animateF (connection link is not yet supported)
        #initialize matplotlib objects
        fig = plt.figure()
        ax1 = p3.Axes3D(fig)        
        # initialize line variables
        Lines = []
        for i in subj:
            Lines.append(ax1.plot([L[i[0]][0]],[L[i[1]][0]], [L[i[2]][0]], label = '(%s,%s,%s)vs Time'%(i[0],i[1],i[2])))
        
        #Setting up labels
        xlab,ylab,zlab = '','',''
        for i in subj:
            xlab += '%s, ' %(i[0])
            ylab += '%s, ' %(i[1])
            zlab += '%s, ' %(i[2])
        ax1.set_xlabel(xlab[:-2])
        ax1.set_ylabel(ylab[:-2])
        ax1.set_zlabel(zlab[:-2])
        
        if tail == 0:
            def ani(t):
                for i in range(len(Lines)):
                    line, = Lines[i]
                    line.set_data([L[subj[i][0]][:int(t/timestep)],L[subj[i][1]][:int(t/timestep)]])
                    line.set_3d_properties(L[subj[i][2]][:int(t/timestep)])
        else:
            def ani(t):
                x = t-tail
                if x<0:
                    x = 0
                for i in range(len(Lines)):
                    line, = Lines[i]
                    line.set_data([L[subj[i][0]][int(x/timestep):int(t/timestep)],L[subj[i][1]][int(x/timestep):int(t/timestep)]])
                    line.set_3d_properties(L[subj[i][2]][int(x/timestep):int(t/timestep)])
        
        # determines proper x, y lim
        ax1.set_autoscale_on(False)
        X = []
        Y = []
        Z = []
        #for i in L.keys():
        #    print (i,L[i][:10])
        #print (subj)
        for i in subj:
            X += L[i[0]]
            Y += L[i[1]]
            Z += L[i[2]]
        minX,minY,maxX,maxY,minZ,maxZ = min(X),min(Y),max(X),max(Y),min(Z),max(Z)
        ax1.set_xlim3d(minX-abs(minX*0.05),maxX+abs(maxX*0.05))
        ax1.set_ylim3d(minY-abs(minY*0.05),maxY+abs(maxY*0.05))
        ax1.set_zlim3d(minZ-abs(minZ*0.05),maxZ+abs(maxZ*0.05))
    
        # the initialization and formats are in place. now for the animation.
        quality = 10/scale
        anchor = np.arange(0,L['t'][-1],1/quality)
        intV = 0.01
        plt.ion()
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

    def animateF(self,subj = [],scale = 1, tail = 1,conS = (),Csize = None): 
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
        
        if len(subj[0]) == 3:
            self.animate3d(L,subj,scale,tail,timestep)
            return        
        
        #initialize matplotlib objects
        if Csize == None:
            fig = plt.figure()
        else:
            fig = plt.figure(figsize=Csize)
        axes = plt.gca()
        
        #setting up labels
        xlab,ylab = '',''
        for i in subj:
            xlab += '%s, ' %(i[0])
            ylab += '%s, ' %(i[1])
        axes.set_xlabel(xlab[:-2])
        axes.set_ylabel(ylab[:-2])
        
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
        plt.ion()
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