import datetime
from logging import loggy #logging module
from anytree import Node, RenderTree
import json

class DirTree:
    def __init__(self):
        try:
            with open('Dir.json') as DirJson:
                self.DirInfo = json.load(DirJson)
        except IOError as err:
            print("Json Parsing Error")
        owner = self.DirInfo['/']['owner']
        crtime = self.DirInfo['/']['crtime']
        modtime = self.DirInfo['/']['modtime']
        dir_type = self.DirInfo['/']['dir_type']
        self.TopParent = Node([*self.DirInfo][0], owner=owner, crtime=crtime, modtime=modtime, type=dir_type)
        self.DirNode = {[*self.DirInfo][0] : self.TopParent} #최상위 부모 노드 설정

    #self.ParentList[parent] 하면 부모 노드가 나옴.
    def GetSavedDir(self):
        for name in self.DirInfo:
            if name == '/':
                continue
            owner = self.DirInfo[name]['owner']
            crtime = self.DirInfo[name]['crtime']
            modtime = self.DirInfo[name]['modtime']
            dir_type = self.DirInfo[name]['dir_type']
            parent = self.DirInfo[name]['parent']
            self.DirNode[name] = Node(name, parent=self.DirNode[parent], owner=owner, crtime=crtime, modtime=modtime, type=dir_type)
        return

    def PrintDir(self):
        for pre, _, node in RenderTree(self.TopParent):
            print("%s%s"%(pre, node.name))
        return

    def SaveDir(self):
        with open('Dir.json', 'w',encoding='utf-8') as dump_json:
            json.dump(self.DirInfo, dump_json, indent="\t")
        #loggy.info("Directory Json Saved")
        return

    #절대경로 상대경로 구별법
    # name을 잘라서 슬래쉬 기준으로 잘라서 확인(/home/tuuna/file에서 /home/tuuna의 존재 확인 ->
    #must call SaveDir after AddDir function and RmDir function
    #이것도 절대경로 상대경로 파악해야하네 앞에 루트표시로?
    def AddDir(self, full_path, crtime, modtime, dir_type, parent, owner): #need current location and current location will be parent node
        self.DirNode[full_path] = Node(full_path, parent=self.DirNode[parent], owner=owner, crtime=crtime, modtime=modtime, type=dir_type)
        self.DirInfo[full_path] = {'owner':owner, 'crtime':crtime, 'modtime':modtime, 'dir_type':dir_type, 'parent':parent}
        #loggy.info("Add Directtory(Parent : {})".format(parent))
        self.SaveDir() #must to record parent node is absolutely location
        return

#만약 /home/tuuna/folder 을 지운다면 현재 플레이어의 절대경로를 파악
#절대 경로에서 + 플레이어가 작성한 위치를 더해 찾는다.
#입력한 문자열이 절대경로인지 상대경로인지 구별방법은? 해당 위치에서의 폴더 및 파일의 유뮤 ?
# 삭제 후 저장
    def RmDir(self, full_path):
        del(self.DirInfo[full_path])
        self.DirNode[full_path].parent = None
        del self.DirNode[full_path]
        self.SaveDir()
        return

    def GetCurrentDir(self):
        pass

    def MvDir(self):
        pass

    def CpDir(self):
        pass
