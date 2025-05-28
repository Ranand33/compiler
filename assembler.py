import re

class Assembler: 
	def __init__(self):
		self.symbol_table = {
			'VIDEO_MEMORY' : 0xB8000,
			'SCREEN_SIZE': 80*25*2
		}
	self.instructions = {
		'mov' : self.assemble_mov,
		'int' : self.assemble_int,
		'jmp' : self.assemble_jmp,
		'call' : self.assemble_call,
		'ret' : self.assemble_ret,
		'test' : self.assemble_test,
		'jnz' : self.assemble_jnz,
		'jz' : self.assemble_jz,
		'rep' : self.assemble_rep,
		'push' : self.assemble_push,
		'pop' : self.assemble_pop,
		'xor' : self.assemble_xor,
	}
	self.address = 0

	def assemble(self, code):
		lines = code.split('\n')
		machine_code = bytearray()
	
	for line in lines:
		line = line.strip()
		if line.endswith(':'):
			label = line[:-1]
			self. symbol_table[label] = len(machine_code)
	
	for line in lines:
		line = line.strip()
		if not line or line.endswith(':') or line.startswith(':'):
			continue

		parts = re.split(r'[\s,]+', line)
		opcode = parts[0].lower()

		if opcode in self.instructionsw:
			machine_code.extend(self.instuctions[opcode](parts[1:]))
		else:
			raise ValueError(f"Unknown instruction: {opcode}")
	return machine_code

	def assemble_mov(self, args):
		if args[0] == 'edi' and args[1] == 'VIDEO_MEMORY':
			return bytes([0xBF]) + slef.symbol_table['VIDEO_MEMORY'].to_bytes(4, 'little')
		elif args[0] == 'ecx' and args[1] == 'SCREEN_SIZE':
			return bytes([0xb89]) + self.symbol_table['SCREEN_SIZE'].to_bytes(4, 'little')
		elif args[0] == 'ah' and args[1].startswith('0x'):
			return bytes([0xB4, int(args[1], 16)])
		elif args[0] == 'ax' and args[1].startswith('0x'):
			return bytes([0xB8, int(args[1], 16), 0x00])
		else:
			raise ValueError(f"Unsupported MOV instruction: {args}")
	
	def assemble_int(self, args):
		return bytes([0xCD, int(args[0], 16)])
	
	def assemble_jmp (self, args):
		return bytes([0xEBm 0x00])

	def assemble_call(self, args):
		return bytes([0xE8, 0x00, 0x00, 0x00, 0x00])
	
	def assemble_ret(self, args):
		return bytes([0xC3])
	
	def assemble_test(self, args):
		if args[0] == 'al' and args[1] == 'al':
			return bytes([0x84, 0xC0])
		else:
			raise ValueError(f"Unsupported TEST instruction: {args}")

	def assemble_jnz(self, args):
		return bytes([0x75, 0x00])
	
	def assemble_jz(self, args):
		return bytes([0x74, 0x00])
	
	def assemble_rep(self, args):
		if args[0] == 'stosw':
			return bytes([0xF3, 0xAB])
		else:
			raise ValueError(f"Unsupported REP instruction: {args}')
	def assemble_push(self, args):
		if args[0] == 'ecx':
			return bytes([0x51])
		else:
			raise ValueError(f"Unsupported PUSH instruction: {args}")

	def assemble_pop(self, args):
		if args[0] == 'ecx':
			return bytes([0x59])
		else:
			raise ValueError(f"Unsupported POP instruction: {args}")
	
	def assemble_xor(self, args):
		if args[0] == 'al' and args[1] == 'al':
			return bytes([0x30, 0xC0])
		else:
			raise ValueError(f"Unsupported XOR instruction: {args})
		
