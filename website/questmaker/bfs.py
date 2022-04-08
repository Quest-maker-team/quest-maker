"""
Contains class for BFS iterating quest questions
"""

from queue import SimpleQueue


class BFS:
    """
    Class for iterating quest questions using BFS
    """
    def __init__(self, question):
        """
        :param question: question BFS start from (not necessary 'start' question)
        """
        self.__start_question__ = question

    def __iter__(self):
        self.__visited__ = set()
        self.__queue__ = SimpleQueue()
        self.__queue__.put(self.__start_question__)
        return self

    def __next__(self):
        if self.__queue__.empty():
            raise StopIteration

        cur = self.__queue__.get()
        while cur in self.__visited__:
            if self.__queue__.empty():
                raise StopIteration
            else:
                cur = self.__queue__.get()

        self.__visited__.add(cur)

        for ans in cur.answers:
            if ans.next_question is not None:
                self.__queue__.put(ans.next_question)
        for move in cur.movements:
            if move.next_question is not None:
                self.__queue__.put(move.next_question)

        return cur
