from math import cos, sin, radians
from random import randrange

from vector import Vector2
from entity import Entity 
from polygon import Polygon

from bullet import Bullet

class Player(Entity):

	def __init__(self, position, angle):
		self.angle = angle
		self.speed = 0.01
		self.acceleration = 0.0001
		self.maximumSpeed = 0.015
		self.minimumSpeed = 0.005
		self.steeringRate = 2
		self.timeout = 0
		self.bullets = []
		self.score = 0
		shape = Polygon(Vector2(-0.1, 0.1),	Vector2(-0.1, -0.1), Vector2(0.1, 0), fill = "red")
		super().__init__(position, shape)

	def adjustSpeed(self, speed):
		if self.timeout == 0:
			self.speed = max(self.minimumSpeed, min(self.maximumSpeed, self.speed + speed))

	def adjustAngle(self, angle):
		if self.timeout == 0:
			self.angle += angle

	def accelerate(self): self.adjustSpeed(self.acceleration)
	def decelerate(self): self.adjustSpeed(-self.acceleration)
	def steerLeft(self):  self.adjustAngle(-self.steeringRate)
	def steerRight(self): self.adjustAngle(self.steeringRate)

	def shoot(self):
		bulletDistance = 0.2
		bulletPosition = Vector2(cos(radians(self.angle)) * bulletDistance, sin(radians(self.angle)) * bulletDistance)
		return Bullet(self.position + bulletPosition, self.angle)

	def explode(self):
		self.timeout = randrange(40, 140)

	def update(self, canvas):
		
		if self.timeout > 0:
			self.angle += 4
			self.polygon.transform(self.position, self.angle)
			if self.timeout // 4 % 2 == 0:
				self.polygon.draw(canvas)
			self.timeout -= 1
		else:
			velocity = Vector2(cos(radians(self.angle)) * self.speed, sin(radians(self.angle)) * self.speed)
			self.position += velocity

			self.polygon.transform(self.position, self.angle)
			self.polygon.draw(canvas)

			self.screenWrap()