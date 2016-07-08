"""
PIG IMPLEMENTATION, the good one is goint to be implemented in C or Cython.
^--^ ___
(00){___}@
    || ||
"""
import socket
import sys
import time

import simplejson as json
from paho import mqtt

from utils import eprint

sock_display = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock_sensor = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
print(sock_display)
print(sock_sensor)


server_address_display = '/var/run/rendezvous/terra/display'
server_address_sensor = '/var/run/rendezvous/vaisala/sensor'

eprint("connecting to ", server_address_display)
eprint("connecting to ", server_address_sensor)
try:
	sock_display.connect(server_address_display)
	sock_sensor.connect(server_address_sensor)
except socket.error, msg:
	eprint(msg)
	sys.exit()

def get_show_message(ln, message):
	print("ln: " + str(ln))
	print("message: " + message)
	response = json.dumps({"command":"show",
			"args":{
				"text":message,
				"line_num":ln
			}})
	print("RESPONSE: " +  response)
	return response

def send_command(sock, message):
	sock.sendall(message)
	amount_received = 0
	amount_expected = len(message)
	data = sock.recv(200)
	amount_received += len(data)
	eprint("received", data)


init_message = get_show_message(0,"NAPIEX")
print init_message
#sock_display.sendall(init_message)
send_command(sock_display, init_message)
init_message = get_show_message(1,"LTDA.")
print init_message
#sock_display.sendall(init_message)
send_command(sock_display, init_message)
time.sleep(3.5)
#sock_display.sendall(json.dumps({"command":"clear"}))

try:
	#message = json.dumps(get_show_message(0,"Rendezvous"))
	"""message = json.dumps({
							"command":"show",
							"args":{
								"text":"rendezvous",
								"line_num":1
								}
						 }
						)"""
	message = json.dumps({
							"command":"read",
							"args":{
									"device_oid": 1
									}
						})
	send_command(sock_sensor, message)
	#sock_sensor.sendall(message)
	#amount_received = 0
	#amount_expected = len(message)

	#while amount_received < amount_expected:
	#data = sock_sensor.recv(200)
	#amount_received += len(data)
	#eprint("received", data)


finally:
	eprint("closing socket")
	sock.close()



