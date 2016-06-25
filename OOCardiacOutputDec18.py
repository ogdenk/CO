#Cardiac Output Calculator
#Matt Vetere and Kent Ogden
#Last updated 12/18/14
#Current state: Is setup so that camparisons can be made to matlab algorithm results from excel file
#Most recent addition: added in the offsets from the new matlab csv

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import csv
import os
###will need to change directory based on location of "CardiacOutputData.csv" on computer
os.chdir("/Users/matt/Desktop")

totalPatients=94
maxShift=6
shiftIncrement=.25



class Patient:
    
    def __init__(self,number,data,offset): # makes a 'person' object with the number (ex. 0-93) and data array.  Other variables are 0 here but they get filled in in other methods
        self.number=number-1
        self.data=data
        self.offset=offset
        self.shift=0
        self.A=0
        self.alpha=0
        self.B=0
        self.times=0
        self.fitdata=0
        self.R2=0
        self.contTimes=0
        self.contData=0
        self.AUC=0
    def gammaFunc(self,tau,A,alpha,B):      #defines the gamma variate function            
        return(A*(tau**alpha)*np.exp(-tau/B))  
        
    def getCoeffs(self,shift): #uses the curvefit function to get coeffs.  Takes in the time shift as parameter
        self.shift=shift
        self.times=np.arange(self.shift,self.shift+len(self.data)*2,2)
        popt,pcov=curve_fit(self.gammaFunc,self.times,self.data,maxfev=50000) 
        self.A,self.alpha,self.B=popt[0],popt[1],popt[2] #popt is the coeff array
        
    def getR2(self): #calculates the R2
        self.fitData=self.A*(self.times**self.alpha)*np.exp(-self.times/self.B)
        dataMean=sum(self.data)/len(self.data)
        SStot=sum((self.data-dataMean)**2)
        SSres=sum((self.data-self.fitData)**2)
        self.R2=1-(SSres/SStot)
         #the R2 comparison is just the 11 data points plus 11 new ones,
         # not the 11 old and all the 100's recreated ones right?
         
    def getContData(self): #uses the coeffs to make a more continuous dataset
        self.contTimes=np.arange(0,50,.01)
        self.contData=self.A*(self.contTimes**self.alpha)*np.exp(-self.contTimes/self.B)
        
    def getStats(self): #uses the continous data for AUC and CO, prints out stats
        self.AUC=np.trapz(self.contData,self.contTimes)
        Imass=0.3*350*75
        self.CO=Imass/self.AUC*24*60/1000
        print("Patient=%i,offset=%i, A=%.9f, alpha=%f, B=%f,R^2=%f, shift=%f, AUC=%f, CO=%f" %(self.number,self.offset, self.A,self.alpha,self.B,self.R2,self.shift, self.AUC,self.CO))
        
    def plot(self): #uses plotting function to graph
        plt.figure(0)
        plt.plot(self.contTimes,self.contData,self.times,self.data,'bs') 
        plt.ylabel('Amplitude')
        plt.xlabel('Time')
        plt.title("Gamma Variate Fit with %f shift" %(self.shift))
        plt.show()
        
        

######General procedure of how the next parts works######
#The following is performed once for each of the 94 patients (each column of excel file)    
# 1. Read in entire excel file, put in each column in data array, grab offset, cut it down to 18 members long, remove blanks, make into integers,
#2. Patient objects are made, each with new data and a new number.  The loop is to adjust time shift. For each shift, it gets the coeffs, gets R2, makes continuous data,prints stats, optional plot, adds R2 to list for finding max
#3. With the list of R2, it finds the index of the max.  Then uses that index to redo the calculations given that time shift. Then it prints out the stats at the shift having the best R2

list=[] #blank list, will get filled in with objects for each of the 94 patients
#---------------------1. Cycles through procedure to get the data for each patient in excel file---------------
for i in np.arange(2,totalPatients+2): #2-96 are the columns in the excel sheet that get looped through
    f = open('Cardiac Output Data from MATLAB.csv') #opens file, * look at line 6 for home directory
    excelData=csv.reader(f) #necessary formatting..
    data=[] #blank array that gets filed in from cells in excel
    for cell in excelData:  #  "for each member of the list, add the ith term to "data""
        data.append(cell[i])
    offset=int(data[17]) # grabs the 19th cell in the column for the offset
    data=data[1:18] #cuts down the column according to excel- also 18 is the max # of data points
    data=filter(None,data) #removes all the blank cells from excel
    data=map(int,data) #prior to this the numbers were strings, this makes them ints
    data=np.array(data)-offset #subtracts offset from each point

#-------------------2. Now, Patient objects can be made, each with a new number and data--------------------------------
    R2list=[] #blank list for appending in R2 values to get the highest one
    person=Patient(i,data,offset) #a Patient object is made, with person number and data as parameters
    for i in np.arange(0,maxShift,shiftIncrement): #the time shifting, maxshift is set at very beginning
        person.getCoeffs(i) #gets the coeffs based on the shift, next methods are based on those new coeffs each time
        person.getR2()
        person.getContData()
        person.getStats()
    #   person.plot()
        R2list.append(person.R2) #adds the R2 to list so the index can be searched
        
#-------------3.Selecting the shift with the highest R2------------------------------
    print("\nBest shift is:")    
    maxindex = np.argmax(R2list)*shiftIncrement #"argmax" is a numpy function that returns index of highest int in the R2list array. multiplied by .25 (shiftIncrement var) to get back to actual time shift
    person.getCoeffs(maxindex) #gets coeffs, basically repeats the same block as before but this time best shift is chosen 
    person.getR2()
    person.getContData()
    person.getStats() 
    print("")
  # person.plot()
    list.append(person)    #adds this person object the list so it can be referred back to

#How to use this:
#It's setup right now so that it prints all of the data available.  To quickly find the best stats of a certain patient
# do list[patientnumber].getStats()
#To have it only print out the best stats, comment out the person.getStats() in section 2



#ignore for now
#list = [ Patient(i) for i in range(94)]
#where i is the column
#list[3].number=4 # will set that num





