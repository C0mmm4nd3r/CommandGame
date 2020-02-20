import sys
 
import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
 
Practice_UI = uic.loadUiType('practice.ui')[0]
flags = {0: "PyQt", 1: "바보"}
class GameMaking(QMainWindow, Practice_UI):
    def __init__(self):
        super().__init__()
        self.setUI()
        self.InputBox.returnPressed.connect(self.commandline)
        self.Accept.clicked.connect(self.AddQuest)
        self.Submit.clicked.connect(self.chkflag)

    def setUI(self):
        self.setupUi(self)

        #OutputBox 배경설정
        qPixmapVar = QPixmap()
        qPixmapVar.load('lobto.png')
        qPixmapVar = qPixmapVar.scaledToWidth(140)
        self.label.setPixmap(qPixmapVar)

        self.status.setText('0')

        #event관리 list ver
        # self.eventlist.addItem('test1')
        # self.eventlist.addItem('test2')

        #event관리 tree ver
        

        #self.eventtree.itemClicked.connect(lambda : self.chkflag(sub_test))



    def commandline(self):
        self.OutputBox.append(self.InputBox.text())
        self.InputBox.clear()

# 리스트 flag체크

#     def chk2(self):
#         On_going = self.eventlist.currentRow()

#         if self.flag.text() == flags.get(On_going):
#             self.eventlist.currentItem().setHidden(True)
#             self.status.setText(str(int(self.status.text())+1))
        
#         self.flag.clear()

    #flag 체크
    def chkflag(self):

        if flags.get(self.root.indexOfChild(self.eventtree.currentItem().parent())) == self.childLineEdit.text():
            self.eventtree.currentItem().parent().setText(0, 'Clear!')
            self.eventtree.currentItem().setHidden(True)
            self.childLineEdit.clear()
            self.status.setText(str(int(self.status.text())+1))

    #Quest 추가
    def AddQuest(self):
        self.root = self.eventtree.invisibleRootItem()

        tmp = QTreeWidgetItem()
        sub_tmp = QTreeWidgetItem()

        self.childLineEdit = QLineEdit()
        tmp.setText(0,'Quest')

        tmp.addChild(sub_tmp)
        self.eventtree.setItemWidget(sub_tmp,0,self.childLineEdit)
        self.root.addChild(tmp)

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    main_window = GameMaking()
    main_window.show()
    sys.exit(app.exec_())