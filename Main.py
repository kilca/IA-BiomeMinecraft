from DataLoader import DataLoader
from DataTrainer import DataTrainer
from CedarLoader import *
import numpy as np

#si on souhaite reduire les donnes trop proches
#https://stackoverflow.com/questions/43035503/efficiently-delete-arrays-that-are-close-from-each-other-given-a-threshold-in-py
radius = 10000+10000

print("===== We prepare the map for Check ==========")
ced = prepareMap(-3212105572273177338,getJarPath(),2,500)
coords = prepareBiomeCoords(ced)
print("here are the coords")
print(coords)
write_file(coords)
'''
print("===== We load block data from database ==========")
dataL = DataLoader(r"map\tess.db",-10000,10000,-10000,10000)
dataL.load_data(100000,percent=80)

#dict idmat:string to id:string
d = dict([(y,x+1) for x,y in enumerate(sorted(set(dataL.MArr)))])
M = [d.get(e) for e in dataL.MArr]

#convert : [a,a] and [b,b] to [[a,b],[a,b]]
#apres vu tp : _c marche aussi
XZ = np.array(np.stack((dataL.XArr, dataL.ZArr, M), axis=1))
Y = [coords.get((x,z)) for x, z in zip(dataL.XArr, dataL.ZArr)]

#------------
print("===== We train the dataset ==========")
dataT = DataTrainer(XZ,Y)
dataT.train()
dataT.plot()
'''

