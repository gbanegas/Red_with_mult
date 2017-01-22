import threading
import itertools
import time
NULL = -1

class ThreadGeneratePairs(threading.Thread):


    def __init__(self, threadID,  locker, lockscreen, collumn, result):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.locker = locker
        self.lockscreen = lockscreen
        self.collumn = collumn
        self.result = result

    def run(self):
        #with self.lockscreen:
        #    print("Starting thread {}".format(self.threadID))
        time1 = time.time()
        a = list(self.combinations(self.collumn[1::], 2))
        time2 = time.time()



        # temp = []
        # for i in xrange(1, len(self.collumn)):
        #     if self.collumn[i] <> NULL :
        #         p1 = self.collumn[i]
        #         for j in xrange(i+1, len(self.collumn)):
        #             p2 = self.collumn[j]
        #             if p2 <> NULL :
        #                 if p1 > p2:
        #                     pair = (p2, p1)
        #                 else:
        #                     pair = (p1, p2)
        #                 temp.append(pair)
        #
        with self.lockscreen:
            print 'function took %0.3f ms' % ((time2-time1)*1000.0)
            print "Number of Pairs (C) : ", len(a)," from ID: ", self.threadID
        #     print "Number of Pairs (old) : ", len(temp)," from ID: ", self.threadID

        #     st = ""
        #     for pair in temp:
        #         st = " " + str(pair) + " "
        #     print st
        #     st = ""
        #     for pair in a:
        #         st = " " + str(pair) + " "
        #     print st
        with self.locker:
            for pair in a:
                self.result.append(pair)
        #self.lockscreen.acquire()
        #print "Thread ID: ", self.threadID, "Pairs: ", self.result
        #self.lockscreen.release()
        #return result

    def get_pairs(self):
        return self.result

    def combinations(self, iterable, r):
        # combinations('ABCD', 2) --> AB AC AD BC BD CD
        # combinations(range(4), 3) --> 012 013 023 123
        iterable = filter(lambda a: a != -1, iterable)

        pool = tuple(iterable)
        n = len(pool)
        if r > n:
            return
        indices = list(range(r))
        yield tuple(pool[i] for i in indices)
        while True:
            for i in reversed(range(r)):
                if indices[i] != i + n - r:
                    break
            else:
                return
            indices[i] += 1
            for j in range(i+1, r):
                indices[j] = indices[j-1] + 1
            yield tuple(pool[i] for i in indices)
