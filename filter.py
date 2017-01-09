from polynomial import Polynomial
import os
from collections import defaultdict
import sys, getopt

def main(argv):
    inputfile = ''
    outputfile = ''
    debug = False
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
    pols = []
    for line in fi:
    	try:
    		pol = Polynomial(line)
    		pols.append(pol)
    	except Exception as e:
    		print line
    		sys.exit(2)
    for pol in pols:
    	st = str(pol.coefs()) + ":0" + "\n"
    	fl.write(st)
    fl.close()


if __name__ == '__main__':
    main(sys.argv[1:])
