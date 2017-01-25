'''
Created on 06 Apr 2015

@author: gustavo
'''

import math
import threading
from counter import Counter
from collections import defaultdict, OrderedDict
import time
from xlsx import Xslxsaver

from thread_pairs import ThreadGeneratePairs



NULL = -1
class Ot(object):

    def optimize(self, matrix, degree, xls=None, debug=False):
        debug = True
        self.matrix = matrix
        self.m = defaultdict()
        self.variable = degree*degree
        self.columns_of_pair = {}
        is_break = False
        self.xls = xls
        self.frequency_counter = {}
        i = 0
        max_frequency = 0
        while (not is_break):
            print "Round : ", i
            pair, is_break, max_frequency = self._generate_all_pairs(self.matrix)
            if debug:
                self.xls.save(self.matrix, str(i))
            i += 1
            if is_break:
                break
            name, self.matrix = self._change_pair(pair, self.matrix)
            self.frequency_counter[name] = max_frequency
            print "--------------------------------------------------"

        return self.m, self.matrix, self.frequency_counter, self.columns_of_pair

    def sort(self, matrix):
        matrix = self.__remove__(matrix, -1, "")
        for i in xrange(0, len(matrix[0])):
            column = self._column(matrix, i)
            column.sort()
            #print column
            self.put_column(column, matrix, i)
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
        size = len(matrix[0])
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

        print "Size pairs: ", len(result)

        #time1 = time.time()
        counter = Counter(result)
        #time2 = time.time()
        #print 'Counter(result) function took %0.3f ms' % ((time2-time1)*1000.0)
        #time1 = time.time()

        max_elements = list(sorted(counter.values(),reverse=True))[0]
        print "Max occurence: ", max_elements
        dic = OrderedDict(sorted(counter.items(), reverse=True))
        keys =  [item[0] for item in dic.items() if item[1] == max_elements]
        sum_pairs = 99999999999

        #dict(counter)
        #time2 = time.time()
        #print 'dict(counter) function took %0.3f ms' % ((time2-time1)*1000.0)
        to_return = (NULL,NULL)
        #time1 = time.time()
        if max_elements > 1:
            for key in keys:
                if sum(key) < sum_pairs:
                    to_return = key

            #to_return = dic.keys()[dic.values().index(max_elements)]
        #print to_return
        #time.sleep(1100)
        #print "returning, ",  pair_t
        #for pair, key in sorted(dic.items(), reverse=True):
        #    if key == max_elements and key > 1:
        #        to_return = pair
        #        break
        #time2 = time.time()
        #print 'pair, key in function took %0.3f ms' % ((time2-time1)*1000.0)
        #print "returning, ",  to_return
        if self._pair_equal(to_return , (NULL,NULL)):
            return to_return, True, max_elements
        else:
            return to_return, False, max_elements


    def _remove_repets(self, pairs):
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
        dict_of_matches = defaultdict()
        for pair in pairs_removed:
            for j in xrange(0, len(self.matrix[0])):
                matches = self._find_matches(pair, self.matrix, j)
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
        time1 = time.time()
        self._find_and_change(pair, matrix, name)
        time2 = time.time()
        print '_find_and_change function took %0.3f ms' % ((time2-time1)*1000.0)
        self.variable +=1
        #print_matrix(matrix)
        return name, matrix


    def _find_and_change(self, pair, matrix, name):
        self.columns_of_pair[name] = []
        for j in xrange(0, len(matrix[0])):
                column = self._column(matrix, j)
                counter = 0
                temp = -1
                if pair[0] in column and pair[1] in column:
                    index = column.index(pair[0])
                    column.insert(index, name)
                    index = column.index(pair[1])
                    column.insert(index, NULL)
                    column.remove(pair[0])
                    column.remove(pair[1])
                    if self.columns_of_pair[name] <> None:
                        self.columns_of_pair[name].append(j)
                    else:
                        self.columns_of_pair[name] = [j]

                #print column
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
