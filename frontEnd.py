#Author: Kyle Norland
#Date: 4/18/22
#Description: Front end for ECE 579 Project

import sys
import random
random.seed(124323423)
from collections import deque
import time

#Import tsp
import tsp


#Import required stuff
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton
from PyQt5.QtCore import pyqtSlot


#---------------------------------------
#--------PyQt set up stuff--------------
#---------------------------------------
class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'ECE 579 Final Project'
        self.left = 300
        self.top = 200
        self.width = 1000
        self.height = 500
        self.num_steps = 0
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        
        #Display text
        self.txt = QLabel('Welcome, User!', self)
        self.txt.move(60,15)

        #Step Counter
        self.step_counter_label = QLabel("Steps", self)
        self.step_counter_label.move(50, 40)
        #step_counter_label.show()

        #Step Box
        self.step_counter_box = QLabel(str(0), self)
        self.step_counter_box.move(100, 40)
        self.step_counter_box.resize(30,20)


        #Run the TSP
        self.tsp_button = QPushButton('Run TSP', self)
        self.tsp_button.move(250, 20)
        self.tsp_button.clicked.connect(lambda: self.run_tsp())
        
        #One Step Button
        self.one_step_button = QPushButton('One Step', self)
        self.one_step_button.move(350, 20)
        self.one_step_button.clicked.connect(lambda: self.run_sim(1))

        #Step 10 at a time.
        self.multi_step_button = QPushButton('Multi Step', self)
        self.multi_step_button.move(450, 20)
        self.multi_step_button.clicked.connect(lambda: self.run_sim(10))
        

        
        
        self.show()
        
    @pyqtSlot()
    def run_sim(self, num_iter):
        print(num_iter)
        for i in range(0, num_iter):
            #Update the step count
            self.num_steps += 1
            self.step_counter_box.setText(str(self.num_steps))
            self.step_counter_box.adjustSize()
            self.step_counter_box.show()
            
            #Push step and render down to children
            dispatch.step()
            dispatch.render(ex)
    
    @pyqtSlot()    
    def run_tsp(self):
        print("Running TSP")
        tsp.run_tsp_algorithm()

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
        self.ms_text = "Messages: "
        self.bottle_types = ["glass", "plastic"]
        self.bottle_capacities = [4, 6]
        
        #Perform initial delivery (TSP has already been solved)
        self.initialDelivery()
        
        
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
        self.robot_type = "fixed"
    
    def initialDelivery(self):
        for i in range(0,3):
            type = random.choice(self.bottle_types)
            capacity = random.choice(self.bottle_capacities)
            self.full_bottle_shelf.appendleft({"type": type , "fullness": capacity, "capacity": capacity})
        
    def replenish(self):
        print("Replenishing house:", str(self.id))
        #Delete all bottles from the empty_bottles_stack
        self.empty_bottle_shelf = deque([])
        
        #Add two bottles to the floor
        for i in range(0,2):
            type = random.choice(self.bottle_types)
            capacity = random.choice(self.bottle_capacities)
            self.floor.appendleft({"type": type , "fullness": capacity, "capacity": capacity})
        
        
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
        
        if len(self.full_bottle_shelf) > 0:
            #Pick Up From Full Stack
            in_hand = self.full_bottle_shelf.pop()
            
            #Put Down on empty stack
            self.empty_bottle_shelf.append(in_hand)
        #else:
            #print("Nothing on full bottle shelf")
        
        #Pick up from floor
        in_hand = self.floor.pop()
        
        #Put down on full_stack
        self.full_bottle_shelf.append(in_hand)
        
        #Pick up from floor
        in_hand = self.floor.pop()
        
        #Put down on full stack
        self.full_bottle_shelf.append(in_hand)
        if len(self.empty_bottle_shelf) > 0:
            #Pick up from empty stack
            in_hand = self.empty_bottle_shelf.pop()
            
            #Put down on full stack
            self.full_bottle_shelf.append(in_hand)
        #else:
            #print("Empty Bottle Shelf is empty")
        
        #Now fully ordered by freshness
        
    def replace_bottle(self):
        print("Replacing")
        
        if len(self.full_bottle_shelf) >= 1 and len(self.empty_bottle_shelf) <= 2:
            #Pick up from stand
            in_hand = self.on_stand.pop()
            
            #Put Down on empty stack
            self.empty_bottle_shelf.append(in_hand)
            
            #Pick Up From Full Stack
            in_hand = self.full_bottle_shelf.pop() 
            
            #Put down on stand
            self.on_stand.append(in_hand)
        elif len(self.full_bottle_shelf) < 1:
            self.ms_text = self.ms_text + " empty!"
        else:
            self.ms_text = self.ms_text + " empty_stack full!"
            
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
        pre_fullness = self.on_stand[0]["fullness"]
        
        #Empty bottle a bit
        if len(self.on_stand) > 0:
            self.on_stand[0]["fullness"] -= self.daily_usage
            #Catch zero
            self.on_stand[0]["fullness"] = max(self.on_stand[0]["fullness"], 0)
            
            #Message if empty
            if self.on_stand[0]["fullness"] < 0.25 and len(self.full_bottle_shelf) <= 1:
                self.need_replenish = True
                self.parent.message_queue.appendleft({"message":"replenish", "house_id": self.id})
                self.ms_text = self.ms_text + " replenish! "
        
        
        #Generate leak randomly, then if leaking, send to dispatch
        random_leak_number = random.random()
        if random_leak_number < self.leak_probability:
            self.on_stand[0]["fullness"] -= (0.20 * self.daily_usage)
        
        post_fullness = self.on_stand[0]["fullness"]
        
        
        #If the leak has made the house use more than its usual daily usage, trigger the leaking signal.
        if pre_fullness - post_fullness > self.daily_usage:
            self.leaking = True
            self.parent.message_queue.appendleft({"message":"leaking", "house_id": self.id}) 
            self.ms_text = self.ms_text + " leaking! "
        
        
        #Replace bottle if empty
        if self.on_stand[0]["fullness"] <= 0.0:
            self.replace_bottle()
        
        
    def render(self, root):
        if(self.new):
        
            base_x = 50
            base_y = 40 + (self.id * 20)
            
            
            self.title = QLabel('I am home: ' + str(self.id), parent = ex)
            self.title.move(base_x, base_y) 
            self.title.show()
            self.new = False
            
            #Fullness
            self.fullness_label = QLabel("Fullness:", parent = ex)
            self.fullness_label.move(base_x + 100, base_y)
            self.fullness_label.show()
            
            #Full Bottles
            self.full_bottles_label = QLabel("Full Bottles:", parent = ex)
            self.full_bottles_label.move(base_x + 200, base_y)
            self.full_bottles_label.show()
            
            #Empty Bottles
            self.empty_bottles_label = QLabel("Empty Bottles:", parent = ex)
            self.empty_bottles_label.move(base_x + 300, base_y)
            self.empty_bottles_label.show()
            
            #Water Temperature
            self.bottle_temperature_label = QLabel("Bottle Temperature: ", parent = ex)
            self.bottle_temperature_label.move(base_x + 425, base_y)
            self.bottle_temperature_label.show()
            
            #Messages sent
            self.messages_sent_label = QLabel(self.ms_text, parent = ex)
            self.messages_sent_label.move(base_x + 600, base_y)
            self.messages_sent_label.show()
            print("The message text is: ", self.ms_text) 

        else:
            print("Mid update: ", self.ms_text)
            

            
            #Fullness
            self.fullness_label.setText("Fullness: " + str(round(self.on_stand[0]["fullness"], 2)) + " / " + str(self.on_stand[0]["capacity"]))
            self.fullness_label.adjustSize()
            
            #Full Bottles
            self.full_bottles_label.setText("Full Bottles: " + str(len(self.full_bottle_shelf)))
            self.full_bottles_label.adjustSize()
            
            #Empty Stack
            self.empty_bottles_label.setText("Empty Bottles: " + str(len(self.empty_bottle_shelf)))
            self.empty_bottles_label.adjustSize()
            
            #Messages
            self.bottle_temperature_label.setText("Bottle Temperature: " + str(self.bottle_temperature))
            self.bottle_temperature_label.adjustSize()
            
            #Messages
            self.messages_sent_label.setText(self.ms_text)
            self.messages_sent_label.adjustSize()
            

