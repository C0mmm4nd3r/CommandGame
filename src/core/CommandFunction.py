from anytree import Node, RenderTree
from manage_dir import DirTree
import datetime

#check permission before execute command
class CmFunc:
    def __init__(self):
        pass

    def make_fullpath(self, userinfo, path):
        path = "".join(path)
        if path[0] == '/':
            return path
        else:
            return userinfo['currloc']+'/'+path

    def make_parent(self, full_path):
        parent = full_path.split('/')[0:-1]
        parent = "/".join(parent)
        return parent

    def CheckPermission(self, component, path):
        userinfo = component['userinfo']
        permission = component['permission']
        if permission[userinfo['username']] < permission[component['dirObj'].DirInfo[path]['owner']]:
            return False
        else:
            return True

    def history_func(self, component, argument_list):
        output = ''
        history = component['history']
        num = 0
        for line in history:
            output += '[{}] '.format(str(num))+line + '\n'
            num += 1
        return output

    def clear_func(self, component, argument_list):
        output = '\n'*100
        return output

    def ls_func(self, component, argument_list):
        userinfo = component['userinfo']
        if len(argument_list) == 1:
            full_path = userinfo['currloc']
        else:
            full_path = self.make_fullpath(userinfo, argument_list[1])
        if full_path not in component['dirObj'].DirInfo:
            return "Don't exist folder or file"
        return component['dirObj'].ls_dir(full_path)

    def pwd_func(self, component, argument_list):
        userinfo = component['userinfo']
        return userinfo['currloc']

