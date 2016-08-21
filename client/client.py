# Client program to solve the CarRemoteTCP probolem
# By Justin Bisignano

import socket
import time
import math

IP = "127.0.0.1"
PORT = 5001
BUFFER_SIZE = 512
SLEEP_TIME = 0.5 # The time to sleep between each request to the server (so as to not overload the server)

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

def find_speed(speed):
	"""Will get the car to the passed speed as fast as possible and then search
	for the pedal position that maintains the desired speed.
	This function never returns as the pedal position will keep """

	# Set the pedal to max (100) and wait until we hit the desired speed
	print "Accelerating to", speed
	cur_speed = set_pedal(100)
	while get_speed() < speed:
		time.sleep(SLEEP_TIME)

	# Then start adjusting the pedal from the middle position to find 
	# the point where the desired speed is maintained

	def speed_increasing():
		"""Returns true if the speed of the car is increasing,
		false if the speed is decreasing"""
		speed = get_speed()
		time.sleep(SLEEP_TIME)
		return get_speed() > speed

	speed_was_increasing = True # Was the speed increasing last time we checked?
	pedal_amt = float(50)
	creep_amt = float(5)

	print "Searching for pedal position to maintain speed"

	while True:#abs(speed - cur_speed) > 0.01:
		pedal_amt = max(0, min(100, pedal_amt)) # Clamp pedal in 0-100
		cur_speed = set_pedal(pedal_amt)
		speed_is_increasing = speed_increasing()

		print "Speed: {:07.4f}\t Pedal: {:07.4f}%\t Creep Amount: {:07.4f}".format(cur_speed, pedal_amt, creep_amt)

		if speed_is_increasing:
			if cur_speed < speed:
				# Wait for the car to speed up
				pedal_amt += creep_amt
				continue
			else:
				# Slow the car down
				pedal_amt -= creep_amt
		else: # Speed is decreasing
			if cur_speed > speed:
				# Wait for the car to slow down
				pedal_amt -= creep_amt
				continue
			else:
				# Speed the car up
				pedal_amt += creep_amt

		# If we went from an increasing to a decreasing speed or vice versa, half the creep amount
		if (speed_is_increasing and not speed_was_increasing) or (not speed_is_increasing and speed_was_increasing):
			creep_amt /= 2

		speed_was_increasing = speed_is_increasing

def main():
	#TODO parse args here
	find_speed(20)

if __name__ == "__main__":
	main()