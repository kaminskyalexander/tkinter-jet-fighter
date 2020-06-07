from math import cos, sin, radians

from vector import Vector2
from entity import Entity 
from polygon import draw

from bullet import Bullet

class Player(Entity):

	def __init__(self, x, y):
		self.position = Vector2(x, y)
		self.angle = 0
		self.speed = 0.01
		self.shape = [
			Vector2(-0.1, 0.1),
			Vector2(-0.1, -0.1),
			Vector2(0.1, 0),
		]
		self.bullets = []
		
	def draw(self, canvas):
		draw(canvas, self.shape, self.position, self.angle)

	def shoot(self):
		self.bullets.append(Bullet(self.position, self.angle))

	def update(self, canvas):
		self.draw(canvas)
		velocity = Vector2(cos(radians(self.angle)) * self.speed, sin(radians(self.angle)) * self.speed)
		self.position += velocity
		self.screenWrap()
		for bullet in self.bullets:
			if bullet.lifeSpan == 0:
				self.bullets.remove(bullet)
			bullet.update(canvas)
