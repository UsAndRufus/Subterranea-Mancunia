#just for testing

import threading
import time
from OSC import OSCServer, OSCClient, OSCMessage

def hardware_callback(addr, tags, data, client_address):
    print(addr)
    print(tags)
    print(data)
    print(client_address)

#setup server and client
server = OSCServer( ("localhost", 7110) )
client = OSCClient()
server.setClient(client)

def sf(server):
    print(server)
    #server.serve_forever()
    

server.addMsgHandler( "/hardware/" + str(1), hardware_callback)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.start()

while True:
    time.sleep(1)
    print("hi")
