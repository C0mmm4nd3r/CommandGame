import sys
from core import Core
import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

Practice_UI = uic.loadUiType('practice.ui')[0]

class GameMaking(QMainWindow, Practice_UI):
    def __init__(self):
        self.core = Core()
        self.core.UserSetting('tuuna', '1234')
        super().__init__()
        self.setUI()
        self.InputBox.returnPressed.connect(self.commandline)
        self.Submit.clicked.connect(self.chkflag)
        self.pwd.setText(self.core.OutputDefault())
        if self.core.component['userinfo']['setup'] == False:
            self.MsgBox('튜토리얼을 시작하겠습니다.')
            self.Tutorial()
        self.setQuestName()
        self.refreshQuest()

    def setUI(self):
        self.setupUi(self)

        self.status.setText('0')
        self.reward.setText('0')

        #배경 설정
        oImage = QImage('Background.jpg')
        sImage = oImage.scaled(QSize(800,572))
        palette = QPalette()
        palette.setBrush(10,QBrush(sImage))
        self.setPalette(palette)

        #OutputBox 투명도 설정
        opacity_effect = QGraphicsOpacityEffect(self.OutputBox)
        opacity_effect.setOpacity(0.5)
        self.OutputBox.setGraphicsEffect(opacity_effect)
        self.OutputBox.setStyleSheet("background-color: black")

    def setQuestName(self):
        tmp = self.core.GetEvent()
        self.EventName = {}
        i = 0
        for key in tmp:
            self.EventName[i] = key
            i += 1

    def Tutorial(self):
        try:
            self.key = next(self.core.iter_TutoInfo)
        except StopIteration:
            self.MsgBox("축하합니다! 튜토리얼이 끝났습니다.")
            userinfo = self.core.component['userinfo']
            userinfo['setup'] = True
            self.core.SaveData()
        self.MsgBox(self.core.TutoInfo[self.key]['explanation'])

    def MsgBox(self, output):
        msgbox = QMessageBox(self)
        msgbox.question(self, 'Tutorial', output, QMessageBox.Yes)

    def commandline(self):
        command = self.InputBox.text()
        if self.core.component['userinfo']['setup'] == False:
            output = self.core.Tutorial(command, self.core.TutoInfo[self.key])
            if output != '':
                self.MsgBox(self.core.TutoInfo[self.key]['reward'])
                self.Tutorial()
            else:
                self.MsgBox("하하 틀렸단다\n"+self.core.TutoInfo[self.key]['explanation'])
        else:
            output = self.core.ExecuteCommand(command)
        self.OutputBox.append(self.pwd.text()+command+output)
        self.InputBox.clear()
        self.pwd.setText(self.core.OutputDefault())


    #flag 체크
    def chkflag(self):
        
        if not(self.eventtree.currentItem()):
            return 0
        elif not(self.eventtree.currentItem().parent()):
            return 0
        if self.core.CompareFlag(self.EventName[self.root.indexOfChild(self.eventtree.currentItem().parent())],getattr(self, 'childLineEdit_{}'.format(self.root.indexOfChild(self.eventtree.currentItem().parent()))).text()):
            self.eventtree.currentItem().setHidden(True)
            getattr(self, 'childLineEdit_{}'.format(self.root.indexOfChild(self.eventtree.currentItem().parent()))).clear()
            self.status.setText(str(int(self.status.text())+1))
            self.refreshQuest()

    #Quest 추가
    def AddQuest(self, Questname):
        self.root = self.eventtree.invisibleRootItem()

        tmp = QTreeWidgetItem()
        sub_tmp = QTreeWidgetItem()
        PosQ = self.core.GetEvent()

        setattr(self, 'childLineEdit_{}'.format(self.eventtree.topLevelItemCount()),QLineEdit())
        
        tmp.setText(0,'{0}'.format(Questname))
        tmp.setToolTip(0,'{0}'.format(PosQ[Questname]['explanation']))

        tmp.addChild(sub_tmp)
        self.eventtree.setItemWidget(sub_tmp,0, getattr(self, 'childLineEdit_{}'.format(self.eventtree.topLevelItemCount())))
        self.root.addChild(tmp)
        

    #새로고침
    def refreshQuest(self):
        self.eventtree.clear()
        tmp = self.core.GetEvent()
        for i in tmp:
            if tmp[i]['status'] == False:
                self.AddQuest(i)
                



if __name__ == "__main__" :
    app = QApplication(sys.argv)
    main_window = GameMaking()
    main_window.show()
    sys.exit(app.exec_())
