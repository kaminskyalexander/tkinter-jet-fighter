from math import cos, radians, sin

from setup import *
from vector import Vector2

class Polygon:
	"""
	Base class for most shapes in the game.
	Contains drawing and transforming functionality.
	"""

	def __init__(self, *vertices, **properties):
		"""
		Sets the properties of the polygon.

		Arguments:
			*vertices (Vector2): All vertices of the polygon.
			**properties: Properties passed on to Tkinter.
		"""
		self.vertices = vertices
		self.transformedVertices = vertices[:]
		self.properties = properties

	def draw(self, canvas):
		"""
		Draws the polygon on the supplied canvas.

		Arguments:
			canvas (tk.Canvas): Canvas on which to draw.
		"""
		canvas.create_polygon([pixelFromPosition(vertex) for vertex in self.transformedVertices], **self.properties)

	def drawWireframe(self, canvas, colour):
		"""
		Draws the polygon without fill.
		
		Arguments:
			canvas (tk.Canvas): Canvas on which to draw.
			colour (string): Tkinter format colour of the outline.
		"""
		canvas.create_polygon([pixelFromPosition(vertex) for vertex in self.transformedVertices], fill = "", outline = colour)

	def transform(self, translation, rotationAngle):
		"""
		Transforms the shape into the correct position and rotation on the screen.
		
		Arguments:
			translation (Vector2): Position where to draw the polygon.
			rotationAngle (float): Angle (in degrees) to which the polygon should be rotated.
		"""
		# Convert to radians
		rotationAngle = radians(rotationAngle)

		# Rotation matrix
		matrix = [
			[cos(rotationAngle), -sin(rotationAngle)],
			[sin(rotationAngle),  cos(rotationAngle)]
		]

		# Apply the translation and rotation on each vertex of the polygon
		self.transformedVertices = []
		for vertex in self.vertices:
			newPoint = Vector2(
				vertex.x * matrix[0][0] + vertex.y * matrix[0][1], 
				vertex.x * matrix[1][0] + vertex.y * matrix[1][1]
			)
			newPoint += translation
			self.transformedVertices.append(newPoint)		

	@property
	def uniqueNormals(self):
		"""
		Finds all unique edge normals.

		Returns:
			list: All unique normals.
		"""
		axes = []
		for i in range(len(self.transformedVertices)):
			# Get the current vertex
			p1 = self.transformedVertices[i]
			# Get the next vertex
			p2 = self.transformedVertices[i+1 if i+1 != len(self.transformedVertices) else 0]
			# Subtract the two to get the edge vector
			edge = p1 - p2
			# Get either perpendicular vector
			# (x, y) => (-y, x) or (y, -x)
			normal = Vector2(-edge.y, edge.x)
			# Make sure the normal is unique
			if normal not in axes and -normal not in axes:
				axes.append(normal.normalized)
		return axes

	@property
	def boundingBox(self):
		"""
		Returns a 2D tuple representing an axis aligned box which contains the polygon.

		Example:
			>>> self.boundingBox
			((-1, -1), (1, 1))
		"""
		minX = self.transformedVertices[0].x
		minY = self.transformedVertices[0].y
		maxX = self.transformedVertices[0].x
		maxY = self.transformedVertices[0].y
		for vertex in self.transformedVertices:
			if vertex.x < minX: minX = vertex.x
			if vertex.x > maxX: maxX = vertex.x
			if vertex.y < minY: minY = vertex.y
			if vertex.y > maxY: maxY = vertex.y
		return (minX, minY), (maxX, maxY)
