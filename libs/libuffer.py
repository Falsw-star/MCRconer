import struct
import uuid
import particle
import ctypes

SEGMENT_BITS = 0x7F
CONTINUE_BIT = 0x80

class LiBuffer (object):
	def __init__(self, capacity=10):
		self.bytes = bytearray(capacity)
		self.r_index = 0
		self.w_index = 0
		self.mr_index = 0
		self.mw_index = 0
		self.length = 0
		
	def readable_length(self):
		return self.length - self.r_index
	
	def mark(self):
		self.mr_index = self.r_index
		self.mw_index = self.w_index
	
	def reset(self):
		self.r_index = self.mr_index
		self.w_index = self.mw_index
	
	def read(self, length):
		if self.readable_length() < length:
			raise IndexError('LiBuffer index out of range!')
		ret = bytes(self.bytes[self.r_index:self.r_index + length])
		self.r_index += length
		return ret
	
	def write(self, bs):
		self.write_bytes(bs)
	
	def write_bytes(self, bs):
		if type(bs) is not bytearray and type(bs) is not bytes:
			raise TypeError('Only bytearray or bytes is allowed!')
		length = len(bs)
		if self.w_index + length > len(self.bytes):
			self.bytes += b'\x00' * (len(self.bytes) // 2)
		self.bytes[self.w_index:self.w_index + length] = bs
		self.w_index += length
		self.length = max(self.length, self.w_index)
	
	def read_bool(self):
		b = self.read(1)
		if b == b'\x00':
			return False
		if b == b'\x01':
			return True
		raise RuntimeError('Got byte %s while reading bool value. Expected 0 or 1!'%str(b))
	
	def write_bool(self, b):
		if type(b) is not bool:
			raise TypeError('Bool value is required.')
		self.write_bytes(b'\x01' if b else b'\x00')
	
	def read_ubyte(self):
		return self.read(1)[0]
	
	def read_byte(self):
		return self.read_ubyte() - 128
		
	def write_ubyte(self, b):
		if 0 <= b <= 255:
			self.write_bytes(b.to_bytes(1,'big'))
		else:
			raise ValueError('ubyte must be in range (0,256)')
	
	def write_byte(self,b):
		if -128 <= b <= 127:
			self.write_bytes((b + 128).to_bytes(1,'big'))
		else:
			raise ValueError('byte must be in range (-128,127). Did you mean ubyte?')
		
	def read_ushort(self):
		s = self.read(2)
		return int.from_bytes(s, byteorder='big')
	
	def read_short(self):
		s = self.read_ushort()
		return s - 32768
	
	def write_ushort(self, s):
		if 0 <= s <= 65535:
			self.write_bytes(s.to_bytes(2, 'big'))
		else:
			raise ValueError('ushort must be in range (0,65535)')
	
	def write_short(self,s):
		if -32768 <= s <= 32767:
			self.write_bytes((b + 32768).to_bytes(2, 'big'))
		else:
			raise ValueError('short must be in range (-32768,32767). Did you mean ushort?')
	
	def read_int(self):
		i = self.read(4)
		return int.from_bytes(i, 'big') - 2147483648
	
	def write_int(self, i):
		self.write_bytes((i+2147483648).to_bytes(4,'big'))
	
	def read_long(self):
		l = self.read(8)
		return int.from_bytes(l, 'big')
	
	def write_long(self,l):
		self.write_bytes(l.to_bytes(8,'big'))
		
	def read_float(self):
		f = self.read(4)
		return struct.unpack('>f',f)[0]
	
	def read_double(self):
		d = self.read(8)
		return struct.unpack('>d',d)[0]
	
	def write_float(self,f):
		self.write_bytes(struct.pack('>f',f))
	
	def write_double(self,d):
		self.write_bytes(struct.pack('>d',d))
	
	def read_varint(self):
		value = 0
		pos = 0
		while True:
			b = int(self.read_ubyte())
			value |= (b & SEGMENT_BITS) << pos
			if (b & CONTINUE_BIT) == 0:
				break
			pos += 7
			if (pos >= 32):
				raise RuntimeError('Var int is too big!')
		return value
	
	@staticmethod
	def int_overflow(val):
		maxint = 2147483647
		if not -maxint-1 <= val <= maxint:
			val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
		return val

	@staticmethod
	def unsigned_right_shitf(n,i):
		if n < 0:
			n = ctypes.c_uint32(n).value
		if i < 0:
			return -LiBuffer.int_overflow(n << abs(i))
		return LiBuffer.int_overflow(n >> i)
	
	def write_varint(self,i):
		while True:
			if (i & ~SEGMENT_BITS) == 0:
				self.write_ubyte(i)
				return 
			self.write_ubyte((i & SEGMENT_BITS) | CONTINUE_BIT)
			i = LiBuffer.unsigned_right_shitf(i,7)
	
	def write_varlong(self,l):
		while True:
			if (l & ~SEGMENT_BITS) == 0:
				self.write_ubyte(l)
				return 
			self.write_ubyte((i & SEGMENT_BITS) | CONTINUE_BIT)
			i = LiBuffer.unsigned_right_shitf(l,7)
	
	def read_str(self):
		l = self.read_varint()
		s = self.read(l)
		return s.decode()
	
	def write_str(self,s):
		b = str.encode(s)
		self.write_varint(len(b))
		self.write_bytes(b)
		
	def read_uuid(self):
		i = self.read(16)
		return uuid.UUID(bytes=i)
	
	def write_uuid(self, u):
		self.write_bytes(u.bytes)
	
	def read_position(self):
		bs = self.read(8)
		intpos = int.from_bytes(bs, 'big')
		x = (intpos >> 38) & 0x3FFFFFF
		z = (intpos >> 12) & 0x3FFFFFF
		y = intpos & 0xFFF
		x = x if x < (1 << 25) else x - (1 << 26)
		z = z if z < (1 << 25) else z - (1 << 26)
		y = y if y < (1 << 11) else y - (1 << 12)
		return (x, y, z)
	
	def write_position(self, pos):
		x = pos[0] & 0x3FFFFFF  # 26位
		z = pos[2] & 0x3FFFFFF  # 26位
		y = pos[1] & 0xFFF      # 12位
		
		bp = (x << 38) | (z << 12) | y
		self.write_bytes(bp.to_bytes(8, 'big'))
	
	def read_bitset(self):
		l = self.read_varint()
		return [self.read_long() for _ in range(l)]
	
	def write_bitset(self, bitset):
		self.write_varint(len(bitset))
		for long in bitset:
			self.write_long(long)
	
	def read_particle(self, pid):
		ret = particle.PARTICLES[pid]
		ret.read_buf(self)
		return ret
	
	def write_particle(self, par):
		par.write_buf(self)
	
	def read_slot(self):
		# !!! 不实现了 !!!
		pass
	
	def read_metadata(self):
		ret = {}
		while True:
			index = self.read_ubyte()
			if index == 0xFF:
				break
			t = self.read_varint()
			value = self.read_metadata_value(t)
			ret[index] = (t, value)
		return ret
	
	def write_metadata(self, metadata):
		for index in metadata:
			t, value = metadata[index]
			self.write_ubyte(index)
			self.write_varint(t)
			self.write_metadata_value(t, value)
		self.write_ubyte(0xFF)
	
	def read_metadata_value(buf, type_id):
		if type_id == 0:
			return buf.read_byte()
		elif type_id == 1:
			return buf.read_varint()
		elif type_id == 2:
			return buf.read_varlong()
		elif type_id == 3:
			return buf.read_float()
		elif type_id == 4:
			return buf.read_str()
		elif type_id == 5:
			return buf.read_str()  # Chat
		elif type_id == 6:
			return buf.read_str() if buf.read_bool() else None  # OptChat
		elif type_id == 7:
			return buf.read_slot()  # Slot
		elif type_id == 8:
			return buf.read_bool()
		elif type_id == 9:
			return (buf.read_float(), buf.read_float(), buf.read_float())
		elif type_id == 10:
			return buf.read_position()
		elif type_id == 11:
			return buf.read_position() if buf.read_bool() else None
		elif type_id == 12:
			return buf.read_varint()
		elif type_id == 13:
			return buf.read_uuid() if buf.read_bool() else None
		elif type_id == 14:
			return buf.read_varint()
		elif type_id == 15:
			return buf.read_varint()  # OptBlockID
		elif type_id == 16:
			return buf.read_nbt()  # NBT
		elif type_id == 17:
			return buf.read_particle()  # Particle
		elif type_id == 18:
			return (buf.read_varint(), buf.read_varint(), buf.read_varint())
		elif type_id == 19:
			return buf.read_varint()
		elif type_id == 20:
			return buf.read_varint()
		elif type_id == 21:
			return buf.read_varint()
		elif type_id == 22:
			return buf.read_varint()
		elif type_id == 23:
			return (buf.read_str(), buf.read_position()) if buf.read_bool() else None
		elif type_id == 24:
			return buf.read_varint()
		elif type_id == 25:
			return buf.read_varint()
		elif type_id == 26:
			return (buf.read_float(), buf.read_float(), buf.read_float())
		elif type_id == 27:
			return (buf.read_float(), buf.read_float(), buf.read_float(), buf.read_float())
		else:
			raise ValueError(f"Unknown metadata type {type_id}")

	def write_metadata_value(buf, type_id, value):
		if type_id == 0:
			buf.write_byte(value)
		elif type_id == 1:
			buf.write_varint(value)
		elif type_id == 2:
			buf.write_varlong(value)
		elif type_id == 3:
			buf.write_float(value)
		elif type_id == 4:
			buf.write_str(value)
		elif type_id == 5:
			buf.write_str(value)  # Chat
		elif type_id == 6:
			buf.write_bool(value is not None)
			if value:
				buf.write_str(value)
		elif type_id == 7:
			buf.write_slot(value)  # Slot
		elif type_id == 8:
			buf.write_bool(value)
		elif type_id == 9:
			buf.write_float(value[0])
			buf.write_float(value[1])
			buf.write_float(value[2])
		elif type_id == 10:
			buf.write_position(value)
		elif type_id == 11:
			buf.write_bool(value is not None)
			if value:
				buf.write_position(value)
		elif type_id == 12:
			buf.write_varint(value)
		elif type_id == 13:
			buf.write_bool(value is not None)
			if value:
				buf.write_uuid(value)
		elif type_id == 14:
			buf.write_varint(value)
		elif type_id == 15:
			buf.write_varint(value) 
			# OptBlockID
		elif type_id == 16:
			buf.write_nbt(value)  # NBT
		elif type_id == 17:
			buf.write_particle(value)  # Particle
		elif type_id == 18:
			buf.write_varint(value[0])
			buf.write_varint(value[1])
			buf.write_varint(value[2])
		elif type_id == 19:
			buf.write_varint(value)
		elif type_id == 20:
			buf.write_varint(value)
		elif type_id == 21:
			buf.write_varint(value)
		elif type_id == 22:
			buf.write_varint(value)
		elif type_id == 23:
			buf.write_bool(value is not None)
			if value:
				buf.write_str(value[0])
				buf.write_position(value[1])
		elif type_id == 24:
			buf.write_varint(value)
		elif type_id == 25:
			buf.write_varint(value)
		elif type_id == 26:
			buf.write_float(value[0])
			buf.write_float(value[1])
			buf.write_float(value[2])
		elif type_id == 27:
			buf.write_float(value[0])
			buf.write_float(value[1])
			buf.write_float(value[2])
			buf.write_float(value[3])
		else:
			raise ValueError(f"Unknown metadata type {type_id}")
