#-----------------------------------------------------------------------
#Quake Launcher v0.1
#Because no damn idiot makes one for fucking linux.
#
#-----------------------------------------------------------------------
#Imports, main load
import sys, atexit
from PySide2 import QtCore, QtWidgets, QtGui
#Imports, program
import LaunchGamePane
import EnginePane
from SharedVar import * 

VERSION = 0.1


#The main load
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)

        #The whole initalization
        self.window = QtWidgets.QWidget()
        self.layout = QtWidgets.QGridLayout()
        self.setCentralWidget(self.window)
        self.window.setLayout(self.layout)
  
        self.TabBar = QtWidgets.QTabBar()
        self.TabBarIcon = QtGui.QIcon()
        
        #Tab 1
        self.T0Widget1 = LaunchGamePane.Panel1()
        self.T0Widget2 = LaunchGamePane.Panel2()
        self.T0Widget3 = LaunchGamePane.Panel1B()

        #Tab 2
        self.T1Widget1 = EnginePane.EnginePane()
        
        #Tab 3
        
        #Properties
        self.TabBar.insertTab(0, self.TabBarIcon, "Game")
        # ~ self.TabBar.insertTab(1, self.TabBarIcon, "Configs")
        self.TabBar.insertTab(1, self.TabBarIcon, "Engine")        

        #Adding Widgets
        self.layout.addWidget(self.TabBar, 0, 0, 1, 5)

        #Signals
        self.TabBar.tabBarClicked.connect(self.TabClicked)
        
        self.Tab0()

    def ClearTab(self):
        #Tab0
        self.T0Widget1.hide()
        self.T0Widget2.hide()
        self.T0Widget3.hide()
        
        self.layout.removeWidget(self.T0Widget1)
        self.layout.removeWidget(self.T0Widget2)
        self.layout.removeWidget(self.T0Widget3)
 
        #Tab1
        self.T1Widget1.hide()
        
        self.layout.removeWidget(self.T1Widget1)

        
    @QtCore.Slot()
    def TabClicked(self, Index):
        self.ClearTab()
        
        if Index == 0:
            self.Tab0()
        elif Index == 1:
            self.Tab1()
        
    #First Tab
    def Tab0(self):

        self.layout.addWidget(self.T0Widget1, 1, 1)
        self.layout.addWidget(self.T0Widget2, 1, 2)
        self.layout.addWidget(self.T0Widget3, 2, 1)
        
        self.T0Widget2.Panel1 = self.T0Widget1
        self.T0Widget2.Panel1B = self.T0Widget3

        
        self.T0Widget1.show()
        self.T0Widget2.show()
        self.T0Widget3.show()
    
    #Second Tab
    def Tab1(self):
        self.layout.addWidget(self.T1Widget1, 1, 1)
        
        #Do some signal connection.
        self.T1Widget1.ParentNode = self
    
    
        self.T1Widget1.show()
        
        
    

#The program initalization
if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.setWindowTitle("Snek Quake Launcher " + str(VERSION))
    widget.resize(640, 320)
    widget.show()

    sys.exit(app.exec_())



