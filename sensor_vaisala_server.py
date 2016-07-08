"""
PIG IMPLEMENTATION, the good one is goint to be implemented in C or Cython.
^--^ ___
(00){___}@
    || ||
"""
import socket
import os

import simplejson as json 

from terra import TemperatureSensor
from utils import eprint 



server_address = '/var/run/rendezvous/vaisala/sensor'
sensor = TemperatureSensor()
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
	command = command[0]
	if command == "read":
		return sensor.read(kwargs)
		#return 0
	elif command =="set_oid":
		sensor.set_oid(kwargs)
		return 0
	else:
		eprint("Command:{0} not supported".format(command))

	return 1


while True:
	eprint("SENSOR_SERVER: waiting for connection")
	connection, client_address = sock.accept()
	try:
		eprint("connection from:", client_address)

		#while True:
		data = connection.recv(200)
		command = json.loads(data)
		eprint(command)
		eprint(command["command"])
		eprint("procesing the command")
		#args = None

		#if "text" in command:
		#	eprint(command["text"])
		#	args = tuple(e for e in command["text"].split(","))

		response = do_command(command["command"], **command["args"])
		if response:
			print "done!"
			data = json.dumps({"response":"ok","data":response})
			connection.sendall(data)
		else:
			eprint("Error executing the command, view log for more details")

		"""
		if data:
			eprint("sending back to the client")
			connection.sendall(data)

		else:
			eprint("no more data from", client_address)
			break
		"""
	finally:
		pass
		#connection.close()



