#-----------------------------------------------------------------------
#CommonFunc.py
#
#Helper functions for the launcher
#-----------------------------------------------------------------------
#Junk by people
from fs.osfs import OSFS
from fs import open_fs
import re #reeee
#My Junk
from SharedVar import * 

#Common variables
MapPath = LoadConfig(SECTION_LAUNCHER, "MapPath")  #Absolute Path to the Map

#Qt5 Filedialog returns a full path to the file
#This function mangles it and returns just the filename.
def GetFileFromPath(Path):

    #Debugging
    TEST = "/Home/Anyon/Fortress/pak0.pk3"
    TEST2 = "/Home/Anyon/Fortress/"
    
    #The Variables 
    StringArray = []
    DashCount = 0

    #Initalization Phase
    for Letters in Path:
        if Letters == "/":
            StringArray.append("")
            DashCount += 1

    #First Phase
    #FileDialog returns with a beginning dash, account for it.
    LoopCount1 = -1
    Stringy1 = ""
    for Letters in Path:

        if Letters != "/":
            Stringy1 += Letters
            StringArray[LoopCount1] = Stringy1

        if Letters == "/":
            Stringy1 = ""
            LoopCount1 += 1
            
    return (StringArray, LoopCount1)

#Function used to reconstruct a path
def GenNewPath(StringArray, Max):
    NewPath = "/"    
    Counter = 0
    
    if len(StringArray) < 1:
        return StringArray[0]
    
    
    for Dirs in StringArray:
        #Do not go over to the max.
        if Counter >= Max:
            break
        
        NewPath += Dirs + "/"
        Counter += 1
        
        
    return NewPath

#A function to figure out if the custom map is a pak or bsp type
def FindMapTypes():
    MapDirectory = open_fs(MapPath)
    CatchedFile = None
    Type = "Unknown"
    TypeFilter = ""
    
    #OwO scan my directory senpai
    for Files in MapDirectory.walk.files(filter=["*.bsp", "*.pak", "*.zip"]):
        CatchedFile = Files
        break
        
    #Looky look at the pretty letters
    Type = GetFileFromPath(CatchedFile)[0][1] 

    Reg1 = None
    Reg2 = None
    
    Reg1 = re.search('\.pak', Type)
    Reg2 = re.search('\.bsp', Type)
    
    if Reg1 is not None:
        Type = "PAK"
    elif Reg2 is not None:
        Type = "BSP"
        
    return Type
    
    
    
    
    
    
    
    







