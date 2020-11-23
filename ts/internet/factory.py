#coding:utf-8
class Factory(object):
    def doStart(self):
        print("===factory doStart")
        self.startFactory()

    def startFactory(self):
        print("===factory startFactory")