'''
Created on 10 Sep 2014

@author: gustavo
'''

import xlsxwriter

class Xslxsaver(object):


	def create_work(self,exp):
		name = "Passo_a_passo"
		self.degree = exp[0]
		name = name + str(self.degree)
		name = name + ".xlsx"
		name = "" + name
		self.workbook = xlsxwriter.Workbook(name)

	def create_worksheet(self,exp):
		name = "degree_"
		self.degree = exp[0]
		for i in exp:
			name = name +  str(i) + "_"
		name = name + ".xlsx"
		name = "" + name
		self.workbook = xlsxwriter.Workbook(name)





	def save_matches(self, matches):
		worksheet = self.workbook.add_worksheet("matches")
		row = 0
		colum = 0
		for i in matches:
			colum = 1
			worksheet.write(row,colum, i)
			colum = 2
			for j in matches[i]:
				worksheet.write(row,colum, j)
				colum = colum+1
			row = row + 1


	def save_complete(self, matrix):
		worksheet = self.workbook.add_worksheet("complete")
		
		row = 0;
		for i in xrange(0, len(matrix)):
			print i 
			colum = 0
			for j in matrix[i]:
				if j == -1:
					worksheet.write(row, colum, '')
				else:
					worksheet.write(row, colum, j)
				colum += 1
			row += 1



	def save(self, matrix, name):
		worksheet = self.workbook.add_worksheet(name)
#		print self.degree
		for i in xrange(0,len(matrix)):
			row = matrix[i]
			h = 0
			for j in xrange(0,len(row)):
				if row[j] == -1:
					worksheet.write(i, h, '')
				else:
					worksheet.write(i, h, row[j])
				h += 1
				 



	def close(self):
		self.workbook.close()
