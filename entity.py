from polygon import Polygon
from sat import SAT

class Entity:

	def __init__(self, position, polygon, hitboxes = None):
		self.position = position
		self.polygon = polygon
		self.hitboxes = hitboxes if hitboxes != None else [polygon]

	def screenWrap(self):
		boundingBox = self.polygon.boundingBox
		halfWidth = (boundingBox[1][0] - boundingBox[0][0]) / 2
		halfHeight = (boundingBox[1][1] - boundingBox[0][1]) / 2

		if self.position.x >  1 + halfWidth:  self.position.x = -1 - halfWidth
		if self.position.x < -1 - halfWidth:  self.position.x =  1 + halfWidth
		if self.position.y >  1 + halfHeight: self.position.y = -1 - halfHeight
		if self.position.y < -1 - halfHeight: self.position.y =  1 + halfHeight

	def transform(self, translation, rotationAngle):
		self.polygon.transform(translation, rotationAngle)
		for hitbox in self.hitboxes:
			hitbox.transform(translation, rotationAngle)

	def detectCollision(self, entity):
		for hitbox1 in self.hitboxes:
			for hitbox2 in entity.hitboxes:
				if SAT.detectCollision(hitbox1, hitbox2):
					return True