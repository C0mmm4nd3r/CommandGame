from logging import loggy
from anytree import Node, RenderTree
import json
from manage_dir import DirTree
from CommandFunction import CmFunc

class Core:
    def __init__(self):
        with open('user.json') as userJson:
            self.userinfo = json.load(userJson)

        self.cmfunc = CmFunc()
        self.dir = DirTree()
        self.dir.GetSavedDir()
        self.dir.PrintDir()
        self.PossibleCommand = {
            'ls':self.cmfunc.ls_func,
            'cd':self.cmfunc.cd_func,
            'cp':self.cmfunc.cp_func,
            'rm':self.cmfunc.rm_func,
            'mv':self.cmfunc.mv_func,
            'cat':self.cmfunc.cat_func,
            'mkdir':self.cmfunc.mkdir_func,
            'touch':self.cmfunc.touch_func,
        }

    def test(self):
        self.cmfunc.mkdir_func(self.dir, self.userinfo, self.command[1:])
        #self.cmfunc.mkdir_func('/home/tuuna/level1', '/home/tuuna', self.dir) #mkdir /home/tuuna/level1
        self.dir.PrintDir()

    def ExecuteCommand(self):
        if self.command[0] in self.PossibleCommand:
            self.PossibleCommand[self.command[0]](self.dir, self.userinfo, self.command[1:]) #서로 인자가 달라서 이방법은 안될듯하네
        else:
            return "Command not found: {}".format(self.command[0])
        self.dir.PrintDir()
        return

    def Handler(self, command):
        self.command = command.split()
        return self.ExecuteCommand()

    def MakeEvent(self):
        pass

    def GetUserInfo(self):
        pass
