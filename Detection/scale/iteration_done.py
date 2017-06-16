import socket
#import server

#server.save_dict()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening
server_address = ('localhost', 4242)
try:
    sock.connect(server_address)
    print "Connected"
finally:
    pass

sock.send("OK")
print "sent"

#msg = sock.recv(1024)
#print msg
