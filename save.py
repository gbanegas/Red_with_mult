from polynomial import Polynomial
import os
from collections import defaultdict
import sys, getopt
import xlsxwriter


def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print 'single.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'single.py -i <inputfile> -o <outputfile> '
            sys.exit()
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
    for i in fi:
        p = Polynomial(i)
        l.append(p)

    name = outputfile
    name = name + ".xlsx"
    name = "" + name
    workbook = xlsxwriter.Workbook(name)
    worksheet = workbook.add_worksheet("irredutiveis")
    worksheet.write(0,0, "Polynomials")
    worksheet.write(0,1, "m")
    worksheet.write(0,2, "a")
    worksheet.write(0,3, "b")
    worksheet.write(0,4, "c")
    worksheet.write(0,5, "d")
    row = 1
    colum = 0
   
    for p in l:
    	colum = 0
    	worksheet.write(row,colum, str(p.coefs()))
    	colum = 1
    	j = sorted(p.coefs(), reverse=True)
    	for num in j:
    		worksheet.write(row,colum, num)
    		colum = colum+1
    	row = row + 1

    workbook.close()


if __name__ == '__main__':
    main(sys.argv[1:])