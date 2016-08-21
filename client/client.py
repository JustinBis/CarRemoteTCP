# Client program to solve the CarRemoteTCP probolem
# By Justin Bisignano

import socket
import time

IP = "127.0.0.1"
PORT = 5001
BUFFER_SIZE = 512

def get_speed():
	"""Asks for the speed of the car from the server.
		Returns a float representing the speed of the car"""
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((IP, PORT))
	sock.send("GET_SPEED\n")
	res = sock.recv(BUFFER_SIZE)
	return float(res)

def set_pedal(amount):
	"""Sets the cars accelerator pedal to the passed amount.
	Accepts a number between 0 and 100 as the amount, representing a percentage of the maximum pedal press.
	Returns the cars current speed as a float."""
	if amount < 0 or amount > 100:
		raise ValueError("Pedal amount must be between 0 and 100")

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((IP, PORT))
	sock.send("SET_PEDAL {}\n".format(amount))
	res = sock.recv(BUFFER_SIZE)
	return float(res)

def main():
	pass
	#TODO

if __name__ == "__main__":
	main()