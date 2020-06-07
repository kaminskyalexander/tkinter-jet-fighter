from math import cos, sin, radians

from vector import Vector2
from polygon import draw

class Player:

	def __init__(self, x, y):
		self.position = Vector2(x, y)
		self.angle = 0
		self.speed = 0.01
		self.shape = [
			Vector2(-0.1, 0.1),
			Vector2(-0.1, -0.1),
			Vector2(0.1, 0),
		]

	@property
	def boundingBox(self):
		minX = self.shape[0].x
		minY = self.shape[0].y
		maxX = self.shape[0].x
		maxY = self.shape[0].y
		for vertex in self.shape:
			if vertex.x < minX: minX = vertex.x
			if vertex.x > maxX: maxX = vertex.x
			if vertex.y < minY: minY = vertex.y
			if vertex.y > maxY: maxY = vertex.y
		return (minX, minY), (maxX, maxY)

	def screenWrap(self):
		boundingBox = self.boundingBox
		playerWidth = (boundingBox[1][0] - boundingBox[0][0]) / 2
		playerHeight = (boundingBox[1][1] - boundingBox[0][1]) / 2

		if self.position.x >  1 + playerWidth:  self.position.x = -1 - playerWidth
		if self.position.x < -1 - playerWidth:  self.position.x =  1 + playerWidth
		if self.position.y >  1 + playerHeight: self.position.y = -1 - playerHeight
		if self.position.y < -1 - playerHeight: self.position.y =  1 + playerHeight
		
	def draw(self, canvas):
		draw(canvas, self.shape, self.position, self.angle)

	def update(self, canvas):
		self.draw(canvas)
		velocity = Vector2(cos(radians(self.angle)) * self.speed, sin(radians(self.angle)) * self.speed)
		self.position += velocity
		self.screenWrap()
