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
        #time1 = time.time()
        combinations = list(self.combinations(self.collumn, 2))
        #time2 = time.time()
        #with self.lockscreen:
        #    #print self.collumn
        #    print 'function took %0.3f ms' % ((time2-time1)*1000.0)
        #    print "Number of Pairs (C) : ", len(combinations)," from ID: ", self.threadID
        with self.locker:
            for pair in combinations:
                self.result.append(pair)

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
