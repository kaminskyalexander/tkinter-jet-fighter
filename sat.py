from vector import Vector2

class SAT:
	"""
	Container class for SAT (Seperating Axis Theorem) collision detection functions.
	"""

	@staticmethod
	def detectCollision(polygon1, polygon2):
		"""
		Detects collision between two polygons.

		Arguments:
			polygon1 (Polygon): Polygon to be checked against polygon2.
			polygon2 (Polygon): Polygon to be checked against polygon1.
		
		Returns:
			bool: True if a collision is detected.
		"""
		# All axes to check overlap on
		axes = polygon1.uniqueNormals + polygon2.uniqueNormals

		for axis in axes:
			# Project shapes on each axis
			p1 = SAT.projectShapeOntoAxis(axis, polygon1)
			p2 = SAT.projectShapeOntoAxis(axis, polygon2)
			# A gap is found, which means there is no collision
			if not SAT.detectOverlap(p1, p2):
				return False
		
		return True

	@staticmethod
	def projectShapeOntoAxis(axis, polygon):
		"""
		Projects polygons onto axis.

		Arguments:
			polygon: Polygon to be projected.

		Returns:
			tuple:float: Minimum and maximum point on the projection.
		"""
		minimum = Vector2.dot(axis, polygon.transformedVertices[0])
		maximum = minimum
		for vertex in polygon.transformedVertices:
			p = Vector2.dot(axis, vertex)
			if p < minimum: minimum = p
			if p > maximum: maximum = p
		return minimum, maximum

	@staticmethod
	def detectOverlap(projection1, projection2):
		"""
		Detects overlap of two projections.

		Arguments:
			projection1 (tuple: float): Contains the minimum and maximum points of the first projection.
			projection2 (tuple: float): Contains the minimum and maximum points of the second projection.

		Returns:
			bool: True if an overlap is detected.
		"""
		min1, max1 = projection1
		min2, max2 = projection2
		return max1 > min2 and min1 < max2
