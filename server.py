#!/usr/bin/env python3

import socket
import struct
from threading import Thread
from os.path import getsize

class Server(Thread):
	def __init__(self, connfd, addr):
		super().__init__()
		self.connfd = connfd
		self.addr = addr

	def run(self):
		while True:
			try:
				data = self.connfd.recv(9)
				if not data:
					break
				
				operation, operand1, operand2 = struct.unpack('>cii', data) # Deconstruct the binary data. It's a character, an int32, and another int32, 9 bytes total
				operator = operation.decode()
				
				# You could easily add different operations here with an if statement. You need to update the client file as well
				if operator == '+':	
					result = operand1 + operand2
				elif operator == '-':
					result = operand1 - operand2
				elif operator == '*':
					result = operand1 * operand2
				elif operator == '/':
					result = operand1 // operand2 if operand2 != 0 else 0 # Dividing by zero is mathmatically impossible.
				else:
					result = 0

				self.connfd.sendall(struct.pack('>i', result)) # Result is a int32

			except Exception as e:
				print(f"Error: {e}")
				break

		print(f"Closed connection to {self.addr}")
		self.connfd.close()

def main():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind(("0.0.0.0", 7777))
	sock.listen(127)

	print("Listening on port 7777...")

	while True:
		try:
			connfd, addr = sock.accept()
			print("Connect from ", addr)
			t = Server(connfd, addr)
			t.setDaemon(True) # Threading to support multiple simultaneous clients
			t.start() # Uses the run loop function
		except KeyboardInterrupt:
			sock.close()
			return

if __name__ == '__main__':
	main()
