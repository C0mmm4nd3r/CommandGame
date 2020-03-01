from anytree import Node, RenderTree
import json
from manage_dir import DirTree
from CommandFunction import CmFunc
from event import EventTrigger
from store import Store
import datetime

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
            'lastlog':self.cmfunc.lastlog_func,
            'find':self.cmfunc.find_func,
            'date':self.cmfunc.date_func,
            'help':self.cmfunc.help_func,
        }

    def SaveData(self):
        with open('json/sysuser.json', 'w', encoding='utf-8') as sysuserdump:
            json.dump(self.sysuserinfo, sysuserdump, indent='\t')
        with open('json/user.json', 'w', encoding='utf-8') as userdump:
            json.dump(self.userinfo, userdump, indent='\t')
        with open('json/system.json', 'w', encoding='utf-8') as systemdump:
            json.dump(self.systeminfo, systemdump, indent='\t')
        self.GetUserInfo()

    #first calling time
    def UserSetting(self, username, password):
        with open('json/sysuser.json', encoding='utf-8') as sysuserJson:
            self.sysuserinfo = json.load(sysuserJson)
        self.sysuserinfo[username] = {'date':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'ip':'192.202.102.32', }
        with open('json/user.json', encoding='utf-8') as userJson:
            self.userinfo = json.load(userJson)
        if self.userinfo['setup'] == False:
            user_setting = {'setup':False, 'username':username, 'password':password, 'money':0, 'home_folder':'/home/'+username, 'currloc':'/home/'+username, 'permission':username}
            with open('json/user.json', 'w', encoding='utf-8') as userdump:
                json.dump(user_setting, userdump, indent='\t')
        self.GetUserInfo()
        userinfo = self.component['userinfo']
        if not((userinfo['username'] == username) and (userinfo['password'] == password)):
            return False #login errro
        self.cmfunc.mkdir_func(self.component, ['', userinfo['home_folder']])
        self.SaveData()
        return True


    def GetUserInfo(self):
        with open('json/tutorial.json',encoding='utf-8') as tutoJson:
            self.TutoInfo = json.load(tutoJson)
        self.iter_TutoInfo = iter(self.TutoInfo)
        with open('json/user.json',encoding='utf-8') as userJson:
            self.userinfo = json.load(userJson)
        with open('json/system.json',encoding='utf-8') as systemJson:
            self.systeminfo = json.load(systemJson)
        self.permission = {self.userinfo['username']:0, 'root':2, 'designer':0, 'welcome':0}
        self.history = []
        self.component = {'sysinfo':self.systeminfo, 'userinfo':self.userinfo, 'dirObj':self.dir, 'permission':self.permission, 'history':self.history, 'sysuserinfo':self.sysuserinfo}
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


    def GetEvent(self):
        return self.event.PossibleEvent()


    def CompareFlag(self, key, userflag):
        reward = self.event.compare_flag(key, userflag)
        if reward != False:
            self.component['userinfo']['money'] += reward
            self.SaveData()
            return True
        else:
            return False


    def StoreProduct(self):
        return self.store.InStore_ProductList()


    def ChestProduct(self):
        return self.store.InChest_ProductList()

#return True and False
    def BuyProduct(self, ItemName):
        #result = {1:'Success', 2:"Already", 3:"Don't exist Item", 4:"Lack of money", 5:"Usage ... get out"}
        self.SaveData()
        return self.store.Buy(self.component, ItemName)


    def SellProduct(self, ItemName):
        #result = {1:'Success', 2:"Don't exist Item"}
        self.SaveData()
        return self.store.Sell(self.component, ItemName)


    def ProductUsage(self, ItemName):
        #result = {1:'Success', 2:"Don't exist Item"}
        self.SaveData()
        return self.store.usage(self.component, ItemName)
