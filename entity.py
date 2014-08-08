class Entity(object):

    def __init__(self, breed, current_node):
        self.current_node = current_node

    def moveTo(self, next_node):
        self.current_node = next_node
