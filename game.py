from setup import *
from inputs import InputListener
from vector import Vector2

inputs = InputListener(root)

from polygon import draw


angle = 0

def update():
	global angle
	canvas.delete("all")
	draw(
		canvas, 
		[
			Vector2(0, -0.1),
			Vector2(-0.1, 0.1),
			Vector2(0.1, 0.1)
		],
		Vector2(0, 0),
		angle
	)
	angle += 1

loop(update)
tk.mainloop()