from math import sqrt

class Vector2:
	"""
	Two dimensional vector.
	Supports adding, subtracting, multiplying, dividing, comparisons, etc.
	"""

	def __init__(self, x, y):
		self.x = x
		self.y = y

	@property
	def normalized(self):
		"""
		Normalizes the vector (sets it to a length of 1)
		"""
		length = sqrt(self.x**2 + self.y**2)
		if length == 0: return self
		else: return self / length

	def normalize(self):
		self.x, self.y = self.normalized

	@staticmethod
	def dot(vector1, vector2):
		"""
		Finds the dot product of two vectors.
		"""
		return round(sum(vector1 * vector2), 5)

	def __add__(self, other):
		if isinstance(other, Vector2):
			return Vector2(
				self.x + other.x,
				self.y + other.y,
			)
		else:
			return Vector2(
				self.x + other,
				self.y + other,
			)

	def __sub__(self, other):
		if isinstance(other, Vector2):
			return Vector2(
				self.x - other.x,
				self.y - other.y,
			)
		else:
			return Vector2(
				self.x - other,
				self.y - other,
			)

	def __mul__(self, other):
		if isinstance(other, Vector2):
			return Vector2(
				self.x * other.x,
				self.y * other.y,
			)
		else:
			return Vector2(
				self.x * other,
				self.y * other,
			)

	def __truediv__(self, other):
		if isinstance(other, Vector2):
			return Vector2(
				self.x / other.x,
				self.y / other.y,
			)
		else:
			return Vector2(
				self.x / other,
				self.y / other,
			)

	def __neg__(self):
		return self * -1

	def __abs__(self):
		return Vector2(
			abs(self.x),
			abs(self.y),
		)

	def __str__(self):
		return "({}, {})".format(self.x, self.y)

	def __iter__(self):
		return iter((self.x, self.y))

	def __eq__(self, other):
		return (self.x == other.x) and (self.y == other.y)