
#가게 + 창고
class Store:
    def __init__(self):
        self.Already = 2
        self.NotIn = 3
        self.Lack = 4
        self.Usage = 5

    def GetData(self):
        with open('json/store.json', encoding='utf-8') as storeJson:
            self.storeinfo = json.load(storeJson)
        with open('json/chest.json', encoding='utf-8') as chestJson:
            self.chestinfo = json.load(chestJson)
        return True

    def InStore_ProductList(self, component):
        self.GetData()
        return self.storeinfo

    def Buy(self, component, ItemName):
        self.GetData()
        userinfo = component['userinfo']
        if ItemName not in self.storeinfo:
            return self.NotIn
        if ItemName in self.chestinfo:
            return self.Already
        Item = self.storeinfo[ItemName]
        if Item['price'] > userinfo['money']:
            return self.Lack
        userinfo['money'] -= Item['price']
        self.chestinfo[ItemName] = {'sell':Item['price']/2, 'type':Item['type'],'usage':False}
        self.SaveData()
        return True

#사용중이면 X
    def Sell(self, component, ItemName):
        self.GetData()
        userinfo = component['userinfo']
        if ItemName not in self.chestinfo:
            return self.NotIn
        #팔려던 아이템이 사용중이라면 
        if self.chestinfo[ItemName]['usage'] == True:
            return self.Usage
        userinfo['money'] += self.chestinfo[ItemName]['sell']
        del(self.chestinfo[ItemName])
        self.SaveData()
        return True


#userinfo 에서 추가하자. ...
    def usage(self, component, ItemName):
        self.GetData()
        if ItemName not in self.chestinfo:
            return self.NotIn
        ItemType = self.chestinfo[ItemName]['type']
        userinfo = component['userinfo']
        #이미 사용중인거 False으로 변경
        usaged_name = userinfo[ItemType]
        self.chestinfo[usaged_name]['usage'] = False
        self.chestinfo[ItemName]['usage'] = True
        #user.json에 사용할 아이템 타입에 맞는 아이템이름으로 변경
        userinfo[ItemType] = ItemName
        self.SaveData()
        return True

    def InChest_ProductList(self, component):
        self.GetData()
        return self.chestinfo


    def SaveData():
        with open('json/store.json', 'w', encoding='utf-8') as storedump:
            json.dump(self.storeinfo, storedump, indent='\t')
        with open('json/chest.json', 'w', encoding='utf-8') as chestdump:
            json.dump(self.chestinfo, chestdump, indent='\t')
        self.GetData()
        return True
