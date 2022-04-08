from queue import SimpleQueue
from .quest import Question


class BFS:
    def __init__(self, node):
        self.__start_node__ = node

    def __iter__(self):
        self.__visited__ = set()
        self.__queue__ = SimpleQueue()
        self.__queue__.put(self.__start_node__)
        return self

    def __next__(self):
        if self.__queue__.empty():
            raise StopIteration

        cur = self.__queue__.get()

        self.__visited__.add(cur)

        if isinstance(cur, Question):
            for ans in cur.answers:
                if ans not in self.__visited__:
                    self.__queue__.put(ans)
            for move in cur.movements:
                if move not in self.__visited__:
                    self.__queue__.put(move)
        else:  # current node type is Answer or Movement
            if cur.next_question not in self.__visited__:
                self.__queue__.put(cur.next_question)

        return cur
