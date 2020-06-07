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
	
	def draw(self, canvas):
		draw(canvas, self.shape, self.position, self.angle)

	def update(self, canvas):
		self.draw(canvas)
		velocity = Vector2(cos(radians(self.angle)) * self.speed, sin(radians(self.angle)) * self.speed)
		self.position += velocity

		if self.position.x > 1.1: self.position.x = -1.1
		if self.position.x < -1.1: self.position.x = 1.1
		if self.position.y > 1.1: self.position.y = -1.1
		if self.position.y < -1.1: self.position.y = 1.1
