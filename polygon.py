from setup import *
from math import sin, cos, radians
from vector import Vector2

def pixelFromPosition(vector):
	# Get the size of the window
	width = canvas.winfo_width()
	height = canvas.winfo_height()
	# Get the coordinates in pixels based on the window width and height
	# This should let the window be stretchable
	x = (width/2)  + (height/2) * vector.x
	y = (height/2) + (height/2) * vector.y
	return x, y

class Polygon:

	def __init__(self, *vertices, **properties):
		self.vertices = vertices
		self.transformedVertices = vertices[:]
		self.properties = properties

	def draw(self, canvas):
		canvas.create_polygon([pixelFromPosition(vertex) for vertex in self.transformedVertices], **self.properties)

	def drawWireframe(self, canvas, color):
		canvas.create_polygon([pixelFromPosition(vertex) for vertex in self.transformedVertices], fill = "", outline = color)

	def transform(self, translation, rotationAngle):
		rotationAngle = radians(rotationAngle)

		matrix = [
			[cos(rotationAngle), -sin(rotationAngle)],
			[sin(rotationAngle),  cos(rotationAngle)]
		]

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