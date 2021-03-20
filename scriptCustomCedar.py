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

#retourne coords dict
def prepareBiomeCoords(cedar):
    return cedar.prepareBiomeCoords()

    
def getBiome(coords,x,y):
    biomeConv = get_biomeData()
    biome = coords.get(pos)
    if (biome):
        return (biomeConv.get(biome))
    else:
        return ""
    
def test():
    #We generate the map
    ced = prepareMap(7037624733059203544,getJarPath())
    
    #We get all blocks coords biomes
    coords = prepareBiomeCoords(ced)
    
    #We get a dictionary that convert biome num id to biome string id
    biomeConv = get_biomeData()
    while 1:
        print("Please Enter position with space:x y")
        posInput = input().split()
        pos = (int(posInput[0]),int(posInput[1]))
        biome = coords.get(pos)
        if (biome):
            print(biomeConv.get(biome))
        else:
            print("biome not found")
        
test()
