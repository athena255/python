 # calc3.py
"""Calculator Program that stores the structure of its statements in an AST

**Mostly works but does not support left associative...**
Example Usage: 
	> x = 5
	> y = 6
	> x + y
		-> 11
	> x > y
		-> False
	> z = x + y
	> z == x
		-> False
	> x
		-> 5

Structure of the Expression is evaluated in the creation of its objects

"""
import re

class Calc:
	"""Represents a Calculator that takes inputs of statements and prints outputs
	Stores user defiend variables and evaluates expressions

	"""
	def __init__(self):
		self.variables = {}

	def assign(self, identifier, val):
		"""Adds a variable, value pair to calculator memory
		Variables may be reassigned

		Args:
			identifier: String to be associated with the value
			val: numeric value (float, int, Boolean etc)

		"""
		assert Expr.isNum(identifier) == False # check that the identifier is not a number

		self.variables[identifier] = val

	def parse(self, tokens):
		"""Evaluates the tokens and returns its numeric/boolean value if applicable
		Assigns the variable, value pair if statement is an assignment expression
		All variables in original tokens have been replaced with its numeric value
			(1) Assignment: identifier = expr
				x = 5
				y = x + 1
			(2) Evaluate: expr 
				4 + 5
				4 + x
				x
				5
		"""

		#Replaces all variables with its dictionary value
		for idx, t in enumerate(tokens): 
			if t in self.variables: 
				tokens[idx] = self.variables[t]

		if len(tokens) == 1:
			# User input is a numeric value (5) or some variable (x)
			return tokens[0]
		elif tokens[1] == "=":
			try: 
				self.assign(tokens[0], EqExpr(tokens[2::]).val) # x=5+6  -> Expr(5 + 6)
			except:
				raise SyntaxError("Syntax Error in assignment of variable: {}".format(tokens[0]))
		else: 
			return EqExpr(tokens) # 5 + 6 -> Expr(5 + 6)


	@staticmethod
	def tokenize(stmt):
		"""Returns a list of tokens derived from stmt
		Ex: x = y + 5
			['x', '=', 'y', '+', '5']
		"""
		reg = re.compile('(\d+|[^0-9])')
		tokens = re.findall(reg, stmt)
		assert len(tokens) > 0
		return tokens



	def run(self):
		"""Runs the main calculator program"""
		while True: 
			stmt = input(">").replace(" ", "")
			tokens = Calc.tokenize(stmt)
			res = self.parse(tokens)
			if res is not None:
				print("    -> {}".format(res))

class Expr:
	"""Expression superclass 
	All subclasses have a self.val that evaluates to some numeric/boolean value
	
	"""

	@staticmethod
	def isNum(val):
		try: 
			val = float(val)
			return True
		except:
			return False

	def __ne__(self, other):
		return self.val != other.val

	def __eq__(self,other):
		return self.val == other.val

	def __lt__(self, other):
		return self.val < other.val

	def __le__(self, other):
		return self.val <= other.val

	def __gt__(self, other):
		return self.val > other.val

	def __ge__(self, other):
		return self.val >= other.val

	def __add__(self, other):
		return self.val + other.val

	def __sub__(self, other):
		return self.val - other.val

	def __mul__(self, other):
		return self.val * other.val

	def __truediv__(self, other):
		return self.val / other.val

	def __str__(self):
		return str(self.val)

class EqExpr(Expr):
	"""Equality Expression: EqExpr -> RelExpr | EqExpr != RelExpr | EqExpr == RelExpr"""
	def __init__(self, tokens):

		print("EqExpr", tokens)
		rel_expr = RelExpr(tokens)

		if len(tokens) < 1: 
			self.val = rel_expr.val
			return

		op = tokens[0]

		if op == '!': #tokens splits '!=' to '!' and '='
			tokens.pop(0)
			tokens.pop(0)
			eq_expr = EqExpr(tokens)
			self.val = rel_expr != eq_expr
			
		elif op == '=':
			tokens.pop(0)
			tokens.pop(0)
			eq_expr = EqExpr(tokens)
			self.val = rel_expr == eq_expr
		else:
			self.val = rel_expr.val
		print("eq self.val", self.val)

class RelExpr(Expr): 
	"""Relational Expression: RelExpr -> AddExpr | RelExpr < AddExpr | RelExpr > AddExpr
								| RelExpr >= AddExpr | RelExpr <= AddExpr
	"""
	def __init__(self,tokens):

		print("RelExpr", tokens)
		add_expr = AddExpr(tokens)

		if len(tokens) < 1:
			self.val = add_expr.val
			return

		op = tokens[0]
		if op == '>':
			if tokens[1] == '=': # >=
				tokens.pop(0)
				tokens.pop(0)
				rel_expr = RelExpr(tokens)
				self.val = add_expr >= rel_expr
			else:
				tokens.pop(0)
				rel_expr = RelExpr(tokens)
				self.val = add_expr > rel_expr

		elif op == '<': 
			if tokens[1] == '=':
				tokens.pop(0)
				tokens.pop(0)
				rel_expr = RelExpr(tokens)
				self.val = add_expr <= rel_expr
			else:
				tokens.pop(0)
				rel_expr = RelExpr(tokens)
				self.val = add_expr < rel_expr
		else:
			self.val = add_expr.val
		print("rel self.val", self.val)

class AddExpr(Expr):
	"""Additive Expression: AddExpr -> MulExpr | AddExpr + MulExpr | AddExpr - MulExpr
	"""
	def __init__(self,tokens):
		print("AddExpr", tokens)
		mul_expr = MulExpr(tokens)

		if len(tokens) < 1:
			self.val = mul_expr.val
			return

		op = tokens[0]
		if op == '+':
			tokens.pop(0)
			add_expr = AddExpr(tokens)
			self.val = mul_expr + add_expr

		elif op == '-':
			tokens.pop(0)
			add_expr = AddExpr(tokens)
			self.val = mul_expr - add_expr
		else:
			self.val = mul_expr.val
		print("add self.val", self.val)



class MulExpr(Expr):
	"""Multiplicative Expression: MulExpr -> Factor | MulExpr * Factor | MulExpr / Factor 
	"""
	def __init__(self,tokens):
		print("MulExpr", tokens)
		fac = Factor(tokens)

		if len(tokens) < 1:
			self.val = fac.val
			return

		op = tokens[0]
		if op == '*':
			tokens.pop(0)
			mul_expr = MulExpr(tokens)
			self.val = fac * mul_expr
		elif op == '/':
			tokens.pop(0)
			mul_expr = MulExpr(tokens)
			self.val = fac / mul_expr
		else:
			self.val = fac.val
		print("mul self.val", self.val)
			

class Factor(Expr):
	"""Factor -> (-) Number | (-) (AddExpr)"""
	def __init__(self,tokens):
		print("Factor", tokens)
		self.negflag = False
		if len(tokens) == 1:
			self.val = float(tokens[0])
			return
		if tokens[0] == '-':
			self.negflag = True
			tokens.pop(0) # consume '-'

		if tokens[0] == '(':
			tokens.pop(0)
			add_expr = AddExpr(tokens)
			tokens.pop(0) # consume ')'
			self.val = self.sign(add_expr.val)
		else:
			self.val = self.sign(float(tokens[0]))
			tokens.pop(0)
		print("fac self.val", self.val)

			
	def sign(self, val):
		"""Handle negative numbers or expressions"""
		if self.negflag == True:
			return (-val)
		else:
			return val



# Testing

mycalc = Calc()
mycalc.run()





