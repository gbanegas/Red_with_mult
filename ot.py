'''
Created on 06 Apr 2015

@author: gustavo
'''

import math
from collections import defaultdict, Counter, OrderedDict

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
        allPairs = OrderedDict()
        #allPairs = []
        #print matrix
        size = len(matrix[0])
        #print "Size : " + str(size)
        for i in xrange(0,size):
            result = self._generate_pairs(self._column(self.matrix,i))
            for pair in result:
                if pair in allPairs:
                    allPairs[pair] = allPairs[pair] + 1
                else:
                    allPairs[pair] = 1

        keys_ordered = sorted(allPairs.values(), reverse=True)

        to_return = (NULL,NULL)
        od = OrderedDict(sorted(allPairs.items()))


        index = 0
        for pair, key in od.iteritems():
            if key == keys_ordered[0]:
                if key > 1:
                    to_return = pair
                    index = key
                    break
        #print allPairs
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
                result = self._generate_pairs(column)
                if pair in result:
                    self.removePair(pair, name, j, matrix)

    def removePair(self, pair, name, j, matrix):
        #print "Pair to Remove" + str(pair) + " in column: " + str(j)
        column = self._column(matrix, j)
        #print "Column before: " + str(column)
        for i in xrange(0, len(column)):
            if column[i] == pair[0]:
                column[i] = name
                break
        for i in xrange(0, len(column)):
            if column[i] == pair[1]:
                column[i] = NULL
                break
        #print column
        self.matrix = self.putColumn(column, matrix, j)
        #self.printMatrix(matrix)

    def putColumn(self, column, matrix, j):
        for i in xrange(0,len(matrix)):
            matrix[i][j] = column[i]

    #def _save_pair(self, pair, name):
        #print "Name : " + str(name) + " pair: " + str(pair)


    def _generate_pairs(self, collumn):
        result = []
        for i in xrange(1, len(collumn)):
            if collumn[i] <> NULL :
                p1 = collumn[i]
                for j in xrange(i+1, len(collumn)):
                    p2 = collumn[j]
                    if p2 <> NULL :
                        if p1 > p2:
                            pair = (p2, p1)
                        else:
                            pair = (p1, p2)
                        result.append(pair)
        #print result
        return result

    def _column(self, matrix, i):
        return [row[i] for row in matrix]

def print_matrix(matrix):
    #for r in matrix:
    #   print ''.join(str(r))
    print '-------------------------------------------'
