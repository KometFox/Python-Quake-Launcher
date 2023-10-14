#-----------------------------------------------------------------------
#MainWindow.py
#
#The first panel windowe of the launcher
#Shows the most important stuff that is needed for well a launcher
#to launch the game of course
#-----------------------------------------------------------------------
#Libraries
import os
import subprocess
from fs import open_fs
from fs.osfs import OSFS
from PySide2 import QtCore, QtWidgets, QtGui
#My shit
from SharedVar import *
from CommonFunc import * 

#Stuff for the Panels
IconPath = "Graphics/GameIcons"

Icons = [
        "Quake1_64.png"]

#The Variables to compose the launch command
GameDir = LoadConfig(SECTION_LAUNCHER, "GameDir") #Game Directory
GamePath = LoadConfig(SECTION_LAUNCHER, "GamePath") #Absolute Path to the Game
MapPath = LoadConfig(SECTION_LAUNCHER, "MapPath")  #Absolute Path to the Map
MapDir = LoadConfig(SECTION_LAUNCHER, "MapDir") #Directory name of the Map
ModPath = LoadConfig(SECTION_LAUNCHER, "ModPath") #Absolute path of the Mod
ModDir = LoadConfig(SECTION_LAUNCHER, "ModDir") #Mod Directory
LaunchCommand = LoadConfig(SECTION_LAUNCHER, "LaunchCommand") #The Launch Command


#Common Variables

#Source Port Engines
Engines = {}
SelEngines = ""

#Boy, keep track of the litter you just made. 
MapFilesArray = []



#-----------------------------------------------------------------------
#Functions for this Program
#-----------------------------------------------------------------------

#Just give the plain name of the file withouth no dashes.
def PlainFileName(Path):
    Array = GetFileFromPath(Path)[0]
    MaxArrayNum = GetFileFromPath(Path)[1]
    
    #o_o do some error checking
    if Array is None:
        return ""

    if len(Array) > 0:
        MaxArrayNum = MaxArrayNum
    else:
        MaxArrayNum = 0

    File = Array[MaxArrayNum]
    
    return File
    
#A function to create the environment so that the source ports
#can load all the custom maps.
def CreateMapEnvironment():
    global MapFilesArray
    # ~ MapType = FindMapTypes()
    FSMapDir = open_fs(MapPath)
    FSGameDir = open_fs(GamePath)
    ID1 = "/id1"

    #Time for a walky uuuu
    #First Phase
    for Cooper in FSMapDir.walk.dirs():
        for Kyna in FSGameDir.walk.dirs():
            
            #First make sure the folder exist.
            try:
                # ~ if String != String:
                    # ~ print("(・ω・) made a {} folder at {} just for you.".format(Cooper, ID1 + Cooper))
                os.mkdir(GamePath + ID1 + Cooper)
                break
            except FileExistsError:
                pass                    
            
    #Second Phase
    for Mirabel in FSMapDir.walk.files(filter=["*.*"]):
        Target = MapPath + Mirabel
        Dest = GamePath + ID1 + Mirabel
        
        #Add it to the list of arrays for clean up purpose.
        # ~ print("(^‿^) I am keeping track of these files: {}".format(Dest))
        MapFilesArray.append(Dest)
        
        try:
            os.symlink(Target, Dest, False)
        except:
            pass       


