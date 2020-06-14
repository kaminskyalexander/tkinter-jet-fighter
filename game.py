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
		bullet.update(canvas)
			
		if bullet.lifespan == -15:
			bullets.remove(bullet)

		elif bullet.lifespan >= 0:
			
			if bullet.detectCollision(player1):
				print("i hit player 1")
				player1.explode()
				bullet.explode()

			if bullet.detectCollision(player2):
				print("i hit player 2")
				player2.explode()
				bullet.explode()

		

loop(update)
tk.mainloop()