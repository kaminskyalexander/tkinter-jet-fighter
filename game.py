from inputs import InputListener
from interface import InterfaceManager, InterfaceStartup, InterfaceTools
from player import Player
from setup import *
from vector import Vector2

class Game:
	"""
	The container for the game.
	Stores the players, responds to events in the game and controls inputs.
	"""

	def __init__(self, player1AI, player2AI, colour1, colour2):
		"""
		Starts the game.

		Arguments:
			player1AI (bool): If Player 1 should be controlled by AI.
			player2AI (bool): If Player 2 should be controlled by AI.
			colour1 (str): Tkinter format colour applied on Player 1.
			colour2 (str): Tkinter format colour applied on Player 2.
		"""
		self.tick = 0
		self.player1 = Player(Vector2(-0.5, -0.5), 90, player1AI, colour1)
		self.player2 = Player(Vector2(0.5, 0.5), -90, player2AI, colour2)
		self.gameDuration = 2 * 60 * fps
		sound.play("music0")

	def update(self):
		"""
		Updates all events in the game.
		Should be called every frame.
		"""
		# Game is not over
		if self.tick < self.gameDuration:
			# Register keypresses and act accordingly
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

			# Update the players
			self.player1.update(canvas, self.player2)
			self.player2.update(canvas, self.player1)

			# Loop over all bullets in the game
			for bullet in self.player1.bullets + self.player2.bullets:
				bullet.update(canvas)
				
				# Remove bullets once they have finished exploding
				if bullet.explosionDuration == 0:
					if bullet in self.player1.bullets: self.player1.bullets.remove(bullet)
					if bullet in self.player2.bullets: self.player2.bullets.remove(bullet)
					continue
				
				if not bullet.exploded:

					# Destroy the bullet after the defined period of time
					if bullet.lifespan == -bullet.decay:
						if bullet in self.player1.bullets: self.player1.bullets.remove(bullet)
						if bullet in self.player2.bullets: self.player2.bullets.remove(bullet)
						continue

					# Check if the bullet has collided with Player 1
					if bullet.detectCollision(self.player1) and self.player1.timeout == 0:
						self.player2.score += 1
						self.player1.explode()
						bullet.explode()

					# Check if the bullet has collided with Player 2
					if bullet.detectCollision(self.player2) and self.player2.timeout == 0:
						self.player1.score += 1
						self.player2.explode()
						bullet.explode()

			# Display the score, flashing it when the game is about to end
			if (self.tick < self.gameDuration - 20 * 60) or (self.tick // 30 % 2):
				# Draw layer 1 score
				canvas.create_text(
					pixelFromPosition(Vector2(-0.9, -0.9)),
					text = str(self.player1.score),
					fill = self.player1.colour,
					font = ("Fixedsys", InterfaceTools.fontSize(80), ""),
					anchor = "nw"
				)
				# Draw player 2 score
				canvas.create_text(
					pixelFromPosition(Vector2(0.9, -0.9)),
					text = str(self.player2.score),
					fill = self.player2.colour,
					font = ("Fixedsys", InterfaceTools.fontSize(80), ""),
					anchor = "ne"
				)

		# Stop the music at the end of the game
		if self.tick == self.gameDuration:
			sound.stop("music0")

		# End of game
		if self.tick > self.gameDuration:

			# Beeping every 30 ticks
			if self.tick % 30 == 0:
				sound.play("beep")

			# Display the winner
			if self.player1.score > self.player2.score:
				gameOverMessage = "Player 1 wins!"
			elif self.player1.score < self.player2.score:
				gameOverMessage = "Player 2 wins!"
			else:
				gameOverMessage = "Tie!"
			canvas.create_text(
				pixelFromPosition(Vector2(0, 0)),
				text = gameOverMessage,
				fill = "#ff5",
				font = ("Fixedsys", InterfaceTools.fontSize(40), "")
			)

		# Exit the game upon completion and return to title screen
		if self.tick == self.gameDuration + 180:
			return 0
		
		self.tick += 1

ui = InterfaceManager()
game = None

def update():
	"""
	The main loop of the process.
	Called every frame.
	"""
	global game, fullscreen
	# Clear all objects from the screen
	canvas.delete("all")

	# Update input dictionary
	inputs.refresh()

	# Fullscreen
	if inputs.key(*binds["f11"]):
		fullscreen = not fullscreen
		root.attributes("-fullscreen", fullscreen)

	# Detect returns from the interface
	response = ui.update()
	if response != None:
		# Start the game
		game = Game(**response)

	if game != None:
		# Return to title screen after game completion
		if game.update() == 0:
			game = None
			ui.currentInterface = InterfaceStartup()

loop(update)
tk.mainloop()
