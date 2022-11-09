import sys

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QLabel, QMainWindow, QMenuBar, QMenu, QToolBar, QAction
from PySide2.QtGui import QPalette, QColor, QPixmap, QFont

class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle("Python Menus & Toolbars")
        self.resize(400, 200)
        self.centralWidget = QLabel("Hello, World")
        self.centralWidget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.centralWidget)



        self._createActions()
        self.statusbar = self.statusBar()
        self._createMenuBar()
        self._connectActions()
        # self._createToolBars()
    
    def displayTextStatusBar(self):
        self.statusbar.showMessage('HOLA', 4000)

    def _createMenuBar(self):
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)
        # Creating menus using a QMenu object
        fileMenu = QMenu("&File", self)
        editMenu = QMenu("&Edit", self) #&: keyboard shortcut
        helpMenu = QMenu("&Help", self)
        menu_bar.addMenu(fileMenu)
        menu_bar.addMenu(editMenu)
        menu_bar.addMenu(helpMenu)

        #Actions
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.exitAction)

        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.pasteAction)
        editMenu.addAction(self.cutAction)

        findMenu = editMenu.addMenu("Find and Replace")
        findMenu.addAction("Find...")
        findMenu.addAction("Replace...")

        helpMenu.addAction(self.helpContentAction)
        helpMenu.addAction(self.aboutAction)

    def _createToolBars(self):
        # Using a QToolBar object and a toolbar area
        fileToolBar = QToolBar('File', self)
        editToolBar = QToolBar('Edit', self)
        helpToolBar = QToolBar("Help", self)
        self.addToolBar(Qt.LeftToolBarArea, fileToolBar)
        self.addToolBar(Qt.LeftToolBarArea, editToolBar)
        self.addToolBar(Qt.LeftToolBarArea, helpToolBar)

    def _createActions(self):
        # Creating action using the first constructor
        self.newAction = QAction(self)
        self.newAction.setText("&New")
        # Creating actions using the second constructor
        self.openAction = QAction("&Open...", self)
        self.saveAction = QAction("&Save", self)
        self.exitAction = QAction("&Exit", self)
        self.copyAction = QAction("&Copy", self)
        self.pasteAction = QAction("&Paste", self)
        self.cutAction = QAction("C&ut", self)
        self.helpContentAction = QAction("&Help Content", self)
        self.aboutAction = QAction("&About", self)

    def newFile(self):
        # Logic for creating a new file goes here...
        self.centralWidget.setText("<b>File > New</b> clicked")

    def openFile(self):
        # Logic for opening an existing file goes here...
        self.centralWidget.setText("<b>File > Open...</b> clicked")

    def saveFile(self):
        # Logic for saving a file goes here...
        self.centralWidget.setText("<b>File > Save</b> clicked")

    def copyContent(self):
        # Logic for copying content goes here...
        self.centralWidget.setText("<b>Edit > Copy</b> clicked")

    def pasteContent(self):
        # Logic for pasting content goes here...
        self.centralWidget.setText("<b>Edit > Paste</b> clicked")

    def cutContent(self):
        # Logic for cutting content goes here...
        self.centralWidget.setText("<b>Edit > Cut</b> clicked")

    def helpContent(self):
        # Logic for launching help goes here...
        self.centralWidget.setText("<b>Help > Help Content...</b> clicked")

    def about(self):
        # Logic for showing an about dialog content goes here...
        self.centralWidget.setText("<b>Help > About...</b> clicked")
    
    def _connectActions(self):
        # Connect File actions
        self.newAction.triggered.connect(self.newFile)
        self.openAction.triggered.connect(self.openFile)
        self.openAction.triggered.connect(self.displayTextStatusBar)
        self.saveAction.triggered.connect(self.saveFile)
        self.exitAction.triggered.connect(self.close)
        # Connect Edit actions
        self.copyAction.triggered.connect(self.copyContent)
        self.pasteAction.triggered.connect(self.pasteContent)
        self.cutAction.triggered.connect(self.cutContent)
        # Connect Help actions
        self.helpContentAction.triggered.connect(self.helpContent)
        self.aboutAction.triggered.connect(self.about)

def darkMode():
	# Dark Theme
	# Adapted from https://github.com/pyqt/examples/tree/_/src/09%20Qt%20dark%20theme
	palette = QPalette()
	palette.setColor(QPalette.Window, QColor(53, 53, 53))
	palette.setColor(QPalette.WindowText, Qt.white)
	palette.setColor(QPalette.Base, QColor(25, 25, 25))
	palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
	palette.setColor(QPalette.ToolTipBase, Qt.black)
	palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
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
	app.setFont(QFont("Arial", 9))
		
	win = Window()
	win.show()

	sys.exit(app.exec_())


