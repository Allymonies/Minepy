import socket
import struct
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
	def sendPacket(self, id, data = None):
		if str(type(data)) == "<class 'bytearray'>":
			self.s.send(bytes((len(data)+len(id),)))
			self.s.send(id)
			if data:
				self.s.send(data)
		else:
			raise TypeError
	def handshake(self):
		packet = bytearray()
		packet_id = 0x00
		packet += struct.pack("<i", 210)
		packet += writeString(writeString(self.ip))
		packet += struct.pack("!H", self.port)
		packet += struct.pack("<i", 1)
		self.sendPacket(packet_id, packet)
		self.sendPacket(0x00)
		response = self.s.recv(16384, 0x40)
		print(str(response))
		print(str(response,"utf-8"))
