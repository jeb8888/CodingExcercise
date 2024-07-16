#!/usr/bin/env python3

import sys
import socket
import struct
from os.path import getsize
import re

LOCALHOST = "127.0.0.1"
#IPv4_ADDR = "192.168.1.2"
PORT = 7777 # Default port is 7777 
cmd_exit = 'EXIT'

"""
If I had more time, then I would consider adding basic authentication to the clients that are connecting to the server. Using secure sockets (TLS/SSL) would ensure security and privacy. 

Another thing that I would do is implement support for floats and doubles. I touch upon this several times in the comments below. I could modify the client and server where needed to support floating-point operations instead of 32-bit integers by modifying the struct-packing format.

I would also consider adding the option for remote IP addreses. I would do this by allowing the server and client to read configuration arguments through an environment variable and/or configuration file. 


I would add support for exponentials (^) and modulus (%) operators. 
"""
class math_client:
	
	"""
	Initialize the client class
	
	return void
	"""
	def __init__(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock = sock
	
	"""
	Connect to the server using the supplied IP and port
	
	ip: a string containing the IP address
	port: an integer contraining the port
	
	return True if successful, False otherwise
	"""
	def connect_server(self, ip, port):
		print(f"Connecting to IP {ip}:{port}")
		try:
			self.sock.connect((ip, port))
		except socket.error as e:
			print(f"Unknown socket error: {e}")
			return False
		return True

	"""
	Close the socket
	
	return void
	"""
	def client_exit(self):
		print("Closing connections...")
		self.sock.close()

	"""
	Sends and retrives equation from the server
	
	operator: the mathmatical operation to perform
	operand1: a 32-bit integer 
	operand2: a 32-bit integer
	return void
	"""
	def send_equation(self, operator, operand1, operand2):
		try:
			# >cii is (c)haracter, (i)nteger, (i)nteger
			# 9 bytes total. A character is one byte, and an int is four
			message = struct.pack('>cii', operator.encode(), int(operand1), int(operand2))
			self.sock.sendall(message)

			result_data = self.sock.recv(4) # int32
			result = struct.unpack('>i', result_data)[0] # You can modify this to be a float
			print(f"Result: {result}")
		except Exception as e:
			print(f"Error: {e}")
			
"""
Prints program usage and correct syntax

return void
"""
def print_usage():
	print("Usage:\nmath <operand1> <operator> <operand2>\nexit")

"""
Initialize the client, connects to the server, handles and validates user input. Prints usage if the input is incorrect. Closes the socketed connection if the user types 'exit' to exit the program. 

return void
"""
def main():
	client = math_client()
	has_connected_to_server = False

	ip_addr = input("Input IP address [127.0.0.1]: ") # Default IP address is localhost. You need to change this to handle secure sockets. 
	if ip_addr == '':
		ip_addr = LOCALHOST

	has_connected_to_server = client.connect_server(ip_addr, PORT)
	if has_connected_to_server:
		print(f"Successfully connected to {ip_addr}:{PORT}")
	print_usage()
	
	while has_connected_to_server:
		cmd_full = input("> ")

		cmd_full = cmd_full.rstrip()
		cmd_input = cmd_full.split(" ")
		args = len(cmd_input)
		cmd = cmd_input[0]

		if cmd == "connect" and args == 2:
			if not has_connected_to_server:
				ip = cmd_input[1]
				has_connected_to_server = client.connect_server(ip, PORT)
			else:
				print("This client is already connected to a server.")
		elif cmd == "math":
			if args == 4:
				operator = cmd_input[2]
				operand1 = cmd_input[1]
				operand2 = cmd_input[3]
				if operator not in ['+', '-', '*', '/']: # You could expand this to add additional operations here.
					print("Error: Operator must be either -, +, /, or *")
					continue

				client.send_equation(operator, operand1, operand2)
			else:
				print_usage()
		elif cmd == "exit":
			if has_connected_to_server:
				client.client_exit()
				has_connected_to_server = False
				sys.exit(0) # Close the program
			else:
				return
		else:
			print_usage()

if __name__ == '__main__':
	main()
