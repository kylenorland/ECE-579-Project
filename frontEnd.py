#Author: Kyle Norland
#Date: 4/18/22
#Description: Front end for ECE 579 Project

import sys
import random
from collections import deque
import time


#Import required stuff
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget, QLineEdit



#---------------------------------------
#--------PyQt set up stuff--------------
#---------------------------------------

#Create instance of QApplication
app = QApplication(sys.argv)

#Create root widget
root = QWidget()
root.setGeometry(300,200,1000,500)
#root.resize(500, 500)

#Adding title to window
root.setWindowTitle('ECE 579 Final Project')

#Place text
#root.move(60, 15)

#Display text
txt = QLabel('Welcome, User!', parent = root)
txt.move(60,15)

#Step Counter
step_counter_label = QLabel("Steps", parent = root)
step_counter_label.move(50, 40)
#step_counter_label.show()

#Step Box
step_counter_box = QLabel(str(5), parent = root)
step_counter_box.move(100, 40)
step_counter_box.resize(30,20)


#-------------------------------------------
#--------------Classes for Home Objects-----
#Globals
FULL = 3

class Home:
    def __init__(self, id, parent, stand_type):
        self.id = id
        self.parent = parent
        self.on_stand = [{"type": "glass", "fullness": 4, "capacity": 4}]
        self.full_bottle_shelf = deque([])
        self.empty_bottle_shelf = deque([])
        self.floor = deque([])
        self.water_column_fullness = []
        self.water_column_occupied = True
        self.new = True
        self.ms_text = ""
        
        #Stand Info
        self.stand_type = stand_type #Chilled or normal
        self.bottle_temperature = 30
        self.max_proper_temperature = 44
        self.min_proper_temperature = 40
        self.goal_temperature = 42
        self.on = True
        self.room_temperature = 70
        self.leak_probability = 0.3
        self.leaking = False
        self.need_replenish = False
        self.daily_usage = 0.5
        
        #Robot Info
        self.r_position = 0      #-1, 0, 1
        self.r_holding_flag = False
        self.r_holding = []
        
        
    def control_temperature(self):
        if self.stand_type == "chilled":
            if self.bottle_temperature > self.max_proper_temperature:
                self.bottle_temperature -= 1
            if self.bottle_temperature < self.min_proper_temperature:
                self.bottle_temperature += 1  
    
    def print_stacks(self):
        print("Full_stack")
        for entry in self.full_stack: print(entry)
        
        print("Empty_stack")
        for entry in self.empty_stack: print(entry)
        
        print("Floor")
        for entry in self.floor: print(entry)
    
    
    def restack(self):
        print("Restacking")
        #Restacking occurs when the delivery comes.
        #Start state is bottle on stand, 1 on full stack, 2 on floor
        #
        #Pick Up From Full Stack
        in_hand = self.full_stack.pop()
        
        #Put Down on empty stack
        self.empty_stack.append(in_hand)
        
        #Pick up from floor
        in_hand = self.floor.pop()
        
        #Put down on full_stack
        self.full_stack.append(in_hand)
        
        #Pick up from floor
        in_hand = self.floor.pop()
        
        #Put down on full stack
        self.full_stack.append(in_hand)
        
        #Pick up from empty stack
        in_hand = self.empty_stack.pop()
        
        #Put down on full stack
        full_stack.append(in_hand)
        
        #Now fully ordered by freshness
        
        
        
    #Sub-Operations
    def stack(self):
        
    def unstack(self):
    
    def put_down(self):
    
    def pick_up(self):
        
    #Properties
    def step(self):
        #A function to step time forward
        print("House: ", self.id, " stepping")
        
        #Reset some variables
        self.ms_text = "Messages: "
        
        
        #-------------Bottle Temperature-----------------
        #Update bottle temperature
        if self.room_temperature > self.bottle_temperature:
            self.bottle_temperature += 0.5
        elif self.room_temperature < self.bottle_temperature:
            self.bottle_temperature -= 0.5
        
        #Run the thermostat
        self.control_temperature()
        
        
        #------------Bottle Fullness---------------------
        #Empty bottle a bit
        if len(self.on_stand) > 0:
            self.on_stand[0]["fullness"] -= self.daily_usage
            #Catch zero
            self.on_stand[0]["fullness"] = max(self.on_stand[0]["fullness"], 0)
            
            #Message if empty
            if self.on_stand[0]["fullness"] < 0.25 and len(self.full_bottle_shelf) <= 1:
                self.need_replenish = True
                self.parent.message_queue.appendleft({"message":"Replenish", "house_id": self.id})
                self.ms_text = self.ms_text + " replenish! "
        
        #Generate leak randomly, then if leaking, send to dispatch
        random.seed(124323423)
        if random.random() < self.leak_probability:
            self.leaking = True
            self.parent.message_queue.appendleft({"message":"Alarm", "house_id": self.id}) 
            self.ms_text = self.ms_text + " leaking! "
        
    def render(self, root):
        if(self.new):
        
            base_x = 50
            base_y = 40 + (self.id * 20)
            
            title = QLabel('I am home: ' + str(self.id), parent = root)
            title.move(base_x, base_y) 
            title.show()
            self.new = False
            
            #Messages sent
            self.messages_sent_label = QLabel("hi", parent = root)
            self.messages_sent_label.move(base_x + 400, base_y)
            self.messages_sent_label.show()
            print("The message text is: ", self.ms_text)   


            #Fullness
            self.fullness_label = QLabel("Fullness:", parent = root)
            self.fullness_label.move(base_x + 80, base_y)
            self.fullness_label.show()
            
            #Full Bottles
            self.full_bottles_label = QLabel("Full Bottles:", parent = root)
            self.full_bottles_label.move(base_x + 200, base_y)
            self.full_bottles_label.show()
            
            #Empty Bottles
            self.empty_bottles_label = QLabel("Empty Bottles:", parent = root)
            self.empty_bottles_label.move(base_x + 300, base_y)
            self.empty_bottles_label.show()

        else:
            print("Mid update: ", self.ms_text)
            
            #Messages
            self.messages_sent_label.setText(self.ms_text)
            self.messages_sent_label.adjustSize()
            
            #Fullness
            self.fullness_label.setText("Fullness: " + str(self.on_stand[0]["fullness"]) + " / " + str(self.on_stand[0]["capacity"]))
            self.fullness_label.adjustSize()
            
            #Full Bottles
            self.full_bottles_label.setText("Full Bottles: " + str(len(self.full_bottle_shelf)))
            self.full_bottles_label.adjustSize()
            
            #Empty Stack
            self.empty_bottles_label.setText("Empty Bottles: " + str(len(self.empty_bottle_shelf)))
            self.empty_bottles_label.adjustSize()
            
            

