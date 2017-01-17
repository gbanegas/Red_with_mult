'''
Created on 10 Sep 2014

@author: gustavo
'''
import threading
from reduction import Reduction

class ThreadCount(threading.Thread):


    def __init__(self, threadID,  locker, lockscreen, polynomials, save):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.locker = locker
        self.polynomials = polynomials
        self.save = save
        self.lockscreen = lockscreen

    def run(self):
        print "Starting thread: " + str(self.threadID) + '\n'
        for i in self.polynomials:
            reduc = Reduction(False)
            self.lockscreen.acquire()
            print 'Thread: '+ str(self.threadID) + ' Doing: ' + str(i.coefs())
            self.lockscreen.release()
            count = reduc.reduction(i.coefs())
            self.locker.acquire()
            r = str(i.coefs()) + ":" + str(count)
            f = open(self.save, "a")
            f.write(r + '\n')
            f.close()
            self.locker.release()
            self.lockscreen.acquire()
            #print r
            self.lockscreen.release()
            del reduc
