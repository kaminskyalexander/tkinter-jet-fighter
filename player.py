from math import cos, sin, radians

from vector import Vector2
from entity import Entity 
from polygon import Polygon

from bullet import Bullet

class Player(Entity):

	def __init__(self, position, angle):
		self.angle = angle
		self.speed = 0.01
		self.timeout = 0
		self.bullets = []
		shape = Polygon(Vector2(-0.1, 0.1),	Vector2(-0.1, -0.1), Vector2(0.1, 0), fill = "red")
		super().__init__(position, shape)

	def shoot(self, bullets):
		bulletDistance = 0.2
		bulletPosition = Vector2(cos(radians(self.angle)) * bulletDistance, sin(radians(self.angle)) * bulletDistance)
		bullets.append(Bullet(self.position + bulletPosition, self.angle))

	def explode(self):
		self.timeout = 30

	def update(self, canvas):
		
		if self.timeout > 0:
			self.timeout -= 1
		else:
			velocity = Vector2(cos(radians(self.angle)) * self.speed, sin(radians(self.angle)) * self.speed)
			self.position += velocity

		self.polygon.transform(self.position, self.angle)
		self.polygon.draw(canvas)

		self.screenWrap()