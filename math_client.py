#!/usr/bin/env python3

import sys
import socket
import struct
from os.path import getsize
import re

LOCALHOST = "127.0.0.1"
#IPv4_ADDR = "192.168.1.2"
PORT = 7777
cmd_exit = 'EXIT'

class math_client:
	def __init__(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock = sock
	
	def connect_server(self, ip, port):
		print(f"Connecting to IP {ip}:{port}")
		try:
			self.sock.connect((ip, port))
		except socket.error as e:
			print(f"Unknown socket error: {e}")
			return False
		return True

	# Close the socket
	def client_exit(self):
		print("Closing connections...")
		self.sock.close()

	# Sends and retrieves equation from the server
	def send_equation(self, operator, operand1, operand2):
		try:
			message = struct.pack('>cii', operator.encode(), int(operand1), int(operand2))
			self.sock.sendall(message)

			result_data = self.sock.recv(4) # int32
			result = struct.unpack('>i', result_data)[0] # You can modify this to be a float
			print(f"Result: {result}")
		except Exception as e:
			print(f"Error: {e}")
			
def print_usage():
	print("Usage:\nmath <operand1> <operator> <operand2>\nexit")

def main():
	client = math_client()
	has_connected_to_server = False

	ip_addr = input("Input IP address [127.0.0.1]: ") # Default IP address is localhost
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
				if operator not in ['+', '-', '*', '/']:
					print("Error: Operator must be either -, +, /, or *")
					continue

				client.send_equation(operator, operand1, operand2)
			else:
				print_usage()
		elif cmd == "exit":
			if has_connected_to_server:
				client.client_exit()
				has_connected_to_server = False
				sys.exit(0)
			else:
				return
		else:
			print_usage()

if __name__ == '__main__':
	main()
