from OSC import OSCClient, OSCMessage

#Example from https://github.com/ptone/pyosc
#Mainly for testing connections
client = OSCClient()
client.connect( ("localhost", 7113) )

msg = OSCMessage("/hardware/1")
msg.extend([1.0, 2.0, 3.0])
client.send(msg)
#client.send( OSCMessage("/user/2", [2.0, 3.0, 4.0 ] ) )
#client.send( OSCMessage("/user/3", [2.0, 3.0, 3.1 ] ) )
#client.send( OSCMessage("/user/4", [3.2, 3.4, 6.0 ] ) )

#client.send( OSCMessage("/quit") )
