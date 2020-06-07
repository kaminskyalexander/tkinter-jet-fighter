from polygon import Polygon
from vector import Vector2
from entity import Entity

from math import radians, sin, cos

class Bullet(Entity):

	def __init__(self, position, angle):
		self.angle = angle
		self.speed = 0.02
		self.velocity = Vector2(cos(radians(self.angle)) * self.speed, sin(radians(self.angle)) * self.speed)
		self.lifespan = 150
		shape = Polygon(
			Vector2(-0.02, -0.02),
			Vector2(0.02, -0.02), 
			Vector2(0.02, 0.02), 
			Vector2(-0.02, 0.02),
			fill = "green"
		)
		super().__init__(position, shape)

	def update(self, canvas):
		self.position += self.velocity
		self.screenWrap()
		self.lifespan -= 1

		self.polygon.transform(self.position, 0)
		self.polygon.draw(canvas)