#Create Game Environment
def LaunchDaGame():
    #Some error checking
    if len(SelEngines) == 0:
        ErrorMsg = QtWidgets.QMessageBox()
        ErrorMsg.setIcon(QtWidgets.QMessageBox.Critical)
        ErrorMsg.setWindowTitle("A error occured.")
        ErrorMsg.setInformativeText("Error: looks like there is no Source Port to play with! ¯\_(ツ)_/¯")
        ErrorMsg.exec_()
    
        print("The Selected Engines variable is empty! No engine to start with!")
        return
    if len(GamePath) == 0:
        ErrorMsg = QtWidgets.QMessageBox()
        ErrorMsg.setIcon(QtWidgets.QMessageBox.Critical)
        ErrorMsg.setWindowTitle("A error occured.")
        ErrorMsg.setInformativeText("Error: There is no game path specified to start the game with! ¯\_(ツ)_/¯")
        ErrorMsg.exec_()
    
        print("There is no game path directory to create a game with! Aborting.")
        return
    
        

    #Needed to make sure to load the custom maps correctly.
    if MapPath != "":
        CreateMapEnvironment()


    Dir = "./Quake"
    Game = "-Quake"
    EngineRunning = False
        
    if ModDir != "":
        Game = "-game " + ModDir

    #The Symbolic Links
    GameLink = Engines[SelEngines] + "/" + GameDir
    
    if ModDir: 
        ModLink = GamePath + "/" + ModDir
    else:
        ModLink = ""
    
    MapLink = ""
     
    #TODO: Handle Symlink error more gracefully
    try:
        os.symlink(GamePath, GameLink, True)
    except FileExistsError:
        pass
        
    if ModDir != "":
        try:
            os.symlink(ModPath, ModLink,  True)
        except FileExistsError:
            pass
        
  
    #The full path to the source port file
    Arg1 = Engines[SelEngines] + "/" + SelEngines
    Arg2 = Game
    Arg3 = "-basedir ./Quake"

    Command = str(Arg1 + " " + Arg2 + " " + Arg3)

    #Run the geimu
    Process = subprocess.run([Command], cwd = Engines[SelEngines], shell = True)
    
    #Clean up the stinky mess, uh oh!
    print("Already done with playing? Time to clean up the mess hehe (´・ω・)")
   
    if Process.returncode >= 0:    
        if GameLink != "":
            os.unlink(GameLink)
        if ModLink != "":
            os.unlink(ModLink)

    
    for Items in MapFilesArray:
        #Error checking
        if os.path.lexists(Items):
            os.remove(Items)


