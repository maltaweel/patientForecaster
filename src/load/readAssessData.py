'''
Created on 06/02/2018

@author: mark
'''

import os
import csv
from datetime import datetime

class ReadAssessData: 
    c_names=set(['N30','N34','N50'])
    time_names=set(['N6','N22'])
    
    def path(self):
        
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]
        

        #The data file path is now created where the data folder and dataFile.csv is referenced
        filepath=os.path.join(pn,'data')
        
        return filepath

    def loadFile(self,filepath):
        
        files=os.listdir(filepath)
        
        self.location={}
        self.values={}
        
        self.timeL={}
        self.timeV={}
        
        self.patients=[]
        
        for fs in files:
            
            fs=os.path.join(filepath,fs)
            
            #first, open the file 
            with open(fs, 'rb') as csvfile:
                reader = csv.reader(csvfile, delimiter=',',quotechar='"')
                
                r=0
                for re in reader:
                    
                    c=0
                    for s in re:
                        if r==0:
                            if s in self.c_names:
                                self.location[s]=c
                                
                            if s in self.time_names:
                                self.timeL[s]=c
                              
                        else:
                            
                            if c==0:
                                self.patients.append(s)
                                
                            if c in self.values.keys():
                                vs=self.values.get(c)
                                vs.append(s)
                                
                            if c in self.location.values():
                                if c not in self.values.keys():
                                    vs=[]
                                    vs.append(s)
                                    self.values[c]=vs
                            
                            if c in self.timeV.keys():
                                tv=self.timeV[c]
                                tv.append(s)
                                
                            if c in self.timeL.values():
                                if c not in self.timeV.keys():
                                    tv=[]
                                    tv.append(s)
                                    self.timeV[c]=tv
                            
                                     
                        c+=1      
                    r+=1  
            
    def runPatientAnalysis(self):
        
        n=self.location['N30']
        self.identifiedSick=[]
        vs=self.values[n]
        
        self.includedPatientsLocation=[]      
        for i in range(0,len(vs)):
            v=int(vs[i])
                   
            if(v>=18 and v<=85):
                nn=self.location['N34']
                vss=self.values[nn]
                vv=int(vss[i])
                
                if(vv>5):
                    nnn=self.location['N50']
                    
                    vsss=self.values[nnn]
                    vvv=int(vsss[i])
                    if(vvv<3):
                        self.identifiedSick.append(self.patients[i])
                        self.includedPatientsLocation.append(i)
                            
    def timeFormat(self, formatt):
        date_format=''
        
        if '/' in formatt and ' ' in formatt:
            date_format='%m/%d/%Y %H:%M'
            
        elif "/" in formatt:
            date_format='%m/%d/%Y'
        
        elif "AM" in formatt or "PM" in formatt:
            date_format= '%I:%M%p'
        
        elif ":" in formatt:
            date_format = "%H:%M"
        
        else:
            date_format='%d%B%Y:%H:%M'  
                
        return date_format                       
                
    def runTimeAnalysis(self):
        self.lessThreeHundred=[]
        self.greaterThreeHundred=[]
        
        lf=self.timeL['N22'] 
        rt=self.timeL['N6']      
         
        lv=self.timeV[lf]
        rv=self.timeV[rt]
        
        for i in self.includedPatientsLocation:
            l=lv[i]
            r=rv[i]
            
            date_format=self.timeFormat(l)
             
            time1=datetime.strptime(l, date_format)
            time2=datetime.strptime(r, date_format)
            
            time=time1-time2
            
            if(time.days<0):
                time1=datetime(year=time1.year,month=time1.month,
                               day=time1.day+1,hour=time1.hour,minute=time1.minute)
                time=time1-time2
            
            minutes=float(time.seconds/60)
            
            if(minutes<300.0):
                self.lessThreeHundred.append(self.patients[i])
            
            else:
                self.greaterThreeHundred.append(self.patients[i])
       
    def printResults(self):
        
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]
        
        #output path
        filename=os.path.join(pn,'output','patients.csv')

        fieldnames = ['Identified Patients','Less 300 Minutes',"More 300 Minutes"]

        with open(filename, 'wb') as csvf:
            writer = csv.DictWriter(csvf, fieldnames=fieldnames)
    
            writer.writeheader()
  
            for i in range(0,len(self.patients)):
                sick=''
                less300=''
                greater300=''
                
                if i <= len(self.identifiedSick)-1:
                    sick=self.identifiedSick[i]
                if i <= len(self.lessThreeHundred)-1:
                    less300=self.lessThreeHundred[i]
                if i <= len(self.greaterThreeHundred)-1: 
                    greater300=self.greaterThreeHundred[i] 
                
                writer.writerow({'Identified Patients':sick,'Less 300 Minutes':less300,'More 300 Minutes':greater300})   
                 
                   
ld=ReadAssessData()
filepath=ld.path()
ld.loadFile(filepath)
ld.runPatientAnalysis()
ld.runTimeAnalysis()
ld.printResults()

print('finished')
