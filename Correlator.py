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

    # Add the file handler to the logger
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
        plt.subplot(4, 2, 1)
        plt.ion()
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
        
        self.stepPlot()
        
        self.fig = plt.gcf()
        
        plt.show(block=True)   
        plt.tight_layout()
    
    def stepPlot(self):
        # Plot the signals together
        plt.subplot(4, 1, 2)
        plt.cla()
        plt.plot(self.correlator.sig1_t, self.correlator.sig1, label='Signal 1')
        plt.plot(self.correlator.sig2_t, self.correlator.sig2, label='Signal 2', color='orange')
        plt.title('Signals Together (Corr step)')
        plt.xlabel('Sample Number')
        plt.ylabel('Amplitude')
        plt.grid(True)
        plt.xlim([-len(self.signal1), len(self.signal2)+len(self.signal1)-1])
        plt.legend()
        plt.pause(1e-6)
        
        # Plot the corr result
        plt.subplot(4, 1, 3)
        plt.cla()
        plt.plot(self.correlator.corrResForSig1ShiftIdx, self.correlator.corrStepResult, label='Corr val', marker='o')
        plt.title('Correlation result')
        plt.xlabel('Shift step for Signal 1')
        plt.ylabel('Corr value')
        plt.grid(True)
        plt.xlim([min(self.correlator.shiftStepsForSig1)-1, max(self.correlator.shiftStepsForSig1)])
        plt.legend()
        plt.pause(1e-6)
        #plt.gcf().canvas.draw()
        
    def btn_step(self, event):
        if (self.correlator.isCorrelationCompleted):
            if hasattr(self, 'timer'):
                self.timer.stop()
                print("Runner stopped!")
            print("Correlation is completed! No need to go further!")
            return
        self.correlator.calculateStep()
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
        self.initShiftForCorr = len(sig2) +1
        self.shiftStepsForSig1 = np.arange(self.initShiftForCorr,-(len(sig1)+1),-1)
        self.numberOfShiftForCorr = len(sig1) + len(sig2)
        self.corrResForSig1ShiftIdx = np.array([])
        self.corrStepResult = np.array([])
        self.sig1_t = np.arange(len(sig2)-1,len(sig2)+len(sig1)-1,1)+1
        self.sig2_t = np.arange(0,len(sig2),1)
        self.isCorrelationCompleted = False
        
        global logger_wrapper
        
        # Init info about the signals
        logger_wrapper.log("Sig1 has been shifted to the right by {} samples.\n".format(self.initShiftForCorr))
        logger_wrapper.log("In each step, Sig1 is shifted to the left by one sample to calculate the step's correlation value.\n")
        
    def calculateStep(self):
        if self.stepCount >= len(self.sig1) + len(self.sig2):
            logger_wrapper.log("Final State: No need to step further. All possible steps explored!\n")
            self.isCorrelationCompleted = True
            self.report()            
            return
        
        # Shift the signal first
        self.shiftSignal()
        
        logger_wrapper.log("corr step [{}]\n".format(self.stepCount))
        logger_wrapper.log("corr eq = sig1[t+{}]*sig2[t]\n".format(-1*(self.initShiftForCorr-1)))
        
        # Keep sig2 as it is, shift sig1 step by step
        # Sig2: 0 -> len(sig2) (ALWAYS)
        # Sig1: len(sig2)-shift -> len(sig2+sig3)-shift   
        
        # Find the intersection indices of the signals
        # This idx values are reference indices showing where they are intersected
        minIdxIntersected = max(min(self.sig1_t),min(self.sig2_t))
        maxIdxIntersected = min(max(self.sig1_t),max(self.sig2_t))
        
        globalIdxIntersected = np.arange(minIdxIntersected, maxIdxIntersected+1)
        
        logger_wrapper.log("intersection idx(global)\t=\t{}\n".format(globalIdxIntersected))
        
        # Find the local indices of the signals corresponding to the intersection indices
        # Sig1 is shifted each step, so each step it's indices in the intersection changes
        # Sig2 is always at the same place
        sig2LocalIdxAtIntersectedPoints = globalIdxIntersected
        sig1LocalIdxAtIntersectedPoints = globalIdxIntersected - (self.initShiftForCorr - 1)
        
        logger_wrapper.log("sig2 intersected idx\t=\t{}\nsig1 intersected idx\t=\t{}\n".format(sig2LocalIdxAtIntersectedPoints, sig1LocalIdxAtIntersectedPoints))
        
        corrVal = 0
        for sig1idx, sig2idx in zip(sig1LocalIdxAtIntersectedPoints,sig2LocalIdxAtIntersectedPoints):
            corrVal += self.sig1[sig1idx]*self.sig2[sig2idx]
        
        logger_wrapper.log("corr result = {}\n\n".format(corrVal))
        
        self.corrResForSig1ShiftIdx = np.append(self.corrResForSig1ShiftIdx, self.initShiftForCorr-1)
        self.corrStepResult = np.append(self.corrStepResult, corrVal)        
    
    def shiftSignal(self):
        # Sig1 shifts over Sig2, so Sig1 indexes are changing
        self.stepCount += 1
        self.initShiftForCorr -= 1
        self.sig1_t -= 1            
    
    def runAllSteps(self):
        global logger_wrapper
        logger_wrapper.setLevel(logging.CRITICAL)
        for k in range(0, self.numberOfShiftForCorr -1):
            self.step()
    
    def report(self):
        if (self.isCorrelationCompleted):
            valOfMaxCorr = max(self.corrStepResult)
            idxOfMaxCorr = np.argmax(self.corrStepResult)
            correspondingDelayForTheMaxVal = self.corrResForSig1ShiftIdx[idxOfMaxCorr]
            
            if correspondingDelayForTheMaxVal < 0:
                shiftDirectionForSig1 = "left"
            else:
                shiftDirectionForSig1 = "right"
            
            logger_wrapper.log("Correlation completed!\n"
                               "\tMaximum match is {}\n"
                               "\tMaximum match found at step {}\n"
                               "\tThe corresponding delay (or shift) for 'Signal 1' = {}\n"
                               "\tShift 'Signal 1' to the {} by {} units to get the maximum result.\n"
                               .format(valOfMaxCorr, idxOfMaxCorr, correspondingDelayForTheMaxVal, shiftDirectionForSig1, correspondingDelayForTheMaxVal))
                
             
class LoggerWrapper:
    def __init__(self, logger):
        self.logger = logger
        self.stdout = True
    
    def setLevel(self, level):
        self.logger.setLevel(level)
        
    def log(self, message, level=logging.INFO):
        if self.stdout:
            print(message, end='')
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
length_signal1 = 10
length_signal2 = 5
delay = -3  # delay in samples

# Set the random seed for reproducibility
np.random.seed(6)

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
