from polygon import Polygon
from vector import Vector2
from entity import Entity

from math import radians, sin, cos
from random import randrange

class Bullet(Entity):

	def __init__(self, position, angle):
		self.angle = angle
		self.speed = 0.02
		self.velocity = Vector2(cos(radians(self.angle)) * self.speed, sin(radians(self.angle)) * self.speed)
		self.lifespan = 140
		self.decay = 40
		self.exploded = False
		self.explosionDuration = 30
		shape = Polygon(
			Vector2(-0.01, -0.01),
			Vector2(0.01, -0.01), 
			Vector2(0.01, 0.01), 
			Vector2(-0.01, 0.01),
			fill = "yellow"
		)
		self.explosionShape = Polygon(
			Vector2( .000000,  .100000),
			Vector2( .018588,  .044876), 
			Vector2( .070711,  .070711),
			Vector2( .044876,  .018588),
			Vector2( .100000,  .000000),
			Vector2( .044876, -.018588),
			Vector2( .070711, -.070711),
			Vector2( .018588, -.044876),
			Vector2( .000000, -.100000),
			Vector2(-.018588, -.044876), 
			Vector2(-.070711, -.070711),
			Vector2(-.044876, -.018588),
			Vector2(-.100000,  .000000),
			Vector2(-.044876,  .018588),
			Vector2(-.070711,  .070711),
			Vector2(-.018588,  .044876),
			fill = "yellow"
		)
		super().__init__(position, shape)

	def explode(self):
		self.exploded = True

	def update(self, canvas):

		if self.exploded:
			self.explosionShape.transform(self.position, 0)
			self.explosionShape.draw(canvas)
			self.explosionDuration -= 1
		else:
			self.position += self.velocity
			self.screenWrap()
			self.polygon.transform(self.position, 0)

			if self.lifespan < 0:
				# Make bullets flash as they despawn
				if self.lifespan // 4 % 2 == 0:
					self.polygon.draw(canvas)
			else:
				self.polygon.draw(canvas)

			self.lifespan -= 1