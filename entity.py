import pygame

class Entity(pygame.sprite.DirtySprite):
    def __init__(self, breed, current_node, img):
        super(Entity, self).__init__()
        self.current_node = current_node
        self.breed = breed
        
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()

        self.rect.center = current_node.pos

    def moveTo(self, next_node):
        self.current_node = next_node
