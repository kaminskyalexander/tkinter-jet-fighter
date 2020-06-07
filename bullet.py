from polygon import draw
from vector import Vector2
from entity import Entity

from math import radians, sin, cos

class Bullet(Entity):

	def __init__(self, position, angle):
		self.position = position
		self.angle = angle
		self.speed = 0.02
		self.velocity = Vector2(cos(radians(self.angle)) * self.speed, sin(radians(self.angle)) * self.speed)
		self.lifeSpan = 150
		self.shape = [
			Vector2(-0.02, -0.02),
			Vector2(0.02, -0.02),
			Vector2(0.02, 0.02),
			Vector2(-0.02, 0.02)
		]

	def draw(self, canvas):
		draw(canvas, self.shape, self.position, 0)

	def update(self, canvas):
		self.draw(canvas)
		self.position += self.velocity
		self.screenWrap()
		self.lifeSpan -= 1