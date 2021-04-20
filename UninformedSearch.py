"""

UninformedSearch.py

Created on Thu Oct  1 10:14:48 2020

@author: Christina Sarkisyan with directions from Sterling McLeod
        (for ease of typing, the author will be reffered to as 'chris' throughout)
        
Documentation key (for quick search):  
    -#provided: shows where code has been provided by another author (Sterling McLeod)     
        -#end of provided section: signals end of provided section
        -#changed: signals where a provided section was altered by the author
        - #temp : denotes a temporary solution or piece of code
        - #todo : denotes a place where something needs to be done
        
Contents: (this is technically not in order anymore)
    -import statements
    -Node class 
    -printGrid function  
    -Access Grid Coordinate Contents Function: getContents()  
    -Set Grid Coordinate Contents Function: setContents()    
    -isinList Function
    -uninformed search function 
    -Get Neighbors function
    -expandNode function 
    -Set Path function 
    -readGrid
    -outputGrid
    -Main function
        
"""
'''
import statements

'''
import queue
import copy

'''
Node class
    Parameters:
        -inParent: reference to a node object
            -the node that is creating this node
        -inValue: a 2-element list
            -should be the location of this node in the grid
            
''' 

class Node ():
    def __init__(self, inParent, inValue):
          self.value = inValue #the location of the value in the grid
          self.parent = inParent
    

        
'''
Print Grid Function
    Mostly for testing
    Parameters:
        -grid: the grid you want printed
        
'''
def printGrid (grid):
    print("%s\n%s\n%s\n" %(grid[0], grid[1], grid[2]))
    

'''
Access Grid Coordinate Contents Function: getContents()
    Parameters: 
        -grid: the grid you're looking in
        -point: a 1 dimensional, 2 element list containing coordinates
    Returns:
        -the conntents of the grid at that coordinate

'''    
def getContents (grid, point):
    return grid[point[0]][point[1]]

'''
Set Grid Coordinate Contents Function: setContents()
    Parameters: 
        -grid: the grid you're looking in
        -point: a 1 dimensional, 2 element list containing coordinates
    Returns:
        -the conntents of the grid at that coordinate

'''    
def setContents (grid, point, value):
    grid[point[0]][point[1]] = value

'''
isinList Function:
    checks if a node is in a list
    Parameters:
        -node: the node you're looking for
        -holder: queue or list you're looking in
        -isqueue: triggers the special stuff for if it's a queue in holder
    Returns: True or False
    
'''
def isinList(node, holder, isqueue):
    if isqueue == False:
        clist = holder
    else: 
        clist = []
        cq = copy._copy_immutable(queue)# so that you don't alter the actual queue
        while cq.Empty() == False:
            clist.append(cq.get()) #so that you can use a for loop
    for i in clist:      
       rownum = i.value[0]
       colnum = i.value[1]
       nrownum = node[0]
       ncolnum = node[1]
       
       if(rownum == nrownum and colnum == ncolnum):
           return True
    

        

'''
Get Neighbors function
    Create a function called getNeighbors that takes in a location and a grid:
    Parameters:
        -location: 1 dimension, 2 element list that describes a location
        -grid: the grid you're looking in
    Returns:
        -neighborArray: a list of positions (same format as location) that:
            - are left, right, up, or down of the location
            -their value is not 1
            -they are within the grid boundaries.
'''
def getNeighbors(location, grid):        
    neighborsArray = [] #holds the neighbors that fit the qualifications for being returned
    newLocations= [None, None, None, None] #holds the relative locations of the neighbors
    
    newLocations[0] = [location[0] + 1, location[1]]  #check right
    newLocations[1] = [location[0] - 1, location[1]]  #check left 
    newLocations[2] = [location[0], location[1] + 1]  #check up
    newLocations[3] = [location[0], location[1] - 1]  #check down
   
           
    cval = 0 #stores current location's grid element value
    for i in newLocations:
        
       cval = getContents(grid, i)
       if (cval != 1 and cval != None): #checks if the remaining neighbors are enter-able
           neighborsArray.append(i)          
    return neighborsArray




'''
expandNode function
    gets all the neighbors of the Node object passed in. 
    Adds those neighbors to the open list if and only if 
    the necessary conditions are passed.
    Parameters:
        -node: the node you're expanding
            -a Node type
        -grid: the grid you're in    
        -openList: fed in from the uninformed search
        -closedList: fed in from the uninformed search
        
        Henceforth this is documentation is from the instructor:

        Note: do not use the “in” operator to check if a Node object is in a list, 
        and do not use the == operator to compare two Node objects. 
        
        Remember that object variables are references so the == operator will return 
        false if the objects do not have the same memory address. The “in” operator 
        uses the == operator. My suggestion is to create a function to compare two 
        Node objects and/or create a function to check if a Node object is in a list 
        of Node objects.
'''
def expandNode(node, grid, openList, closedList, numExpanded):
    for i in getNeighbors(node.value, grid):
       if not (isinList(i, openList, True)) and not (isinList(i, closedList, False)):
           newN  = Node(node, i)
           openList.put(newN)
    return node    
