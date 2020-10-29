#-*-coding:utf-8-*-

import numpy as np
import openpyxl as xl
# import matplotlib
# print (matplotlib.get_backend())
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import mpl_toolkits.mplot3d.axes3d as p3


class InvalidAttach(Exception):
    pass

class UnmatchingSubj(Exception):
    pass

def rectXLSX(ws,rect):
    for i in range(len(rect)):
        for j in range(len(rect[i])):
            ws.cell(row=1+i,column=1+j).value=rect[i][j]
    return ws


class Result():
    """
    hashbrown: Result Class

    Parameters
    ----------
    values (tuple): an iterable with the form of ((t0,(x10,x20,x30)),(t1,(x11,x21,x31)),...), which is a typical output of rk4 function
    
    varName (tuple): an iterable listing each names of variables ('t' is reserved for time)
    
    name   (string): name of Result

    Notes
    -----
    A dictionary representation is automatically generated, which is used by most built-in methods in hashbrown.
    """

    def __init__(self,values,varName,name):
        """
        hashbrown: Result Class

        Parameters
        ----------
        values (tuple): an iterable with the form of ((t0,(x10,x20,x30)),(t1,(x11,x21,x31)),...), which is a typical output of rk4 function
        
        varName (tuple): an iterable listing each names of variables ('t' is reserved for time)
        
        name   (string): name of Result

        Notes
        -----
        A dictionary representation is automatically generated, which is used by most built-in methods in hashbrown.
        """
        self.values = values  #format: [(t0,(x1,x2,x3)),(t0+timestep,(x1,x2,x3), ...)
        self.varName = varName
        self.name = name
        self.timestepR = values[1][0]-values[0][0] #timestep for inherent value dataset

        #a new representation is introduced (ver 4.3.1) Result.L: a dictionary with variables (including t) as keys and list their values (chronological) as values.
        self.L = dict()
        self.L['t'] = []
        for i in self.varName:
            self.L[i] = []
        
        for j in values:
            self.L['t'].append(j[0])
            for k in range(len(j[1])):
                self.L[varName[k]].append(j[1][k])

        self.L['t'] = np.array(self.L['t'])
        for l in self.varName:
            self.L[l]  =np.array(self.L[l])
    #X1#BUILTIN OVERLOADS

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

    #X2#Result-Result Relation methods

    def get(self,t,varN = ''):
        """
        retrieves value(s) of a result at a given time

        Parameters
        ----------
        t (number): time

        varN (string): name of variable (case sensitive). If left blank, .get() returns a tuple of all outputs at a given time

        Notes
        -----
        output is not interpolated, but rounded down to the nearest timestep.
        """
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
        """
        merges two Result class objects and returns it. the timeframe casts to that of (self)

        Parameters
        ----------
        R (Result Class): another result class variable to merge: X.merger(Y,~) means that Y X is merged with Y


        name (string): name of the returned class Result. default: self.name + ', ' + R.name 

        varMerge (bool): when true, merges variable names without changing variable name. when false, R's varname is chages to R.name+(varname)

        Notes
        -----
        Only set varMerge to True when it is confirmed that the varNames of the two variables do not interfere.
        """

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
                print ('[hashbrown] WARN>> merge conflict: '+self.get(i)[1] , R.get(i)[1])
                newVal.append((i,list(self.get(i)[1]) + list(R.get(i)[1])))                
        return Result(newVal,newvarName,newname)
    
    def attach(self,R):
        """
        attaches two (Class Result)'s into a continuous Result and returns it.

        Parameters
        ----------
        R (Class Result): the Result class variable to attach. must have same .timestepR and coincide at one point.

        Notes
        ----------
        Internal Function. not recommended for use in user API
        """
        if R.varName != self.varName:
            raise InvalidAttach('Attachment not compatible (varName different)')
        elif self.values[-1][0] - R.values[0][0] >= self.timestepR:
            raise InvalidAttach('Attachment not compatible (time incompatible)')
        elif self.timestepR - R.timestepR >= self.timestepR*0.01:
            raise InvalidAttach('Attachment not compatible (timestep incompatible)')
        return Result(self.values+R.values[1:],self.varName,self.name)

    #X3#Table output methods

    def rect(self,s=1,incT=0,incN=True): #incN determines to include the name or not
        """
        returns a "rectangular" 2D iterable containing values.

        Parameters
        ----------
        s (int): skip factor: only samples 1 out of s data. (defaults to 1)

        incT (num): time increment. overrides s

        incN (bool): include name: if true: the first "row" is an iterable of 't' followed by varnames

        Notes
        -----
        usually used for excel and csv output methods. not recommended for user API use
        """
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

    def writeCSV(self,s=1):
        """
        writes a csv file in the same directory of the running root directory.

        Parameters
        ----------
        s (int): skip factor: only samples 1 out of s data. (defaults to 1)

        Notes
        -----
        writeCSV is faster than writeXLSX. recommeded to use this if simple value obtaining is the focus
        """
        print ('[hashbrown] Writing CSV file...')
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
        print ('[hashbrown] CSV Output Successful\n\tName >> %s\n'%(self.name+'.csv')) 

    def writeXLSX(self,s=1):
        """
        writes an excel file in the same directory of the running root directory.

        Parameters
        ----------
        s (int): skip factor: only samples 1 out of s data. (defaults to 1)

        Notes
        -----
        writeCSV is faster than writeXLSX. recommeded to use writeCSV if simple value obtaining is the focus
        """
        print ('[hashbrown] Writing XLSX file...')
        wb = xl.Workbook()
        ws = wb.active
        ws.title = self.name[:30] #worksheet title cannot be longer than 31 characters!
        rectXLSX(ws,self.rect(s))
        wb.save(self.name+'.xlsx')
        print ('[hashbrown] EXCEL Output Successful\n\tName >> %s\n'%(self.name+'.xlsx'))
        return wb

    #X4#Visualization Methods

    def close(self):
        """
        closes open plots

        Notes
        -----
        Not a dependant method. call by [Result.close()]
        """
        plt.close()

    def writePLOT(self,subj = None,points = 1000,s=1):
        """
        plots a Class Result as described by parameters

        Parameters
        ----------
        subj (list): list of (tuples of length 2 or 3). rules which variables are animated. default value results in all variables plotted (2D) against time

        points (int): total number of points within plot. used for time - efficient plotting. overrides s. default 1000

        s (int): skip factor: only samples 1 out of s data.

        Notes
        -----
        subj = [('t','a'),('t','b')] plotts with x axis as time, and y axis as values, overlapped

        subj can contain tuples of length 3, this results in a 3D plot.
        
        all elements of subj must have the same length.
        """		
        print('[hashbrown] Plotting: %s'%(self.name))
        
        if subj == None:
            subj = []
            for i in self.varName:
                subj.append(('t',i))
        
        # initialize objects
        L = self.L
        timestep = self.timestepR
        timestep = timestep + 1 - 1 #haha someone find this please
        for i in subj:
            if len(i) != len(subj[0]) or (len(i)!=2 and len(i)!=3):
                raise(UnmatchingSubj("Subject array invalid (Length). Animate Failed."))

        is2D = (len(subj[0]) == 2)

        if is2D:
            fig,ax = plt.subplots()

        else:
            fig = plt.figure()
            ax = p3.Axes3D(fig)

        ######################################################		
        xlab,ylab,zlab = '','',''
        for i in subj:
            xlab += '%s, ' %(i[0])
            ylab += '%s, ' %(i[1])
            if not is2D:
                zlab += '%s, ' %(i[2])

        ax.set_xlabel(xlab[:-2])
        ax.set_ylabel(ylab[:-2])
        if not is2D:
            ax.set_zlabel(zlab[:-2])
        
        Hskipper = s
        if points != 0:
            Hskipper = len(self.L['t'])//int(points)

        for i in subj:
            if is2D:
                ax.plot(L[i[0]][::Hskipper],L[i[1]][::Hskipper], label = '%s - %s' %(i[0],i[1]) )
            else:
                ax.plot(L[i[0]][::Hskipper],L[i[1]][::Hskipper],L[i[2]][::Hskipper], label = '%s - %s - %s' %(i[0],i[1],i[2]))

        #print (self.name)
        t = self.name+'\n'
        for i in subj:
            t += i[0] + ', '
        t = t[:-2] + ' - '
        for i in subj:
            t += i[1] + ', '
        t = t[:-2] + ' - '

        if not is2D:
            for i in subj:
                t += i[2] + ', '
        
        # plt.title(t[:-2] + ' graph')
        fig.suptitle(t[:-2] + ' graph')
        plt.legend(loc = 'lower right')

        if points == 0:
            points == len(self.L['t'])/s
        
        print ('[hashbrown] Plot Complete : %s'%(self.name+' : '+str(subj)))
        if is2D:
            print('\tDimension: 2D')
        else:
            print('\tDimension: 3D')
        print('\tMapped Points: %d\n'%(points))

        plt.show()

        plt.ioff()		
        #plt.ion() 
        #ion results in a lagging plot while input() is atcive
        
        plt.pause(0.05)
        #this pause is in case a "hold" function (such as input() is active before / after plt.show(). This helps the plot appear)

    def animateF (self,subj = None,scale = 1,tail = 1,conS = None):
        """
        an obsolete function for animation. kept for version consistancy.

        Parameters
        ----------
        subj (list): list of (tuples of length 2 or 3). rules which variables are animated. default value results in all variables animated (2D) against time

        scale (num): an "abstract" scale for time

        tail (num): the "time length" of the animated line; the time difference of the newest and oldest point in the animated line. 0 results in infinite tail.

        conS (None): [Deleted]

        Notes
        -----
        subj = [('t','a'),('t','b')] animates with x axis as time, and y axis as values, overlapped

        subj can contain tuples of length 3, this results in a 3D animation.
        
        all elements of subj must have the same length.
        """
        self.writeANIM(subj,scale*3,tail)
        return

    def writeANIM(self,subj = None,timescale = 1, tail = 1, refreshRate = 20, quality = 100): 
        """
        animates the subject Result with the given parameters. utilizes matplotlib.animation.FuncAnimation() method

        Parameters
        ----------
        subj (list): list of (tuples of length 2 or 3). rules which variables are animated. default value results in all variables animated (2D) against time

        timescale (num): ratio of playback speed and actual time speed (defaults to 1)

        tail (num): the "time length" of the animated line; the time difference of the newest and oldest point in the animated line. 0 results in infinite tail.

        refreshRate (int): the refresh rate (Hz) of the animation. Defaults to 20

        quality (int): number of points animated on a segment which is equivalent to 1 second of time. Defaults to 100.

        Notes
        -----
        subj = [('t','a'),('t','b')] animates with x axis as time, and y axis as values, overlapped

        subj can contain tuples of length 3, this results in a 3D animation.
        
        all elements of subj must have the same length.

        quality = 200 and tail = 3 yields a total of 600 animated points
        """
    
        #scale governs the scale ratio between the real and animated time, and tail governs the 'time length' of tail
        #subj governs the things to plot ex) (('x','y'),('t','x')) versus time
        #conn connects the respective places. (putting 'O' includes the origin as the starting point) (putting 'L' forms a loop)
        
        #default subject graphs everything with respect to time
        
        #tail as an int (30): the time difference of the two tips 0: infinite tail
        #tail as a string ('30'): the number of points between the two tips

        print ('[hashbrown] Prepairing Animation: %s '%(self.name))

        if subj == None:
            subj = []
            for i in self.varName:
                subj.append(('t',i))
        
        # initialize objects
        L = self.L
        timestep = self.timestepR

        for i in subj:
            if len(i) != len(subj[0]) or (len(i)!=2 and len(i)!=3):
                raise(UnmatchingSubj("Subject array invalid (Length). Animate Failed."))

        is2D = (len(subj[0]) == 2)

        if is2D:
            fig,ax = plt.subplots()

        else:
            fig = plt.figure()
            ax = p3.Axes3D(fig)

        Lines = []
        #Lines: actual plot lines that are written in object (use set_data (and maybe set_3d_properties))
        #L: stores all plot data that are written in object as a dictionary (same format as self.L)

        # as animate(~) cannot pass empty lines, the first point of each line is passed as initial.
        if is2D:
            for i in subj:
                # print (type(i),"Line 528")
                Lines.append(ax.plot([L[i[0]][0]],[L[i[1]][0]],label = '(%s,%s)vs Time'%(i[0],i[1])) )
        else:
            for i in subj:
                # print (L['t'],'line 533')
                Lines.append(
                    ax.plot(
                        [L[i[0]][0]],
                        [L[i[1]][0]],
                        [L[i[2]][0]],
                        label = '(%s,%s,%s)vs Time' %(i[0],i[1],i[2]))
                        )
        
        #Setting up labels
        xlab,ylab,zlab = '','',''

        for i in subj:
            xlab += '%s, ' %(i[0])
            ylab += '%s, ' %(i[1])

            if not is2D:
                zlab += '%s, ' %(i[2])


        ax.set_xlabel(xlab[:-2])
        ax.set_ylabel(ylab[:-2])
        
        if not is2D:
            ax.set_zlabel(zlab[:-2])
        
        #TODO: add init funciton for blitting

        def animate(t,Lines,L,is2D,tail,skipper):
            x = t-tail
            if tail == 0:
                x = 0
            if x<0:
                x = 0
            for i in range(len(Lines)):
                line, = Lines[i]
                if is2D:
                    line.set_data([
                        L[subj[i][0]][int(x/timestep):int(t/timestep):skipper],
                        L[subj[i][1]][int(x/timestep):int(t/timestep):skipper]
                        ])
                else:
                    line.set_data([
                        L[subj[i][0]][int(x/timestep):int(t/timestep):skipper],
                        L[subj[i][1]][int(x/timestep):int(t/timestep):skipper]
                        ])
                    line.set_3d_properties(L[subj[i][2]][int(x/timestep):int(t/timestep):skipper])
                        # line.set_3d_properties(L[subj[i][2]][int(x/timestep):int(t/timestep)])
            return Lines
        
        # determines proper x, y lim
        ax.set_autoscale_on(False)
        X,Y,Z = [],[],[]
        #for i in L.keys():
        #    print (i,L[i][:10])
        #print (subj)
        for i in subj:
            X+=list(L[i[0]])
            Y+=list(L[i[1]])
            if not is2D:
                Z+=list(L[i[2]])
        minX,minY,maxX,maxY = min(X),min(Y),max(X),max(Y)
        if not is2D:
            minZ,maxZ = min(Z),max(Z)

        if is2D:
            ax.set_xlim(minX-abs(minX*0.05),maxX+abs(maxX*0.05))
            ax.set_ylim(minY-abs(minY*0.05),maxY+abs(maxY*0.05))
        else:
            ax.set_xlim3d(minX-abs(minX*0.05),maxX+abs(maxX*0.05))
            ax.set_ylim3d(minY-abs(minY*0.05),maxY+abs(maxY*0.05))
            ax.set_zlim3d(minZ-abs(minZ*0.05),maxZ+abs(maxZ*0.05))
    
        # the initialization and formats are in place. now for the animation.

        #plt.ion() #do NOT turn interactive on for animation.
        plt.ioff()
        # plt.title(self.name+'\nAnimation %s vs time'%(str(subj)))
        fig.suptitle(self.name+'\nAnimation %s vs time'%(str(subj)))
        plt.legend(loc = 'lower right')

        #interval: 1000/refresh Rate
        #frames = np.arage((starting time),(ending time),interval*timescale)
        #skipper (animate: set_data ... [~:~:skpper]) = 1/quality*timestep
        Hinterval = int(1000//refreshRate)

        Hskipper = int(1/quality*timestep)
        if Hskipper == 0:
            Hskipper = 1
        
        Hframes = np.arange(L['t'][0],L['t'][-1],Hinterval/1000*timescale)

        print("[hashbrown] Animation Ready! : "+self.name+(' Animation %s vs time'%(str(subj))) )
        if is2D:
            print("\tDimension: 2D")
        else:
            print("\tDimension: 3D")
        
        if tail==0:
            print('\tTail: Infinite')
        else:
            print('\tTail: %.3f sec'%(float(tail)))
        print("\tRefresh Rate: %d\n\tTimescale: %.3f x realtime \n\tQuality: %d (points per second)\n"%(refreshRate,float(timescale),quality))

        ani = animation.FuncAnimation(fig, animate, Hframes, fargs=(Lines,L,is2D,tail,Hskipper),interval=Hinterval, blit=False)
        #one of the most complicated functions. Strongly recommend investigating how this works with the man page

        plt.show()
        plt.pause(0.05) # for some reason, some environments do not display animation since they do not exit .show()

        return ani
   
if __name__ == '__main__':
    pass