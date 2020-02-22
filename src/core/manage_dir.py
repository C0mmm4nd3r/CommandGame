import datetime
from anytree import Node, RenderTree
import json

class DirTree:
    def __init__(self):
        try:
            with open('json/Dir.json') as DirJson:
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
            content = self.DirInfo[name]['content']
            self.DirNode[name] = Node(name, parent=self.DirNode[parent], owner=owner, crtime=crtime, modtime=modtime, dir_type=dir_type, content=content)
        return

    def ls_dir(self, parent_path):
        output = '\n'
        for name in self.DirInfo:
            if self.DirInfo[name]['parent'] != parent_path:
                continue
            else:
                output += "{} {} {} {}".format(self.DirInfo[name]['dir_type'],self.DirInfo[name]['owner'], self.DirInfo[name]['modtime'], name) + '\n'
        return output

    def PrintDir(self, path):
        if path not in self.DirInfo:
            return False
        output = ''
        path_node = self.DirNode[path]
        for pre, _, node in RenderTree(path_node):
            output += "%s%s"%(pre, node.name) + '\n'
            #print("%s%s"%(pre, node.name))
        return output

    def SaveDir(self):
        with open('json/Dir.json', 'w',encoding='utf-8') as dump_json:
            json.dump(self.DirInfo, dump_json, indent="\t")
        #저장했으면 그 내용을 다시 불러온다.
        with open('json/Dir.json') as DirJson:
            self.DirInfo = json.load(DirJson)
        self.GetSavedDir()
        return True

    def AddDir(self, full_path, crtime, modtime, dir_type, parent, owner, content): #need current location and current location will be parent node
        self.DirNode[full_path] = Node(full_path, parent=self.DirNode[parent], owner=owner, crtime=crtime, modtime=modtime, dir_type=dir_type, content=content)
        self.DirInfo[full_path] = {'owner':owner, 'crtime':crtime, 'modtime':modtime, 'dir_type':dir_type, 'parent':parent, 'content':content}
        #loggy.info("Add Directtory(Parent : {})".format(parent))
        self.SaveDir() #must to record parent node is absolutely location and getdir
        return

    def CatDir(self, path):
        return '\n'+self.DirInfo[path][content]

# 삭제 후 저장
    def RmDir(self, full_path):
        del(self.DirInfo[full_path])
        self.DirNode[full_path].parent = None
        del self.DirNode[full_path]
        self.SaveDir()
        return
