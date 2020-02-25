import json

class EventTrigger:
    def __init__(self):
        with open('json/event_list.json',encoding='utf-8') as eventdump:
            self.event = json.load(eventdump)

    def make_event(self, component):
        pass

    def compare_flag(self, component):
        pass

    def delete_event(self, component):
        pass
