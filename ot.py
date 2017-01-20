'''
Created on 06 Apr 2015

@author: gustavo
'''

import math
import threading
import collections
from collections import defaultdict

from thread_pairs import ThreadGeneratePairs
from itertools import groupby


#from collections import defaultdict


NULL = -1
class Ot(object):

    def optimize(self, matrix, degree, xls=None, debug=False):
        self.matrix = matrix
        self.m = defaultdict()
        self.variable = degree*degree
        is_break = False
       # xls = Xslxsaver()
       # xls.create_work([degree])
        self.xls = xls
        i = 0

        while (not is_break):
        #for i in xrange(0,1):
            print "Round : ", i
            pair, is_break = self._generate_all_pairs(self.matrix)
            if debug:
                self.xls.save(self.matrix, str(i))
            i += 1
            #pairs_removed = self._remove_repets(pairs)
            #pair, is_break = self._max_matches(pairs_removed)
            if is_break:
                #print "pair to break, ", pair
                break

            #print_matrix(self.matrix)
            name, self.matrix = self._change_pair(pair, self.matrix)
            print "--------------------------------------------------"
            #xls.save(self.matrix, str(i))
            #print_matrix(self.matrix)
            #self._save_pair(pair, name)
            #print_matrix(self.matrix)
        #print self.m
        #xls.close()
        return self.m, self.matrix

    def sort(self, matrix):
        matrix = self.__remove__(matrix, -1, "")
        for i in xrange(0, len(matrix[0])):
            column = self._column(matrix, i)
            column.sort()
            #print column
            self.putColumn(column, matrix, i)
        matrix = self.__remove__(matrix, "", -1)
        return matrix

    def __remove__(self, matrix, toCompare, toChange):
        for i in xrange(0, len(matrix)):
            for j in xrange(0, len(matrix[i])):
                if matrix[i][j] == toCompare:
                    matrix[i][j] = toChange
        return matrix

    def _generate_all_pairs(self, matrix):
        lock = threading.Lock()
    	lockScreen = threading.Lock()
        threads = []
        allPairs = {}
        #allPairs = []
        #print matrix
        size = len(matrix[0])
        #print "Size : " + str(size)
        result = []
        for i in xrange(0,size):
            thread = ThreadGeneratePairs(i,lockScreen, lock, self._column(self.matrix,i), result)
            threads.append(thread)

        with lockScreen:
            print("Starting threads")

        [x.start() for x in threads]
        [x.join() for x in threads]

        with lockScreen:
            print("Threads Done!")

        counter = collections.Counter(result)
        max_elements = sorted(counter.values(),reverse=True)[0]
        dic = dict(counter)
        to_return = (NULL,NULL)
        index = 0
        for pair, key in sorted(dic.items()):
            if key == max_elements:
                if key > 1:
                    to_return = pair
                    index = key
                    break


        #print "pair: ", to_return, " index ", index
        if self._pair_equal(to_return , (NULL,NULL)):
            return to_return, True
        else:
            return to_return, False


        #return allPairs

    def _remove_repets(self, pairs):
        #print pairs
        repeated = []
        for i in xrange(0,len(pairs)):
            for j in xrange(i+1, len(pairs)):
                if self._pair_equal(pairs[i], pairs[j]):
                    if pairs[j] not in repeated:
                        repeated.append(pairs[j])

        #print repeated
        for j in repeated:
            pairs.remove(j)
        return pairs

    def _pair_equal(self, pair_to_compare, pair):
        if pair_to_compare[0] == pair[0]:
            if pair_to_compare[1] == pair[1]:
                return True
        return False


    def _max_matches(self, pairs_removed):
        #print pairs_removed
        dict_of_matches = defaultdict()
        for pair in pairs_removed:
            for j in xrange(0, len(self.matrix[0])):
                matches = self._find_matches(pair, self.matrix, j)
                #print matches
                if pair in dict_of_matches:
                    dict_of_matches[pair] = matches + dict_of_matches[pair]
                else:
                    dict_of_matches[pair] = matches

        to_return = (NULL,NULL)
        index = 1


        for pair in dict_of_matches:
            if dict_of_matches[pair] > index:
                to_return = pair
                index = dict_of_matches[pair]

        if self._pair_equal(to_return , (NULL,NULL)):
            return to_return, True
        else:
            return to_return, False

    def _find_matches(self, pair, matrix, j):
        matches = 0
        collumn = self._column(matrix, j)
        pairs = self._generate_pairs(collumn)
        #print "all pairs per collumn: " + str(pairs)
        for pair_to_compare in pairs:
            #print "Comparing = " + str(pair) + " == " + str(pair_to_compare)
            if self._pair_equal(pair_to_compare, pair):
                #print "it's equal"
                matches = matches + 1
        return matches


    def _change_pair(self, pair, matrix):
        name = self.variable
        self.m[name] = pair
        self._find_and_change(pair, matrix, name)
        self.variable +=1
        #print_matrix(matrix)
        return name, matrix


    def _find_and_change(self, pair, matrix, name):
        for j in xrange(0, len(matrix[0])):
                column = self._column(matrix, j)
                counter = 0
                temp = -1
                for i in xrange(0, len(column)):
                    if pair[0] == column[i]:
                        temp = i
                        counter = 1
                        break
                for h in xrange(0, len(column)):
                    if pair[1] == column[h] and counter > 0:
                        column[temp] = name
                        column[h] = NULL
                        break
                if column > 0:
                    self.matrix = self.put_column(column, matrix, j)

                #result = self._generate_pairs(column)
                #if pair in result:
                #    self.removePair(pair, name, j, matrix)


    def put_column(self, column, matrix, j):
        for i in xrange(0,len(matrix)):
            matrix[i][j] = column[i]

    #def _save_pair(self, pair, name):
        #print "Name : " + str(name) + " pair: " + str(pair)




    def _column(self, matrix, i):
        return [row[i] for row in matrix]

def print_matrix(matrix):
    for r in matrix:
       print ''.join(str(r))
    print '-------------------------------------------'
