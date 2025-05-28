#input
scan
- data types (category of values)
	- primitive
	- composite
- statements
	- expression
	- variable (assignment)
	- import
	- return
	- declaration
- expressions
	- arithmetic
	- conditional
- function
- class
- programs/files
	- modules/packages
tokenize DFA regex
AST
create a symbol table
IR code
optimization
linking
#output
#

import re

class TokenType:
	KEYWORD = 'KEYWORD'
	IDENTIFIER = 'IDENTIFIER'
	SYMBOL = 'SYMBOL'
	INTEGER_CONSTANT = 'INTEGER_CONSTANT'
	STRING_CONSTANT = 'STRING_CONSTANT'

class Token:
	def __init__(self, type, value):
		self.type = type
		self.value = value

class Tokenizer:
	def __init__(self, input_string):
		self.tokens = self.tokenize(input_string)
		self.current_token_index = 0
	
	def tokenize(self, input_string):
		token_specification = [
		('KEYWORD', r'\b(int|if|else|while)\b'),
		('IDENTIFIER', r'[a-zA-Z_][a-zA-z0-9_]*'),
		('INTEGER_CONSTANT', r'\d+'),
		('STRING_CONSTANT', r'"[^"]*"'),
		('SYMBOL', r'[{}\(\);=<>+\-*/\]'),
		('SKIP', r'[ \t\n]+'),
		('MISMATCH', r'.'),
		]
		
		tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
		tokens = []
		for mo in re.finditer(tok_regexm input_string):
			kind = mo.lastgroup
			value = mo.group()
			if kind == 'SKIP':
				continue
			elif kind == 'MISMATCH':
				raise RuntimeError(f'Unexpected character: {value}')
			else:
				tokens.append(Token(getattr(TokenType, kind), value))
		return tokens

	def has_more_tokens(self):
	return self.current_token_index < len(self.tokens)

	def advance(self:
		if self.has_more_tokens():
			self.current_token_index += 1
	
	def current_token(self):
		if self.has_more_tokens():
			return self.tokens[self.current_token_index]
		return None

class SymbolTable:
	def __init__(self):
		self.class_table = {}
		self.subroutine_table = {}
		self.index_counters = {'static' : 0, 'field': 0, 'argument': 0, 'local': 0}
	
	def start_subroutine(self):
		self.subroutine_table.clear()
		self.index_counters['argument'] = 0
		self.index_counters['local'] = 0
	
	def define(self, name, type, kind):
		if kind in ['static', 'field']:
			self.class_table[name] = (type, kind, self.index_counters[kind])
		else:
			self.subroutine_table[name] = (type, kind, self.index_counters[kind])
		self.index_counters[kind] += 1
	
	def var_count(self, kind):
		return self.index_counters[kind]
	
	def kind_of(self, name):
		if name in self.subroutine_table:
			return self.subroutine_table[name][1]
		elif name in self.class_table:
			return self.class_table[name][1]
		return None
	
	def type_of(self, name):
		if name in self.subroutine_table:
			return self.subroutine_table[name][0]
		elif name in self.class_table:
			return self.class_table[name][0]
		return None
	
	def index_of(self, name):
		if name in self.subroutine_table:
			return self.subroutine_table[name][2]
		elif name in self.class_table:
			return self.class_table[name][2]
		return None

Class VMWriter:
	def __init__(self):
		self.output = []
	
	def write_push(self, segment, index):
		self.output.append(f"push {segment} {index}")
	
	def write_pop(self, segment, index):
		self.output.append(f"pop {segment} {index}")
	
	def write_arithmetic(self, command):
		self.output.append(command)
	
	def write_label(self, label):
		self.output.append(f"label {label}")
	
	def write_goto(self, label):
		self.output.append(f"goto {label}")
	
	def write_if(self, label):
		self.output.append(f"if-goto {label}")
	
	def write_call(self, name, n_args):
		self.output.append(f"call {name} {n_args}")
	
	def write_function(self, name, n_locals):
		self.output.append(f"function {name} {n_locals}")
	
	def write_return(self):
		self.output.append("return")
	
	def get_output(self):
		return '\n'.join(self.output)

Class Compiler:
	def __init__(self, tokenizer):
		self.tokenizer = tokenizer
		self.symbol_table = SymbolTable()
		self.vm_writer = VMWriter()
		self.class_name = ""
		self.label_counter = 0
	
	def compile(self):
		self.compile_class()
		return self.vm_writer.get_output()
	
	def compile_class(self):
		self.eat('class')
		self.class_name = self.eat(TokenType.IDENTIFIER)
		self.eat('{')
		while self.tokenizer.current_token().value in ['static', 'field']:
			self.compile_class_var_dec()
		while self.tokenizer.current_token().value in ['constructor', 'function', 'method']:
			self.compile_subroutine()
		self.eat('}')
	
	def compile_class_var_dec(self):
		kind = self.eat(['static', 'field'])
		type = self.eat([TokenType.IDENTIFIER, 'int', 'char', 'boolean'])
		name = self.eat(TokenType.IDENTIFIER)
		self.symbol_table.define(name, type, kind)
		while self.tokenizer.current_token().value == ',':
			self.eat(',')
			name = self.eat(TokenType.IDENTIFIER)
			self.symbol_table.define(name, type, kind)
		self.eat(';')

	def compile_subroutine(self):
		self.symbol_table.start_subroutine()
		subroutine_type = self.eat(['constructor', 'function', 'method'])
		return_type = self.eat([TokeType.IDENTIFIER, 'void', 'int', 'char', 'boolean'])
		name = self.eat(TokenType.IDENTIFIER)
		self.eat('(')
		self.compile_parameter_list()
		self.eat(')')
		self.compile_subroutine_body(f"{self.class_name}.{name}")

	def compile_parameter_list(self):
		if self.tokenizer.current_token().value != ')':
		type = self.eat(TokenType.IDENTIFIER, 'int', 'char', 'boolean'])
		name = self.eat(TokenType.IDENTIFIER)
		self.symbol_table.define(name, type, 'argument')
		while self.tokenizer.current_token().value == ',':
			self.eat(',')
			type = self.eat([TokenType,IDENTIFIER, 'int', 'char', 'boolean'])
			name = self.eat(TokenType.IDENTIFIER)
			self.symbol_table.define(name, type, 'argument')
	
	def compile_subroutine_body(self, function_name):
		self.eat('{')
		while self.tokenizer.current_token().value == 'var':
			self.compile_var_dec()
		self.vm_writer.write_function(function_name, self.symbol_table.var_count('local'))
		self.compile_statements()
		self.eat('}')
	
	def compile_var_dec(self):
		self.eat('var')
		type = self.eat([TokenType.IDENTIFIER, 'int', 'char', 'boolean'])
		name = self.eat(TokenType.IDENTIFIER)
		self.symbol_table.define(name, type, 'local')
		while self.tokenizer.current_token().value == ',':
			self.eat(',')
			name = self.eat(TokenType.IDENTIFIER)
			self.symbol_table.define(name, type, 'local')
		self.eat(';')
	
	def compile_statements(self):
		while self.tokenizer.current_token().value in ['let', 'if', 'while', 'do', 'return']:
			if self.tokenizer.current_token().value == 'let':
				self.compile_let()
			elif self.tokenizer.current_token().value == 'if':
				self.compile_if()
			elif self.tokenizer.current_token().value == 'while':
				self.compile_while()
			elif self.tokenizer.current_token().value == 'do':
				self.compile_do()
			elif self.tokenizer.current_token().value == 'return':
				self.compile_return()
	
	def compile_let(self):
		self.eat('let')
		var_name = self.eat(TokenType.IDENTIFIER)
		if self.tokenizer.current_token().value == '[':
			self.eat('[')
			self.compile_expression()
			self.eat(']')
			self.vm_writer.write_push(self.symbol_table.kind_of(var_name), self.symbol_table.index_of(var_name))
			self.vm_writer.write_arithmetic('add')
			self.eat('=')
			self.compile_expression()
			self.vm_writer.write_pop('temp', 0)
			self.vm_writer.write_pop('pointer', 1)
			self.vm_writer.write_push('temp', 0)
			self.vm_writer.write_push('that', 0)
		else:
			self.eat('=')
			self.compile_expression()
			self.vm_writer.write_pop(self.symbol_table.kind_of(var_name), self.symbol_table.index_of(var_name))
			self.eat(';')
	
	def compile_if(self):
		self.eat('if')
		label_true = self.new_label()
		label_false = self.new_label()
		label_end = self.new_label()
		self.eat('(')
		self.compile_expression()
		self.eat(')')
		self.vm_writer.write_if(label_true)
		self.vm_writer.write_goto(label_false)
		self.vm_writer.write_label(label_true)
		self.eat('{')
		self.compile_statements()
		self.eat('}')
		self.vm_writer.write_goto(label_end)
		self.vm_writer.write_label(label_false)
		if self.tokenizer.current_token().value == 'else':
			self.eat('else')
			self.eat('{')
			self.compile_statements()
			self.eat('}')
		self.vm_writer.write_label(label_end)
	
	def compile_while(self):

	def compile_do(self):

	def compile_return(self):

	def compile_expression(self):

	def compile term(self):

	def compile_subroutine_call(self):

	def compile_epxression_list(self):
	
	def eat(self, expected):
		token = self.tokenizer.current_token()
		if isinstance(expected, list):
			if token.type in expected or token.value in expected:
				self.tokenizer.advance()
				return token.value
		elif token.type == expected or token.value == expected:
			self.tokenizer.advance()
			return token.value
		raise SyntaxError(f"Expected {expected}, got {token.value}")
	
	def new_label(self):
		label = f"LABEL_{self.label_counter}"
		self.label_counter += 1
		return label
