from setup import *
from inputs import InputListener
from vector import Vector2
from player import Player

class Game:

	def __init__(self):
		self.player1 = Player(Vector2(-0.5, -0.5), 90, "#f00")
		self.player2 = Player(Vector2(0.5, 0.5), -90, "#0f0")
		self.gameDuration = 2 * 60 * fps
		self.gameTick = 0

	def update(self):
		if self.gameTick < self.gameDuration:
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

			self.player1.update(canvas)
			self.player2.update(canvas)

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
		
		else:
			if self.player1.score > self.player2.score:
				canvas.create_text(400, 400, text = "Player 1 wins!", font = ("Fixedsys", 30, ""), fill = "yellow")
			elif self.player1.score < self.player2.score:
				canvas.create_text(400, 400, text = "Player 2 wins!", font = ("Fixedsys", 30, ""), fill = "yellow")
			else:
				canvas.create_text(400, 400, text = "Tie!", font = ("Fixedsys", 30, ""), fill = "yellow")

		canvas.create_text(10, 10, text = f"{self.player1.score}", font = ("Fixedsys", -80, ""), fill = "#f00", anchor = "nw")
		canvas.create_text(790, 10, text = f"{self.player2.score}", font = ("Fixedsys", -80, ""), fill = "#0f0", anchor = "ne")
		self.gameTick += 1

# the code in this class sucks, its a prototype
class Splash:

	def __init__(self):
		self.state = "title"
		self.selections = ["Player vs Player", "Player vs AI", "How to play"]
		self.selectionIndex = 0
		self.selectionIndexAlt = 0
		self.colourOptions = ["red", "orange", "yellow", "green", "cyan", "blue", "purple", "pink"]
		self.splashImage = tk.PhotoImage(file = "assets/title.png").zoom(8)
	
	def update(self):
		if self.state == "title":
			canvas.create_rectangle(0, 0, 800, 800, fill = "darkblue")
			canvas.create_image(400, 200, image = self.splashImage)
			# Flashing text
			if time.time() // 0.5 % 2:
				canvas.create_text(400, 500, text = "PRESS SPACE TO PLAY", fill = "white", font = ("Fixedsys", "30", ""))

			if inputs.key(*binds["ui-select"]): self.state = "selection"
		elif self.state == "selection":
			canvas.create_image(400, 200, image = self.splashImage)
			for i, selection in enumerate(self.selections):
				canvas.create_text(100, 300 + i*50, text = selection, fill = "white", font = ("Arial", "30", ""), anchor = "nw")
			# Flashing cursor
			#if time.time() // 0.15 % 2:
			canvas.create_polygon([(50, 300 + self.selectionIndex * 50), (50, 330 +  self.selectionIndex * 50), (75, 315 + self.selectionIndex * 50)], fill = "blue")
			if inputs.key(*binds["ui-down"]): self.selectionIndex = (self.selectionIndex + 1) % len(self.selections)
			if inputs.key(*binds["ui-up"]): self.selectionIndex = (self.selectionIndex - 1) % len(self.selections)
			if inputs.key(*binds["ui-select"]):
				if self.selectionIndex == 0: 
					self.selectionIndex = 0
					self.selectionIndexAlt = 0
					self.state = "colourSelection"
		elif self.state == "colourSelection":
			canvas.create_text(200, 150, text = "Player 1 colour", fill = "white", font = ("Arial", "30", ""))
			canvas.create_text(600, 150, text = "Player 2 colour", fill = "white", font = ("Arial", "30", ""))
			# draw two palettes of colours
			for i in range(2):
				for j, colour in enumerate(self.colourOptions):
					canvas.create_rectangle(50 + (j%3)*100 + i*400, 200 + (j//3)*100, 150 + (j%3)*100 + i*400, 300 + (j//3)*100, fill = colour)
				canvas.create_rectangle(
					((self.selectionIndex if i == 0 else self.selectionIndexAlt) % 3 ) * 100 + 50 + i*400,
					((self.selectionIndex if i == 0 else self.selectionIndexAlt) // 3) *100 + 200, 
					((self.selectionIndex if i == 0 else self.selectionIndexAlt) % 3 ) * 100 + 150 + i*400, 
					((self.selectionIndex if i == 0 else self.selectionIndexAlt) // 3) *100 + 300 , 
					fill = "", width = 10, outline = "white"
				)


			if inputs.key(*binds["ui-p1-up"]):  self.selectionIndex = (self.selectionIndex - 1) % len(self.colourOptions)
			if inputs.key(*binds["ui-p1-down"]): self.selectionIndex = (self.selectionIndex + 1) % len(self.colourOptions)

			if inputs.key(*binds["ui-p2-up"]):  self.selectionIndexAlt = (self.selectionIndexAlt - 1) % len(self.colourOptions)
			if inputs.key(*binds["ui-p2-down"]): self.selectionIndexAlt = (self.selectionIndexAlt + 1) % len(self.colourOptions)
			if inputs.key(*binds["ui-select"]): return 0

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