#-----------------------------------------------------------------------
#SharedVar.py
#
#A shared variable used by the launcher
#-----------------------------------------------------------------------
import os, sys
from configparser import ConfigParser

#Constants
SECTION_LAUNCHER = "Launcher"
SECTION_ENGINES = "Engine"
ENGINESINI = "Engines.ini"
CONFIGINI = "Config.ini"
   
#-----------------------------------------------------------------------
#Generic ini processor 
#-----------------------------------------------------------------------
def SaveData(File, Section, Var, Value):    
    Config = ConfigParser()
    Config.read(File)
    Section = str(Section)
    Var = str(Var)

    if Config.has_section(Section) == False:
        Config.add_section(Section)

    Config.set(Section, Var, Value)
    
    with open(File, "w") as File2:
        Config.write(File2)
        File2.flush()
        File2.close()
    

def LoadData(File, Section, Var):
    Config = ConfigParser()
    Config.read(File)
    Section = str(Section)
    Var = str(Var)

    if Config.has_section(Section) == False:
        print("Error: ", Section, " is not there")
        return

    Value = Config.get(Section, Var)
    
    return Value

#-----------------------------------------------------------------------
#Aliases
#-----------------------------------------------------------------------

#Config.ini
def SaveConfig(Section, Var, Value):
    SaveData("Config.ini", Section, Var, Value)

def LoadConfig(Section, Var):
    return LoadData("Config.ini", Section, Var) 

#Engines.ini
def SaveEngine(Section, Var, Value):
    SaveData("Engines.ini", Section, Var, Value)

def LoadEngine(Section, Var):
    return LoadData("Engines.ini", Section, Var) 


