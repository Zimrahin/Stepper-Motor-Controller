# A thread-worker that dispatches the commands used by the flowmeter
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, QObject, pyqtSignal
import serial
import time
import math

# Constants

WRITE_CMD = 'AZ.{channel}P1={sp_value:.3f}\r'
ABORT_CMD = 'az.{channel}P1=0.000\r'

TIME_UNIT = 0.5 # Wait 0.5 s in every sleep cycle

class Dispatcher(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(float)

    def __init__(self, serial_comms, channel, step_route, dispatcher_ctrl):
        super().__init__()
        self.serial_comms = serial_comms
        self.channel = channel
        self.step_route = step_route
        self.dispatcher_ctrl = dispatcher_ctrl

    def run(self):
        progress_counter = 0.0
        n_steps = len(self.step_route['step_list'])
        
        # Iterate through calculated steps
        for step in self.step_route['step_list']:
            progress_counter += (1/n_steps)*100.0
            self.progress.emit(progress_counter)
            self.toDevice(step)            
            if(self.waitRoutine(self.step_route['time_step'])):
                if(self.dispatcher_ctrl['abort']):
                    self.abortRoutine()
                # In case of stop, the last SP is mantained
                break
        self.finished.emit()


    def toDevice(self, next_step):
        if not(self.dispatcher_ctrl['abort'] or self.dispatcher_ctrl['stop']):
            self.serial_comms.write(self.setupSP(self.channel, next_step))
        else:
            return

    def setupSP(self,channel, sp_value):
        cmd = WRITE_CMD.format(channel=channel, sp_value=sp_value)
        return cmd.encode('utf_8')

    def waitRoutine(self, seconds):
        time_to_wait = math.ceil(seconds/TIME_UNIT)
        for i in range(time_to_wait):
            # Check for stop or abort signal
            if(self.dispatcher_ctrl['abort'] or self.dispatcher_ctrl['stop']):
                return True
            else:
                time.sleep(0.5)
        return False

    def abortRoutine(self):
        # Set all channels to zero
        for i in range(1,5):
            CMD = ABORT_CMD.format(channel=2*i).encode('utf_8')
            self.serial_comms.write(CMD)

