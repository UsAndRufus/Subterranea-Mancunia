class Node(object):
    def __init__(self, name, pos):
        #parse parameters into attributes
        self.name = name
        self.pos = pos

        self.links = []

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
    
