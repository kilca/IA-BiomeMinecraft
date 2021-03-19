#so i herd u liek cedar
from cedar.cedar import Cedar
from cedar.biomeData import get_biomeData
import pathlib
import sys

def getJarPath():
    jarStringPath = str(pathlib.Path(__file__).parent.absolute())+"\map\minecraft_server.1.12.2.jar"
    if not pathlib.Path(jarStringPath).exists():
        print("path to minecraft_server not found : ",jarStringPath)
        print("DO NOT FORGET TO ADD THE JAR IN MAP DIRECTORY")
        print("You can download the file here :")
        print("http://s3.amazonaws.com/Minecraft.Download/versions/1.12.2/minecraft_server.1.12.2.jar")
        sys.exit()
    return jarStringPath
        
def prepareMap(seed,path):
    config = {
        'center': None,
        'jar': path.encode('unicode_escape'),
        'output': 'seed_{seed}.png',
        'radius': 100,
        'resolution': 1,
        'seed': seed,
        'verbosity':2
    }
    return Cedar(**config)

def prepareBiomeCoords(cedar):
    return cedar.prepareBiomeCoords()
    
def test():
    #We generate the map
    ced = prepareMap(-4448730549960990376,getJarPath())
    
    #We get all blocks coords biomes
    coords = prepareBiomeCoords(ced)
    
    #We get a dictionary that convert biome num id to biome string id
    biomeConv = get_biomeData()
    
    for key, value in coords.items() :
        print (key, biomeConv[value])

        
test()