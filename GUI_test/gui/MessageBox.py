import sys
from PyQt5.QtWidgets import QApplication, QMessageBox

class errorBox(QMessageBox):
    
    def __init__(self, error_e, parent=None):
        super().__init__(parent)
        self.setIcon(QMessageBox.Critical)
        self.setText('<b>An error has ocurred!</b>')
        self.setInformativeText(str(error_e))
        self.setWindowTitle('Error!')


class warningBox(QMessageBox):
    def __init__(self, warning, parent=None):
        super().__init__(parent)
        self.setIcon(QMessageBox.Warning)
        self.setText('<b>Warning:</b>')
        self.setInformativeText(warning)
        self.setWindowTitle('Warning!')

class informationBox(QMessageBox):
    def __init__(self, info, parent=None):
        super().__init__(parent)
        self.setIcon(QMessageBox.Information)
        self.setText('<b>Information:</b>')
        self.setInformativeText(info)
        self.setWindowTitle('Information!')


if __name__ == '__main__':
    app = QApplication([])
    widget = errorBox('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla porta est interdum, vulputate metus et, bibendum dui. Nunc fermentum tincidunt mi nec semper')
    widget.show()
    sys.exit(app.exec_())