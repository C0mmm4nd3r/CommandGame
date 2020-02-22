import datetime

class loggy:
    def __init__(self):
        pass
        #self.log_level = log_level

    def info(self, log):
        print("[{}] {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), log))
        return

    def debug(self, log):
        pass
