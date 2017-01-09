import os
from collections import defaultdict,OrderedDict
import sys, getopt
import xlsxwriter

def uniq(lst):
    last = object()
    for item in lst:
        if item == last:
            continue
        yield item
        last = item

def sort_and_deduplicate(l):
    return sorted(list(uniq(sorted(l, reverse=True))),reverse=True)

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile=",])
    except getopt.GetoptError:
      print 'extract.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'extract.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            print "-i", arg
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            print "-o", arg + ".xlsx"
            outputfile = arg


    try:
        f = open(inputfile,'r')
    except IOError:
        print 'Error to open the file'
        print 'extract.py -i <inputfile> -o <outputfile>'
        sys.exit(2)


    
    pols = defaultdict(list)
    
    for line in f:
        splited = line.split(':')
        number = splited[1].replace('\n','')

        if pols[int(number)] == None:   
            pols[int(number)] = set()

        spl = splited[0].replace(",","").replace("[","").replace("]","").split(' ')
        numbers = []
        for i in spl:
            numbers.append(int(i))

        numbers_set = set(numbers)
        pols[int(number)].append(list(numbers_set))


    
    for i in pols:
        l = pols[i] 
        result = sort_and_deduplicate(l)
        pols[i] = result   
        #print i, pols[i]
            #pols.sort(reverse=True)

    name = outputfile
    name = name + ".xlsx"
    name = "" + name
    workbook = xlsxwriter.Workbook(name)
    worksheet = workbook.add_worksheet("irredutiveis")
    worksheet.write(0,0, "XORs")
    worksheet.write(0,1, "m")
    worksheet.write(0,2, "a")
    worksheet.write(0,3, "b")
    worksheet.write(0,4, "c")
    worksheet.write(0,5, "d")
    row = 1
    colum = 0
    f = sorted(pols.keys())
    for i in f:
        for j in pols[i]:
            colum = 0
            worksheet.write(row,colum, i)
            colum = 1
            j = sorted(j, reverse=True)
            for num in j:
                worksheet.write(row,colum, num)
                colum = colum+1
            row = row + 1    

    workbook.close()


if __name__ == '__main__':
    main(sys.argv[1:])
    
    
    
    #for i in pols:
    #    print str(i) + ":" +str(pols[i])
    

    