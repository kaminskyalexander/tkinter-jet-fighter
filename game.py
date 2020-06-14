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
	if inputs.key(*binds["p1-accelerate"]): player1.accelerate()
	if inputs.key(*binds["p1-decelerate"]): player1.decelerate()
	if inputs.key(*binds["p1-left"]):       player1.steerLeft()
	if inputs.key(*binds["p1-right"]):      player1.steerRight()
	if inputs.key(*binds["p1-shoot"]):      bullets.append(player1.shoot())
	if inputs.key(*binds["p2-accelerate"]): player2.accelerate()
	if inputs.key(*binds["p2-decelerate"]): player2.decelerate()
	if inputs.key(*binds["p2-left"]):       player2.steerLeft()
	if inputs.key(*binds["p2-right"]):      player2.steerRight()
	if inputs.key(*binds["p2-shoot"]):      bullets.append(player2.shoot())
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
				player1.score += 1
				player1.explode()
				bullet.explode()

			if bullet.detectCollision(player2) and player2.timeout == 0:
				player2.score += 1
				player2.explode()
				bullet.explode()

	canvas.create_text(0, 0, text = f"{player1.score} : {player2.score}", fill = "white", font = ("Arial", 36, ""), anchor = "nw")

loop(update)
tk.mainloop()