"""
PIG IMPLEMENTATION, the good one is goint to be implemented in C or Cython.
^--^ ___
(00){___}@
    || ||
"""
import socket
import os
from thread import *

import simplejson as json 

from terra import Display
from utils import eprint 


	
server_address = '/var/run/rendezvous/terra/display'
display = Display()
try:
	os.unlink(server_address)
except OSError:
	if os.path.exists(server_address):
		raise

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
eprint("starting up on ", server_address)
sock.bind(server_address)

sock.listen(1)

def do_command(*command, **kwargs):
	print command
	command = command[0]
	print kwargs
	if command == "backlight_on":
		display.turn_backlight(1)
		return 0
	elif command =="backlight_off":
		display.turn_backlight(0)
		return 0
	elif command == "show":
		display.write_line(**kwargs)
		return 0
	elif command == "clear":
		display.clear()
		return 0
	else:
		eprint("Command:{0} not supported".format(command))

	return 1


def clientthread(connection):
		data = connection.recv(200)
		command = json.loads(data)
		eprint(command["command"])
		eprint("procesing the command")
		#args = None

		#if "text" in command:
		#	eprint(command["text"])
		#	args = tuple(e for e in command["text"].split(","))

		response = do_command(command["command"], **command["args"])
		if response == 0:
			print "done!"
			data = json.dumps({"response":"ok"})
			connection.sendall(data)
		else:
			eprint("Error executing the command, view log for more details")


while True:
	eprint("DISPLAY SERVER: waiting for connection")
	connection, client_address = sock.accept()
	try:
		eprint("connection from:", client_address)
		start_new_thread(clientthread,(connection,))

		#while True:


		"""
		if data:
			eprint("sending back to the client")
			connection.sendall(data)

		else:
			eprint("no more data from", client_address)
			break
		"""
	finally:
		#connection.close()
		pass



