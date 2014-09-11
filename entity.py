import pygame
import random

class Entity(pygame.sprite.DirtySprite):
    def __init__(self, breed, current_node, speed, img, destination):
        super(Entity, self).__init__()
        self.current_node = current_node
        self.next_node = ""
        self.last_node = current_node
        self.breed = breed
        self.destination = destination

        #movement
        self.speed = speed
        self.moving = False
        self.reverse = False
        self.travelled = 0
        self.current_link = ""
        
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = current_node.pos

    def move_to(self, next_node, link):
        if next_node.open:
            self.next_node = next_node
            self.current_link = link
            self.moving = True

            if link.node1 != self.current_node:
                self.reverse = True
            else:
                self.reverse = False
        else:
            print("next_node is closed")

    def move(self):
        #calculate step based on speed, framerate, and length
        dist = 1 / float(self.speed * 60 * self.current_link.length)
        dist *= 3
        self.travelled += dist
        #if next_node becomes closed, go back to where you came from
        #but only if you can see that it is closed
        if not self.next_node.open:
            if self.travelled > 0.8:
                self.reverse = not self.reverse
                temp = self.next_node
                self.next_node = self.current_node
                self.current_node = temp
                self.travelled = 1 - self.travelled
        #if overshot destination, go back to destination
        if self.travelled > 1:
            self.travelled = 1
        if self.reverse:
            #if in reverse, we go from 1 to 0
            self.rect.center = self.current_link(1 - self.travelled)
        else:
            self.rect.center = self.current_link(self.travelled)
        self.dirty = 1

    def navigate(self, nav_net):
        #check not already there
        if self.current_node != self.destination:
            #check not just been there
            dest = nav_net[self.destination]
            #check not closed and you haven't just been there
            if dest.open and self.last_node != dest:
                #if  we haven't, go there
                print("standard")
                self.move_to(dest, self.current_node.link_to(dest))
            else:
                #else go somewhere random
                #get new destination
                n = random.randint(0,(len(self.current_node.links)-1))
                #get new link
                new_link = self.current_node.links[n]
                #get new dest from link
                if new_link.node1 != self.current_node:
                    new_dest = new_link.node1
                else:
                    new_dest = new_link.node2
                print("blocked, random move")
                #move there
                #if the move fails here, the navigate call will make entity move next frame
                self.move_to(new_dest, self.current_node.link_to(new_dest))
            

    def update(self):
        if self.moving:
            if self.travelled != 1:
                self.move()
            #when it reaches destination, stop moving
            else:
                self.travelled = 0
                self.moving = False
                self.last_node = self.current_node
                self.current_node = self.next_node
                print(self.current_node.name)
                
            
