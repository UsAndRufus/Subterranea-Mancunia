class Entity(object):

    def __init__(self, currentNode):
        self.currentNode = currentNode

    def moveTo(self, nextNode):
        self.currentNode = nextNode
