
import socket
import os

import simplejson as json 

from utils import eprint 


server_address = '/var/run/rendezvous/terra/display'
try:
	os.unlink(server_address)
except OSError:
	if os.path.exists(server_address):
		raise

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
eprint("starting up on ", server_address)
sock.bind(server_address)

sock.listen(1)

def do_command(command):
	return 0

while True:
	eprint("waiting for connection")
	connection, client_address = sock.accept()
	try:
		eprint("connection from:", client_address)

		#while True:
		data = connection.recv(100)
		#eprint("received", data)
		command = json.loads(data)
		print command["command"]
		print command["text"]
		print "procesing the command"
		response = do_command(command)
		if response == 0:
			print "done!"
			data = json.dumps({"response":"ok"})
			connection.sendall(data)

		"""
		if data:
			eprint("sending back to the client")
			connection.sendall(data)

		else:
			eprint("no more data from", client_address)
			break
		"""
	finally:
		connection.close()



