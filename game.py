from setup import *
from inputs import InputListener
from vector import Vector2
from player import Player

class Game:

	def __init__(self):
		self.player1 = Player(Vector2(0, -0.5), 90)
		self.player2 = Player(Vector2(0, 0.5), -90)
		self.bullets = []

	def update(self):
		if inputs.key(*binds["p1-accelerate"]): self.player1.accelerate()
		if inputs.key(*binds["p1-decelerate"]): self.player1.decelerate()
		if inputs.key(*binds["p1-left"]):       self.player1.steerLeft()
		if inputs.key(*binds["p1-right"]):      self.player1.steerRight()
		if inputs.key(*binds["p1-shoot"]):      self.bullets.append(self.player1.shoot())
		if inputs.key(*binds["p2-accelerate"]): self.player2.accelerate()
		if inputs.key(*binds["p2-decelerate"]): self.player2.decelerate()
		if inputs.key(*binds["p2-left"]):       self.player2.steerLeft()
		if inputs.key(*binds["p2-right"]):      self.player2.steerRight()
		if inputs.key(*binds["p2-shoot"]):      self.bullets.append(self.player2.shoot())
		self.player1.update(canvas)
		self.player2.update(canvas)
		

		for bullet in self.bullets:
			bullet.update(canvas)
				
			if bullet.explosionDuration == 0:
				self.bullets.remove(bullet)
				continue
			
			if not bullet.exploded:

				if bullet.lifespan == -bullet.decay:
					self.bullets.remove(bullet)
					continue

				if bullet.detectCollision(self.player1) and self.player1.timeout == 0:
					self.player1.score += 1
					self.player1.explode()
					bullet.explode()

				if bullet.detectCollision(self.player2) and self.player2.timeout == 0:
					self.player2.score += 1
					self.player2.explode()
					bullet.explode()

# the code in this class sucks, its a prototype
class Splash:

	def __init__(self):
		self.state = "title"
		self.selections = ["Player vs Player", "Player vs AI", "How to play"]
		self.selectionIndex = 0
	
	def update(self):
		canvas.create_text(400, 100, text = "Jet Fighter!!", fill = "white", font = ("Arial", "64", "bold"))
		if self.state == "title":
			# Flashing text
			if time.time() // 0.5 % 2:
				canvas.create_text(400, 300, text = "Press space...", fill = "white", font = ("Arial", "30", ""))

			if inputs.key(*binds["ui-select"]): self.state = "selection"
		elif self.state == "selection":
			for i, selection in enumerate(self.selections):
				canvas.create_text(100, 300 + i*50, text = selection, fill = "white", font = ("Arial", "30", ""), anchor = "nw")
			# Flashing cursor
			#if time.time() // 0.15 % 2:
			canvas.create_polygon([(50, 300 + self.selectionIndex * 50), (50, 330 +  self.selectionIndex * 50), (75, 315 + self.selectionIndex * 50)], fill = "blue")
			if inputs.key(*binds["ui-down"]): self.selectionIndex = (self.selectionIndex + 1) % len(self.selections)
			if inputs.key(*binds["ui-up"]): self.selectionIndex = (self.selectionIndex - 1) % len(self.selections)
			if inputs.key(*binds["ui-select"]):
				return self.selectionIndex

inputs = InputListener(root)
splash = Splash()
game = None

def update():
	global game, splash
	canvas.delete("all")
	inputs.refresh()
	response = splash.update() if splash != None else None
	if response != None:
		# Start game with Player vs Player
		if response == 0:
			splash = None
			game = Game()
		else:
			print("Undefined response")
	game.update() if game != None else None

	#canvas.create_text(0, 0, text = f"{player1.score} : {player2.score}", fill = "white", font = ("Arial", 36, ""), anchor = "nw")

loop(update)
tk.mainloop()