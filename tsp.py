"""
    File: tsp.py
    Author: Teresa Pham
    Purpose: Implement the Branch and Bound algorithm to solve the traveling salesman problem
             for ThirstAID. The algorithm searches for the shortest path between the dispatcher
             and the 5 customers (a, b, c, d, and e). The path begins and ends at the dispatcher's
             location, and only visits each customer once.
"""

import tkinter as tk
from tkinter import *
from tkinter import messagebox

# GUI window
window = Tk()
window.title("ThirstAID TSP")
window.geometry("550x750")

# text of directions for user in the GUI
direction = Label(text = "Enter the corresponding distances.\nIf there is no path between two locations,"
                        + "\nenter 0 for the distance between them")
direction.grid(row = 0, column = 1, padx = 10, pady = 10)

# label texts in the GUI to prompt user for distances
in_sa = Label(text = "Distance between the Dispatcher and A")
in_sb = Label(text = "Distance between the Dispatcher and B")
in_sc = Label(text = "Distance between the Dispatcher and C")
in_sd = Label(text = "Distance between the Dispatcher and D")
in_se = Label(text = "Distance between the Dispatcher and E")
in_ab = Label(text = "Distance between A and B")
in_ac = Label(text = "Distance between A and C")
in_ad = Label(text = "Distance between A and D")
in_ae = Label(text = "Distance between A and E")
in_bc = Label(text = "Distance between B and C")
in_bd = Label(text = "Distance between B and D")
in_be = Label(text = "Distance between B and E")
in_cd = Label(text = "Distance between C and D")
in_ce = Label(text = "Distance between C and E")
in_de = Label(text = "Distance between D and E")

# position the label texts in the GUI
in_sa.grid(row = 1, column = 1, padx = 10, pady = 10)
in_sb.grid(row = 2, column = 1, padx = 10, pady = 10)
in_sc.grid(row = 3, column = 1, padx = 10, pady = 10)
in_sd.grid(row = 4, column = 1, padx = 10, pady = 10)
in_se.grid(row = 5, column = 1, padx = 10, pady = 10)
in_ab.grid(row = 6, column = 1, padx = 10, pady = 10)
in_ac.grid(row = 7, column = 1, padx = 10, pady = 10)
in_ad.grid(row = 8, column = 1, padx = 10, pady = 10)
in_ae.grid(row = 9, column = 1, padx = 10, pady = 10)
in_bc.grid(row = 10, column = 1, padx = 10, pady = 10)
in_bd.grid(row = 11, column = 1, padx = 10, pady = 10)
in_be.grid(row = 12, column = 1, padx = 10, pady = 10)
in_cd.grid(row = 13, column = 1, padx = 10, pady = 10)
in_ce.grid(row = 14, column = 1, padx = 10, pady = 10)
in_de.grid(row = 15, column = 1, padx = 10, pady = 10)

# input boxes to get user input for each distance
entrySA = Entry()
entrySB = Entry()
entrySC = Entry()
entrySD = Entry()
entrySE = Entry()
entryAB = Entry()
entryAC = Entry()
entryAD = Entry()
entryAE = Entry()
entryBC = Entry()
entryBD = Entry()
entryBE = Entry()
entryCD = Entry()
entryCE = Entry()
entryDE = Entry()

# position input boxes in the GUI
entrySA.grid(row = 1, column = 2)
entrySB.grid(row = 2, column = 2)
entrySC.grid(row = 3, column = 2)
entrySD.grid(row = 4, column = 2)
entrySE.grid(row = 5, column = 2)
entryAB.grid(row = 6, column = 2)
entryAC.grid(row = 7, column = 2)
entryAD.grid(row = 8, column = 2)
entryAE.grid(row = 9, column = 2)
entryBC.grid(row = 10, column = 2)
entryBD.grid(row = 11, column = 2)
entryBE.grid(row = 12, column = 2)
entryCD.grid(row = 13, column = 2)
entryCE.grid(row = 14, column = 2)
entryDE.grid(row = 15, column = 2)