'''
Set Path function:
    Used to find the final path once the goal is found and the final path must be obtained. 
    Parameters: 
        -current: the goal's node
        -path: a list holding only the root node. Gets filled in with the final path and eventualyy returned
    Returns:
        -path: filled path list
            -filled with locations
                                                                                              
        
'''
def setPath(curent, path):
    pathCost = 0;
    root = path[0]
    path.remove(root)
    while curent.value != root.value:
        path.append(curent.value)
        curent = curent.parent
        path.append(curent.value)
        pathCost += 1
    print("\nThe path is : (writen from bottom up)" )
    for i in path:
        print(i)
    print("the final path cost was: %d" %(pathCost))   


        
'''
Uninformed Search Function
    Parameters: 
        -grid: the grid environment for the search to use
            -input as an array of 1's and 0's
        -start: the array position where the agent should start its search for the goal
            -a coordinate [x,y] 
                -where x is the row number (up to down)
                 and y is the column number (left to right)
                     -ie: [1, 2]
                         |0 0 0 0 |                
                         |0 0 s 0 |        's' denotes the position of 'start'
                         |0 0 0 0 |
        -goal: the array position the agent should search for
            -a coordinate [x,y]
                -see 'start' for explaination of syntax for this argument
        -searchType: The type of search to be used (BFS or DFS)
            -a char:
                -'b' : BFS will be performed
                -'d' : DFS will be performed
                - anything else will print an error and assume you meant 'd'
            
'''

def uninformedSearch(grid, in_start, in_goal, searchType):    
    #initializes some variables:
    path = []
    num_nodes_expanded = 0
    openList= None #for holding stuff you need to eventualy expand
    closedList = [] #for holding stuff you've already expanded
    done = False #controls a loop
    curent = None #will hold the current node here
    fin_file = None
    fin_file_name ='path.txt'
    #casts start and goal to int here 
    start = [int(in_start[0]), int(in_start[1])]
    goal = [int(in_goal[0]), int(in_goal[1])]
    
    #sets start and goal in grid as 'S' ang 'G'
    setContents(grid, start, 'S')
    setContents(grid, goal, 'G')
    
    #initializing values:    
    if(searchType == 'b'):
        openList = queue.Queue(maxsize=0)
    else:
         openList = queue.LifoQueue(maxsize=0)        
         if (searchType != 'd'):
             print("Error: the parameter you've input for searchType is innacurate\nThe program will asume you meant 'd'")
    openList.put(Node(None, start))     
    path.append(Node(None, start))#used temporarily for setPath to have access to the root
     
    while done is False :
        if(openList.empty()):#checks if openList is empty
            print("There is no way to the goal from the given start position")
            done = True
        else:
            curent = openList.get()            
            if(curent.value[0] == goal[0] and curent.value[1] == goal[1] ):
                print("you found the goal!!!")
                setPath(curent, path)
                done = True
            else:
                closedList.append(expandNode(curent, grid, openList, closedList, num_nodes_expanded))
                num_nodes_expanded += 1
   
    print("\nThe number of nodes expanded was:\t%d" %(num_nodes_expanded))
    outputGrid(grid, start, goal, path)
        
    #returns from the conclusion of the function 
    fin_file = open(fin_file_name, "r")
    print("\nThis is a visual representation of that path: \n")
    for x in fin_file:
        print(x)
    fin_file.close()
    

'''
Reading and Writing functions

'''    
    
#provided by Sterling McLeod  (https://pastebin.com/S5yzfJPf)  
# Returns a 2D list of 1s and 0s
def readGrid(filename):
    grid = []
    with open(filename) as f:
        for l in f.readlines():
            grid.append([int(x) for x in l.split()])
    
    f.close()
    return grid
    #end of provided section

#provided by Sterling McLeod  (https://pastebin.com/S5yzfJPf)     
def outputGrid(grid, start, goal, path):
    filenameStr = 'path.txt'
 
    # Open filename
    f = open(filenameStr, 'w')
 
    # Mark the start and goal points
    grid[start[0]][start[1]] = 'S'
    grid[goal[0]][goal[1]] = 'G'
 
    # Mark intermediate points with *
    for i, p in enumerate(path):
        if i > 0 and i < len(path)-1:
            grid[p[0]][p[1]] = '*'
 
    # Write the grid to a file
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            
            # Don't add a ' ' at the end of a line
            if c < len(row)-1:
                f.write(str(col)+' ')
            else:
                f.write(str(col))
 
        # Don't add a '\n' after the last line
        if r < len(grid)-1:
            f.write("\n")
 
    # Close file
    f.close()    
    #end of provided section
    

'''
Main function
    Output:
        -The path in the file “path.txt” or print to console that no solution exists.
        -The path cost of the solution (printed as output)
        -The number of nodes expanded for the search (printed as output)

'''
def main():    
    #prompt user for .txt file to read for grid formation
    gridfile = input("Please input the name of the file you want to read for grid formation\n\t(don't forget to include '.txt' at the end)")
    
    #makes a grid from it
    grid = readGrid(gridfile)
    print("\n\nThis is the grid you've input:")
    printGrid(grid)
    
    #prompt user for start-point, goal, and searchtype
    start = [input("Please input the row number of the starting point for this grid (starts at 0)\n"), input("Please input the column number of the starting point for this grid (starts at 0)\n")]
    
    goal = [input("Please input the row number of the goal point for this grid (starts at 0)\n"), input("Please input the column number of the goal point for this grid (starts at 0)\n")]
    
    searchType = input("Please input the search type for this grid\n\t('b' for Breadth first search, 'd' for depth first search)")

    uninformedSearch(grid, start, goal, searchType)
    print("check your files for 'path.txt'")
main() #included for easier testing
    
