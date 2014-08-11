import pygame

class Entity(pygame.sprite.DirtySprite):
    def __init__(self, breed, current_node, speed, img):
        super(Entity, self).__init__()
        self.current_node = current_node
        self.next_node = ""
        self.breed = breed

        #movement
        self.speed = speed
        self.moving = False
        self.travelled = 0
        self.current_link = ""
        
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = current_node.pos

    def move_to(self, next_node, link):
        print("move_to(" + next_node.name + str(link) + ")")
        self.next_node = next_node
        self.current_link = link
        self.moving = True

    def move(self):
        print("move, self.travelled = " + str(self.travelled))
        dist = 1 / float(self.speed * 60 * self.current_link.length)
        self.travelled += dist
        if self.travelled > 1:
            self.travelled = 1
        self.rect.center = self.current_link(self.travelled)
        print(self.rect.center)
        self.dirty = 1

    def update(self):
        if self.moving:
            if self.travelled != 1:
                self.move()
            #when it reaches destination, stop moving
            else:
                print("movement finished")
                self.travelled = 0
                self.moving = False
                self.current_node = self.next_node
                
            
