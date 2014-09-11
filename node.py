class Node(object):
    def __init__(self, name, pos):
        #parse parameters into attributes
        self.name = name
        self.pos = pos
        
        self.open = True
        self.links = []
        self.nav_net = {}

    def link_to(self, next_node):
        link = ""
        for l in self.links:
            if l.node1 == next_node or l.node2 == next_node:
                link = l
        if link != "":
            return link
        else:
            print("Error:", self,"does not link to",next_node)

class Junction(Node):
    def __init__(self, name, pos, junction_id):
        super(Junction, self).__init__(name, pos)
        self.junction_id = junction_id
        self.isOn = False

class Destination(Node):
    def __init__(self, name, pos, img):
        super(Destination, self).__init__(name, pos)
        self.img = img
        self.occupied = False
    
