'''
Created on 10 Sep 2014

@author: gustavo
'''

import math
import re
from ot import Ot
#from xlsx import Xslxsaver



import copy

NULL = -1
max_collum = 0
mdegree = 0;


class Reduction(object):

    def __init__(self, debug):
        self.debug = debug

    def reduction(self,exp):
        #xls = Xslxsaver()
        #xls.create_worksheet(exp)
        self.otimizator = Ot()
        exp_sorted = sorted(exp, reverse=True)
        self.mdegree = exp_sorted[0]
        self.max_collum = (2*exp_sorted[0])-1
        nr = self.__calc_NR__(exp_sorted)
        self.matrix = self.__generate_matrix__()
        exp_sorted.remove(self.mdegree)
        self.matrix = self.__multiply__(self.matrix, self.mdegree)
        #xls.save(self.matrix, 'Multiplication')
        print "Finished Multiplication"

        for i in range(0,nr+1):
            self.__reduce_others__(self.matrix,exp_sorted)
            #xls.save(self.matrix, 'step_reduction_'+str(i))

        self.__remove_repeat__(self.matrix)
        self.clean(self.matrix)
        self.matrix = self.otimizator.sort(self.matrix)
        self.clean(self.matrix)
        self.matrix = self.__reduce_matrix__(self.mdegree, self.matrix)
        #xls.save(self.matrix, 'reduced')
        print "Finished Cleaning"

        self.p, self.matrix, self.frequency_counter, self.columns_of_pair = self.otimizator.optimize(self.matrix, self.mdegree, xls)

        self.__remove_one__(self.matrix)
        row = [-1 for x in xrange(self.mdegree)]
        self.matrix.append(row)
        count = self.__count_xor__(self.matrix,self.p)
        #xls.save(self.matrix, 'Optimized')
        #xls.save_matches(self.p, self.frequency_counter, self.columns_of_pair)
        del self.matrix
        return count

    def __multiply__(self, matrix, degree):
        temp_reuse = 0
        for offset in xrange(0, degree):
            index = self.max_collum-1;
            row = [-1 for x in xrange(self.max_collum)]
            temp = 0
            for j in xrange(0,self.mdegree):
                row[index] = j + temp_reuse
                index = index-1
                temp = j + temp_reuse
            index = 2*self.mdegree - 2 - self.mdegree;
            temp_reuse = temp
            for j in xrange(self.mdegree, 2*self.mdegree - 1):
                #print self.max_collum - index
                row[index] = temp + degree
                index = index - 1
                temp = temp + degree
            #print index
            for i in xrange(0, offset):
                row[i] = -1
                row[self.max_collum-1-i] =-1

            matrix.append(row)



        return matrix

    def __reduce_matrix__(self, degree, matrix):
        #print "printing..."
        matrix_copy = [[-1 for x in range(degree)] for x in range(len(matrix))]
        for i in xrange(0, len(matrix)):
            h = 0
            #print i
            for j in xrange(degree-1, len(matrix[0])):
                matrix_copy[i][h] = matrix[i][j]
                h += 1

        #print_matrix(matrix_copy)
        del matrix
        return matrix_copy

    def __count_matchs__(self, matches):
        count = 0;
        for i in matches:
            count = count + (len(matches[i])-1)
        return count

    def __count_xor__(self, matrix, p):
        rowToWrite = [-1 for x in xrange(self.mdegree)]

        row = matrix[0]
        for j in range(0,len(row)):
            countT = 0
            element = row[j]
            if element <> NULL:
                for l in range(1, len(matrix)):
                    rowToCompare = matrix[l]
                    elementToCompare = rowToCompare[j]
                    if elementToCompare <> NULL or (re.search('[a-zA-Z]', str(elementToCompare)) <> None):
                        countT = countT + 1;
                        #print "Column :", j, " count: ", countT, " element: ", elementToCompare
            rowToWrite[j] = countT
        matrix.append(rowToWrite)
        rowToCalc = matrix[len(matrix)-1]
        count = 0
        for i in range(0,len(rowToCalc)):
            tx = rowToCalc[i]
            count = count + tx
        count = count + len(p)
        #print
        return count


    def delete(self):
        del self.matrix

    def clean(self, matrix):
        toRemove = []
        for m in matrix:
            if self.is_clean(m):
                toRemove.append(m)
        for i in toRemove:
            matrix.remove(i)

    def is_clean(self, row):
        for i in row:
            if i <> NULL:
                return False
        return True

    def __reduce_others__(self, matrix, exp):
        to_reduce = self.__need_to_reduce__(matrix)
        for index in to_reduce:
            for e in exp:
                reduceRow = self.reduce(matrix[index],e)
                matrix.append(reduceRow)
            self.__clean_reduced__(matrix,index)
        self.__remove_repeat__(self.matrix)
        matrix = self.clean(matrix)

    def __remove_one__(self, matrix):
        for j in range(1, len(matrix)):
            row = matrix[j]
            for i in range(self.mdegree-1, len(row)):
                valueToCompare = row[i]
                if valueToCompare <> NULL:
                    for m in range(j+1, len(matrix)):
                        rowToCompare = matrix[m]
                        toCompare = rowToCompare[i]
                        if toCompare <> NULL:
                            if valueToCompare == toCompare:
                                rowToCompare[i] = NULL;
                        matrix[m] = rowToCompare
            matrix[j] = row


    def __remove_repeat__(self, matrix):
        for j in range(1, len(matrix)):
            row = matrix[j]
            for i in range(0, len(row)):
                found = False
                valueToCompare = row[i]
                if valueToCompare <> NULL:
                    for m in range(j+1, len(matrix)):
                        rowToCompare = matrix[m]
                        toCompare = rowToCompare[i]
                        if toCompare <> NULL:
                            if valueToCompare == toCompare:
                                rowToCompare[i] = NULL;
                                row[i] = NULL;
                                found = True;
                        matrix[m] = rowToCompare
                        if found:
                            break
            matrix[j] = row

    def __clean_reduced__(self, matrix, index):
        row = matrix[index]
        for j in range(0,self.mdegree-1):
            row[j] = NULL
        matrix[index] = row

    def reduce(self, row, exp):
        index = self.max_collum-1;
        rowReduced = [-1 for x in xrange(self.max_collum)]
        for j in range(self.mdegree-2,-1,-1):
            element = row[j]
            rowReduced[index - exp] = element
            index = index -1
        return rowReduced

    def __need_to_reduce__(self, matrix):
        indexOfRows = []
        index = (self.max_collum - 1 - self.mdegree);
        for i in range(1,len(matrix)):
            row = matrix[i]
            if row[index] <> NULL:
                indexOfRows.append(i)

        return indexOfRows


    def __reduce_first__(self, matrix, exp):
        index = self.max_collum-1;
        row = [-1 for x in xrange(self.max_collum)]
        for j in xrange(self.mdegree-2,-1,-1):
            element = matrix[0][j]
            row[index - exp] = element
            index = index -1

        matrix.append(row)

    def __calc_NR__(self, exp_sorted):
        nr = 2
        nr = int(math.floor((exp_sorted[0]-2)/(exp_sorted[0]-exp_sorted[1])))
        #print "NR = ", nr
        #temp = (exp_sorted[0]+1)/2
        #deg = math.floor(temp)
        #if exp_sorted[1] > deg:
        #    nr = 2* (exp_sorted[0] + 1) - exp_sorted[0]
        return nr

    def __generate_matrix__(self):
        #row = sorted(list(range(0, self.max_collum)), reverse=True)
        matrix = [[]]
        return matrix

    def _column(self, matrix, i):
        return [row[i] for row in matrix]

def print_matrix(matrix):
        for r in matrix:
            print ''.join(str(r))
        print '----------------------FIM---------------------'
