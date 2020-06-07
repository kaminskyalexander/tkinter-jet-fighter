from vector import Vector2

class SAT:

	@staticmethod
	def detectCollision(polygon1, polygon2):
		axes = polygon1.uniqueNormals + polygon2.uniqueNormals

		for axis in axes:
			p1 = SAT.projectShapeOntoAxis(axis, polygon1)
			p2 = SAT.projectShapeOntoAxis(axis, polygon2)
			if not SAT.detectOverlap(p1, p2):
				return False

		return True

	@staticmethod
	def projectShapeOntoAxis(axis, polygon):
		minimum = Vector2.dot(axis, polygon.transformedVertices[0])
		maximum = minimum
		for vertex in polygon.transformedVertices:
			p = Vector2.dot(axis, vertex)
			if p < minimum: minimum = p
			if p > maximum: maximum = p
		return minimum, maximum

	@staticmethod
	def detectOverlap(projection1, projection2):
		min1, max1 = projection1
		min2, max2 = projection2
		return max1 > min2 and min1 < max2
