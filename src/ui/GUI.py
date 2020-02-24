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
        self.core = Core()
        self.core.UserSetting('tuuna', '1234')
        super().__init__()
        self.setUI()
        self.InputBox.returnPressed.connect(self.commandline)
        self.Accept.clicked.connect(self.AddQuest)
        self.Submit.clicked.connect(self.chkflag)
        self.pwd.setText(self.core.OutputDefault())

    def setUI(self):
        self.setupUi(self)

        #OutputBox 배경설정
        # qPixmapVar = QPixmap()
        # qPixmapVar.load('lobto.png')
        # qPixmapVar = qPixmapVar.scaledToWidth(140)
        # self.label.setPixmap(qPixmapVar)

        self.status.setText('0')

        #event관리 list ver
        # self.eventlist.addItem('test1')
        # self.eventlist.addItem('test2')

        #event관리 tree ver
        

        #self.eventtree.itemClicked.connect(lambda : self.chkflag(sub_test))



    def commandline(self):
        command = self.InputBox.text()
        self.OutputBox.append(self.pwd.text()+command+self.core.ExecuteCommand(command))
        self.InputBox.clear()
        self.pwd.setText(self.core.OutputDefault())
        


# 리스트 flag체크

#     def chk2(self):
#         On_going = self.eventlist.currentRow()

#         if self.flag.text() == flags.get(On_going):
#             self.eventlist.currentItem().setHidden(True)
#             self.status.setText(str(int(self.status.text())+1))
        
#         self.flag.clear()

    #flag 체크
    def chkflag(self):
        if not(self.eventtree.currentItem().parent()):
            return 0
        if flags.get(self.root.indexOfChild(self.eventtree.currentItem().parent())) == getattr(self, 'childLineEdit_{}'.format(self.root.indexOfChild(self.eventtree.currentItem().parent()))).text():
            self.eventtree.currentItem().parent().setText(0, 'Clear!')
            self.eventtree.currentItem().setHidden(True)
            getattr(self, 'childLineEdit_{}'.format(self.root.indexOfChild(self.eventtree.currentItem().parent()))).clear()
            self.status.setText(str(int(self.status.text())+1))

    #Quest 추가
    def AddQuest(self):
        self.root = self.eventtree.invisibleRootItem()

        tmp = QTreeWidgetItem()
        sub_tmp = QTreeWidgetItem()

        setattr(self, 'childLineEdit_{}'.format(self.eventtree.topLevelItemCount()),QLineEdit())

        tmp.setText(0,'Quest')

        tmp.addChild(sub_tmp)
        self.eventtree.setItemWidget(sub_tmp,0, getattr(self, 'childLineEdit_{}'.format(self.eventtree.topLevelItemCount())))
        self.root.addChild(tmp)

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    main_window = GameMaking()
    main_window.show()
    sys.exit(app.exec_())
