from math import cos, sin, atan2, radians, degrees, sqrt, inf
from random import randrange

from setup import *
from vector import Vector2
from entity import Entity 
from polygon import Polygon
from bullet import Bullet

class Player(Entity):

	def __init__(self, position, angle, computer, colour):
		self.angle = angle % 360
		self.computer = computer
		self.speed = 0.01
		self.acceleration = 0.0001
		self.maximumSpeed = 0.015
		self.minimumSpeed = 0.005
		self.steeringRate = 2
		self.timeout = 0
		self.bullets = []
		self.score = 0
		self.shootCooldown = 60
		self.timeSinceLastShot = 0
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
			fill = colour
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
			self.angle = (self.angle + angle) % 360

	def accelerate(self): self.adjustSpeed(self.acceleration)
	def decelerate(self): self.adjustSpeed(-self.acceleration)
	def steerLeft(self):  self.adjustAngle(-self.steeringRate)
	def steerRight(self): self.adjustAngle(self.steeringRate)

	def shoot(self):
		if self.timeout == 0 and self.timeSinceLastShot > self.shootCooldown:
			sound.play("shoot0")
			sound.play("shoot1")
			self.timeSinceLastShot = 0
			bulletDistance = 0.1
			bulletPosition = Vector2(cos(radians(self.angle)) * bulletDistance, sin(radians(self.angle)) * bulletDistance)
			self.bullets.append(Bullet(self.position + bulletPosition, self.angle))

	def explode(self):
		sound.play("explosion")
		self.timeout = randrange(40, 140)

	def update(self, canvas, enemy):

		if self.timeout > 0:
			self.angle += 4
			self.transform(self.position, self.angle)
			if self.timeout // 4 % 2 == 0:
				self.polygon.draw(canvas)
			self.timeout -= 1
		else:

			if self.computer:
				bulletNearby = False
				smallestDistance = inf
				nearestBullet = None
				

				distanceFromPlayer = sqrt((self.position.x - enemy.position.x)**2 + (self.position.y - enemy.position.y)**2)
				if distanceFromPlayer < 0.5:
					self.accelerate()
				elif distanceFromPlayer > 1:
					self.decelerate()
				
				for bullet in self.bullets + enemy.bullets:
					distanceToBullet = sqrt((self.position.x - bullet.position.x)**2 + (self.position.y - bullet.position.y)**2)
					if distanceToBullet < smallestDistance:
						smallestDistance = distanceToBullet
						nearestBullet = bullet
				
				targetDirection = enemy.position - self.position
				angle = degrees(atan2(targetDirection.y, targetDirection.x))
				steeringDirection = ""

				if angle < 0: angle += 360
				if abs(angle - self.angle) > 10:
					if self.angle < angle:
						if abs(self.angle - angle) < 180:
							steeringDirection = "right"
						else:
							steeringDirection = "left"
					else:
						if abs(self.angle - angle) < 180:
							steeringDirection = "left"
						else:
							steeringDirection = "right"
					
				if smallestDistance < 0.5:
					angle = (90 if steeringDirection == "right" else -90) + degrees(atan2(nearestBullet.velocity.y, nearestBullet.velocity.x))
					if angle < 0: angle += 360
					if abs(angle - self.angle) > 10:
						if self.angle < angle:
							if abs(self.angle - angle) < 180:
								self.steerRight()
							else:
								self.steerLeft()
						else:
							if abs(self.angle - angle) < 180:
								self.steerLeft()
							else:
								self.steerRight()
				else:	
					if steeringDirection == "left": self.steerLeft()
					elif steeringDirection == "right": self.steerRight()
					else: self.shoot()

				# canvas.create_line(
				# 	*pixelFromPosition(self.position),
				# 	*pixelFromPosition(self.position + Vector2(cos(radians(angle)) * 0.5, sin(radians(angle)) * 0.5)),
				# 	fill = "red"
				# )
			


			velocity = Vector2(cos(radians(self.angle)) * self.speed, sin(radians(self.angle)) * self.speed)
			self.position += velocity

			self.transform(self.position, self.angle)
			self.polygon.draw(canvas)

			self.screenWrap()

			self.timeSinceLastShot += 1

		# draw hitboxes
		# for hitbox in self.hitboxes:
		# 	hitbox.drawWireframe(canvas, "white")

		# # draw boundingbox
		# bbox = self.polygon.boundingBox
		# Polygon(Vector2(bbox[0][0], bbox[0][1]), Vector2(bbox[1][0], bbox[0][1]), Vector2(bbox[1][0], bbox[1][1]), Vector2(bbox[0][0], bbox[1][1])).drawWireframe(canvas, "blue")



