import datetime
import logging
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
        pass

    def AddDir(self):
        pass

    def RmDir(self):
        pass

    def GetCurrentDir(self):
        pass

    def MvDir(self):
        pass

    def CpDir(self):
        pass

dir = DirTree()
dir.GetSavedDir()
dir.PrintDir()
