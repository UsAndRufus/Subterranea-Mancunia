#!/usr/bin/env python

#This should be able to send and receive messages
#Based on receive.py and send.py

from OSC import OSCServer, OSCClient, OSCMessage
import sys
from time import sleep

server = OSCServer( ("localhost", 7110) )
client = OSCClient()
server.setClient(client)

server.timeout = 0
run = True

# this method of reporting timeouts only works by convention
# that before calling handle_request() field .timed_out is
# set to False
def handle_timeout(self):
    self.timed_out = True

# funny python's way to add a method to an instance of a class
import types
server.handle_timeout = types.MethodType(handle_timeout, server)

def user_callback(path, tags, args, source):
    # which user will be determined by path:
    # we just throw away all slashes and join together what's left
    user = ''.join(path.split("/"))
    # tags will contain 'fff'
    # args is a OSCMessage with data
    # source is where the message came from (in case you need to reply)
    print ("Now do something with", user,args)

def quit_callback(path, tags, args, source):
    # don't do this at home (or it'll quit blender)
    print("QUTTING")
    global run
    run = False

server.addMsgHandler( "/user/1", user_callback )
server.addMsgHandler( "/user/2", user_callback )
server.addMsgHandler( "/user/3", user_callback )
server.addMsgHandler( "/user/4", user_callback )
server.addMsgHandler( "/quit", quit_callback )

# user script that's called by the game engine every frame
def each_frame(n):
    # clear timed_out flag
    server.timed_out = False

    #send message
    msg = OSCMessage("/user/1")
    msg.append(n)
    server.client.sendto(msg,("localhost", 7110))
    
    # handle all pending requests then return
    print("receive")
    while not server.timed_out:
        server.handle_request()

# simulate a "game engine"
n = 0

server.serve_forever()

server.close()
