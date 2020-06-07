from math import cos, sin, radians

from vector import Vector2
from entity import Entity 
from polygon import Polygon

from bullet import Bullet

class Player(Entity):

	def __init__(self, position):
		self.angle = 0
		self.speed = 0.01
		self.bullets = []
		shape = Polygon(Vector2(-0.1, 0.1),	Vector2(-0.1, -0.1), Vector2(0.1, 0), fill = "red")
		super().__init__(position, shape)

	def shoot(self):
		self.bullets.append(Bullet(self.position, self.angle))

	def update(self, canvas):
		velocity = Vector2(cos(radians(self.angle)) * self.speed, sin(radians(self.angle)) * self.speed)
		self.position += velocity
		self.screenWrap()

		for bullet in self.bullets:
			if bullet.lifespan == 0:
				self.bullets.remove(bullet)
			bullet.update(canvas)

		self.polygon.transform(self.position, self.angle)
		self.polygon.draw(canvas)
