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
	
Class SyntaxAnalyzer:
	def __init__(self, tokenizer):
		self.tokenizer = tokenizer
		self.xml_output = []
		self.indent_level = 0
	
	def parse(self):
		self.program()
		return '\n'.join(self.xml_output)

	def program(self):
		self.write_tag('program')
		self.indent_level += 1
		while self.tokenizer.has_more_tokens():
			self.statement()
		self.indent_level -= 1
		self.write_tag('/program')

	def statement(self):
		token = self.tokenizer.current_token()
		if token.value == 'int':
			self.var_declaration()
		elif token.type == TokenType.IDENTIFIER:
			self.assigment()
		elif token.value == 'if':
			self.if_statement()
		elif token.value == 'while':
			self.while_statement()
		else:
			raise SyntaxError(f"Unexpected token: {token.value}")
	
	def var_declaration(self):
		self.write_tag('varDeclaration')
		self.indent_level += 1
		self.eat('int)
		self.eat(TokenType.IDENTIFIER)
		self.eat(';')
		self.indent_level -= 1
		self.write_tag('/varDeclaration')
	
	def assignment(self):
		self.write_tag('assigment')
		self.indent_level += 1
		self.eat(TokenType.IDENTIFIER)
		self.eat('=')
		self.expression()
		self.eat(';')
		self.indent_level -= 1
		self.write_tag('/assignment')
	
	def if_statement(self):
		self.write_tag('ifStatement')
		self.indent_level += 1
		self.eat('if')
		self.eat('(')
		self.expression()
		self.eat(')')
		self.eat('{')
		while self.tokenizer.current_token().value != '}':
			self.statement()
		self.eat('}')
		if self.tokenizer.current_token().value == 'else':
			self.eat('else')
			self.eat('{')
			while self.tokenizer.current_token().value != '}':
				self.statement()
			self.eat('}')
		self.indent_level -= 1
		self.write_tag('/ifStatement')

	def while_statement(self):
		self.write_tag('whileStatement')
		self.indent_level += 1
		self.eat('while')
		self.eat('(')
		self.expression()
		self.eat(')')
		self.eat('{')
		while self.tokenizer.current_token().value != '}':
			self.statement()
		self.eat('}')
		self.indent_level -= 1
		self.write_tag('/whileStatement')

	def expression(self):
		self.write_tag('expression')
		self.indent_level += 1
		self.term()
		while self.tokenizer.current_token().value in ['+', '-', '*', '/']:
			self.eat(self.tokenizer.current_token().value)
			self.term()
		self.indent_level -= 1
		self.write_tag('/expression')

	def term(self):
		self.write_tag('term')
		self.indent_level += 1
		token = self.tokenizer.current_token()
		if token.type == TokenType.INTEGER_CONSTANT:
			self.eat(TokenType.INTEGER_CONSTANT)
		self.indent_level -= 1
		self.write_tag('/term')
	
	def eat(self, expected):
		token = self.tokenizer.current_token()
		if isinstance(expected, str) and token.value == expected:
			self.write_leaf(token)
			self.tokenizer.advance()
		elif token.type == expected:
			self.write_leaf(token)
			self.tokenizer.advance()
		else:
			raise SyntaxError(f"Expected {expected}, got {token.value}")
	
	def write_tag(self, tag):
		self.xml_output.append('  ' * self.indent_level + f'<{tag}>')

	def write_leaf(self, token):
		escaped_value = token.value.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
		self.xml_output.append('  ' * (self.indent_level + 1) + f'<{token.type}> {escaped_value} </{token.type}>')
