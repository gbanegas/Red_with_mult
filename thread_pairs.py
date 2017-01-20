import threading
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
        temp = []
        for i in xrange(1, len(self.collumn)):
            if self.collumn[i] <> NULL :
                p1 = self.collumn[i]
                for j in xrange(i+1, len(self.collumn)):
                    p2 = self.collumn[j]
                    if p2 <> NULL :
                        if p1 > p2:
                            pair = (p2, p1)
                        else:
                            pair = (p1, p2)
                        temp.append(pair)


        with self.locker:
            for pair in temp:
                self.result.append(pair)
        #self.lockscreen.acquire()
        #print "Thread ID: ", self.threadID, "Pairs: ", self.result
        #self.lockscreen.release()
        #return result

    def get_pairs(self):
        return self.result