class Node:
    """
        This class resprsents a Node (customer)

        The constructor builds a Node and must be passed a value for the
        Node's name and a list of Edges connected to that Node.

        The class defines several helpful methods and fields:
           getName():              - getter for the Node's name
           getEdges():             - getter for the list of the Node's Edges
    """

    def __init__(self, name, edges):
        """
            This function is the constructor for the Node Class, it initializes name and edges
            Arguments: name (string), edges (list of Edge objects)
            Return: None
        """
        self.name = name
        self.edges = edges

    def getName(self):
        """
            This function is the getter for a Node's name
            Arguments: None
            Return: string
        """
        return self.name

    def getEdges(self):
        """
            This function is the getter for a Node's Edges
            Arguments: None
            Return: list of Edge objects
        """
        return self.edges

class Edge:
    """
        This class resprsents an Edge (a connection between two customers)

        The constructor builds an Edge and must be passed a value for the
        Edge's name and distance.

        The class defines several helpful methods and fields:
           getName():                   - getter for the Edge's name
           getDistance():               - getter for the Edge's distance
    """

    def __init__(self, name, distance):
        """
            This function is the constructor for the Edge Class, it initializes name and distance
            Arguments: name (string), distance (positive number)
            Return: None
        """
        self.name = name
        self.distance = distance

    def getName(self):
        """
            This function is the getter for an Edge's name
            Arguments: None
            Return: string
        """
        return self.name

    def getDistance(self):
        """
            This function is the getter for an Edge's distance
            Arguments: None
            Return: float
        """
        return self.distance

def tsp(nodes):
    """
        This function uses the Branch and Bound algorithm to solve the traveling salesman problem
        for ThirstAID. The algorithm searches for the shortest path between the dispatcher
        and the 5 customers (a, b, c, d, and e). The path begins and ends at the dispatcher's
        location, and only visits each customer once.
        Arguments: list of Node objects
        Return: list of tuples (first element in the tuple is a string indicating the path, second
                element in the tuple is the float of the corresponding distance)
    """
    nodes_name = ['s', 'a', 'b', 'c', 'd', 'e'] # list of all customer names
    queue = [('S', 0)] # queue starts at dispatcher's node with a distance of 0

    while len(queue) != 0: # loop until queue is empty
        # if first element in queue is full path (reach goal), return
        if queue[0][0][0] == 'S' and queue[0][0][len(queue[0][0]) - 1] == 'S' and len(queue[0][0]) == 7:
            paths = [queue[0]]
            # checks if there are multiple full paths with the same distance
            for i in range(len(queue) - 1):
                # return all full paths with shortest distance
                if queue[i][1] == queue[i+1][1] and len(queue[i+1][0]) == 7:
                    paths.append(queue[i+1])
                else:
                    break
            return paths

        cur_node = queue[0]
        temp_queue = []
        to_remove = []
        for i in range(len(nodes_name)): # iterate through each node
            if nodes_name[i] == cur_node[0][len(queue[0][0])-1].lower(): # found node to expand on
                queue.remove(queue[0])
                # generate next paths based on the edges of the node to expand on
                # new paths are added to temp_queue
                for connections in nodes[i].getEdges():
                    if connections.getName()[0].lower() == nodes_name[i]:
                        temp_queue.append((cur_node[0] + connections.getName()[1], cur_node[1] + connections.getDistance()))
                    else:
                        temp_queue.append((cur_node[0] + connections.getName()[0], cur_node[1] + connections.getDistance()))
                # remove paths that loop
                # indicate looping paths in to_remove
                for new_node in temp_queue:
                    letters = []
                    for let in range(len(new_node[0])-1):
                        letters.append(new_node[0][let])
                    if new_node[0][len(new_node[0])-1] in letters:
                        if new_node[0][len(new_node[0])-1] != 'S':
                            to_remove.append(new_node)
                        else:
                            if len(letters) != 6:
                                to_remove.append(new_node)
                # remove looping paths from temp_queue before adding temp_queue to queue
                for node_remove in to_remove:
                    if node_remove in temp_queue:
                        temp_queue.remove(node_remove)
                # add paths in temp_queue to queue
                for new_node in temp_queue:
                    queue.append(new_node)
                break

        queue = sort_list(queue) # sort queue by shortest distance

