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

    def AddDir(self, full_path, crtime, modtime, dir_type, parent, owner): #need current location and current location will be parent node
        self.DirNode[full_path] = Node(full_path, parent=self.DirNode[parent], owner=owner, crtime=crtime, modtime=modtime, type=dir_type)
        self.DirInfo[full_path] = {'owner':owner, 'crtime':crtime, 'modtime':modtime, 'dir_type':dir_type, 'parent':parent}
        #loggy.info("Add Directtory(Parent : {})".format(parent))
        self.SaveDir() #must to record parent node is absolutely location
        return

# 삭제 후 저장
    def RmDir(self, full_path):
        del(self.DirInfo[full_path])
        self.DirNode[full_path].parent = None
        del self.DirNode[full_path]
        self.SaveDir()
        return
