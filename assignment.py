import sys
import queue
from PIL import Image

class CompNode:
    def __init__(self, parent, bound):
        self.parent = parent
        self.children = []
        self.boundaries = bound

    def addChild(self, node):
        self.children.append(node)
    def getChildren():
        return children

def countSpace(string):
    count = 0
    for i in string:
        if i == '\t':
            count += 1
    return count

def getBounds(string):
    string = string.lstrip()
    bounds = string[14: string.index("checkable") - 2]
    return bounds

xml = sys.argv[1]
picture = sys.argv[2]

root = None

f = open(xml, "r")


def parseXML(file, root):
    prevSpace = -1
    curNode = None
    prevNode = None
    for line in file:
        if line.startswith("\t"):
            spaces = countSpace(line)
            if line.lstrip().startswith("</node>"):
                curNode = prevNode
                prevNode = curNode.parent
                prevSpace = spaces
            elif curNode == None and prevNode == None:
                bounds = getBounds(line)
                node = CompNode(None, bounds)
                root = node
                curNode = node
                prevSpace = spaces
            else:
                if spaces > prevSpace:
                    bounds = getBounds(line)
                    node = CompNode(curNode, bounds)
                    prevNode = curNode
                    curNode = node
                    prevSpace = spaces
                    prevNode.addChild(curNode)
                elif spaces == prevSpace:
                    bounds = getBounds(line)
                    node = CompNode(prevNode, bounds)
                    prevNode.addChild(node)
                    curNode = node
                else:
                    bounds = getBounds(line)
                    prevNode = prevNode.parent
                    node = CompNode(prevNode, bounds)
                    prevNode.addChild(node)
                    curNode = node
                    prevSpace = spaces
    return root

root = parseXML(f, root)

q = queue.Queue()
q.put(root)

leaves = []

while not q.empty():
    node = q.get()
    if len(node.children) == 0:
        leaves.append(node)
    else:
        for i in node.children:
            q.put(i)


leafBounds = []
for k in leaves:
    b = k.boundaries
    bound = []
    topLeft = [int(b[1:b.find(",")]), int(b[b.find(",") +1: b.find("]")])]
    bottomRight = [int(b[b.find("]") + 2:b.find(",", b.find("]") + 1)]), int(b[b.find(",", b.find("]") + 1) +1: b.find("]", b.find("]") + 1)])]
    bound.append(topLeft)
    bound.append(bottomRight)
    leafBounds.append(bound)

YELLOW = (255,255,0)

img = Image.open(picture)

pixels = img.load()


for b in leafBounds:
    topLeft = b[0]
    bottomRight = b[1]
    for i in range(topLeft[0], bottomRight[0]):
        pixels[i, topLeft[1]] = YELLOW
        pixels[i, bottomRight[1]-1] = YELLOW
    for j in range(topLeft[1], bottomRight[1]):
        pixels[topLeft[0], j] = YELLOW
        pixels[bottomRight[0] - 1, j] = YELLOW

img.save("output" + picture, format="png")
