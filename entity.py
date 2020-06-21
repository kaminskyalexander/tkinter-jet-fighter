from polygon import Polygon
from sat import SAT

class Entity:
	"""
	Base class of all objects in the game.
	Contains the position, shape, hitboxes and collision detection.
	"""

	def __init__(self, position, polygon, hitboxes = None):
		"""
		Create an entity.

		Arguments:
			position (Vector2): The intial location of the entity
			polygon (Polygon): Used for drawing and collision detection if no hitboxes are specifed.
			hitboxes (List:Polygon): Optional polygons used for collision detection.
		"""
		self.position = position
		self.polygon = polygon
		self.hitboxes = hitboxes if hitboxes != None else [polygon]

	def screenWrap(self):
		"""
		Wraps an entity around the screen.
		Should be called every frame.
		"""
		boundingBox = self.polygon.boundingBox
		halfWidth = (boundingBox[1][0] - boundingBox[0][0]) / 2
		halfHeight = (boundingBox[1][1] - boundingBox[0][1]) / 2
		# Translate the entity to the other side of the screen
		if self.position.x >  1 + halfWidth:  self.position.x = -1 - halfWidth
		if self.position.x < -1 - halfWidth:  self.position.x =  1 + halfWidth
		if self.position.y >  1 + halfHeight: self.position.y = -1 - halfHeight
		if self.position.y < -1 - halfHeight: self.position.y =  1 + halfHeight

	def transform(self, translation, rotationAngle):
		"""
		Translate and rotate an entity.

		Arguments:
			translation (Vector2): The position where the entity should be translated to.
			rotationAngle (float): The angle (in degrees) which the entity should be rotated to.
		"""
		self.polygon.transform(translation, rotationAngle)
		for hitbox in self.hitboxes:
			hitbox.transform(translation, rotationAngle)

	def detectCollision(self, entity):
		"""
		Detects collision between two entities.

		Arguments:
			entity (Entity): The entity to check collision with

		Returns:
			bool: True if a collision was detected.
		"""
		for hitbox1 in self.hitboxes:
			for hitbox2 in entity.hitboxes:
				if SAT.detectCollision(hitbox1, hitbox2):
					return True
