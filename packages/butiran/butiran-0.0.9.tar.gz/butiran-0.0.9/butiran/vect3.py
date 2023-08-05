"""
	A 3-d vector for butiran
	Sparisoma Viridi | https://github.com/dudung
"""
#	
#	Vect3.py
#	A 3-d vector for butiran.
#	
#	Sparisoma Viridi | https://github.com/dudung
#	
#	20210206
#	1318 Start creating in-house Python package according to [1].
#	1322 Create class of Vect3 as explained [2].
# 1341 Finally it works but cannot without argument.
# 1347 Fix it and it works without arguments using None [3].
# 1405 Create and test add function.
# 1408 Use multiline comments in hard way [4] dan try [5].
# 1426 Find this but can not read [6] today due to limitation.
#	1433 Use the terms attribute and function in a class [7].
# 1447 Create sub and test it. It works.
#	1449 Create dot, test it, and it is ok.
#	1452 Create cross and it works.
# 1503 Problem by mul due to different arguments types.
# 1509 Done with mul (scalar, Vect3) and (Vect3, scalar).
# 1512 Done with div and it works after test.
# 1523 Set .gitignore for butiran compiled bytecode [8].
#	1527 Change to_str to strval as in JS and C++.
# 1558 Finish len and unit, even the first works fortunately.
# 1604 Finish neg function and test it. It is ok.
#	1604 Add note and finalize this class.
#	1616 Move to math subfolder different than the other version.
# 1620 Document [9] that is used for mul.
#	1623 Add sys for module search path [10] for test file.
#	1626 Forget [11] but already implement naming convention.
#	20210207
#	0827 Put additional comment for mul function.
#	
#	References
#	1. Jason Dzouza, "How to Build Your Very First Python Package", freeCodeCamp, 27 Oct 2020, url https://www.freecodecamp.org/news/build-your-first-python-package/ [20210206].
#	2. -, "Python Classes and Objects", W3Schools, url https://www.w3schools.com/python/python_classes.asp [20210206].
#	3. jamylac, "Answer to 'How to allow __init__ to allow 1 or no parameters in python'", StackOverflow, 20 Apr 2013 at 03:17, url https://stackoverflow.com/a/16116166 [20210206].
#	4. Dan Baser, "Python Multi-line Comments: Your Two Best Options", DBader.org, 2018, url https://dbader.org/blog/python-multiline-comment [20210206].
#	5.  Wikipedia contributors, "Docstring", Wikipedia, The Free Encyclopedia, 28 Nov 2020, 13:46 UTC, url https://en.wikipedia.org/w/index.php?oldid=991140087 [20210206].
#	6. Yong Cui, "Declare Your First Python Class — Understand 3 Basic Components: Better organize your code using custom classes", The Startup, 24 May 2020, url https://medium.com/swlh/declare-your-first-python-class-understand-3-basic-components-15768c8d35b0 [20210206].
#	7. Karleigh Moore, Evans Njeru, Matas Pocevicius, ChongHeng Tan, N A, B! C, Jimin Khim, "Classes (OOP)", Brillian, url https://brilliant.org/wiki/classes-oop/ [20210206].
#	8. fmaline, "Answer to 'What is __pycache__?'", StackOverflow, 6 Feb 2015 at 11:52, url https://stackoverflow.com/a/28365204 [20210206].
#	9. Johannes Weiss, "Answer to 'Type checking of arguments Python [duplicate]'", StackOverflow, 9 Apr 2009 at 14:00, url https://stackoverflow.com/a/734385 [20210206].
#	10. Shibero, "Answer to 'Importing modules from parent folder'", StackOverflow, 29 Jan 2020 at 04:06, url https://stackoverflow.com/a/28712742 [20210206].
#	11. Jasmine Finer, "How to Write Beautiful Python Code With PEP 8", Real Python, 2019, url https://realpython.com/python-pep8/ [20210206].
#	
#	Notes
#	1. That l = sqrt(self.dot(self)) is confusing, even it works.
#	

from numpy import sqrt

class Vect3:
	"""Vect3 class has 3 attributes and 3 functions"""
	def __init__(self, x=None, y=None, z=None):
		"""Initialize with 3 arguments or none"""
		if x is None: 
			self.x = 0
		else:
			self.x = x
		if y is None: 
			self.y = 0
		else:
			self.y = y
		if z is None: 
			self.z = 0
		else:
			self.z = z
	
	def strval(self):
		"""Get string value of Vect3 instance"""
		x = str(self.x)
		y = str(self.y)
		z = str(self.z)
		s = "(" + x + ", " + y + ", " + z + ")"
		return s
	
	def add(v1, v2):
		"""Add two Vect3 instances"""
		x = v1.x + v2.x
		y = v1.y + v2.y
		z = v1.z + v2.z
		v3 = Vect3(x, y, z)
		return v3
	
	def sub(v1, v2):
		"""Substract two Vect3 instances"""
		x = v1.x - v2.x
		y = v1.y - v2.y
		z = v1.z - v2.z
		v3 = Vect3(x, y, z)
		return v3
		
	def dot(v1, v2):
		"""Dot product of two Vect3 instances"""
		a = v1.x * v2.x
		b = v1.y * v2.y
		c = v1.z * v2.z
		d = a + b + c
		return d
	
	def cross(v1, v2):
		"""Cross product of two Vect3 instances"""
		x = v1.y * v2.z - v1.z * v2.y
		y = v1.z * v2.x - v1.x * v2.z
		z = v1.x * v2.y - v1.y * v2.x
		v3 = Vect3(x, y, z)
		return v3
	
	def mul(v1, v2):
		"""Multiply a scalar with a Vect3 instance (or vice versa)"""
		b1 = isinstance(v1, Vect3)
		b2 = isinstance(v2, Vect3)
		v3 = Vect3()
		if b1 and not b2:
			v3.x = v1.x * v2
			v3.y = v1.y * v2
			v3.z = v1.z * v2
		elif not b1 and b2:
			v3.x = v1 * v2.x
			v3.y = v1 * v2.y
			v3.z = v1 * v2.z
		return v3
	
	def div(v, a):
		"""Divide a Vect3 instance with a scalar"""
		x = v.x / a
		y = v.y / a
		z = v.z / a
		w = Vect3(x, y, z)
		return w
	
	def len(self):
		"""Get length or magnitude of a Vect3 instance"""
		x = self.x
		y = self.y
		z = self.z
		l = sqrt(self.dot(self))
		return l
	
	def unit(self):
		"""Get unit vector of a Vect3 instance"""
		l = self.len()
		v = Vect3()
		v.x = self.x / l
		v.y = self.y / l
		v.z = self.z / l
		return v
	
	def neg(self):
		"""Set a Vect3 instance to opposite direction"""
		v = Vect3()
		v.x = -self.x
		v.y = -self.y
		v.z = -self.z
		return v
