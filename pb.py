# -*- coding:utf8 -*-
import numpy as  np

class PriceBlock(object):
	"""docstring for PriceBlock"""
	def __init__(self, inputfile):
		super(PriceBlock, self).__init__()
		self.infile=inputfile
		self.dArray=PriceBlock.__readfile(self)
		self.gArray=PriceBlock.__grad(self) #分级处理,类似于图像二值化。0~1万:0.5,1万~2万:1,2万~3万:2...类推
		self.gArray_ori=np.array(self.gArray) #保持不变

	def __readfile(self):
		nils=list()
		for line in open(self.infile):
			nil=line.split(',')[:-1] #drop the ''
			nil=map(lambda x:float(x),nil) #convert string to float
			nils+=nil
		return np.array(nils).reshape(4000,4000)
	##根据阈值对原始数据进行标记
	def __grad(self):
		def sobel(value):
			if value ==0:  return -1 #空值用-1表示
			elif value>0 and value<1:return 0.5 #低于一万
			elif value>=1 and value<2:return 1
			elif value>=2 and value<3:return 2
			elif value>=3 and value<4:return 3
			elif value>=4 and value<5:return 4
			elif value>=5 and value<6:return 5
			elif value>=6 and value<7:return 6
			elif value>=7 and value<8:return 7
			elif value>=8 and value<9:return 8
			elif value>=9 and value<10:return 9
			elif value>=10 and value<11:return 10
			elif value>=11 and value<12:return 11
			elif value>=12 and value<13:return 12
			elif value>=13 and value<14:return 13
			elif value>=14 and value<15:return 14
			elif value>=15 and value<16:return 15
			elif value>=16 and value<17:return 16
			elif value>=17 and value<18:return 17
			elif value>=18 and value<19:return 18
			elif value>=19 and value<20:return 19
			elif value>=20: return 20

		sobel_ufunc=np.frompyfunc(sobel,1,1)
		return sobel_ufunc(self.dArray) 
	def lianTong(self):
		#某种标记的点的个数
		#每种价格区间使用自己的编码计数，一万至两万区间使用100001,100002...类推
		#即 10×万+标记区域个数，之所以乘以10是因为网格容量 400*400 =160000，对于1万最多一万个编码可能不够
		dic_label_p =dict({'0.5':1})
		for i in range(1,20):
			dic_label_p[str(i)]=1
		for y in range(4000):
			print y
			for x in range(4000):
				if self.gArray[y][x]!=-1: #
					if y==0: #first row
						if x==0:#first col
							self.gArray[y][x]=self.gArray_ori[y][x]*100000+dic_label_p[str(self.gArray_ori[y][x])]
							dic_label_p[str(self.gArray_ori[y][x])]+=1
					#第一行，非第一列  
						else:
							if self.gArray_ori[y][x-1] == self.gArray_ori[y][x]:#跟左边相同  
								self.gArray[y][x] = self.gArray[y][x-1]
                   #否则，填充自增标记  
							else:
								self.gArray[y][x]=self.gArray_ori[y][x]*100000+dic_label_p[str(self.gArray_ori[y][x])]  
								dic_label_p[str(self.gArray_ori[y][x])]+=1
					else: #非第一行
						if x == 0: 
							#最左边  --->不可能出现衔接情况  
                            #/*分析上和右上*/  
                            #如果上方数据等于该数据，则该数据填充上方数据的标记  
							if self.gArray_ori[y - 1][x] == self.gArray_ori[y][x]:  
								self.gArray[y][x] = self.gArray[y-1][x]  
                            #如果右上方数据等于该数据，则该数据填充右上方数据的标记 
							elif self.gArray_ori[y-1][x+1] == self.gArray_ori[y][x]:  
								self.gArray[y][x] = self.gArray[y -1][x+1] 
                            #否则填充自增标记  
							else:
								self.gArray[y][x] =self.gArray_ori[y][x]*100000+dic_label_p[str(self.gArray_ori[y][x])]  
								dic_label_p[str(self.gArray_ori[y][x])]+=1   
						
						elif x == self.gArray.shape[1]-1: #最右边   --->不可能出现衔接情况  
                            #/*分析左上和上*/  
                            #如果左上数据等于该数据，则则该数据填充左上方数据的标记  
							if self.gArray_ori[y-1][x-1] == self.gArray_ori[y][x]:  
								self.gArray[y][x] = self.gArray[y - 1][x-1]  
                            #上方数据等于该数据，则该数据填充上方数据的标记  
							elif self.gArray_ori[y - 1][x] == self.gArray_ori[y][x]:
								self.gArray[y][x] = self.gArray[y - 1][x]  
                            #左上和上都不等
							else:  
                                #如果左侧数据等，则该数据填充左侧数据的标记  
								if self.gArray_ori[y][x-1] == self.gArray_ori[y][x]:  
									self.gArray[y][x] = self.gArray[y][x-1]   
                                #否则填充自增标记  
								else:
									self.gArray[y][x] =self.gArray_ori[y][x]*100000+dic_label_p[str(self.gArray_ori[y][x])]  
									dic_label_p[str(self.gArray_ori[y][x])]+=1
						else:#中间    --->可能出现衔接情况  
                            #/*分析左上、上和右上*/  
                            #上方数据等，直接填充上方标记  
							if self.gArray_ori[y-1][x] == self.gArray_ori[y][x]:  
								self.gArray[y][x] = self.gArray[y-1][x]
                            #上方数据不等 
							else: 
                                #左上和右上都等，填充左上标记  
								if self.gArray_ori[y-1][x-1] == self.gArray_ori[y][x] and self.gArray_ori[y-1][x+1] == self.gArray_ori[y][x]:  
									self.gArray[y][x] = self.gArray[y-1][x-1]
                                    #如果右上和左上数据标记不同，右上标记所在block需更改  
									if self.gArray[y-1][x-1] != self.gArray[y-1][x+1]:
										temp=np.array(self.gArray)
										for y_ in range(4000):
											for x_ in range(4000):
												if self.gArray[y_][x_]==temp[y-1][x+1]:
													self.gArray[y_][x_]=temp[y][x]
                                #左上不等，右上等  
								elif self.gArray_ori[y-1][x-1] != self.gArray_ori[y][x] and self.gArray_ori[y-1][x+1] == self.gArray_ori[y][x]:  
                                    #左侧等，则填充左侧标记  
									if self.gArray_ori[y][x-1] == self.gArray_ori[y][x]:
										self.gArray[y][x] = self.gArray[y][x-1]  
                                        #如果左侧和右上标记不同，则右上标记所在block需要更改  
										if self.gArray[y][x-1] != self.gArray[y-1][x+1]:
											temp=np.array(self.gArray)
											for y_ in range(4000):
												for x_ in range(4000):
													if self.gArray[y_][x_]==temp[y-1][x+1]:
														self.gArray[y_][x_]=temp[y][x]
                                    #左侧不等，则直接填充右上标记  
									else: 
										self.gArray[y][x] = self.gArray[y-1][x+1]  
                                
                                #左上等，右上不等，填充左上标记  
								elif self.gArray_ori[y-1][x-1] == self.gArray_ori[y][x] and self.gArray_ori[y-1][x+1] != self.gArray_ori[y][x]: 
									self.gArray[y][x] = self.gArray[y-1][x-1]  
                                #左上和右上都不等  
								elif self.gArray_ori[y-1][x-1] != self.gArray_ori[y][x] and self.gArray_ori[y-1][x+1] != self.gArray_ori[y][x]: 
                                    #如果左侧等，则填充左侧标记  
									if self.gArray_ori[y][x-1] == self.gArray_ori[y][x]:
										self.gArray[y][x] = self.gArray[y][x-1]  
                                    #否则填充自增标记  
									else:  
										self.gArray[y][x] =self.gArray_ori[y][x]*100000+dic_label_p[str(self.gArray_ori[y][x])]  
										dic_label_p[str(self.gArray_ori[y][x])]+=1
if __name__ == '__main__':
	obj=PriceBlock('ContourLine-2015-10.txt') #原始数据
	obj.lianTong()
	with open('resu_1010.csv','w') as fw:
		for y in range(4000):
			fw.write('\n')
			for x in range(4000):	
				fw.write(str(obj.gArray[y][x]))
				fw.write(',')
	# print obj.dArray[44][44]
