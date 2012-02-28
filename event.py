class Event:
    def __init__(self):
        self.__handlers = []

    def __iadd__(self, handler):
        self.__handlers.append(handler)
        return self

    def __isub__(self, handler):
        self.__handlers.remove(handler)
        return self

    def call(self, *args, **keywargs):
        for handler in self.__handlers:
            handler(*args, **keywargs)

	def registerHandler(self,handler):
		self.__iadd__(handler)
	
	def removeHandler(self,handler):
		self.__isub__(handler)