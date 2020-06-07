from polygon import Polygon

class Entity:

	def __init__(self, position, polygon):
		self.position = position
		self.polygon = polygon

	def screenWrap(self):
		boundingBox = self.polygon.boundingBox
		halfWidth = (boundingBox[1][0] - boundingBox[0][0]) / 2
		halfHeight = (boundingBox[1][1] - boundingBox[0][1]) / 2

		if self.position.x >  1 + halfWidth:  self.position.x = -1 - halfWidth
		if self.position.x < -1 - halfWidth:  self.position.x =  1 + halfWidth
		if self.position.y >  1 + halfHeight: self.position.y = -1 - halfHeight
		if self.position.y < -1 - halfHeight: self.position.y =  1 + halfHeight

	def detectCollision(self, entity):
		...