import sys                                         #needed for parameter input
import queue                                        #needed for traversing tree
from PIL import Image                                #needed to manipulate image

class CompNode:                                    #simple tree structure, by yours truly
    def __init__(self, parent, bound):
        self.parent = parent                         #reference to parent node (that has this node as a child)
        self.children = []                         #list of all the node's children (can be more than two since tree is not binary)
        self.boundaries = bound                    #stored data: boundaries for highlighting purposes

    def addChild(self, node):
        self.children.append(node)                   #add node to the list of children

def countTabs(string):                            #counts the amount of tabs, usually found in front of each xml file line, returns as integer
    count = 0
    for i in string:
        if i == '\t':
            count += 1
    return count

def countSpace(string):                            #counts the amount of spaces in front of xml file line (in case of lack of tabs), returns as integer
    count = 0
    for i in string[:string.find("<") +1]:
        if i == " ":
            count += 1
    return count

def getBounds(string):                            #takes xml file line and finds where the boundaries are stored, returned as string
    string = string.lstrip()
    start = string.find("bounds=") + 8            #finds first occurance of bounds=
    end = string.find('"', start)                 #finds end of string after the start of bounds (lengths of bounds vary)
    bounds = string[start:end]                    #slice and dice
    return bounds

xml = sys.argv[1]                                 #gets name of xml file from parameters
picture = sys.argv[2]                             #gets name of png file from parameters
root = None                                       #initialises tree as empty root

f = open(xml, "r")                                #opens xml file for reading

def parseXML(file, root):                        #converts xml file into tree
    prevSpace = -1                               #spaces of previous line, to be compared against current line
    curNode = None                               #current node before line was read
    prevNode = None                              #parent node to the current node
    for line in file:                            #going through every line in the file (ignoring the ones about hierarchy and xml header
        if line.startswith("\t"):                #if the line has tabs at the front
            spaces = countTabs(line)                   #we count them
            if line.lstrip().startswith("</node>"):    #if the line indicates a node end, we must go back in terms if tree height
                curNode = prevNode
                prevNode = curNode.parent
                prevSpace = spaces
            elif curNode == None and prevNode == None:    #if this is the first line, we need to establish the root node
                bounds = getBounds(line)
                node = CompNode(None, bounds)                #create a node with no parent
                root = node
                curNode = node
                prevSpace = spaces
            else:                                        #if none of the above, we start comparing spaces to see where the new node should go
                if spaces > prevSpace:                    #if there are more spaces now, the new node must be a child of the current node
                    bounds = getBounds(line)
                    node = CompNode(curNode, bounds)        #create a node with no the current node as their parent
                    prevNode = curNode
                    curNode = node
                    prevSpace = spaces
                    prevNode.addChild(curNode)
                elif spaces == prevSpace:                #if the spaces are equal to that of the previous line, the new node is a sibling to the current node and a child to the one that node's parent
                    bounds = getBounds(line)
                    node = CompNode(prevNode, bounds)    #create a node with no the current node's parent as their parent
                    prevNode.addChild(node)
                    curNode = node
                else:                                    #if the spaces are less than previous line, that means the new node is an aunt or uncle to the current node, and needs to be the child of the current node's grandfather
                    bounds = getBounds(line)
                    prevNode = prevNode.parent
                    node = CompNode(prevNode, bounds)      #create a node with no the current node's grandfather as their parent
                    prevNode.addChild(node)
                    curNode = node
                    prevSpace = spaces
        elif line.startswith(" "):
            spaces = countSpace(line)                  #we count them
            if line.lstrip().startswith("</node>"):    #if the line indicates a node end, we must go back in terms if tree height
                curNode = prevNode
                prevNode = curNode.parent
                prevSpace = spaces
            elif curNode == None and prevNode == None:    #if this is the first line, we need to establish the root node
                bounds = getBounds(line)
                node = CompNode(None, bounds)                 #create a node with no parent
                root = node
                curNode = node
                prevSpace = spaces
            else:                                          #if none of the above, we start comparing spaces to see where the new node should go
                if spaces > prevSpace:                        #if there are more spaces now, the new node must be a child of the current node
                    bounds = getBounds(line)
                    node = CompNode(curNode, bounds)            #create a node with no the current node as their parent
                    prevNode = curNode
                    curNode = node
                    prevSpace = spaces
                    prevNode.addChild(curNode)
                elif spaces == prevSpace:                   #if the spaces are equal to that of the previous line, the new node is a sibling to the current node and a child to the one that node's parent
                    bounds = getBounds(line)
                    node = CompNode(prevNode, bounds)        #create a node with no the current node's parent as their parent
                    prevNode.addChild(node)
                    curNode = node
                else:                                        #if the spaces are less than previous line, that means the new node is an aunt or uncle to the current node, and needs to be the child of the current node's grandfather
                    bounds = getBounds(line)
                    prevNode = prevNode.parent
                    node = CompNode(prevNode, bounds)         #create a node with no the current node's grandfather as their parent
                    prevNode.addChild(node)
                    curNode = node
                    prevSpace = spaces
    return root

root = parseXML(f, root)                          #make the tree from the file

q = queue.Queue()                                #make an empty queue to use to traverse the tree
q.put(root)                                    #start by putting the root node in

leaves = []                                #list to keep track of the leaf nodes

while not q.empty():                        #traverse through all the tree nodes using Breadth First Search
    node = q.get()                            #get the node at the top of the queue
    if len(node.children) == 0:                #if the node does not have children
        leaves.append(node)                    #it is a leaf node
    else:
        for i in node.children:                #if the node has children, add them to the queue
            q.put(i)

leafBounds = []                        #list to keep track of the leaf node bounds
for k in leaves:                            #parse the boundaries in the nodes (stored as strings) to a 2D list of integers
    b = k.boundaries                        #get the bounds from the node
    bound = []
    topLeft = [int(b[1:b.find(",")]), int(b[b.find(",") +1: b.find("]")])]                   #start after the first "[", to the first "," for the first int, then after the "," to the "]" for the second int
    bottomRight = [int(b[b.find("]") + 2:b.find(",", b.find("]") + 1)]), int(b[b.find(",", b.find("]") + 1) +1: b.find("]", b.find("]") + 1)])] #start after the first "]", to the first "," after the "]" for first int, then after the "," after the first "]" to the second "]" for the second int
    bound.append(topLeft)       #add them to the bounds
    bound.append(bottomRight)
    leafBounds.append(bound)    #add the bounds of the leaf node to a list of leaf node bounds

YELLOW = (241,231,64)            #highlight yellow, according to Google

img = Image.open(picture)        #open the image

pixels = img.load()                #make a matrix of pixel values from the image


for b in leafBounds:                 #for every leaf we need to highlight
    topLeft = b[0]                    
    bottomRight = b[1]

    for i in range(topLeft[0], bottomRight[0]):        #make a vertical line along the left side and the right side of the component
        pixels[i, topLeft[1]] = YELLOW
        pixels[i, topLeft[1] + 1] = YELLOW            #added to make the line thicker
        pixels[i, bottomRight[1]-1] = YELLOW
        pixels[i, bottomRight[1]-2] = YELLOW            #added to make the line thicker
    for j in range(topLeft[1], bottomRight[1]):        #make a horizontal line along the top and bottom of the component
        pixels[topLeft[0], j] = YELLOW
        pixels[topLeft[0] + 1, j] = YELLOW            #added to make the line thicker
        pixels[bottomRight[0] - 1, j] = YELLOW
        pixels[bottomRight[0] - 2, j] = YELLOW        #added to make the line thicker

img.save("output" + picture, format="png")            #saved the new file as "output" + picture name
