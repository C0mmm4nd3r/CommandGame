from anytree import Node, RenderTree
import json
from manage_dir import DirTree
from CommandFunction import CmFunc
from event import EventTrigger
from store import Store

class Core:
    def __init__(self):
        self.cmfunc = CmFunc()
        self.dir = DirTree()
        self.dir.GetSavedDir()
        self.event = EventTrigger()
        self.store = Store()
        self.PossibleCommand = {
            "mkdir":self.cmfunc.mkdir_func,
            "ifconfig":self.cmfunc.ifconfig_func,
            "pwd":self.cmfunc.pwd_func,
            "cd":self.cmfunc.cd_func,
            "clear":self.cmfunc.clear_func,
            "rm":self.cmfunc.rm_func,
            "tree":self.cmfunc.tree_func,
            "history":self.cmfunc.history_func,
            "ls":self.cmfunc.ls_func,
            'touch':self.cmfunc.touch_func,
            'cat':self.cmfunc.cat_func,
        }
        self.CheckTutorial = False
        self.TutorialList = {}

    def SaveData(self):
        with open('json/user.json', 'w', encoding='utf-8') as userdump:
            json.dump(self.userinfo, userdump, indent='\t')
        with open('json/system.json', 'w', encoding='utf-8') as systemdump:
            json.dump(self.systeminfo, systemdump, indent='\t')
        with open('json/game_data.json', 'w', encoding='utf-8') as gamedump:
            json.dump(self.game_data, gamedump, indent='\t')

    #first calling time
    def UserSetting(self, username, password):
        with open('json/user.json') as userJson:
            self.userinfo = json.load(userJson)
        if self.userinfo['success_setup'] == False:
            self.CheckTutorial = True
            user_setting = {}
            user_setting['success_setup'] = True
            user_setting['username'] = username
            user_setting['password'] = password
            user_setting['PossibleCommand'] = ["ls", "rm", "mkdir"]
            user_setting['exp'] = 0
            user_setting['money'] = 0
            user_setting['home_folder'] = "/home/"+username
            user_setting['currloc'] = "/home/"+username
            user_setting['permission'] = "tuuna"
            with open('user.json', 'w', encoding='utf-8') as userdump:
                json.dump(user_setting, userdump, indent='\t')
        self.GetUserInfo()
        userinfo = self.component['userinfo']
        if not((userinfo['username'] == username) and (userinfo['password'] == password)):
            return False #login errro
        self.cmfunc.mkdir_func(self.component, ['', userinfo['home_folder']])
        return True

    def GetUserInfo(self):
        with open('json/user.json') as userJson:
            self.userinfo = json.load(userJson)
        with open('json/system.json') as systemJson:
            self.systeminfo = json.load(systemJson)
        with open('json/game_data.json') as gameJson:
            self.game_data = json.load(gameJson)
        self.permission = {self.userinfo['username']:0, 'root':2, 'attacker':0, 'super_attacker':1}
        self.history = []
        self.component = {'sysinfo':self.systeminfo, 'userinfo':self.userinfo, 'dirObj':self.dir, 'permission':self.permission, 'history':self.history}
        return True

    def OutputDefault(self):
        sysinfo = self.component['sysinfo']
        userinfo = self.component['userinfo']
        #return "{}@{}:~${}".format(userinfo['username'], sysinfo['system_name'], self.command[0])
        return "{}@{}:{}$".format(userinfo['username'], sysinfo['system_name'], userinfo['currloc'])


    def ExecuteCommand(self, command):
        if self.CheckTutorial == True:
            pass
        else:
            if command == '':
                return ''
            self.command = command.split()
            self.component['history'].append(command)
            if self.command[0] in self.PossibleCommand:
                output = self.PossibleCommand[self.command[0]](self.component, self.command)
            else:
                return " Command not found: {}".format(self.command[0])
            return output

    #gui 측면에서 Event를 가지려할 때 이 함수 호출
    def GetEvent(self):
        pass
