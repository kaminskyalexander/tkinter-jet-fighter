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
	if inputs.key(*binds["accelerate"]): player1.accelerate()
	if inputs.key(*binds["decelerate"]): player1.decelerate()
	if inputs.key(*binds["left"]):  player1.steerLeft()
	if inputs.key(*binds["right"]): player1.steerRight()
	if inputs.key(*binds["shoot"]): player1.shoot(bullets)
	canvas.delete("all")
	player1.update(canvas)
	player2.update(canvas)

	for bullet in bullets:
		bullet.update(canvas)
			
		if bullet.explosionDuration == 0:
			bullets.remove(bullet)
			continue
		
		if not bullet.exploded:

			if bullet.lifespan == -bullet.decay:
				bullets.remove(bullet)
				continue

			if bullet.detectCollision(player1) and player1.timeout == 0:
				print("i hit player 1")
				player1.explode()
				bullet.explode()

			if bullet.detectCollision(player2) and player2.timeout == 0:
				print("i hit player 2")
				player2.explode()
				bullet.explode()

loop(update)
tk.mainloop()