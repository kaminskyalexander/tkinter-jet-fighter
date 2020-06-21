from math import atan2, cos, degrees, inf, radians, sin, sqrt
from random import randrange

from bullet import Bullet
from entity import Entity
from polygon import Polygon
from setup import *
from vector import Vector2

class Player(Entity):
	"""
	Entity with controls.
	"""

	def __init__(self, position, angle, computer, colour):
		"""
		Creates a player.

		Arguments:
			position (Vector2): The starting position.
			angle (int): The starting angle (in degrees).
			computer (bool): Whether the player is controlled by a human (False) or an AI (True).
			colour (str): Tkinter format color.
		"""
		self.angle = angle % 360
		self.computer = computer
		self.colour = colour
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
		# The vertices of the displayed shape
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
			fill = self.colour
		)
		# Hitboxes supplied to entity
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
		"""
		Adjusts the speed of the player.
		
		Arguments:
			speed (float): How much to increment the speed.
		"""
		if self.timeout == 0:
			self.speed = max(self.minimumSpeed, min(self.maximumSpeed, self.speed + speed))

	def adjustAngle(self, angle):
		"""
		Adjust the angle of the player.

		Arguments:
			angle (float): How much to increment the angle.
		"""
		if self.timeout == 0:
			self.angle = (self.angle + angle) % 360

	def accelerate(self): self.adjustSpeed(self.acceleration)
	def decelerate(self): self.adjustSpeed(-self.acceleration)
	def steerLeft(self):  self.adjustAngle(-self.steeringRate)
	def steerRight(self): self.adjustAngle(self.steeringRate)

	def shoot(self):
		"""
		Creates an instance of Bullet in front of the player.
		"""
		if self.timeout == 0 and self.timeSinceLastShot > self.shootCooldown:
			sound.play("shoot")
			self.timeSinceLastShot = 0
			bulletDistance = 0.1
			bulletPosition = Vector2(cos(radians(self.angle)) * bulletDistance, sin(radians(self.angle)) * bulletDistance)
			self.bullets.append(Bullet(self.position + bulletPosition, self.angle))

	def explode(self):
		"""
		Explodes the player and sets a random cooldown duration.
		"""
		sound.play("explosion")
		self.timeout = randrange(40, 140)

	def getSteeringDirection(self, angle):
		"""
		Determines which way is fastest to turn to get to a specific angle.

		Arguments:
			angle (float): The desired angle to turn to.

		Example:
			>>> self.getSteeringDirection(90)
			"left"
		"""
		
		if self.angle < angle:
			if abs(self.angle - angle) < 180:
				return "right"
			return "left"
		else:
			if abs(self.angle - angle) < 180:
				return "left"
			return "right"
		return ""

	def update(self, canvas, enemy):
		"""
		This function should be called every frame.
		It transforms, draws and can control the player.
		"""
		if self.timeout > 0:
			# Spin the player when on timeout
			self.angle += 4
			self.transform(self.position, self.angle)
			# Flash the player every 4 ticks
			if self.timeout // 4 % 2 == 0:
				self.polygon.draw(canvas)
			self.timeout -= 1
		else:
			# If the player has AI enabled
			if self.computer:
				smallestDistanceFromBullet = inf
				nearestBullet = None
				
				# Finds the nearest bullet
				for bullet in self.bullets + enemy.bullets:
					distanceToBullet = sqrt((self.position.x - bullet.position.x)**2 + (self.position.y - bullet.position.y)**2)
					if distanceToBullet < smallestDistanceFromBullet:
						smallestDistanceFromBullet = distanceToBullet
						nearestBullet = bullet
				
				# Find optimal path (direction to steer) to player
				directionToEnemy = enemy.position - self.position
				targetAngle = degrees(atan2(directionToEnemy.y, directionToEnemy.x)) % 360
				angleToPlayer = targetAngle
				steeringDirection = self.getSteeringDirection(targetAngle)
					
				# Avoid bullets when they are nearby
				if smallestDistanceFromBullet < 0.5:
					# Steer perpendicular to the bullet path
					targetAngle = nearestBullet.angle
					# Prefer turning in the direction of the enemy
					targetAngle += 90 if steeringDirection == "right" else -90
					direction = self.getSteeringDirection(targetAngle)

				# Steer towards the target angle
				if abs(targetAngle - self.angle) > 10: 
					if steeringDirection == "left": self.steerLeft()
					elif steeringDirection == "right": self.steerRight()
				
				# Accelerate/decelerate depending on how far the enemy is
				distanceFromPlayer = sqrt((self.position.x - enemy.position.x)**2 + (self.position.y - enemy.position.y)**2)
				if distanceFromPlayer < 0.5:
					self.accelerate()
				elif distanceFromPlayer > 1:
					self.decelerate()
					
				# Shoot if pointing towards the enemy
				if abs(angleToPlayer - self.angle) <= 10:
					self.shoot()

				# Draw current AI target for debugging
				# canvas.create_line(
				# 	*pixelFromPosition(self.position),
				# 	*pixelFromPosition(self.position + Vector2(cos(radians(targetAngle)) * 0.5, sin(radians(targetAngle)) * 0.5)),
				# 	fill = "red"
				# )

			velocity = Vector2(cos(radians(self.angle)) * self.speed, sin(radians(self.angle)) * self.speed)
			self.position += velocity

			self.transform(self.position, self.angle)
			self.polygon.draw(canvas)

			self.screenWrap()

			self.timeSinceLastShot += 1

		# Draw hitboxes for debugging
		# for hitbox in self.hitboxes:
		# 	hitbox.drawWireframe(canvas, "white")

		# Draw boundingbox for debugging
		# bbox = self.polygon.boundingBox
		# Polygon(Vector2(bbox[0][0], bbox[0][1]), Vector2(bbox[1][0], bbox[0][1]), Vector2(bbox[1][0], bbox[1][1]), Vector2(bbox[0][0], bbox[1][1])).drawWireframe(canvas, "blue")

