##Description##
This is a Python based launcher for Quake 1. Inspired by Rocket Launcher 2 for Doom source ports. 
This launcher has been tested mainly on Linux/XUbuntu. 

The launcher handles Quake 1 custom maps, mods and source ports differently. It does not follow the standard procedure
of installing Quake 1 source ports, mods and maps but instead it creates symbolic link to the respective path in order
to keep the Quake 1 installation base tidy. 

And yes it does work fine, I tested the launcher with FTE quake and it was possible to load custom maps, mods and the source port
withouth cluttering the Quake 1 installation base. FTE Quake handled everything fine and that is all done through symbolic links.

The launcher will remove the symbolic links as soon the game closes 

This software is considered Alpha and there may be some hidden bugs which could impact negatively on your experience, 
so use it on your own risk. 



##Dependencies <LINUX>##
It requires these libraries:

Operating System (Ubuntu):
python3 
pip3

it can be installed with sudo apt install

then with pip3 installed run this command.
pip3 install pyqt5
pip3 install fs

##Dependencies <WINDOWS>##
TODO.


##How to Run <LINUX>##
Just start Python Quake Launcher.bash

##License##
GNU GPL v3. See LICENSE.txt for more info.