class ActionFlow:
    def __init__(self):
        self.__flow__: list = []
        self.__limit__ = 10
        self.__current__ = 0

    def setFlowLimit(self, limit: int):
        if limit < 5:
            limit = 5
        self.__limit__ = limit

    def add(self, item):
        if self.count() == 0 or self.__flow__[0] != item:
            self.__flow__ = self.__flow__[self.__current__:]
            self.__flow__.insert(0, item)
            if len(self.__flow__) > self.__limit__:
                self.__flow__ = self.__flow__[:self.__limit__]

    def count(self):
        return len(self.__flow__)

    def next(self):
        if self.__current__ == 0 and self.count() > 0:
            return self.__flow__[0]
        elif self.count() == 0:
            return None
        else:
            self.__current__ -= 1
            if self.__current__ <= 0:
                self.__current__ = 0
            return self.__flow__[self.__current__]

    def previous(self):
        self.__current__ += 1
        if self.__current__ >= self.count():
            self.__current__ = self.count() - 1
        return self.__flow__[self.__current__]

    def isEnd(self):
        return self.__current__ == self.count() - 1 or (self.__current__ == 0 and self.count() == 0)

    def isFirst(self):
        return self.__current__ == 0
