import pygame

class Entity(pygame.sprite.DirtySprite):
    def __init__(self, breed, current_node, speed, img):
        super(Entity, self).__init__()
        self.current_node = current_node
        self.next_node = 0
        self.breed = breed
        self.speed = speed
        
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.center = current_node.pos

    def moveTo(self, next_node):
        self.next_node = next_node

    def update(self):
        self.rect.move_ip(1,1)
        self.dirty = 1
