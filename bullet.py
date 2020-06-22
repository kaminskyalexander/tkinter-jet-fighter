from math import cos, radians, sin
from random import randrange

from entity import Entity
from polygon import Polygon
from vector import Vector2

class Bullet(Entity):
	"""
	Stores information relevant to in-game bullets.
	"""

	def __init__(self, position, angle):
		"""
		Creates a bullet.

		Arguments:
			position (Vector2): Where the bullet should be located upon creation.
			angle (Vector2): The direction the bullet should travel.
		"""
		self.angle = angle
		self.speed = 0.02
		self.velocity = Vector2(cos(radians(self.angle)) * self.speed, sin(radians(self.angle)) * self.speed)
		self.lifespan = 140
		self.decay = 40
		self.exploded = False
		self.explosionDuration = 30
		# The vertices of the displayed shape
		shape = Polygon(
			Vector2(-0.01, -0.01),
			Vector2(0.01, -0.01), 
			Vector2(0.01, 0.01), 
			Vector2(-0.01, 0.01),
			fill = "#ff5"
		)
		# The vertices shape created upon explosion
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
			fill = "#ff5"
		)
		super().__init__(position, shape)

	def explode(self):
		self.exploded = True

	def update(self, canvas, graphics):
		"""
		This function should be called every frame.
		It transforms and draws the bullet.
		"""
		if self.exploded:
			# Draw the explosion if the bullet has exploded
			self.explosionShape.transform(self.position, 0)
			if graphics: self.explosionShape.draw(canvas)
			self.explosionDuration -= 1
		else:
			# Move the bullet
			self.position += self.velocity
			self.screenWrap()
			self.polygon.transform(self.position, 0)

			if self.lifespan < 0:
				# Make bullets flash as they despawn
				if self.lifespan // 4 % 2 == 0 and graphics:
					self.polygon.draw(canvas)
			elif graphics:
				self.polygon.draw(canvas)

			self.lifespan -= 1
