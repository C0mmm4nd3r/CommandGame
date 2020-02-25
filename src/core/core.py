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
            'whoami':self.cmfunc.whoami_func,
        }
        self.CheckTutorial = False

    def SaveData(self):
        with open('json/user.json', 'w', encoding='utf-8') as userdump:
            json.dump(self.userinfo, userdump, indent='\t')
        with open('json/system.json', 'w', encoding='utf-8') as systemdump:
            json.dump(self.systeminfo, systemdump, indent='\t')
        with open('json/game_data.json', 'w', encoding='utf-8') as gamedump:
            json.dump(self.game_data, gamedump, indent='\t')

    #first calling time
    def UserSetting(self, username, password):
        with open('json/user.json', encoding='utf-8') as userJson:
            self.userinfo = json.load(userJson)
        if self.userinfo['setup'] == False:
            #self.CheckTutorial = True
            user_setting = {'setup':False, 'username':username, 'password':password, 'money':0, 'home_folder':'/home/'+username, 'currloc':'/home/'+username, 'permission':username }
            with open('json/user.json', 'w', encoding='utf-8') as userdump:
                json.dump(user_setting, userdump, indent='\t')
        self.GetUserInfo()
        userinfo = self.component['userinfo']
        if not((userinfo['username'] == username) and (userinfo['password'] == password)):
            return False #login errro
        self.cmfunc.mkdir_func(self.component, ['', userinfo['home_folder']])
        return True


    def GetUserInfo(self):
        with open('json/tutorial.json',encoding='utf-8') as tutoJson:
            self.TutoInfo = json.load(tutoJson)
        self.iter_TutoInfo = iter(self.TutoInfo)
        with open('json/user.json',encoding='utf-8') as userJson:
            self.userinfo = json.load(userJson)
        with open('json/system.json',encoding='utf-8') as systemJson:
            self.systeminfo = json.load(systemJson)
        with open('json/game_data.json',encoding='utf-8') as gameJson:
            self.game_data = json.load(gameJson)
        self.permission = {self.userinfo['username']:0, 'root':2, 'attacker':0}
        self.history = []
        self.component = {'sysinfo':self.systeminfo, 'userinfo':self.userinfo, 'dirObj':self.dir, 'permission':self.permission, 'history':self.history}
        return True

    def OutputDefault(self):
        sysinfo = self.component['sysinfo']
        userinfo = self.component['userinfo']
        #return "{}@{}:~${}".format(userinfo['username'], sysinfo['system_name'], self.command[0])
        return "{}@{}:{}$".format(userinfo['username'], sysinfo['system_name'], userinfo['currloc'])


    def Tutorial(self, command, explain):
        if command != explain['answer']:
            return ''
        else:
            self.command = command.split()
            if self.command[0] in self.PossibleCommand:
                output = self.PossibleCommand[self.command[0]](self.component, self.command)
            else:
                return " Command not found: {}".format(self.command[0])
            return output


    def ExecuteCommand(self, command):
        if command == '':
            return ''
        self.command = command.split()
        self.component['history'].append(command)
        if self.command[0] in self.PossibleCommand:
            output = self.PossibleCommand[self.command[0]](self.component, self.command)
        else:
            return " Command not found: {}".format(self.command[0])
        return "\n"+output

    #gui 측면에서 Event를 가지려할 때 이 함수 호출
    def GetEvent(self):
        pass