def sort_list(list_in):
    """
        This function sorts a list of tuples by the second element in the tuple from smallest to largest.
        Arguments: list of tuples
        Return: sorted list of tuples
    """
    for i in range(len(list_in)):
        for j in range(len(list_in)-i-1):
        # iterate through sorted portion and insert current tuple where it belongs in the sorted list
            if (list_in[j][1] > list_in[j + 1][1]):
                temp = list_in[j]
                list_in[j]= list_in[j + 1]
                list_in[j + 1]= temp
    return list_in

def createNodesAndEdges(input):
    """
        This function creates all the Nodes and Edges based on the user input, and then calls the
        tsp function to get the shortest path.
        Arguments: input (list of string)
        Return: None
    """
    edgeNames = ["SA", "SB", "SC", "SD", "SE", "AB", "AC", "AD", "AE", "BC", "BD", "BE", "CD", "CE", "DE"]
    nodeNames = ["S", "A", "B", "C", "D", "E"]
    edges = []
    nodes = []

    # creates an Edge object if the distance of that Edge is greater than 0
    for i in range(len(input)):
        if float(input[i]) > 0:
            temp = Edge(edgeNames[i], float(input[i]))
            edges.append(temp)

    # creates all the nodes depending on which Edges each node contains
    for node in nodeNames:
        privateEdges = []
        for edge in edges: # edge is present in the Node
            if edge.getName()[0] == node or edge.getName()[1] == node:
                privateEdges.append(edge)
        temp = Node(node, privateEdges)
        nodes.append(temp)

    paths = tsp(nodes) # call the tsp function to find the shortest path
    if paths is None: # no full path was found
        messagebox.showerror(title = "Error", message = "No full path is possible")
    else: # full path was found, show info message indicating the shortest path and its distance
        out = ""
        for path in paths:
            out += f"Possible path: {path[0]}\nTotal Length is {path[1]}\n"
        messagebox.showinfo(title = "Possible Paths", message = out)

def main():
    # get value of user input
    sa = entrySA.get()
    sb = entrySB.get()
    sc = entrySC.get()
    sd = entrySD.get()
    se = entrySE.get()
    ab = entryAB.get()
    ac = entryAC.get()
    ad = entryAD.get()
    ae = entryAE.get()
    bc = entryBC.get()
    bd = entryBD.get()
    be = entryBE.get()
    cd = entryCD.get()
    ce = entryCE.get()
    de = entryDE.get()

    try: # verify that user input is a positive number or 0
        assert((float)(sa) >= 0)
        assert((float)(sb) >= 0)
        assert((float)(sc) >= 0)
        assert((float)(sd) >= 0)
        assert((float)(se) >= 0)
        assert((float)(ab) >= 0)
        assert((float)(ac) >= 0)
        assert((float)(ad) >= 0)
        assert((float)(ae) >= 0)
        assert((float)(bc) >= 0)
        assert((float)(bd) >= 0)
        assert((float)(be) >= 0)
        assert((float)(cd) >= 0)
        assert((float)(ce) >= 0)
        assert((float)(de) >= 0)
    except: # show error message if user input is not a positive number or 0
       messagebox.showerror(title = "Error", message = "Please only enter positive distances")

    createNodesAndEdges([sa, sb, sc, sd, se, ab, ac, ad, ae, bc, bd, be, cd, ce, de])

# create button in the GUI
button = Button(text = "Calculate Optimal Route", command = main)
button.grid(row = 16, column = 3, padx = 10, pady = 10)
