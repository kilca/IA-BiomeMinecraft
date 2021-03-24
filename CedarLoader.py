#so i herd u liek cedar
from cedar.cedar import Cedar
from cedar.biomeData import get_biomeData
import pathlib
import sys
import numpy as np

def getJarPath():
    jarStringPath = str(pathlib.Path(__file__).parent.absolute())+r"\map\minecraft_server.1.12.2.jar"
    if not pathlib.Path(jarStringPath).exists():
        print("path to minecraft_server not found : ",jarStringPath)
        print("DO NOT FORGET TO ADD THE JAR IN MAP DIRECTORY")
        print("You can download the file here :")
        print("http://s3.amazonaws.com/Minecraft.Download/versions/1.12.2/minecraft_server.1.12.2.jar")
        sys.exit()
    return jarStringPath
        
def prepareMap(seed,path, verbosity, radius=100,center=None):
    config = {
        'center': center,
        'jar': path.encode('unicode_escape'),
        'output': 'seed_{seed}.png',
        'radius': radius,
        'resolution': 1,
        'seed': seed,
        'verbosity':verbosity
    }
    return Cedar(**config)


import json

def key_to_json(data):
    if data is None or isinstance(data, (bool, int, str)):
        return data
    if isinstance(data, (tuple, frozenset)):
        return str(data)
    raise TypeError

def to_json(data):
    if data is None or isinstance(data, (bool, int, tuple, range, str, list)):
        return data
    if isinstance(data, (set, frozenset)):
        return sorted(data)
    if isinstance(data, dict):
        return {key_to_json(key): to_json(data[key]) for key in data}
    raise TypeError

def write_file(mat):
    with open('coords.json', 'w') as f:
        json.dump(to_json(mat), f)


def loadDict():
    with open("coords.json", "rb") as file:
        return formatDict(json.load(file))
    
def formatDict(data):
    return dict((eval(k), v) for k, v in data.items()) 


#retourne coords dict
def prepareBiomeCoords(cedar):
    return cedar.prepareBiomeCoords()

    
def getBiome(coords,x,y):
    biomeConv = get_biomeData()
    biome = coords.get((x,y))
    if (biome):
        return (biomeConv.get(biome))
    else:
        return ""

def test():
    #We generate the map
    
    ced = prepareMap(7037624733059203544,getJarPath())
    #ced = prepareMap(-4448730549960990376,getJarPath())

    #We get all blocks coords biomes
    coords = prepareBiomeCoords(ced)

    #We get a dictionary that convert biome num id to biome string id
    biomeConv = get_biomeData()
    while 1:
        print("Please Enter position with space:x y")
        posInput = input().split()
        if (posInput == ['show']):
            for key, value in coords.items():
                print(key,",",value) 
        else:
            pos = (int(posInput[0]),int(posInput[1]))
            biome = coords.get(pos)
            if (biome):#! do not work with id 0 (considered false)
                print(biomeConv.get(biome))
            else:
                print("biome not found")

