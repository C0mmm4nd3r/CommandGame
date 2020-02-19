from logging import loggy
from anytree import Node, RenderTree
from manage_dir import DirTree
import datetime

#check permission before execute command
class CmFunc:
    def __init__(self):
        pass

    def ls_func(self):
        pass

    def pwd_func(self):
        pass

    def rm_func(self, dirObj, userinfo, path):
        path = "".join(path)
        if path[0] == '/':
            full_path = path
        else:
            full_path = userinfo['currloc']+'/'+path
        if not(full_path in dirObj.DirInfo):
            return False
        #if userinfo['permission'] < dirObj.DirInfo['permission']:
        #    return False
        dirObj.RmDir(full_path)
        return True

#mkdir /home/tuuna/level1
#mkdir test/level1   ### 맨앞에 /가 있다면 절대, 없다면 상대 current_location을 붙인다.
    def mkdir_func(self, dirObj, userinfo, path):
        path = "".join(path)
        if path[0] == '/': #절대경로
            full_path = path
        else:
            full_path = userinfo['currloc'] + '/' + path
        if full_path in dirObj.DirInfo:
            return False
        #if userinfo['permission'] < dirObj.DirInfo['permission']:
        #    return False
        parent = full_path.split('/')[0:-1]
        parent = "/".join(parent)
        if parent in dirObj.DirInfo:
            dir_type = 'dir'
            crtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            modtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            owner = 'tuuna'#get user info
            #이렇게 해도 되는지 테스트 필요 안되면 객체를 인수로 넘기고
            dirObj.AddDir(full_path, crtime, modtime, dir_type, parent, 'tuuna')
        else:
            return False
        return True

    def scp_func(self):
        pass

    def ifconfig_func(self):
        pass

    def cd_func(self):
        pass

    def file_func(self):
        pass

    def cp_func(self):
        pass

    def cat_func(self):
        pass

    def editor_func(self):
        pass

    def whoami_func(self):
        pass

    def ps_func(self):
        pass

    def lastlog_func(self):
        pass

    def id_func(self):
        pass

    def mv_func(self):
        pass

    def fund_func(self):
        pass

    def tree_func(self):
        pass

    ## execl maked binary
    def execl_func(self):
        pass

    def access_func(self):
        pass

    def nc_func(self):
        pass

    def touch_func(self):
        pass

    def netstat_func(self):
        pass

    def nmap_func(self):
        pass

    def ufw_func(self):
        pass

    def who_func(self):
        pass

    def date_func(self):
        pass
