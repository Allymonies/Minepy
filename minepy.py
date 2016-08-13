import socket
import struct
from threading import Thread
import time

def writeString(toConvert):
	strByte = bytearray(toConvert, "utf-8")
	result = struct.pack("<i", len(strByte)) + strByte
	return result

class Connect:
	def __init__(self, ip, port):
		self.ip = ip
		self.port = port
		self.s = socket.socket()
		self.s.connect((ip,port))
		self.handshake()
		self.thread = Thread(target = self.receive)
		self.thread.start()
	def sendPacket(self, id, data = None):
		if str(type(id)) == "<class 'int'>":
			id = struct.pack("<i", id)
		if (data != None and str(type(data)) == "<class 'bytearray'>") or (data == None):
			if data != None:
				self.s.send(bytes((len(data)+len(id),)))
			else:
				self.s.send(bytes((1,)))
			self.s.send(bytearray(id))
			if data != None:
				self.s.send(data)
		else:
			raise TypeError
	def handshake(self):
		packet = bytearray()
		packet_id = b'\x00'
		packet += struct.pack("<i", 210)
		packet += writeString(self.ip)
		packet += struct.pack("!H", self.port)
		packet += struct.pack("<i", 1)
		self.sendPacket(packet_id, packet)
		self.sendPacket(b'\x00')
	def receive(self):
		while True:
			try:
				response = self.s.recv(4096)
				if response:
					print(str(response))
					print(str(response,"utf-8"))
			except BlockingIOError:
				pass
