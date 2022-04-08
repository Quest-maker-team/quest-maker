from queue import SimpleQueue


class BFS:
    def __init__(self, quest):
        self.__quest__ = quest

    def __iter__(self):
        self.__visited__ = set()
        self.__queue__ = SimpleQueue()
        self.__queue__.put(self.__quest__.first_question)
        return self

    def __next__(self):
        if self.__queue__.empty():
            raise StopIteration

        cur = self.__queue__.get()
        cur_type = type(cur)

        self.__visited__.add(cur)

        if cur_type == 'Question':
            for ans in cur.answers:
                if ans not in self.__visited__:
                    self.__queue__.put(ans)
            for move in cur.movements:
                if move not in self.__visited__:
                    self.__queue__.put(move)
        else:  # cur_type is answer or movement
            if cur.next_question not in self.__visited__:
                self.__queue__.put(cur.next_question)

        return cur
