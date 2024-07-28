# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import datetime
import logging

# A logger class breaks Spyder Variable Explorer...
# So use a function instead to setup the logger
def setup_logger():
    # Generate log file name based on current datetime
    log_file = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")
    
    # Create a logger
    logger = logging.getLogger('custom_logger')
    logger.setLevel(logging.INFO)  # Set the desired logging level

    # Create a file handler
    handler = logging.FileHandler(log_file)
    handler.setLevel(logging.INFO)

    # Create a logging format without timestamps
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    handler.terminator = ""

    # Add the file handler to the logger if not already added
    if not logger.handlers:
        logger.addHandler(handler)    
    
    return logger

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
        #plt.tight_layout()
        plt.show(block=True)
    
    def stepPlot(self):
        # Plot the signals together
        plt.subplot(4, 1, 2)
        plt.tight_layout()
        plt.cla()
        plt.plot(self.correlator.sig1_t - self.correlator.stepCount, self.correlator.sig1, label='Signal 1')
        plt.plot(self.correlator.sig2_t, self.correlator.sig2, label='Signal 2', color='orange')
        plt.title('Signals Together (Corr step)')
        plt.xlabel('Sample Number')
        plt.ylabel('Amplitude')
        plt.grid(True)
        plt.legend()
        plt.pause(1e-6)
        
        # Plot the corr result
        plt.subplot(4, 1, 3)
        plt.tight_layout()
        plt.cla()
        plt.plot(self.correlator.corrStepIdx, self.correlator.corrStepResult, label='Corr val')
        plt.title('Correlation result')
        plt.xlabel('Shift step')
        plt.ylabel('Amplitude')
        plt.grid(True)
        plt.legend()
        plt.pause(1e-6)
        plt.tight_layout()
        plt.gcf().canvas.draw()
        
    def btn_step(self, event):
        self.correlator.step()
        self.stepPlot()
    
    def btn_run(self, event):
        print("Run triggered...")
        
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        print("Press any key to stop it...")
        
        self.timer = self.fig.canvas.new_timer(interval=50)
        self.timer.add_callback(self.btn_step, "None")
        self.timer.start()      
    
    def on_key(self,event):
        print("Run stopped...")
        self.timer.stop()

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
        
        global logger_wrapper
        
        #Init info about the signals
        logger_wrapper.log("Sig1 has been shifted to the right by {} samples.\n".format(self.initShiftForCorr))
        logger_wrapper.log("In each step, Sig1 is shifted to the left by one sample to calculate the step's correlation value.\n")
        
    def step(self):
        tmpCorrRes = 0
        logger_wrapper.log("corr [{}] = ".format(self.initShiftForCorr)) 
        for i in range(0, self.stepCount+1):
            logger_wrapper.log("sig1[{}]*sig2[{}]".format(i,(self.initShiftForCorr-1)+i))            
            tmpCorrRes += self.sig1[i]*self.sig2[(self.initShiftForCorr-1)+i]
            if i != self.stepCount:
                logger_wrapper.log("+")
        
        logger_wrapper.log("= {}\n".format(tmpCorrRes))
        
        self.corrStepIdx = np.append(self.corrStepIdx, self.initShiftForCorr)
        self.corrStepResult = np.append(self.corrStepResult, tmpCorrRes)
               
        self.stepCount += 1
        self.initShiftForCorr -= 1
        
             
class LoggerWrapper:
    def __init__(self, logger):
        self.logger = logger

    def log(self, message, level=logging.INFO):
        if level == logging.DEBUG:
            self.logger.debug(message)
        elif level == logging.INFO:
            self.logger.info(message)
        elif level == logging.WARNING:
            self.logger.warning(message)
        elif level == logging.ERROR:
            self.logger.error(message)
        elif level == logging.CRITICAL:
            self.logger.critical(message)
        else:
            self.logger.info(message)

# Create a global logger instance
logger = setup_logger()
logger_wrapper = LoggerWrapper(logger)

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