class Dispatch:
    def __init__(self):
        self.id = 1
        self.message_queue = deque([])
        self.homes = []
        self.num_employees = 8
       
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
                if len(self.message_queue) > 0:
                    message = self.message_queue.pop()
                    print("Message:" +  str(message))
                   
                    #Figure out which house messaged
                    for h in self.homes:
                        if str(h.id) == str(message['house_id']):
                            #Not a copy
                            house = h
                            
                            #Handle messages    
                            if message["message"] == "replenish":
                                print("Working with house: ", house.id)
                                house.need_replenish = False
                                house.replenish()
                                house.restack()
                            
                            if message["message"] == "leaking":
                                print("one is leaking")
                                house.leaking = False
                        
    def render(self, root):
        #Render all homes
        for home in self.homes:
            home.render(root)           
            
    def run_TSP(self):
        print("TSP")



#Run main loop

if __name__ == "__main__":
    #--------------------------------------------------
    #----------Tkinter Initial Interface for TSP-------
    #--------------------------------------------------
    
    '''
    #Tkinter window for the TSP
    import tkinter as tk
    tk_root = tk.Tk()
    tk_root.title("TSP Problem")
    tk_root.mainloop()
    '''
    #----------Initialize Environment
    #---------------------------

     #Create dispatch unit and houses
    dispatch = Dispatch()
    for i in range(1, 5):
        dispatch.homes.append(Home(i, dispatch, "chilled")) 
        
    #Create instance of QApplication and other objects
    app = QApplication(sys.argv)
    ex = App()    


    #Initial
    dispatch.render(ex)

    sys.exit(app.exec_())




