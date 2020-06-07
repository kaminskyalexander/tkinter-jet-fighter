from setup import *
from inputs import InputListener
from vector import Vector2
from player import Player

inputs = InputListener(root)

player1 = Player(Vector2(0, -0.5), 90)
player2 = Player(Vector2(0, 0.5), -90)
bullets = []

def update():
	inputs.refresh()
	if inputs.key(*binds["accelerate"]): player1.speed = min(0.015, player1.speed + 0.0001)
	if inputs.key(*binds["decelerate"]): player1.speed = max(0.005, player1.speed - 0.0001)
	if inputs.key(*binds["left"]): player1.angle -= 2
	if inputs.key(*binds["right"]): player1.angle += 2
	if inputs.key(*binds["shoot"]): player1.shoot(bullets)
	canvas.delete("all")
	player1.update(canvas)
	player2.update(canvas)

	for bullet in bullets:
		if bullet.lifespan == 0:
			bullets.remove(bullet)
		bullet.update(canvas)
		bullet.detectCollision(player1)
		bullet.detectCollision(player2)

loop(update)
tk.mainloop()