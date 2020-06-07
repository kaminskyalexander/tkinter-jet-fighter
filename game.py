from setup import *
from inputs import InputListener
from vector import Vector2
from player import Player

inputs = InputListener(root)

from polygon import draw

player = Player(0, 0)

def update():
	inputs.refresh()
	if inputs.key(*binds["accelerate"]): player.speed = min(0.015, player.speed + 0.0001)
	if inputs.key(*binds["decelerate"]): player.speed = max(0.005, player.speed - 0.0001)
	if inputs.key(*binds["left"]): player.angle -= 2
	if inputs.key(*binds["right"]): player.angle += 2
	if inputs.key(*binds["shoot"]): player.shoot()
	canvas.delete("all")
	player.update(canvas)

loop(update)
tk.mainloop()