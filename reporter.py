from abc import ABCMeta, abstractmethod

class Reporter():
    __metaclass__ = ABCMeta

    @abstractmethod
    def printLine(self, *args):
        pass

    @abstractmethod
    def clear(self):
        pass 

class normalReporter(Reporter):

    def printLine(self, *args):
        if (len(args) == 1):
            print(args[0])
        elif (len(args) == 2):
            print(args[0], args[1])

    def clear(self):
        pass
