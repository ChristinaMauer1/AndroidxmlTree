class CompNode:
    def __init__(self, parent, bound):
        self.parent = parent
        self.children = []
        self.boundaries = bound

    def addChild(node):
        self.children.append(node)
    def getChildren():
        return children

def countSpace(string):
    count = 0
    for i in string:
        if i == ' ':
            count += 1

def getBounds(string):
    string = string.lstrip()
    bounds = string[14, string.index("checkable") - 3]
    return bounds

root = None

def parseXML(file):
    prevSpace = -1
    curNode = None
    prevNode = None
    for line in file:
        if line.startswith(' '):
            spaces = countSpace(line)
            bounds = getBounds(line)
            if curNode == None and prevNode == None:
                node = CompNode(None, bounds)
                root = node
                curNode = node
                prevSpace = spaces
            else:
                if spaces > prevSpace:
                    node = CompNode(curNode, bounds)
                    prevNode = curNode
                    curNode = node
                    prevSpace = spaces
                    prevNode.addChild(curNode)
                else:
                    node = CompNode(prevNode, bounds)
                    prevNode.addChild(node)
                    curNode = node
