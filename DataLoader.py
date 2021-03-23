import sqlite3 as sql
import time

import numpy as np
import matplotlib.pyplot as plt

import random

class DataLoader():
	def __init__(self,path,minX,maxX,minZ,maxZ):
		self.maxX = maxX
		self.minX = minX
		self.minZ = minZ
		self.maxZ = maxZ
		self.sourceDB = sql.connect(path)
		colorDict = {}
		colorDict['minecraft:dirt'] = 'brown'
		colorDict['minecraft:lava'] = 'red'
		colorDict['minecraft:sand'] = 'yellow'
		colorDict['minecraft:leaves'] = 'green'
		colorDict['minecraft:log'] =  'orange'
		colorDict['minecraft:sandstone'] = 'tan'
		colorDict['minecraft:grass'] = 'olive'
		colorDict['minecraft:snow'] = 'gray'
		colorDict['minecraft:water'] ='blue'
		colorDict['minecraft:long_grass'] ='darkgreen'
		colorDict['minecraft:cactus'] ='lime'
		self.colorDict = colorDict

	def plot_values(self):
		colors = [self.colorDict.get(e) for e in self.MArr]
		#cList = list(self.colorDict.keys())
		plt.scatter(self.XArr, self.ZArr,marker="s",s=2.0, color=colors,alpha=0.5)
		plt.xlabel('X position')
		plt.ylabel('Z position')
		#scatter.legend_elements()[0] 
		#print(scatter.legend_elements()[1])
		#plt.legend(cList, self.colorDict.keys())
		#plt.legend()
		plt.show()

	def load_data(self,nbrows,percent=100):
		print("Loading request")
		'''
		cursor = self.sourceDB.execute(f"SELECT C.id, C.user, C.action, cm.material, c.data, \
									C.X, C.Y, C.Z, C.time \
								FROM Event as C, Material as cm \
								WHERE c.material = cm.id \
								AND Cm.material IN \
								(\'minecraft:dirt\',\'minecraft:long_grass\',\'minecraft:sand\',\
								\'minecraft:leaves\',\'minecraft:log\',\'minecraft:sandstone\',\
								\'minecraft:grass\',\'minecraft:water\',\'minecraft:snow\',\
								\'minecraft:cactus\') \
								AND C.Y > 40 \
								AND C.X < {self.maxX}\
								AND C.X > {self.minX}\
								AND C.Z < {self.maxZ}\
									AND C.Z > {self.minZ}\
								LIMIT {nbrows}")
		'''
		cursor = self.sourceDB.execute(f"SELECT C.rowid, C.user, C.action, cm.material, c.data, \
									C.X, C.Y, C.Z, C.time \
								FROM co_block as C, co_material_map as cm \
								WHERE c.type = cm.id \
								AND Cm.material IN \
								(\'minecraft:dirt\',\'minecraft:long_grass\',\'minecraft:sand\',\
								\'minecraft:leaves\',\'minecraft:log\',\'minecraft:sandstone\',\
								\'minecraft:grass\',\'minecraft:water\',\'minecraft:snow\',\
								\'minecraft:cactus\') \
								AND C.Y > 40 \
								AND C.X < {self.maxX}\
								AND C.X > {self.minX}\
								AND C.Z < {self.maxZ}\
									AND C.Z > {self.minZ}\
								LIMIT {nbrows}")

		start = time.time()
		cursor.arraysize = 200000#size of array
		total = cursor.fetchmany()

		if not total:
			print("no data found")
			exit(0)

		if percent != 100:
			nb = int(len(total)*(percent/100))
			total = random.choices(total, k=nb)

		res = [list(ele) for ele in total] 
		res = np.array(res)
		self.MArr = res[:,3]
		self.XArr = res[:,5]
		self.ZArr = res[:,7]
		self.XArr = self.XArr.astype(np.float)
		self.ZArr = self.ZArr.astype(np.float)