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
		shape = Polygon(
			Vector2( 0.0637760,  0.0000000),
			Vector2( 0.0526240, -0.0099696), 
			Vector2( 0.0133332, -0.0127572), 
			Vector2( 0.0004352, -0.0619000),
			Vector2(-0.0180848, -0.0646520), 
			Vector2(-0.0133332, -0.0127572), 
			Vector2(-0.0558679, -0.0127572), 
			Vector2(-0.0619320, -0.0255467),
			Vector2(-0.0673440, -0.0255467), 
			Vector2(-0.0630360,  0.0000000), 
			Vector2(-0.0673440,  0.0255467), 
			Vector2(-0.0619320,  0.0255467), 
			Vector2(-0.0558679,  0.0127572), 
			Vector2(-0.0133332,  0.0127572), 
			Vector2(-0.0180848,  0.0646520), 
			Vector2( 0.0004352,  0.0619000), 
			Vector2( 0.0133332,  0.0127572),
			Vector2( 0.0526240,  0.0099696),
			fill = "red"
		)
		hitboxes = [
			Polygon(
				Vector2(-0.015, -0.075),
				Vector2( 0.015, -0.075),
				Vector2( 0.015,  0.075),
				Vector2(-0.015,  0.075)
			),
			Polygon(
				Vector2(-0.09, -0.025),
				Vector2( 0.08, -0.025),
				Vector2( 0.08,  0.025),
				Vector2(-0.09,  0.025)
			)
		]
		super().__init__(position, shape, hitboxes)

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
		if self.timeout == 0:
			bulletDistance = 0.1
			bulletPosition = Vector2(cos(radians(self.angle)) * bulletDistance, sin(radians(self.angle)) * bulletDistance)
			self.bullets.append(Bullet(self.position + bulletPosition, self.angle))

	def explode(self):
		self.timeout = randrange(40, 140)

	def update(self, canvas):

		if self.timeout > 0:
			self.angle += 4
			self.transform(self.position, self.angle)
			if self.timeout // 4 % 2 == 0:
				self.polygon.draw(canvas)
			self.timeout -= 1
		else:
			velocity = Vector2(cos(radians(self.angle)) * self.speed, sin(radians(self.angle)) * self.speed)
			self.position += velocity

			self.transform(self.position, self.angle)
			self.polygon.draw(canvas)

			self.screenWrap()

		# draw hitboxes
		for hitbox in self.hitboxes:
			hitbox.drawWireframe(canvas, "white")

		# draw boundingbox
		bbox = self.polygon.boundingBox
		Polygon(Vector2(bbox[0][0], bbox[0][1]), Vector2(bbox[1][0], bbox[0][1]), Vector2(bbox[1][0], bbox[1][1]), Vector2(bbox[0][0], bbox[1][1])).drawWireframe(canvas, "blue")