#-----------------------------------------------------------------------
#The GUI
#-----------------------------------------------------------------------
#Panel 1
class Panel1(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Layout = QtWidgets.QGridLayout()
        self.setLayout(self.Layout)
        
        #Widgets
        self.Label = QtWidgets.QLabel()
        self.Engine = QtWidgets.QPushButton()
        self.EngineMenu = QtWidgets.QMenu()
        self.LIcon = QtWidgets.QLabel()
        self.PMapIcon = QtGui.QPixmap(IconPath + "/" + Icons[0])
        #Vars
        self.EngineMenu_Actions = []        
        
        #Set properties
        self.Label.setText("Engine")
        #self.Label.alignment = QtCore.Qt.AlignCenter
        
        self.Engine.setMenu(self.EngineMenu)
        self.Engine.setText("Select a Engine")

        self.LIcon.setPixmap(self.PMapIcon)
        
        #Do initalization stuff >)
        self.InitEngines()
        
        #Add it bruh
        self.Layout.addWidget(self.Label, 0, 0, 1, 3)
        self.Layout.addWidget(self.LIcon, 1, 0, 1, 2)
        self.Layout.addWidget(self.Engine, 2, 0, 1, 2)
        
        #Ding a ding connect em
        self.EngineMenu.triggered.connect(self.EngineSelect)
        self.Engine.pressed.connect(self.InitEngines)

        
    @QtCore.Slot()
    #Initalize the previously selected Engine.
    def InitEngines(self):
        global SelEngines
        global Engines
    
        #Load previously selected Engine
        SelEngines = LoadConfig(SECTION_LAUNCHER, "Engine")
        Engines[SelEngines] = LoadConfig(SECTION_LAUNCHER, "EnginePath")

        ActionMan = QtWidgets.QAction(SelEngines, self)
        
        #Add it to the menu.
        self.EngineMenu_Actions.append(ActionMan)
        self.EngineMenu.addAction(ActionMan)       
        self.EngineMenu.setDefaultAction(ActionMan)
        self.Engine.setText(SelEngines)


        self.Config = ConfigParser()
        self.Config.read(ENGINESINI)
                
        self.Sections = self.Config.sections()
        
        for Stuff in self.Sections:
            self.Name = self.Config[Stuff]["Name"]
            self.Path = self.Config[Stuff]["Path"]        
        
            Engines[self.Name] = self.Path

        #This method is needed to prevent duplication, shit. 
        #No clue how to do it better, tbh. 
        if len(self.EngineMenu_Actions) >= 0:
            for Stuff in self.EngineMenu_Actions:
                self.EngineMenu.removeAction(Stuff)


        for Stuff in Engines:
            ActionMan = QtWidgets.QAction(Stuff, self)
            
            #Dont add empty entries.
            if len(ActionMan.text()) > 0:
                self.EngineMenu_Actions.append(ActionMan)
                self.EngineMenu.addAction(ActionMan)
        
        self.Engine.setText(SelEngines)


    def EngineSelect(self, sel):
        global SelEngines
    
        self.InitEngines()
  
        SelEngines = sel.text()
        self.Engine.setText(sel.text())
        
        #Save to Config
        SaveConfig(SECTION_LAUNCHER, "Engine", SelEngines)
        SaveConfig(SECTION_LAUNCHER, "EnginePath", Engines[SelEngines])

    #Reinit the config values
    def Reinit(self):
        global SelEngines
        global Engines
        
        self.Engine.setText(SelEngines) 
        self.InitEngines()




class Panel2(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.Layout = QtWidgets.QGridLayout()
        self.setLayout(self.Layout)
        
        self.Panel1B = None
        self.Panel1 = None
        

        #The Widgets
        self.Label = QtWidgets.QLabel()
        self.LaunchButton = QtWidgets.QPushButton()
        self.SaveConfigButton = QtWidgets.QPushButton()
        self.LoadConfigButton = QtWidgets.QPushButton()
        
        #Properties
        self.Label.setText("Launch Game")
        self.LaunchButton.setText("Start Game")
        self.SaveConfigButton.setText("Save Config")
        self.LoadConfigButton.setText("Load Config")
        
        self.Layout.addWidget(self.Label, 0, 0, 1, 2) 
        self.Layout.addWidget(self.SaveConfigButton, 1, 0, 1, 1)
        self.Layout.addWidget(self.LoadConfigButton, 2, 0, 1, 1)
        self.Layout.addWidget(self.LaunchButton, 3, 0, 1, 1)
        
        #Connections
        self.LaunchButton.pressed.connect(self.LaunchGame)
        self.SaveConfigButton.pressed.connect(self.SaveConfigFile)
        self.LoadConfigButton.pressed.connect(self.LoadConfigFile)
        
    @QtCore.Slot()
    def LaunchGame(self):
        
        #Do some error checking first baby UwU
        if SelEngines is not None and Engines is not None:
            LaunchDaGame()
        else:
            print("Error: looks like there is no Source Port to play with! ¯\_(ツ)_/¯") 
            
            ErrorMsg = QtWidgets.QMessageBox()
            ErrorMsg.setIcon(QtWidgets.QMessageBox.Critical)
            ErrorMsg.setWindowTitle("A error occured!")
            ErrorMsg.setInformativeText("Error: Looks like there is no Source Port to play with! ¯\_(ツ)_/¯")
            ErrorMsg.exec_()
            
            
    @QtCore.Slot()
    def SaveConfigFile(self):
        
        FileDialog = QtWidgets.QFileDialog()
        ConfigFile = None
        
        #Configurate the Filedialog first
        FileDialog.Option(QtWidgets.QFileDialog.DontResolveSymlinks)
        FileDialog.setDefaultSuffix(".ini")
        FileDialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        
        #Set the path of the File
        ConfigFile = FileDialog.getSaveFileName(self, 
                                                "Save Launcher Configuration", 
                                                "./", 
                                                "Config File (*.ini)") 
        
        with open(ConfigFile[0], "w") as File:
            #C'mon bruh why so many globals?
            global GamePath
            global GameDir
            global MapPath
            global MapDir
            global ModPath
            global ModDir
            global SelEngines
            global Engines 
        
            File.write("[Launcher] \n")
            File.write("gamepath = " + GamePath + "\n")
            File.write("gamedir = " + GameDir + "\n")
            File.write("mappath = " + MapPath + "\n")
            File.write("mapdir = " + MapDir + "\n")
            File.write("modpath = " + ModPath + "\n")
            File.write("moddir = " + ModDir + "\n")
            File.write("engine = " + SelEngines + "\n")
            File.write("enginepath = " + Engines[SelEngines] + "\n")
            
            #Done with the stuff
            File.flush()
            File.close()
        
    def LoadConfigFile(self):
        FileDialog = QtWidgets.QFileDialog()
        ConfigFile = None
            
        FileDialog.Option(QtWidgets.QFileDialog.ShowDirsOnly)
        FileDialog.Option(QtWidgets.QFileDialog.ReadOnly)
        FileDialog.Option(QtWidgets.QFileDialog.DontResolveSymlinks)

        ConfigFile = FileDialog.getOpenFileName(self, 
                                                "Open ini File", 
                                                "./",
                                                "Config File (*.ini)")

        #Do some error checking
        if len(ConfigFile[0]) > 0:
            global GamePath
            global GameDir
            global MapPath
            global MapDir
            global ModPath
            global ModDir
            global SelEngines
            global Engines 
        
            #Read the config file
            Config = ConfigParser()
            Config.read(ConfigFile[0])

            #Set the variables
            GamePath = Config.get("Launcher", "GamePath")
            GameDir = Config.get("Launcher", "GameDir")
            MapPath = Config.get("Launcher", "MapPath")
            MapDir = Config.get("Launcher", "MapDir")
            ModPath = Config.get("Launcher", "ModPath")
            ModDir = Config.get("Launcher", "ModDir")
            SelEngines = Config.get("Launcher", "Engine")
            Engines[SelEngines] = Config.get("Launcher", "EnginePath")
            
            SaveConfig(SECTION_LAUNCHER, "GamePath", GamePath)
            SaveConfig(SECTION_LAUNCHER, "GameDir", GameDir)
            SaveConfig(SECTION_LAUNCHER, "MapPath", MapPath)
            SaveConfig(SECTION_LAUNCHER, "MapDir", MapDir)
            SaveConfig(SECTION_LAUNCHER, "ModPath", ModPath)
            SaveConfig(SECTION_LAUNCHER, "ModDir", ModDir)
            SaveConfig(SECTION_LAUNCHER, "Engine", SelEngines)
            SaveConfig(SECTION_LAUNCHER, "EnginePath", Engines[SelEngines])
    
            #Reinitalize the values
            self.Panel1B.Reinit()
            self.Panel1.Reinit()
            
        


class Panel1B(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.Layout = QtWidgets.QGridLayout()
        self.setLayout(self.Layout)
        
        #Widgets
        #Labels
        self.TopLabel = QtWidgets.QLabel()
        self.GameLabel = QtWidgets.QLabel()
        self.MapLabel = QtWidgets.QLabel()
        self.ModLabel = QtWidgets.QLabel()
        #Pushy Buttons
        self.Game = QtWidgets.QPushButton()
        self.Map = QtWidgets.QPushButton()
        self.Mod = QtWidgets.QPushButton()
        #Clear Button
        self.ClearGame = QtWidgets.QPushButton()
        self.ClearMap = QtWidgets.QPushButton()
        self.ClearMod = QtWidgets.QPushButton()
        
        #Set Properites
        #Labels
        self.TopLabel.setText("Files to load:")
        self.GameLabel.setText("[Load Game]")
        self.ModLabel.setText("[Load Mod]")
        self.MapLabel.setText("[Load Map]")
        
        #Push buttons
        self.Game.setText(GameDir)
        self.Map.setText(MapDir)
        self.Mod.setText(ModDir)
        self.ClearGame.setText("Clear")
        self.ClearMap.setText("Clear")
        self.ClearMod.setText("Clear")
        

        #The layout
        #Labels
        self.Layout.addWidget(self.TopLabel, 1, 0, 1, 2)
        self.Layout.addWidget(self.GameLabel, 2, 0, 1, 2)
        self.Layout.addWidget(self.MapLabel, 3, 0, 1, 2)
        self.Layout.addWidget(self.ModLabel, 4, 0, 1, 2)
    
        #Buttons
        self.Layout.addWidget(self.Game, 2, 2, 1, 2)
        self.Layout.addWidget(self.Map, 3, 2, 1, 2)
        self.Layout.addWidget(self.Mod, 4, 2, 1, 2)

        self.Layout.addWidget(self.ClearGame, 2, 4, 1, 1)
        self.Layout.addWidget(self.ClearMap, 3, 4, 1, 1)
        self.Layout.addWidget(self.ClearMod, 4, 4, 1, 1)

        
        #Connectiong me baby, UwU
        self.Game.pressed.connect(self.GetGame)
        self.Map.pressed.connect(self.GetMap)
        self.Mod.pressed.connect(self.GetMod)
        
        self.ClearGame.pressed.connect(self.DefClearGame)
        self.ClearMap.pressed.connect(self.DefClearMap)
        self.ClearMod.pressed.connect(self.DefClearMod)
   
    #Reinit the values from loaded config
    def Reinit(self):
        self.Game.setText(GameDir)
        self.Map.setText(MapDir)
        self.Mod.setText(ModDir)
    

    @QtCore.Slot()
    def GetGame(self):
        self.Directory = ""
        
        self.FileDialog = QtWidgets.QFileDialog()
        self.FileDialog.Option(QtWidgets.QFileDialog.ShowDirsOnly)
        self.FileDialog.Option(QtWidgets.QFileDialog.ReadOnly)
        self.FileDialog.Option(QtWidgets.QFileDialog.DontResolveSymlinks)

        self.Directory = self.FileDialog.getExistingDirectory(self, 
            ("Open Quake Folder"), "./")
        
        
        if self.Directory != "":
            global GamePath
            global GameDir
            
            TheFileArray = GetFileFromPath(self.Directory)[0]
            TheFileMax = GetFileFromPath(self.Directory)[1]            
            GamePath = self.Directory
            GameDir = TheFileArray[TheFileMax]
            
            SaveConfig(SECTION_LAUNCHER, "GamePath", GamePath)
            SaveConfig(SECTION_LAUNCHER, "GameDIr", GameDir)

            self.Game.setText(GameDir)
               
        
    @QtCore.Slot()
    def GetMap(self):
        self.Directory = None
        
        self.FileDialog = QtWidgets.QFileDialog()
        
        self.FileDialog.Option(QtWidgets.QFileDialog.ShowDirsOnly)
        self.FileDialog.Option(QtWidgets.QFileDialog.ReadOnly)
        self.FileDialog.Option(QtWidgets.QFileDialog.DontResolveSymlinks)

        self.Directory = self.FileDialog.getExistingDirectory(self, 
            ("Open Quake Map Directory"), "./")

        if self.Directory != "":
            global MapPath
            global MapDir
            global MapFile
                     
            TheFileArray = GetFileFromPath(self.Directory)[0]
            TheFileMax = GetFileFromPath(self.Directory)[1]
  
            MapPath = self.Directory
            MapFile = ""
            MapDir = TheFileArray[TheFileMax]

            SaveConfig(SECTION_LAUNCHER, "MapPath", MapPath)
            SaveConfig(SECTION_LAUNCHER, "MapFile", MapFile)
            SaveConfig(SECTION_LAUNCHER, "MapDir", MapDir)
 
            self.Map.setText(MapDir)


 
    @QtCore.Slot()
    def GetMod(self):
        self.Directory = None
        
        self.FileDialog = QtWidgets.QFileDialog()
        
        self.FileDialog.Option(QtWidgets.QFileDialog.ShowDirsOnly)
        self.FileDialog.Option(QtWidgets.QFileDialog.ReadOnly)
        self.FileDialog.Option(QtWidgets.QFileDialog.DontResolveSymlinks)

        self.Directory = self.FileDialog.getExistingDirectory(self, 
            ("Open Quake Mod Directory"), "./")
        
        if self.Directory != "":            
            global ModDir
            global ModPath
            global ModFile
            
            TheFileArray = GetFileFromPath(self.Directory)[0]
            TheFileMax = GetFileFromPath(self.Directory)[1]
            ModPath = self.Directory
            ModFile = ""
            ModDir = TheFileArray[TheFileMax]
            
            SaveConfig(SECTION_LAUNCHER, "ModDir", ModDir)
            SaveConfig(SECTION_LAUNCHER, "ModPath", ModPath)
            SaveConfig(SECTION_LAUNCHER, "ModFile", ModFile)

            self.Mod.setText(ModDir)
        
    @QtCore.Slot()
    def DefClearGame(self):
        global GamePath
        global GameDir 
            
        GamePath = ""
        GameDir = ""
            
        self.Game.setText("")
        
        #Clear the Config of it too
        SaveConfig(SECTION_LAUNCHER, "GamePath", "")
        SaveConfig(SECTION_LAUNCHER, "GameDir", "")
        
            
    @QtCore.Slot()
    def DefClearMap(self):
        global MapPath
        global MapDir
        global MapFile 
            
        MapPath = ""
        MapDir = ""
        MapFile = ""
            
        self.Map.setText("")

        #Clear the Config of it too
        SaveConfig(SECTION_LAUNCHER, "MapPath", "")
        SaveConfig(SECTION_LAUNCHER, "MapDir", "")
        SaveConfig(SECTION_LAUNCHER, "MapFile", "")
        


    @QtCore.Slot()
    def DefClearMod(self):
        global ModPath
        global ModDir
        global ModFile
            
        ModPath = ""
        ModDir = ""
        ModFile = ""
            
        self.Mod.setText("")
        
        #Clear the Config of it too
        SaveConfig(SECTION_LAUNCHER, "ModPath", "")
        SaveConfig(SECTION_LAUNCHER, "ModDir", "")
        SaveConfig(SECTION_LAUNCHER, "ModFile", "")         
            
        
