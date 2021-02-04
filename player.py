from math import atan2, cos, degrees, inf, radians, sin, sqrt
from random import uniform

from bullet import Bullet
from entity import Entity
from polygon import Polygon
from setup import *
from vector import Vector2

class Player(Entity):
	"""
	Entity with controls.
	"""
	maximumSpeed = 0.9
	minimumSpeed = 0.3
	steeringRate = 120
	acceleration = 0.6
	shootCooldown = 1
	bulletSpawnDistance = 0.1

	def __init__(self, position, angle, colour):
		"""
		Creates a player.

		Arguments:
			position (Vector2): The starting position.
			angle (int): The starting angle (in degrees).
			computer (bool): Whether the player is controlled by a human (False) or an AI (True).
			colour (str): Tkinter format color.
		"""
		self.angle = angle % 360
		self.colour = colour
		self.speed = 0.6
		self.timeout = 0
		self.bullets = []
		self.score = 0
		self.timeSinceLastShot = 0
		self.drawHitboxes = False
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
		if self.timeout <= 0:
			self.speed = max(self.minimumSpeed, min(self.maximumSpeed, self.speed + speed))

	def adjustAngle(self, angle):
		"""
		Adjust the angle of the player.

		Arguments:
			angle (float): How much to increment the angle.
		"""
		if self.timeout <= 0:
			self.angle = (self.angle + angle) % 360

	def accelerate(self, deltaTime): self.adjustSpeed( self.acceleration * deltaTime)
	def decelerate(self, deltaTime): self.adjustSpeed(-self.acceleration * deltaTime)
	def steerLeft(self, deltaTime):  self.adjustAngle(-self.steeringRate * deltaTime)
	def steerRight(self, deltaTime): self.adjustAngle( self.steeringRate * deltaTime)

	def shoot(self):
		"""
		Creates an instance of Bullet in front of the player.
		"""
		if self.timeout <= 0 and self.timeSinceLastShot > self.shootCooldown:
			sound.play("shoot")
			self.timeSinceLastShot = 0
			
			bulletPosition = Vector2(cos(radians(self.angle)) * self.bulletSpawnDistance, sin(radians(self.angle)) * self.bulletSpawnDistance)
			self.bullets.append(Bullet(self.position + bulletPosition, self.angle))

	def explode(self):
		"""
		Explodes the player and sets a random cooldown duration.
		"""
		sound.play("explosion")
		self.timeout = uniform(0.667, 2.333)

	def update(self, canvas, deltaTime, enemy):
		"""
		This function should be called every frame.
		It transforms, draws and can control the player.
		"""
		if self.timeout > 0:
			# Spin the player when on timeout
			self.angle += 240 * deltaTime
			self.transform(self.position, self.angle)
			# Flash the player every 4 ticks
			if self.timeout*60 // 4 % 2 == 0:
				self.polygon.draw(canvas)
			self.timeout -= deltaTime
		else:
			velocity = Vector2(cos(radians(self.angle)) * self.speed, sin(radians(self.angle)) * self.speed)
			self.position += velocity * deltaTime

			self.transform(self.position, self.angle)
			self.polygon.draw(canvas)

			self.screenWrap()

			self.timeSinceLastShot += deltaTime

		if self.drawHitboxes:
			# Draw hitboxes for debugging
			for hitbox in self.hitboxes:
				hitbox.drawWireframe(canvas, "white")

			# Draw bounding box for debugging
			bbox = self.polygon.boundingBox
			Polygon(Vector2(bbox[0][0], bbox[0][1]), Vector2(bbox[1][0], bbox[0][1]), Vector2(bbox[1][0], bbox[1][1]), Vector2(bbox[0][0], bbox[1][1])).drawWireframe(canvas, "blue")

