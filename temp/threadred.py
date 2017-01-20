import threading

NULL = -1
class ThreadRed(threading.Thread):


    def __init__(self,id, matrix, mdegree, exp, max_col, nr):
        threading.Thread.__init__(self)
        self.id = id
        self.matrix = []
        self.matrix.append(matrix)
        self.exp_sorted = exp
        self.mdegree = mdegree
        print "Starting thread id : ", self.id
        #print self.exp_sorted
        #self.exp_sorted.append(0)
        #print self.exp_sorted[0]
        self.nr = nr
        self.max_collum = max_col
        rowToWrite  = [-1 for x in xrange(self.max_collum)]
        self.matrix.append(rowToWrite)
        #print_matrix(self.matrix)



    def getMatrix(self):
        del self.matrix[0]
        #print "FINAL "
        #print_matrix(self.matrix)
        return self.matrix



    def run(self):

        for i in xrange(0,self.nr):
            to_reduce = self._need_to_reduce(self.matrix)
            for index in to_reduce:
                for e in self.exp_sorted:
                    reduceRow = self.reduce(self.matrix[index],e)
                    self.matrix.append(reduceRow)
                self._clean_reduced(self.matrix,index)
            print "Thread is alive : ", self.id

        self._remove_repeat(self.matrix)
        print "Finishing thread : ", self.id
        #self.matrix = self.clean(self.matrix)
        #print_matrix(self.matrix)

    def _remove_repeat(self, matrix):
        for j in range(1, len(matrix)):
            row = matrix[j]
            for i in range(self.mdegree-1, len(row)):
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

    def _clean_reduced(self, matrix, index):
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

    def _need_to_reduce(self, matrix):
        indexOfRows = []
        #print "Printing... ", self.matrix
        index = (self.max_collum - 1 - self.mdegree);
        for i in range(0,len(self.matrix)):
            row = self.matrix[i]
            if row[index] <> NULL:
                indexOfRows.append(i)

        return indexOfRows

    def clean(self, matrix):
        #print_matrix(matrix)
        toRemove = []
        for m in matrix:
            if self.isClean(m):
                toRemove.append(m)
        for i in toRemove:
            matrix.remove(i)
        return matrix

    def isClean(self, row):
        for i in row:
            if i <> NULL:
                return False
        return True

def print_matrix(matrix):
    print '----------------------------------------------'
    for r in matrix:
        print ''.join(str(r))
    print '----------------------FIM---------------------'
