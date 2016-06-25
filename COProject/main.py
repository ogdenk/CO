#http://www.technicaljar.com/?p=688
import sys
from PlotGUI import *
#from UIv3 import *
import numpy as np
from scipy.optimize import curve_fit


class GUIForm(QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setWindowTitle('Demo: PyQt with matplotlib')
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        QtCore.QObject.connect(self.ui.commandLinkButton, QtCore.SIGNAL('clicked()'), self.PlotFunc)
            
    def PlotFunc(self):
            #text=str(self.line1.text())
            #a = [int(i) for i in text.split(',')]
            #b=int(self.line2.text())
            #a=np.array(a)
            a=[]
            
            for i in np.arange(1,20,1):
                name=("self.ui.lineEdit_%i.text()"% i)
                if(eval(name)):
                    a.append(int(eval(name)))
            print(a)

            b=int(self.ui.lineEdit_21.text())
            
            a=np.array(a)
            
            person1=Patient()
            person1.data=a
            person1.offset=b
            person1.data=a-b
            person1.getCoeffs(4) 
            person1.getR2()
            person1.getContData()
            person1.getStats()
            
            self.ui.widget.canvas.ax.clear()
            self.ui.widget.canvas.ax.plot(person1.contTimes,person1.contData,person1.times,person1.data,'bs')
            self.ui.widget.canvas.draw()
            self.ui.lineEdit_24.setText("%.7s" % str(person1.CO))
            self.ui.lineEdit_23.setText("%.7s" % str(person1.AUC))
            self.ui.lineEdit_25.setText("%.7s" % str(person1.R2))

            print(person1.CO)
            
class Patient:
    
    def __init__(self): # makes a 'person' object with the number (ex. 0-93) and data array.  Other variables are 0 here but they get filled in in other methods.  Need to input data and offset
        self.number=0
        self.data=0
        self.offset=0
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
        self.CO=0

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
        self.R2 = 1-(SSres/SStot)
        self.R2 = 1 - (SSres / SStot)
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
        
        
  #  def (self):

    
      #  plt.figure(0)
      #  plt.plot(self.contTimes,self.contData,self.times,self.data,'bs') 
      #  plt.xlabel('Time')
      #  plt.title("Gamma Variate Fit with %f shift" %(self.shift))
      #  plt.show()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = GUIForm()
    myapp.show()
    sys.exit(app.exec_())