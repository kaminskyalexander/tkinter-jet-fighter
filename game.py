from setup import *
from inputs import InputListener
from vector import Vector2
from player import Player
from interface import InterfaceManager, InterfaceStartup

class Game:

	def __init__(self, player1AI, player2AI, colour1, colour2):
		self.tick = 0
		self.player1 = Player(Vector2(-0.5, -0.5), 90, player1AI, colour1)
		self.player2 = Player(Vector2(0.5, 0.5), -90, player2AI, colour2)
		self.gameDuration = 2 * 60 * fps
		sound.play("music0")

	def update(self):
		if self.tick < self.gameDuration:
			if inputs.key(*binds["p1-accelerate"]): self.player1.accelerate()
			if inputs.key(*binds["p1-decelerate"]): self.player1.decelerate()
			if inputs.key(*binds["p1-left"]):       self.player1.steerLeft()
			if inputs.key(*binds["p1-right"]):      self.player1.steerRight()
			if inputs.key(*binds["p1-shoot"]):      self.player1.shoot()
			if inputs.key(*binds["p2-accelerate"]): self.player2.accelerate()
			if inputs.key(*binds["p2-decelerate"]): self.player2.decelerate()
			if inputs.key(*binds["p2-left"]):       self.player2.steerLeft()
			if inputs.key(*binds["p2-right"]):      self.player2.steerRight()
			if inputs.key(*binds["p2-shoot"]):      self.player2.shoot()

			self.player1.update(canvas, self.player2)
			self.player2.update(canvas, self.player1)

			for bullet in self.player1.bullets + self.player2.bullets:
				bullet.update(canvas)
					
				if bullet.explosionDuration == 0:
					if bullet in self.player1.bullets: self.player1.bullets.remove(bullet)
					if bullet in self.player2.bullets: self.player2.bullets.remove(bullet)
					continue
				
				if not bullet.exploded:

					if bullet.lifespan == -bullet.decay:
						if bullet in self.player1.bullets: self.player1.bullets.remove(bullet)
						if bullet in self.player2.bullets: self.player2.bullets.remove(bullet)
						continue

					if bullet.detectCollision(self.player1) and self.player1.timeout == 0:
						self.player2.score += 1
						self.player1.explode()
						bullet.explode()

					if bullet.detectCollision(self.player2) and self.player2.timeout == 0:
						self.player1.score += 1
						self.player2.explode()
						bullet.explode()
		elif self.tick < self.gameDuration + 180:
			...
		else:
			sound.stop("music0")
			return 0
		
		self.tick += 1

ui = InterfaceManager()
game = None

def update():
	global game
	canvas.delete("all")
	inputs.refresh()
	response = ui.update()
	if response != None:
		game = Game(**response)
	if game != None:
		if game.update() == 0:
			game = None
			ui.currentInterface = InterfaceStartup()

loop(update)
tk.mainloop()