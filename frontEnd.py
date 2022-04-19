#Author: Kyle Norland
#Date: 4/18/22
#Description: Front end for ECE 579 Project

import sys
import random

#Import required stuff
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget











#---------------------------------------
#--------PyQt set up stuff--------------
#---------------------------------------

#Create instance of QApplication
app = QApplication(sys.argv)

#Create root widget
root = QWidget()

#Adding title to window
root.setWindowTitle('Geeks App')

#Place text
root.move(60, 15)

#Display text
txt = QLabel('Welcome, Geek!', parent = root)
txt.move(60,15)


#-------------------------------------------
#--------------Classes for Home Objects-----
#Globals
FULL = 3

class Robot:
    def __init__(self, id):
        self.id = id
        self.position = 0      #-1, 0, 1
        self.holding_flag = False
        self.holding = []
        
    def restack(self):
        print("Restacking")
        
        
class Bottle:
    def __init__(self, type, capacity, fullness):
        self.type = type  #Glass or Plastic
        self.capacity = capacity   #4 or 6
        self.fullness = fullness #Up to capacity
        
class Stand:
    def __init__(self, type):
        self.type = type #Chilled or normal
        self.has_bottle = True
        self.bottle = None
        self.bottle_temperature = 30
        self.max_proper_temperature = 44
        self.min_proper_temperature = 40
        self.goal_temperature = 42
        self.on = True
        self.room_temperature = 70
        self.leak_probability = 0.05
        self.leaking = False
    
    def control_temperature(self):
        if self.type == "chilled":
            if self.bottle_temperature > self.max_proper_temperature:
                self.bottle_temperature -= 1
            if self.bottle_temperature < self.min_proper_temperature:
                self.bottle_temperature += 1

    def step(self):
        #Simulates gradual change in bottle temp
        if self.room_temperature > self.bottle_temperature:
            self.bottle_temperature += 0.5
        elif self.room_temperature < self.bottle_temperature:
            self.bottle_temperature -= 0.5
        
        #Run the thermostat
        control_temperature()
        
        #If bottle empty send command to dispatch
        
        #Generate leak randomly, then if leaking, send to dispatch
        seed(124323423)
        if random() > self.leak_probability:
            self.leaking = True
            #Send message to dispatch   

class Home:
    def __init__(self, id):
        self.id = id
        self.full_bottle_shelf = []
        self.empty_bottle_shelf = []
        self.floor = []
        self.water_column_fullness = []
        self.water_column_occupied = True
        
    #Properties
    def step(self):
        #A function to step time forward
        print("Time stepping")
        
    def render(self, root):
        #Renders self on PyQt
        print("Rendering")
        #Display text
        title = QLabel('I am home 1', parent = root)
        title.move(90,40) 
        
        

class Management_Unit:
    def __init__(self):
        self.id = 1
        
    def run_TSP(self):
        print("TSP")





#---------------------------
#----------Initialize Environment
#---------------------------
homeOne = Home(1)
print("HI")
homeOne.render(root)


#----------------------------
#---------PyQt Main Loop-----
#----------------------------
#Show gui
root.show()

#Run main loop
sys.exit(app.exec_())




