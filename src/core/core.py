from logging import loggy
from anytree import Node, RenderTree
import json
from manage_dir import DirTree
from CommandFunction import CmFunc
from event import EventTrigger

class Core:
    def __init__(self):
        self.cmfunc = CmFunc()
        self.dir = DirTree()
        self.dir.GetSavedDir()
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
        }

    def SaveData(self):
        with open('user.json', 'w', encoding='utf-8') as userdump:
            json.dump(self.userinfo, userdump, indent='\t')
        with open('system.json', 'w', encoding='utf-8') as systemdump:
            json.dump(self.systeminfo, systemdump, indent='\t')
        with open('game_data.json', 'w', encoding='utf-8') as gamedump:
            json.dump(self.game_data, gamedump, indent='\t')

    #first calling time
    def UserSetting(self, username, password):
        with open('user.json') as userJson:
            self.userinfo = json.load(userJson)
        if self.userinfo['success_setup'] == False:
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
        with open('user.json') as userJson:
            self.userinfo = json.load(userJson)
        with open('system.json') as systemJson:
            self.systeminfo = json.load(systemJson)
        with open('game_data.json') as gameJson:
            self.game_data = json.load(gameJson)
        self.permission = {self.userinfo['username']:0, 'root':1}
        self.history = []
        self.component = {'sysinfo':self.systeminfo, 'userinfo':self.userinfo, 'dirObj':self.dir, 'permission':self.permission, 'history':self.history}
        return True

    def OutputDefault(self):
        sysinfo = self.component['sysinfo']
        userinfo = self.component['userinfo']
        #return "{}@{}:~${}".format(userinfo['username'], sysinfo['system_name'], self.command[0])
        return "{}@{}:{}$".format(userinfo['username'], sysinfo['system_name'], userinfo['currloc'])

    def ExecuteCommand(self): #실행차으로 나누는거 말고 명령어에 해당하는 딕션을 따로 만들어야겠다.
        if self.command[0] in self.PossibleCommand:
            output = self.PossibleCommand[self.command[0]](self.component, self.command)
        else:
            return "Command not found: {}".format(self.command[0])
        return output

    def Handler(self):
        while True:
            command = input(self.OutputDefault())
            self.component['history'].append(command)
            self.command = command.split()
            print(self.ExecuteCommand())
            #return self.ExecuteCommand()
