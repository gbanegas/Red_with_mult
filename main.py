from reduction import Reduction
from polynomial import Polynomial
import os
from collections import defaultdict
import sys, getopt

def recoverfile(saved, readed):
    if not os.path.exists(saved):
        return True, []
    f = open(saved,'r')
    if(not os.stat(saved).st_size==0):
        pols = []
        pols_done = []
        for line in readed:
            pol = Polynomial(line)
            pols.append(pol)
        for line in f:
            line = line.replace("[","")
            line = line.replace("]","")
            spl = line.split(',')
            p = ""
            for i in xrange(0,len(spl)-1):
                p = p + " + x^" + str(spl[i].replace(" ",""))
            p = p + " + 1"
            p = p.replace("+","",1)
            #print p
            pol_ = Polynomial(p)
            pols_done.append(pol_)

        pols_set = set(pols)
        pols_set_done = set(pols_done)
        result = pols_set - pols_set_done
        return False, list(result)
    else:
        return True, []

def main(argv):
    inputfile = ''
    outputfile = ''
    debug = True
    try:
        opts, args = getopt.getopt(argv,"hi:o:d",["ifile=","ofile="])
    except getopt.GetoptError:
        print 'single.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'single.py -i <inputfile> -o <outputfile> -d for debug'
            sys.exit()
        elif opt in ("-d", "--debug"):
            debug = True
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg


    try:
        fi = open(inputfile,"r")
        fl = open(outputfile,"a")
    except IOError:
        print 'main.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    l = []
    pols = []
    files = [inputfile]
    for fileName in files:
        save = outputfile
        f = open(fileName,'r')
        if True:
            for line in f:
                try:
                    pol = Polynomial(line)
                    pols.append(pol)
                except Exception as e:
                    print line
                    sys.exit(2)
    result = defaultdict(list)
    print len(pols)
    for pol in pols:
        if len(pol.coefs()) > 1:
            red = Reduction(debug)
            count = red.reduction(pol.coefs())
            result =  str(pol.coefs()) + ":" + str(count)
            print result
            fl.write(result + "\n")



if __name__ == '__main__':
    main(sys.argv[1:])
