import sys 
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QThread
from connectionFields import connectionFields
from paramFields import paramFields
from messageFields import messageFields
from plotWidget import plotWidget
from MessageBox import InformationBox
import os

ABORT_CMD = 'az.{channel}P1=0.000\r'

class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        #Objects 
        self.Thread = None
        self.Dispatcher = None
        self.dispatcher_ctrl = None
        self.route = None
        self.comms = None

        # Widgets
        # -> Connection Widget
        self.connection_wdg = connectionFields(self)
        
        # -> Param fields Widget
        self.param_wdg = paramFields(self)

        # -> Message fields Widget
        self.msg_wdg = messageFields(self)

        # -> Plot Widget
        self.plot_wdg = plotWidget(self)
        # self.plot_wdg.resize(440,330)


        # Init routines
        self.param_wdg.setEnabled(False)

        # Signals and Slots
        self.connection_wdg.connect_signal.connect(self.connectUnlock)
        self.connection_wdg.disconnect_signal.connect(self.disconnectLock)
        self.param_wdg.start_signal.connect(self.runTest)
        self.param_wdg.abort_signal.connect(self.abortSequence)
        self.param_wdg.stop_signal.connect(self.stopSequence)

        # Layout
        v_layout = QVBoxLayout()
        
        v_layout.addWidget(self.connection_wdg)
        v_layout.addWidget(self.param_wdg)
        v_layout.addWidget(self.msg_wdg)
        

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.plot_wdg,6)
        h_layout.addLayout(v_layout,2)

        self.setLayout(h_layout)

    def disconnectLock(self):
        self.comms = None
        self.param_wdg.setEnabled(False)

    def connectUnlock(self):
        self.comms = self.connection_wdg.getComms()
        self.param_wdg.setEnabled(True)


    def runTest(self):
        # Lock Control fields during Thread operation
        self.lockForRun()

        # Reset progress bar
        self.resetBar()

        # Create a thread
        self.Thread = QThread()
        
        # -> Get Route 
        self.route = self.param_wdg.getRoute()

        # -> Generate dispatcher ctrl
        self.dispatcher_ctrl = {'abort':False}
        self.dispatcher_ctrl['stop'] = False

        # Assign worker to thread
        self.Dispatcher.moveToThread(self.Thread)

        # Connect signals
        self.Thread.started.connect(self.Dispatcher.run)
        self.Dispatcher.finished.connect(self.Thread.quit)
        self.Dispatcher.finished.connect(self.Dispatcher.deleteLater)
        self.Thread.finished.connect(self.Thread.deleteLater)
        self.Thread.finished.connect(self.ThreadEnd)
        self.Dispatcher.progress.connect(self.updateBar)
        # Start Dispatcher on thread
        self.Thread.start()    
    
    def abortSequence(self):
        # Stop any running threads
        if self.Thread and self.Thread.isRunning():
            
            # Disable thread ability to send cmds to device
            self.dispatcher_ctrl['abort'] = True

            # Wait for thread to end
            self.Thread.quit()
            self.Thread.wait()

            # Clean before ending
            self.dispatcher_ctrl = None
            self.route = None
        
        else:
            # No thread is running
            self.abortRoutine()

            
        # Clear Thread
        self.Thread = None

        msg = InformationBox('Abort sequence ended. All channels were set to zero')
        msg.exec_()

        # Restore progress bar
        self.resetBar()
    
    def lockForRun(self):
        # Lock fields
        self.param_wdg.lockFields()


    def stopSequence(self):
        if self.Thread and self.Thread.isRunning():
            
            # Disable thread ability to send cmds to device
            self.dispatcher_ctrl['stop'] = True

            # Wait for thread to end
            self.Thread.quit()
            self.Thread.wait()

            # Clean before ending
            self.dispatcher_ctrl = None
            self.route = None
        
        # Clear Thread
        self.Thread = None

        # Reset progress bar
        self.resetBar()

    def abortRoutine(self):
        # Set all channels to zero
        for i in range(1,5):
            CMD = ABORT_CMD.format(channel=2*i).encode('utf_8')
            self.comms.write(CMD)

    def ThreadEnd(self):
        # Unlock fields
        self.lockForRun()
        self.param_wdg.stopHandler()

    def manualRoutine(self):
        # Generate Window
        manual_window = ManualControl(self.comms, channel, self)

        # Lock automatic control fields 
        self.lockForRun()

        # Signals 
        manual_window.finished.connect(self.lockForRun)

        # Start Window
        manual_window.exec_()

    def updateBar(self, val):
        self.param_wdg.progressHandler(val)


    def resetBar(self):
        self.param_wdg.resetBar()


if __name__ == '__main__':
    app = QApplication([])
    if os.name == 'nt':
        app.setStyle('Fusion')
    widget = CentralWidget()
    widget.show()
    sys.exit(app.exec_())