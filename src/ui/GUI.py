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
        self.qPixmapVar = QPixmap()
        self.qPixmapVar.load('lobto.png')
        self.qPixmapVar = self.qPixmapVar.scaledToWidth(140)
        self.label.setPixmap(self.qPixmapVar)
        

    def setUI(self):
        self.setupUi(self)

    def commandline(self):
        self.OutputBox.append(self.InputBox.text())
        self.InputBox.clear()
 
if __name__ == "__main__" :
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())