class Dispatch:
    def __init__(self):
        self.id = 1
        self.message_queue = deque([])
        self.homes = []
        self.num_employees = 1
       
    def step(self):
        #Step children
        print("Stepping")
        for home in self.homes:
            home.step()
            
        #Check messages
        #Handle one house per employee per step
        print("Checking Messages")
        if len(self.message_queue) > 0:
            for i in range(0, self.num_employees):
                message = self.message_queue.pop()
                print("Message")
                print(message["message"])
               
                #Figure out which house messaged
                for h in self.homes:
                    if h.id == message['house_id']:
                        #Not a copy
                        house = h
                        
                    #Handle messages    
                    if message["message"] == "replenish":
                        house.need_replenish = False
                    
                    if message["message"] == "leaking":
                        house.leaking = False
                        
    def render(self, root):
        #Render all homes
        for home in self.homes:
            home.render(root)                
                    
                    
                        
        

            
    def run_TSP(self):
        print("TSP")





#---------------------------
#----------Initialize Environment
#---------------------------
#Create management unit
dispatch = Dispatch()
for i in range(1, 5):
    dispatch.homes.append(Home(i, dispatch, "chilled"))

#Initial
dispatch.render(root)

#----------------------------
#---------PyQt Main Loop-----
#----------------------------
#Show gui
root.show()

num_steps = 10

for i in range(1, num_steps+1):
    #Update the step count
    step_counter_box.setText(str(i))
    #step_counter_box.show()
    
    #Push step and render down to children
    dispatch.step()
    dispatch.render(root)
    
    #Process events
    app.processEvents()
    #Sleep for a bit
    time.sleep(0.25)


#Run main loop
sys.exit(app.exec_())




