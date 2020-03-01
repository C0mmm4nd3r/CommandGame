import json

class EventTrigger:
    def __init__(self):
        self.GetEvent()

    def GetEvent(self):
        with open('json/event_list.json', encoding='utf-8') as eventdump:
            self.AllEvent = json.load(eventdump)

#Fail 값과 precede 고려 해당 값의 status값을 보고, 일차검수 -> pre의 값 체크
    def PossibleEvent(self):
        self.GetEvent()
        self.PosEvent = {}
        for key in self.AllEvent:
            if self.AllEvent[key]['status'] == False:
                precede_key = self.AllEvent[key]['precede']
                if precede_key != '*':
                    if self.AllEvent[precede_key]['status'] == True:
                        self.PosEvent[key] = self.AllEvent[key]
                else:
                    self.PosEvent[key] = self.AllEvent[key]
        return self.PosEvent

    def compare_flag(self, key, userflag):
        if (self.AllEvent[key]['flag'] == userflag) and (self.AllEvent[key]['status'] == False):
            self.AllEvent[key]['status'] = True
            self.SaveEvent()
            self.GetEvent()
            return self.AllEvent[key]['reward']
        else:
            return False

    def StatusEvent(self):
        count = 0
        for key in self.AllEvent:
            if self.AllEvent[key]['status'] == True:
                count+=1 
        return count


    def SaveEvent(self):
        with open('json/event_list.json', 'w', encoding='utf-8') as eventdump:
            json.dump(self.AllEvent, eventdump, indent='\t')
