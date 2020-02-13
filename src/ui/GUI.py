import sys
 
import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
 
Practice_UI = uic.loadUiType('practice.ui')[0]

class MainWindow(QMainWindow, Practice_UI):
    def __init__(self):
        super().__init__()
        self.setUI()
        self.InputBox.returnPressed.connect(self.commandline)

    def setUI(self):
        self.setupUi(self)

    def commandline(self):
        self.OutputBox.append(self.InputBox.text())
        self.InputBox.clear()
 
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
app.exec_()