class PlayerComputerLegacy(Player):

	def __init__(self, position, angle, colour):
		super().__init__(position, angle, colour)
		self.drawAITarget = False

	def getSteeringDirection(self, targetAngle):
		"""
		Determines which way is fastest to turn to get to a specific angle.
		Returns a Direction.LEFT or Direction.RIGHT.

		Arguments:
			targetAngle (float): The desired angle to turn to.

		Example:
			>>> self.getSteeringDirection(90)
			0
		"""

		epsilon = 2.5
		if abs(self.angle - targetAngle) < epsilon:
			return

		if self.angle < targetAngle:
			if abs(self.angle - targetAngle) < 180:
				return Direction.RIGHT
			return Direction.LEFT
		elif self.angle > targetAngle:
			if abs(self.angle - targetAngle) < 180:
				return Direction.LEFT
			return Direction.RIGHT

	def update(self, canvas, deltaTime, enemy):
		super().update(canvas, deltaTime, enemy)
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
			targetAngle += 90 if steeringDirection == Direction.RIGHT else -90

		# Steer towards the target angle
		if abs(targetAngle - self.angle) > 10: 
			if steeringDirection == Direction.LEFT: self.steerLeft(deltaTime)
			elif steeringDirection == Direction.RIGHT: self.steerRight(deltaTime)
		
		# Accelerate/decelerate depending on how far the enemy is
		distanceFromPlayer = sqrt((self.position.x - enemy.position.x)**2 + (self.position.y - enemy.position.y)**2)
		if distanceFromPlayer < 0.5:
			self.accelerate(deltaTime)
		elif distanceFromPlayer > 1:
			self.decelerate(deltaTime)
			
		# Shoot if pointing towards the enemy
		if abs(angleToPlayer - self.angle) <= 10:
			self.shoot()

		# Draw current AI target for debugging
		if self.drawAITarget:
			canvas.create_line(
				*pixelFromPosition(self.position),
				*pixelFromPosition(self.position + Vector2(cos(radians(targetAngle)) * 0.5, sin(radians(targetAngle)) * 0.5)),
				fill = "red"
			)

class PlayerComputer(Player):

	def __init__(self, position, angle, colour):
		super().__init__(position, angle, colour)
		self.steeringEpsilon = 2.5
		self.aimEpsilon = 2

	def getSteeringDirection(self, targetAngle):
		"""
		Determines which way is fastest to turn to get to a specific angle.
		Returns a Direction.LEFT or Direction.RIGHT.

		Arguments:
			targetAngle (float): The desired angle to turn to.

		Example:
			>>> self.getSteeringDirection(90)
			0
		"""

		if abs(self.angle - targetAngle) < self.steeringEpsilon:
			return

		if self.angle < targetAngle:
			if abs(self.angle - targetAngle) < 180:
				return Direction.RIGHT
			return Direction.LEFT
		elif self.angle > targetAngle:
			if abs(self.angle - targetAngle) < 180:
				return Direction.LEFT
			return Direction.RIGHT

	def update(self, canvas, deltaTime, enemy):
		super().update(canvas, deltaTime, enemy)

		enemySpeed = enemy.speed if enemy.timeout <= 0 else 0
		enemyVelocity = Vector2(cos(radians(enemy.angle)) * enemySpeed, sin(radians(enemy.angle)) * enemySpeed)

		bulletOffset = Vector2(cos(radians(self.angle)) * self.bulletSpawnDistance, sin(radians(self.angle)) * self.bulletSpawnDistance)
		relativePosition = enemy.position - self.position - bulletOffset
		
		a = Vector2.dot(-enemyVelocity, -enemyVelocity) - Bullet.speed**2
		b = Vector2.dot(-relativePosition, -enemyVelocity) * 2
		c = Vector2.dot(-relativePosition, -relativePosition)

		h = -b / (2*a)
		k2 = h**2 - c/a
		t = None
		
		if k2 == 0:
			if 0 < h:
				t = h		

		elif k2 > 0:
			k = sqrt(k2)
			root1 = h - k
			root2 = h + k
			if 0 < root1:
				t = root1 
			elif 0 < root2:
				t = root2

		if t is not None:
			target = Vector2(t * enemyVelocity.x + enemy.position.x, t * enemyVelocity.y + enemy.position.y) - self.position

			# Compensate for screenwrap
			enemyBounds = enemy.polygon.boundingBox
			enemyWidth = enemyBounds[1][0] - enemyBounds[0][0]
			enemyHeight = enemyBounds[1][1] - enemyBounds[0][1]
			target.x -= enemyWidth * int(target.x + self.position.x)
			target.y -= enemyHeight * int(target.y + self.position.y)

			targetAngle = degrees(atan2(target.y, target.x)) % 360

			steeringTarget = self.getSteeringDirection(targetAngle)
			if steeringTarget == Direction.RIGHT:
				self.steerRight(deltaTime)			
			elif steeringTarget == Direction.LEFT:
				self.steerLeft(deltaTime)

			if abs(targetAngle - self.angle) <= self.aimEpsilon:
				self.shoot()