#if cat root file input password 
    def cat_func(self, component, argument_list):
        if len(argument_list) != 2:
            return "cat command need one argument"
        userinfo = component['userinfo']
        full_path = self.make_fullpath(userinfo, argument_list[1])
        if not(full_path in component['dirObj'].DirInfo):
            return "Don't existed folder or file"
        if not(self.CheckPermission(component, full_path)):
            return "Permission Denied"
        if component['dirObj'].DirInfo[full_path]['dir_type'] == 'dir':
            return "this is dir"
        return component['dirObj'].CatDir(full_path)

    def rm_func(self, component,argument_list):
        if len(argument_list) != 2:
            return "rm command need one argument"
        full_path = self.make_fullpath(component['userinfo'], argument_list[1])
        if not(full_path in component['dirObj'].DirInfo):
            return "Don't existed folder or file"
        if not(self.CheckPermission(component, full_path)):
            return "Permission Denied"
        component['dirObj'].RmDir(full_path)
        return ''

    def mkdir_touch(self, component, path, dir_type, content):
        full_path = self.make_fullpath(component['userinfo'], path)
        if full_path in component['dirObj'].DirInfo:
            return "Already exist"
        parent = full_path.split('/')[0:-1]
        parent = "/".join(parent)
        userinfo = component['userinfo']
        permission = component['permission']
        if not(self.CheckPermission(component, parent)):
            return "Permission Denied"

        if parent in component['dirObj'].DirInfo:
            crtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            modtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            owner = userinfo['username']
            component['dirObj'].AddDir(full_path, crtime, modtime, dir_type, parent, owner, content)
        else:
            return "Don't exist folder {}".format(parent)
        return ""

    def touch_func(self, component, argument_list):
        if len(argument_list) != 2:
            return "touch command need one argument"
        return self.mkdir_touch(component, argument_list[1], 'file', '')

    def mkdir_func(self, component, argument_list):
        if len(argument_list) != 2:
            return "mkdir command need one argument"
        return self.mkdir_touch(component, argument_list[1], 'dir', '*')



    def tree_func(self, component, argument_list):
        userinfo = component['userinfo']
        if len(argument_list) == 1:
            full_path = userinfo['currloc']
        else:
            full_path = self.make_fullpath(userinfo, argument_list[1])
        if not(full_path in component['dirObj'].DirInfo):
            return "Don't exist folder"
        if component['dirObj'].DirInfo[full_path]['dir_type'] == 'file':
            return "This is file"
        return component['dirObj'].PrintDir(full_path)

    def scp_func(self, component, argument_list):
        pass

    def help_func(self, component, argument_list):
        if len(argument_list) != 1:
            return "Plz help command don't need argument"
        output = '''
[command guild line]
/help : show command guild line.
/find : if you need get detail plz input /find -help 
/mkdir : make folder using one argument. 
/touch : make fine using one argument.
/cat : watch file content using one argument .
/tree : list about folder and file like tree, may or may not have one argument.
/ls : list folder and file, may or may not have one argument.
/whoami : print my permission
/date : print system date
/rm : remove folder or file
/lastlog : print user access log
/cd : move my current location
/ifconfig : print system interface and ip. etc...
/clear : remove text in terminal
/pwd : print current location
'''
        return output

    def ifconfig_func(self, component, argument_list):
        systeminfo = component['sysinfo']
        output = '''
{}: flag=3213<UP, BORADCAST, RUNNING, MULTICAST> mtu 1500
inet {} netmask 255.255.255.0 boardcast 192.202.102.255
ehter {} txqueuelen 100 (Ethernet)
        '''.format(systeminfo['interface'], systeminfo['ip'], systeminfo['mac_address'])
        return output

    def cd_func(self, component, argument_list):
        userinfo = component['userinfo']
        if len(argument_list) == 1:
            full_path = userinfo['home_folder']
        else:
            full_path = self.make_fullpath(userinfo, argument_list[1])
        if not(full_path in component['dirObj'].DirInfo):
            return "Don't exist folder"
        if component['dirObj'].DirInfo[full_path]['dir_type'] == 'file':
            return "This is file"
        userinfo['currloc'] = full_path
        return ""
        #return userinfo['currloc']

    def cp_func(self, component, argument_list):
        if len(argument_list) != 3:
            return "cp command need 2 argument"
        userinfo = component['userinfo']
        src_fullpath = self.make_fullpath(userinfo, argument_list[1])
        dst_fullpath = self.make_fullpath(userinfo, argument_list[2])
        if src_fullpath not in component['dirObj'].DirInfo:
            return "Don't exist folder or file"
        if not(self.CheckPermission(component, src_fullpath)):
            return "Permission Denied"
        if component['dirObj'].DirInfo[src_fullpath]['dir_type'] == 'dir':
            return "sorry we will update this"
        else:
            pass


    def editor_func(self, component, argument_list):
        pass

    def whoami_func(self, component, argument_list):
        userinfo = component['userinfo']
        return "\nyour permission is {}".format(userinfo['permission'])

    def ps_func(self, component, argument_list):
        pass

    def lastlog_func(self, component, argument_list):
        sysuserinfo = component['sysuserinfo']
        output = '\n{} \t{}\t\t{}'.format('계정', 'IP', "date")
        for key in sysuserinfo:
            output += '\n{}:\t{}\t{}'.format(key, sysuserinfo[key]['ip'], sysuserinfo[key]['date'])
        return output

    def mv_func(self, component, argument_list):
        pass

# find command option
# -owner : 소유권자 
# -cdate : 생성 날짜 
# -mdate : 수정 날짜 
# -name : 파일 이름 
# -path : 경로
    def find_func(self, component, argument_list):
        if len(argument_list) != 4:
            return "find command need more argument, enter find -help"
        if argument_list[1] == '-help':
            return '''
find [-Option] [Option argument] [Path]
ex) find -owner tuuna /
ex) find -name tutorial /
ex) find -time 2020-10-20  /
'''
        option_function = {'-owner':component['dirObj'].Find_Owner, '-name':component['dirObj'].Find_Name, '-time':component['dirObj'].Find_Time}
        userinfo = component['userinfo']
        full_path = self.make_fullpath(userinfo, argument_list[3])
        if not(full_path in component['dirObj'].DirInfo):
            return "Don't exist folder"
        if component['dirObj'].DirInfo[full_path]['dir_type'] == 'file':
            return "This is file"
        try:
            output = option_function[argument_list[1]](argument_list[2], full_path)
        except KeyError:
            return "option error..."
        return output


    ## execl was maked binary
    def execl_func(self, component, argument_list):
        pass

    def access_func(self, component, argument_list):
        pass

    def nc_func(self, component, argument_list):
        pass


    def netstat_func(self, component, argument_list):
        pass

    def nmap_func(self, component, argument_list):
        pass

    def ufw_func(self, component, argument_list):
        pass

    def date_func(self, component, argument_list):
        return '\n'+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
