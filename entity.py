class Entity:

	def __init__(self, position, shape):
		self.position = position
		self.shape = shape

	@property
	def boundingBox(self):
		minX = self.shape[0].x
		minY = self.shape[0].y
		maxX = self.shape[0].x
		maxY = self.shape[0].y
		for vertex in self.shape:
			if vertex.x < minX: minX = vertex.x
			if vertex.x > maxX: maxX = vertex.x
			if vertex.y < minY: minY = vertex.y
			if vertex.y > maxY: maxY = vertex.y
		return (minX, minY), (maxX, maxY)

	def screenWrap(self):
		boundingBox = self.boundingBox
		halfWidth = (boundingBox[1][0] - boundingBox[0][0]) / 2
		halfHeight = (boundingBox[1][1] - boundingBox[0][1]) / 2

		if self.position.x >  1 + halfWidth:  self.position.x = -1 - halfWidth
		if self.position.x < -1 - halfWidth:  self.position.x =  1 + halfWidth
		if self.position.y >  1 + halfHeight: self.position.y = -1 - halfHeight
		if self.position.y < -1 - halfHeight: self.position.y =  1 + halfHeight