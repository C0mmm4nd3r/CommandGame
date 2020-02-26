import json

class EventTrigger:
    def __init__(self):
        with open('json/event_list.json',encoding='utf-8') as eventdump:
            self.AllEvent = json.load(eventdump)


#Fail 값과 precede 고려 해당 값의 status값을 보고, 일차검수 -> pre의 값 체크
    def PossibleEvent(self):
        self.PosEvent = {}
        for key in self.AllEvent:
            if self.AllEvent[key]['status'] == False:
                precede_key = self.AllEvent[key]['precede']
                if precede_key != '*':
                    if self.AllEvent[precede_key]['status'] == True:
                        self.PosEvent[key] = self.AllEvent[key]
                else:
                    self.PosEvent[key] = self.AllEvent[key]
        return

    def compare_flag(self, component, flag):
        return self.PossibleEvent()

