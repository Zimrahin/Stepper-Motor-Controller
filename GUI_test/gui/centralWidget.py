import sys 
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QMainWindow
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, Qt
from PyQt5.QtGui import QPalette, QColor

from connectionWidget import connectionWidget
from paramWidget import paramWidget
from angleWidget import angleWidget
from plotWidget import plotWidget
from MessageBox import informationBox

# https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105
import ctypes
myappid = 'StepperMotorController' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

ABORT_CMD = 'az.{channel}P1=0.000\r'

class centralWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.setWindowTitle("Stepper motor controller")

        #Objects 
        self.Thread = None
        self.Dispatcher = None
        self.dispatcher_ctrl = None
        self.route = None
        self.COM = None

        # Widgets
        # -> Connection Widget
        self.connection_wdg = connectionWidget(self)
        
        # -> Param fields Widget
        self.param_wdg = paramWidget(self)

        # -> Message fields Widget
        self.msg_wdg = angleWidget(self)

        # -> Plot Widget
        self.plot_wdg = plotWidget(self)

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
        v_layout.addStretch()
        

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.plot_wdg, 5)
        h_layout.addLayout(v_layout, 1)

        self.setLayout(h_layout)

    def disconnectLock(self):
        self.COM = None
        self.param_wdg.setEnabled(False)

    def connectUnlock(self):
        self.COM = self.connection_wdg.serial_COM
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

        msg = informationBox('Abort sequence ended. All channels were set to zero')
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
            self.COM.write(CMD)

    def ThreadEnd(self):
        # Unlock fields
        self.lockForRun()
        self.param_wdg.stopHandler()

    def updateBar(self, val):
        self.param_wdg.progressHandler(val)


    def resetBar(self):
        self.param_wdg.resetBar()

def darkMode():
    # Dark Theme
    # Adapted from https://github.com/pyqt/examples/tree/_/src/09%20Qt%20dark%20theme
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    palette.setColor(QPalette.Disabled, QPalette.Base, QColor(49, 49, 49))
    palette.setColor(QPalette.Disabled, QPalette.Text, QColor(90, 90, 90))
    palette.setColor(QPalette.Disabled, QPalette.Button, QColor(42, 42, 42))
    palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(90, 90, 90))
    palette.setColor(QPalette.Disabled, QPalette.Window, QColor(49, 49, 49))
    palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(90, 90, 90))
    return palette


if __name__ == '__main__':
    app = QApplication([])
    # if os.name == 'nt': # New Technology GUI (Windows)
    app.setStyle('fusion') 
    palette = darkMode()
    app.setPalette(palette)
        
    widget = centralWidget()
    widget.show()

    sys.exit(app.exec_())