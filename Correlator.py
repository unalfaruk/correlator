# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import datetime
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.widgets as mwidgets

def btn_step(event):
    correlator.step()
    
def btn_run(event):
    correlator.run()
    


class Plotter:
    def __init__(self, correlator):
        self.correlator = correlator
        self.signal1 = correlator.sig1
        self.signal2 = correlator.sig2
        self.samples1 = np.arange(0,len(self.signal1))
        self.samples2 = np.arange(0,len(self.signal2))
        
        # Plot the first signal
        plt.ion()
        plt.subplot(4, 2, 1)
        plt.plot(self.samples1, self.signal1, label='Signal 1')
        plt.title('Signal 1')
        plt.xlabel('Sample Number')
        plt.ylabel('Amplitude')
        plt.grid(True)
        plt.legend()

        # Plot the second signal
        plt.subplot(4, 2, 2)
        plt.plot(self.samples2, self.signal2, label='Signal 2', color='orange')
        plt.title('Signal 2 (Delayed)')
        plt.xlabel('Sample Number')
        plt.ylabel('Amplitude')
        plt.grid(True)
        plt.legend()        
        
        # Create a button for Step
        axnext = plt.axes([0.80, 0.05, 0.1, 0.075])
        self.bstep = Button(axnext, 'Step')
        self.bstep.on_clicked(self.btn_step)
        
        # Create a button for Run
        axnext = plt.axes([0.55, 0.05, 0.2, 0.075])
        self.brun = Button(axnext, 'Run Animation')
        self.brun.on_clicked(self.btn_run)

        self.fig = plt.gcf()
        plt.tight_layout()
        plt.show()
        
    def btn_step(self, event):
        self.correlator.step()
    
    def btn_run(self, event):
        print("Run triggered...")
        
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        print("Press any key to stop it...")
        
        self.timer = self.fig.canvas.new_timer(interval=50)
        self.timer.add_callback(self.btn_step, "None")
        self.timer.start()      
    
    def on_key(event):
        print("Run stopped...")
        plotter.timer.stop()

class Correlator:
    def __init__(self, sig1, sig2):
        self.fig = None
        self.sig1 = sig1
        self.sig2 = sig2
        self.stepCount = 0
        self.initShiftForCorr = len(sig2)
        self.corrStepIdx = np.array([])
        self.corrStepResult = np.array([])
        self.sig1_t = np.arange(len(sig2),len(sig2)+len(sig1),1)
        self.sig2_t = np.arange(0,len(sig2),1)
        
        current_time = datetime.datetime.now()
        timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S")
        self.logFile = open('correlation_log_{}.txt'.format(timestamp), 'a')        
        
        #Init info about the signals
        self.logFile.write("Sig1 has been shifted to the right by {} samples.\n".format(self.initShiftForCorr))
        self.logFile.write("In each step, Sig1 is shifted to the left by one sample to calculate the step's correlation value.\n")
        
    def step(self):
        tmpCorrRes = 0
        self.logFile.write("corr [{}] = ".format(self.initShiftForCorr)) 
        for i in range(0, self.stepCount+1):
            self.logFile.write("sig1[{}]*sig2[{}]".format(i,(self.initShiftForCorr-1)+i))            
            tmpCorrRes += self.sig1[i]*self.sig2[(self.initShiftForCorr-1)+i]
            if i != self.stepCount:
                self.logFile.write("+")
        
        self.logFile.write("= {}".format(tmpCorrRes))
        
        self.corrStepIdx = np.append(self.corrStepIdx, self.initShiftForCorr)
        self.corrStepResult = np.append(self.corrStepResult, tmpCorrRes)
               
        self.stepCount += 1
        self.initShiftForCorr -= 1
        
        # Plot the signals together
        plt.subplot(4, 1, 2)
        plt.tight_layout()
        plt.cla()
        plt.plot(self.sig1_t - self.stepCount, self.sig1, label='Signal 1')
        plt.plot(self.sig2_t, self.sig2, label='Signal 2', color='orange')
        plt.title('Signals Together (Corr step)')
        plt.xlabel('Sample Number')
        plt.ylabel('Amplitude')
        plt.grid(True)
        plt.legend()
        plt.pause(1e-6)
        
        # Plot the signals together
        plt.subplot(4, 1, 3)
        plt.tight_layout()
        plt.cla()
        plt.plot(self.corrStepIdx, self.corrStepResult, label='Corr val')
        plt.title('Correlation result')
        plt.xlabel('Shift step')
        plt.ylabel('Amplitude')
        plt.grid(True)
        plt.legend()
        plt.pause(1e-6)
        plt.tight_layout()
        plt.gcf().canvas.draw()     
        

# Parameters for dummy signals
length_signal1 = 1000
length_signal2 = 800
delay = 250  # delay in samples

# Set the random seed for reproducibility
np.random.seed(0)

# Generate the first signal (random signal)
signal1 = np.random.randn(length_signal1)

# Generate the second signal (delayed version of the first signal)
signal2 = np.roll(signal1, delay)[:length_signal2]

# Create a sample number array
samples1 = np.arange(length_signal1)
samples2 = np.arange(length_signal2)

# Init correlator
correlator = Correlator(signal1, signal2)
plotter = Plotter(correlator)




