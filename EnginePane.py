#-----------------------------------------------------------------------
#EnginePane.py
#
#The third pane of the launcher
#Used to setup the engines and their path to launch the game with.
#
#-----------------------------------------------------------------------
import os
from PySide2 import QtCore, QtWidgets, QtGui
from SharedVar import *
from CommonFunc import *

#Common Variables
Engines = {}

#-----------------------------------------------------------------------
#Functions
#-----------------------------------------------------------------------



#Contains list of Engines
class EnginePane(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Layout = QtWidgets.QGridLayout()
        self.setLayout(self.Layout)
        self.ParentNode = None        


        #---------------------------------------------------------------
        #Left Panel
        #---------------------------------------------------------------
        #Widgets
        self.List = QtWidgets.QListView()
        self.Model = QtGui.QStandardItemModel()
        self.AddButton = QtWidgets.QPushButton()
        self.RemoveButton = QtWidgets.QPushButton()

        
        #Vars
        
        #Properties
        self.AddButton.setText("Add Custom")
        self.RemoveButton.setText("Remove")
        
        self.List.setModel(self.Model)

        
        #Add It bruh        
        self.Layout.addWidget(self.List, 1, 0, 10, 2)
        # ~ self.Layout.addWidget(self.AddButton, 11, 0, 2, 1)
        self.Layout.addWidget(self.RemoveButton, 11, 0, 2, 1)
        
        #Signals
        self.AddButton.pressed.connect(self.AddEngines)
        self.RemoveButton.pressed.connect(self.RemoveEngines)

        #---------------------------------------------------------------
        #Right Panel
        #---------------------------------------------------------------
        #Widgets
        self.Label1 = QtWidgets.QLabel()
        self.Label2 = QtWidgets.QLabel()
        self.Label3 = QtWidgets.QLabel()
        self.NameText = QtWidgets.QLineEdit()
        self.PathText = QtWidgets.QLineEdit()
        self.OkButton = QtWidgets.QPushButton()
        self.GetEngine = QtWidgets.QPushButton()
        
        #Properties
        self.OkButton.setText("Confirm")
        self.GetEngine.setText("Browse")
        self.Label1.setText("[Engine Properties]")
        self.Label2.setText("Name: ")
        self.Label3.setText("Path: ")
        
        self.InitEngines()
        
        self.GetEngine.pressed.connect(self.BrowseEngine)      
        self.OkButton.pressed.connect(self.AddEngines)
        
        #Add it bruh
        self.Layout.addWidget(self.NameText, 4, 3, 1, 1)
        self.Layout.addWidget(self.PathText, 5, 3, 1, 1)
        self.Layout.addWidget(self.OkButton, 4, 4, 1, 1)
        self.Layout.addWidget(self.GetEngine, 5, 4, 1, 1)
        self.Layout.addWidget(self.Label1, 3, 2, 1, 4)
        self.Layout.addWidget(self.Label2, 4, 2, 1, 1)
        self.Layout.addWidget(self.Label3, 5, 2, 1, 1)
        
        
        
    #Load Engines to the list model widget OwO
    def InitEngines(self):
        global Engines
        
        self.Config = ConfigParser()
        self.Config.read(ENGINESINI)
                
        self.Sections = self.Config.sections()
        
        for Stuff in self.Sections:
            Name = self.Config[Stuff]["Name"]
            Path = self.Config[Stuff]["Path"]
        
            Engines[Name] = Path
            
            Item = QtGui.QStandardItem(Name)
            self.Model.appendRow(Item)
            
        self.RefreshEngine()
        

        
    #Add Engines to the list model widget awww, more little puppies
    def AddEngines(self):
        global Engines

        #awww little puppies
        self.Puppy = self.NameText.text()
        self.PuppySection = SECTION_ENGINES + "_" + self.Puppy

        
        #Dont add empty entries to the engines list.
        if len(self.Puppy) == 0:
            return
        
        
        Engines[self.Puppy] = self.PathText.text()
        
        #Save to the confy file uuuooo                
        SaveEngine(self.PuppySection, "Name" , self.NameText.text())
        SaveEngine(self.PuppySection, "Path", self.PathText.text())    
        
        #Load it inside the Model. 
        Item = QtGui.QStandardItem(self.Puppy)
        self.Model.appendRow(Item)
        
        self.RefreshEngine()
            
    def RemoveEngines(self):
        #Get the sick puppy
        Puppy = self.List.currentIndex()
              
        if Puppy.row() == -1:
            #Clean up the currently used engines.
            
            SaveData = (CONFIGINI, "Launcher", "Engine", "")
            SaveData = (CONFIGINI, "Launcher", "EnginePath", "")
            
            #Refresh it.
            self.RefreshEngine()
        
            #Do not do further processing.
            return        
        
        PuppyRow = Puppy.row()
        PuppySectionID = str(SECTION_ENGINES + "_" + Puppy.data())
                
        #Get the configuration of the engine ini
        Config = ConfigParser()
        Config.read(ENGINESINI)
        
        Sections = self.Config.sections()

        #Bring the puppy on a place for sick animals
        #You're missed, puppy ;_;
        self.Model.removeRow(PuppyRow)
        Config.remove_section(PuppySectionID)
        
        with open(ENGINESINI, "w") as File:
            Config.write(File)
            File.flush()
            File.close()
            
        self.RefreshEngine()
    
    #A signal function.
    def RefreshEngine(self):
        if self.ParentNode is not None:
            self.ParentNode.T0Widget1.InitEngines()
    
        
    def BrowseEngine(self):
        self.Path = None
        
        #Widgets
        self.Browser = QtWidgets.QFileDialog()

        #Properties
        self.Browser.setReadOnly(True)
        self.Browser.setMimeTypeFilters("application/x-executable")
        self.Path = self.Browser.getOpenFileName(self, 
            ("Open Quake Engine"), "./")

        if self.Path[0] != None and \
        self.Path[0]:
            self.ArrayMax = GetFileFromPath(self.Path[0])[1]
            self.Name = GetFileFromPath(self.Path[0])[0][self.ArrayMax]
    
            #Some ugly mistakes has been made here, ow.
            DaPath = GetFileFromPath(self.Path[0])[0]
            DaPath.pop()
            NewPath = ""
            
            for Items in DaPath:
                NewPath += "/" + Items
                        
            self.NameText.setText(self.Name)
            self.PathText.setText(NewPath)

        
















