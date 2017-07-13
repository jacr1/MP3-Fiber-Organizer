from abc import ABCMeta, abstractmethod

class Reporter():
    __metaclass__ = ABCMeta

    @abstractmethod
    def printLine(line):
        pass

    @abstractmethod
    def clear():
        pass 

class normalReporter(Reporter):
	
	def printLine(line):
		print(line);

	def clear():
		pass
