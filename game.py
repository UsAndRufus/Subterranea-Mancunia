import sys, time, os
import win32api
from sets import Set
import threading

from node import *
from entity import Entity
from bezier import Bezier, Link
from game_event import *

from OSC import OSCServer, OSCClient, OSCMessage

import pygame
from pygame.locals import * #lets us use KEYDOWN rather than pygame.KEYDOWN etc.

#-----------#
# Constants #
#-----------#

#23 is user defined event ID
NETWORK_HARDWARE = 23

#IDs for the different hardware
JUNCTION = 1
SCIENCE = 2
COMMANDER = 3
RADIO = 4

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
    vic.links = [quay_vic]

    nodes = [quay, vic, pic, chepstow, deansgate, jrlib, mosi]
    #nodes = [quay, vic]

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
    window = pygame.display.set_mode(res_tuple, NOFRAME)

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

#Network
def hardware_callback(addr, tags, d, client_address):
    #d is data

    h_id = int(addr.split("/")[-1])

    event = None
    error = False

    if h_id == JUNCTION:
        if len(d) == 13:    
            #create event object
            event = pygame.event.Event(NETWORK_HARDWARE,{"hardware_id":JUNCTION,
                    "topRowOn":d[0],1:d[1],2:d[2],3:d[3],4:d[4],5:d[5],6:d[6],
                    7:d[7],8:d[8],9:d[9],10:d[10],11:d[11],12:d[12]})
        else:
            error = True
    elif h_id == SCIENCE:
        event = pygame.event.Event(NETWORK_HARDWARE,{"hardware_id":SCIENCE,"s1":True})
    elif h_id == COMMANDER:
        event = pygame.event.Event(NETWORK_HARDWARE,{"hardware_id":COMMANDER,"has_power":True})
    elif h_id == RADIO:
        event = pygame.event.Event(NETWORK_HARDWARE,{"hardware_id":RADIO,"frequency":55})

    if event != None:
        pygame.event.post(event)
    if error:
        #object malformed, return error
        msg = OSCMessage("/user/1")
        msg.append("Error")
        server.client.sendto(msg,client_address)

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

#set pygame window to be on other screen
#os.environ['SDL_VIDEO_WINDOW_POS'] = str(1900) + "," + str(0)

#start window        
pygame.init() 
window = create_window((1920,1080), "images/map_draft.png")
background = pygame.image.load("images/map_draft.png").convert()
background_rect = background.get_rect()

#initialise fonts
pygame.font.init()
default_font = pygame.font.SysFont("trebuchetms", 15)

#setup server and client
server = OSCServer( ("localhost", 7126) )
client = OSCClient()
server.setClient(client)

server.addMsgHandler("/hardware/" + str(JUNCTION), hardware_callback)
server.addMsgHandler("/hardware/" + str(SCIENCE), hardware_callback)
server.addMsgHandler("/hardware/" + str(COMMANDER), hardware_callback)
server.addMsgHandler("/hardware/" + str(RADIO), hardware_callback)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.start()


#create nodes
new_nodes = create_nodes()

#create Game
game = Game("medium", new_nodes)

entities = create_entities(game.nodes)

render_nodes(background, game.nodes, game.links)
window.blit(background, background_rect)

entities.clear(window, background)

clock = pygame.time.Clock()

#testing
junction_event = pygame.event.Event(NETWORK_HARDWARE,{"hardware_id":JUNCTION,"j1":True})
science_event = pygame.event.Event(NETWORK_HARDWARE,{"hardware_id":SCIENCE,"s1":True})
commander_event = pygame.event.Event(NETWORK_HARDWARE,{"hardware_id":COMMANDER,"has_power":True})
radio_event = pygame.event.Event(NETWORK_HARDWARE,{"hardware_id":RADIO,"frequency":55})

#pygame.event.post(junction_event)
#pygame.event.post(science_event)
#pygame.event.post(radio_event)
#pygame.event.post(commander_event)

#----------------#
# Game Sequences #
#----------------#

#Test sequence
_phone1 = PhoneEvent("phone1", "sounds/ring.wav")
_enemies1 = SpawnEvent("enemies1",pygame.sprite.LayeredDirty(Entity("Badger", game.nodes[1], 1,"images/Entities/triangle_alpha.png"), Entity("Badger", game.nodes[1], 1,"images/Entities/triangle_alpha.png")))
_spawn1 = SpawnEvent("spawn1", _enemies1)
_cond1 = ConditionEvent("cond1", "fake condition")
_sound1 = PhoneEvent("sound1", "sounds/fake.wav")
_wait1 = WaitEvent("wait1", 10)
_sound2 = SoundEvent("sound2", "sounds/fake2.wav")

test_seq = [_phone1, _enemies1, _spawn1, _sound1, _wait1, _sound2]

seq_pos = 0

###

frame = 0

#Game loop
running = True
while running:
    clock.tick(60)

    frame += 1

    #message sending testing
    msg = OSCMessage("/user/1")
    msg.append("hellooo tharrr")
    msg.append(100.1)
    #server.client.sendto(msg,("localhost", 7110))

    #printer testing
    '''
    if frame == 100:
        
        filename = "test.txt"
        print_args = (
          0,
          "print",
          filename,
          '/d:\\EdwardB-ASUSN56\Toshiba4610',
          ".",
          0
        )
        
        print_args = ('\"C:\Program Files (x86)\Adobe\Reader 10.0\Reader\AcroRd32.exe\" /t test.pdf',)
        print_thread = threading.Thread(target = os.system, args = print_args)
        #print_thread.start()
    '''
        
    #event handling
    for event in pygame.event.get():
        if event.type == NETWORK_HARDWARE:
            print(event)
            if event.hardware_id == JUNCTION:
                print("junction")
            if event.hardware_id == SCIENCE:
                print("science")
            if event.hardware_id == COMMANDER:
                print("commander")
            if event.hardware_id == RADIO:
                print("radio")
        elif event.type == KEYDOWN or event.type == QUIT:
            print("FPS: " + str(clock.get_fps()))
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            game.nodes[0].open = not game.nodes[0].open
            game.nodes[1].open = not game.nodes[1].open

    #handle sequence events
    current_event = test_seq[seq_pos]
    
    if not current_event.finished and not current_event.running:
        current_event.run()
        seq_pos += 1
        if seq_pos == 5:
            seq_pos = 0
         

    #update game state
    if entities.sprites()[0].moving == False:
        if entities.sprites()[0].current_node.name == "Quay Street":
            entities.sprites()[0].move_to(game.nodes[1], game.nodes[0].links[0])
        else:
            entities.sprites()[0].move_to(game.nodes[0], game.nodes[1].links[0])

    entities.update()

    #render
    
    #entities
    dirty_rects = entities.draw(window)
    pygame.display.update(dirty_rects)

#if we quit
server.close()
pygame.quit()
sys.exit()


