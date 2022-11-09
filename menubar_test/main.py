import sys

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QLabel, QMainWindow, QMenuBar, QMenu, QToolBar
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

        self._createMenuBar()
        self._createToolBars()
    
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

    def _createToolBars(self):
        # Using a QToolBar object and a toolbar area
        fileToolBar = QToolBar('File', self)
        editToolBar = QToolBar('Edit', self)
        helpToolBar = QToolBar("Help", self)
        self.addToolBar(Qt.LeftToolBarArea, fileToolBar)
        self.addToolBar(Qt.LeftToolBarArea, editToolBar)
        self.addToolBar(Qt.LeftToolBarArea, helpToolBar)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
