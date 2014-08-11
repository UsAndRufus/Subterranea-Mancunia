import sys, time
from sets import Set

from node import *
from entity import Entity
from bezier import Bezier, Link

import pygame

#--------------------#
# Method definitions #
#--------------------#

def create_nodes():
    #Junctions
    pic = Junction("Piccadilly Station", (1464,790), 1)
    vic = Junction("Victoria Station", (968,92), 2)
    quay = Junction("Quay Street", (450,580), 3)
    chepstow = Junction("Chepstow", (952,894), 4)
    deansgate = Junction("Deansgate Den", (683,742), 5)
    #node6 = Junction("Junction 6", (540,305), 6)
    #node7 = Junction("Junction 7", (640,360), 7)
    #node8 = Junction("Junction 8", (740,415), 8)
    #node9 = Junction("Junction 9", (840,470), 9)
    #node10 = Junction("Junction  10", (940,525), 10)
    #node11 = Junction("Junction 11", (1040,580), 11)
    #node12 = Junction("Junction 12", (1140,635), 12)

    #Destinations
    jrlib = Destination("John Ryland's Library", (720,587), "path/to/img")
    mosi = Destination("MOSI", (438, 804), "path/to/img")

    #create links
    #pic.links = [vic, chepstow]
    #vic.links = [pic, quay]
    #quay.links = [deansgate, mosi]
    #chepstow.links = [deansgate, pic]
    #deansgate.links = [quay, chepstow, mosi, jrlib]

    quay_vic = Link(quay, vic, (511,495), (869,410), 20)
    #quay_vic = Link(quay, vic, (511,495), (1000,1000), 20)
    quay.links = [quay_vic]

    #nodes = [pic, vic, quay, chepstow, deansgate, jrlib, mosi]
    nodes = [quay, vic]

    #nodes = [node1, node2, node3, node4, node5, node6, node7,
    #         node8, node9, node10, node11, node12, node13, node14]
    return nodes

def create_entities(nodes):
    entity1 = Entity("Badger", nodes[1], 1,"images/Entities/triangle_alpha.png")
    entity2 = Entity("Badger", nodes[0], 1,"images/Entities/triangle_alpha.png")
    entity3 = Entity("Scientist", nodes[1], 2,"images/Entities/triangle_alpha.png")

    entities = pygame.sprite.LayeredDirty(entity2)
    return entities

def create_window(res_tuple, image_location):
    #create the screen
    window = pygame.display.set_mode(res_tuple, pygame.FULLSCREEN) 

    pygame.mouse.set_visible(False)

    mapimage = pygame.image.load(image_location)
    mapimagerect = mapimage.get_rect()
    window.blit(mapimage, mapimagerect)

    return window

def render_nodes(background, nodes, links):
    #draw links
    '''
    for link in links:
        pygame.draw.line(background, pygame.Color(255,255,100),
                         link[0].pos, link[1].pos, 10)
    '''
    
    #draw nodes
    for node in nodes:

        rect = pygame.Rect(0,0,10,10)
        for l in node.links:
            for t in [x * 0.01 for x in range(0,100)]:  
                rect.center = l(t)
                pygame.draw.rect(background, pygame.Color(25,200,255), rect)
        
        if isinstance(node, Junction):
            #draw Junction
            if node.isOn:
                width = 0
            else:
                width = 5
            pygame.draw.circle(background, pygame.Color(255,50,100),
                               node.pos, 20, width)
        else:
            #draw Destination
            #creates a rect to draw: tuple operation minuses 20 from each item
            rect = pygame.Rect(0, 0, 40, 40)
            rect.center = node.pos
            pygame.draw.rect(background, pygame.Color(50,200,200), rect)
        #draw text
        text = default_font.render(node.name, True, (0, 0, 0))
        text_pos = text.get_rect()
        text_pos.midleft = node.pos
        background.blit(text, text_pos)

def render_entities(window, entities):
    triangle = [(-20,18),(0,-17),(20,18)]

    for entity in entities:
        pos = entity.current_node.pos
        translated_triangle =[
            (t[0] + pos[0], t[1] + pos[1]) for t in triangle ]
        pygame.draw.polygon(window, pygame.Color(100,0,150),translated_triangle)
    
    pygame.display.flip()

        

#--------------------#
# Object definitions #
#--------------------#

#class to handle conceptual elements of the game
#node states, enemies & locations
#controller classes also report to it
class Game(object):
    def __init__(self, difficulty, nodes):
        self.difficulty = difficulty
        self.nodes = nodes
        self.calc_links()

    #creates a list of all links between nodes
    #duplicates are removed
    def calc_links(self):
        link_set = set()
        for node in self.nodes:
            #get all links from node, sort them so (a,b)= (b,a)
            sorted_links = [ tuple(sorted((node,l))) for l in node.links ]
            #adding to set eliminates duplicates
            link_set |= set(sorted_links)
        self.links = list(link_set)

#-------#
#Runtime#
#-------#

#start window        
pygame.init() 
window = create_window((1920,1080), "images/map_draft.png")
background = pygame.image.load("images/map_draft.png").convert()
background_rect = background.get_rect()

#initialise fonts
pygame.font.init()
default_font = pygame.font.SysFont("trebuchetms", 15)

new_nodes = create_nodes()

#create Game
game = Game("medium", new_nodes)

entities = create_entities(game.nodes)

render_nodes(background, game.nodes, game.links)
window.blit(background, background_rect)

entities.clear(window, background)

clock = pygame.time.Clock()

entities.sprites()[0].move_to(game.nodes[1], game.nodes[0].links[0])


running = True
while running:
    clock.tick(60)
    
    #event handling, bit rubbish for now
    for event in pygame.event.get(): 
      if event.type == pygame.KEYDOWN:
          print("FPS: " + str(clock.get_fps()))
          running = False

    entities.update()

    #render
    
    #entities
    dirty_rects = entities.draw(window)
    pygame.display.update(dirty_rects)


    pygame.display.flip()
    
pygame.quit()


