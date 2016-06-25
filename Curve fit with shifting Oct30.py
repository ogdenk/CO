#Gamma Variate Curve fit code with display
#Matt Vetere and Kent Ogden
#Last Updated 10/30/14
#Takes in list of datapoints as y, fits the curve and displays coeffs and r^2
#What's next: Include shifting along x axis for optimal r^2 with noise at start

##########################    Imports   #####################
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

################### Gamma Variate Function Definition   ############
def func(tau,A,alpha,B):                  
    return(A*(tau**alpha)*np.exp(-tau/B))   #returns the distribtion function, 3 consts
    
#################   Getting correct y values  ############
y=np.array([51,96,157,218,231,269,235,203,153,123,66])# user given data [array]
y=y-51 #density offset 

################# Making multiple sets of tau(x-values) for R^2 optimizing##############
R2list=[]
shift=[]
for i in np.arange(0,20,.25): ###when its shifted past 14, the R^2 gets very eradict
    tau=np.arange(i,i+22,2) ##is the shifted x, 22 allows for the data, everything prior is 0
    popt,pcov=curve_fit(func,tau,y,maxfev=5000) # popt is [array] of coeff
    A,alpha,B=popt[0],popt[1],popt[2] #grabs each coeff from array (float)
    
    #######################     Getting R^2 and Printout   ##################
    fi=A*(tau**alpha)*np.exp(-tau/B) # 
    ymean=sum(y)/len(y)
    SStot=sum((y-ymean)**2)
    SSres=sum((y-fi)**2)
    rsquared=1-(SSres/SStot)
    R2list.append(rsquared)
    shift.append(i)    
    print("A=%.9f, alpha=%f, B=%f,r^2=%f, shift=%f" %(A,alpha,B,rsquared,i))
    
    #######################      Plotting with fit equation    ########################
    x=np.arange(0,50,.25) #**new list of x values,28+.25= 28.25
    eqn=A*(x**alpha)*np.exp(-x/B)  
    plt.figure(0)
    plt.plot(x,eqn,tau,y,'bs') # plots points as blue squares and line as blue line
    plt.ylabel('Amplitude')
    plt.xlabel('Time')
    plt.title("gamma variate fit")
    plt.show()

#print("Shift is: %f, R^2 is: %f" %(shift,R2list))

plt.figure(1)
plt.ylabel('R^2')
plt.xlabel('x-shift')
plt.plot(shift,R2list)
plt.title('R^2 given shifting')
plt.show()
