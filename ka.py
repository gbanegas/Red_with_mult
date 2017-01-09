import os
from collections import defaultdict,OrderedDict
import sys, getopt
import xlsxwriter
from polynomial import Polynomial
import math

def main(argv):
    inputfile = ''
    outputfile = ''
    ka = ''
    try:
      opts, args = getopt.getopt(argv,"hi:o:k:",["ifile=","ofile=",])
    except getopt.GetoptError:
      print 'extract.py -i <inputfile> -o <outputfile> -k 1,2,3,4,5,...'
      sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'extract.py -k 1,2,3,4,5,... -i <inputfile> -o <outputfile> '
            sys.exit()
        elif opt in ("-i", "--ifile"):
            print "-i", arg
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            print "-o", arg + "_" + str(ka)
            outputfile = arg + "_" + str(ka)
        elif opt in ("-k"):
            print "ka = ", arg
            ka = arg



    try:
        f = open(inputfile,'r')
    except IOError:
        print 'Error to open the file'
        print 'ka.py -i <inputfile> -o <outputfile> -k 1,2,3,4,5,6,...'
        sys.exit(2)


    to_save = open(outputfile,"a")
    for line in f:
        pol = Polynomial(line)
        l = sorted(pol.coefs(), reverse=True)
        k = math.floor((l[0]-2)/(l[0]-l[1]))
        if k == int(ka):
            to_save.write(line)

if __name__ == '__main__':
    main(sys.argv[1:])
