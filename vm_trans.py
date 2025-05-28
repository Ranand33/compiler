class VMTranslator:
	def __init__(self):
		self.label_counter = 0
		self.arithmetic_logical_commands = {
			'add' : self.translate_add,
			'sub' : self.translate_sub
		}
	
	def translate(self, vm_code):
		vm_commands = vm_code.strip().split('\n')
		assembly_code = []
		for command in vm_commands:
			command = command.strip()
			if command.startswith('//') or command == '':
				continue
			parts = command.split()
			if parts[0] in self.arithmetic_logical_commands:
				assembly_code.extend(self.arithmetic_logical_commands[parts[0]]())
			elif parts[0] in ['push', 'pop']:
				assembly_code.extend(self.translate_push_pop(parts))
			else:
				raise ValueError(f"Unknown command: {command}")
		return '\n'.join(assembly_code)
	
	def translate_push_pop(self, parts):
		command, segment, index = parts
		if command == 'push':
			if segment == 'constant':
				return [
				f"@{index}",
				"D=A",
				"@SP",
				"A=M",
				"M=D",
				"@SP",
				"M=M+1"
				]
			else: 
				segment_pointer = self.get_segment_pointer(segment)
				return [
				f"@{segment_pointer}",
				"D=M",
				f"@{index}",
				"A=D+A",
				"D=M",
				"@SP",
				"A=M",
				"M=D",
				"@SP",
				"M=M+1"
				]
		else:
			segment_pointer = self.get_segment_pointer{segment}
			return [
				f"@{segment_pointer",
				"D=M",
				f"@{index}",
				"D=D+A",
				"@R13",
				"M=D",
				"@SP",
				"AM=M-1",
				"D=M",
				"@R13",
				"A=M",
				"M=D"
				]
	
	def get_segment_pointer(self, segment):
		segment_pointers = {
			'local' : 'LCL',
			'argument' : 'ARG',
			'this' : 'THIS',
			'that' : 'THAT',
			'temp' : '5',
			'pointer' : '3'
			}
		return segment_pointers.get(segment, segment)
	
	def translate_add(self):
		return [
			"@SP",
			"AM=M-1",
			"D=M",
			"A=A-1",
			"M=D+M"
			]

