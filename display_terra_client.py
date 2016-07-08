import socket
import sys

import simplejson as json

from utils import eprint

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

server_address = '/var/run/rendezvous/terra/display'
eprint("connecting to ", server_address)
try:
	sock.connect(server_address)
except socket.error, msg:
	eprint(msg)
	sys.exit()



try:
	message = json.dumps({
							"command":"show",
							"args":{
								"text":"rendezvous",
								"line_num":1
								}
						 }
						)
	sock.sendall(message)
	amount_received = 0
	amount_expected = len(message)

	#while amount_received < amount_expected:
	data = sock.recv(100)
	amount_received += len(data)
	eprint("received", data)


finally:
	eprint("closing socket")
	sock.close()



