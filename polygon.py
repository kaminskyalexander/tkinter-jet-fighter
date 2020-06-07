from setup import *
from math import sin, cos, radians
from vector import Vector2

def pixelFromPosition(vector):
	# Get the size of the window
	width = canvas.winfo_width()
	height = canvas.winfo_height()
	# Get the coordinates in pixels based on the window width and height
	# This should let the window be stretchable
	x = (width/2)  + (height/2) * vector.x
	y = (height/2) + (height/2) * vector.y
	return x, y

def draw(canvas, vertices, translation, rotationAngle):

	rotationAngle = radians(rotationAngle)

	matrix = [
		[cos(rotationAngle), -sin(rotationAngle)],
		[sin(rotationAngle),  cos(rotationAngle)]
	]

	transformedVertices = []
	for vertex in vertices:
		newPoint = Vector2(
			vertex.x * matrix[0][0] + vertex.y * matrix[0][1], 
			vertex.x * matrix[1][0] + vertex.y * matrix[1][1]
		)
		
		newPoint += translation
		transformedVertices.append(newPoint)
		
	return canvas.create_polygon([pixelFromPosition(vertex) for vertex in transformedVertices], fill = "red")


# def rotate2dLine(line, degrees, origin = None):
# 	angle = degrees*pi/180

# 	x1, y1 = line[0]
# 	x2, y2 = line[1]

# 	if origin != None:
# 		mx, my = origin
# 	else:
# 		mx = (x1 + x2) / 2
# 		my = (y1 + y2) / 2

# 	# Use a rotation matrix, centering the point to (0, 0)
# 	rotated = (
# 		(
# 			(cos(angle) * (x1-mx) - sin(angle) * (y1-my)) + mx,
# 			(sin(angle) * (x1-mx) + cos(angle) * (y1-my)) + my
# 		),
# 		(
# 			(cos(angle) * (x2-mx) - sin(angle) * (y2-my)) + mx,
# 			(sin(angle) * (x2-mx) + cos(angle) * (y2-my)) + my
# 		)
# 	)

# 	return rotated