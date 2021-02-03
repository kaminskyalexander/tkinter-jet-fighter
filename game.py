from player import Player, PlayerComputer
from setup import *
from vector import Vector2
from interface import InterfaceTools

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
		player1Type = Player if not player1AI else PlayerComputer
		player2Type = Player if not player2AI else PlayerComputer
		self.player1 = player1Type(Vector2(-0.5, -0.5), 90, colour1)
		self.player2 = player2Type(Vector2(0.5, 0.5), -90, colour2)
		self.gameDuration = 180

		sound.play("music0")
		self.isMusicPlaying = True
		self.previousBeepTime = 0

	def update(self, deltaTime):
		"""
		Updates all events in the game.
		Should be called every frame.
		"""
		# Game is not over
		if self.tick < self.gameDuration:
			# Register keypresses and act accordingly if the player is not an AI
			if isinstance(self.player1, Player):
				if inputs.key(*binds["p1-accelerate"]): self.player1.accelerate(deltaTime)
				if inputs.key(*binds["p1-decelerate"]): self.player1.decelerate(deltaTime)
				if inputs.key(*binds["p1-left"]):       self.player1.steerLeft(deltaTime)
				if inputs.key(*binds["p1-right"]):      self.player1.steerRight(deltaTime)
				if inputs.key(*binds["p1-shoot"]):      self.player1.shoot()
			if isinstance(self.player2, Player):
				if inputs.key(*binds["p2-accelerate"]): self.player2.accelerate(deltaTime)
				if inputs.key(*binds["p2-decelerate"]): self.player2.decelerate(deltaTime)
				if inputs.key(*binds["p2-left"]):       self.player2.steerLeft(deltaTime)
				if inputs.key(*binds["p2-right"]):      self.player2.steerRight(deltaTime)
				if inputs.key(*binds["p2-shoot"]):      self.player2.shoot()

			# Draw collision debugging
			if inputs.key(*binds["f2"]):
				self.player1.drawHitboxes = not self.player1.drawHitboxes
				self.player2.drawHitboxes = not self.player2.drawHitboxes

			# Draw AI debugging
			if inputs.key(*binds["f3"]):
				self.player1.drawAITarget = not self.player1.drawAITarget
				self.player2.drawAITarget = not self.player2.drawAITarget

			# Update the players
			self.player1.update(canvas, deltaTime, self.player2)
			self.player2.update(canvas, deltaTime, self.player1)

			# Loop over all bullets in the game
			for bullet in self.player1.bullets + self.player2.bullets:
				bullet.update(canvas, deltaTime)
				
				# Remove bullets once they have finished exploding
				if bullet.explosionDuration <= 0:
					if bullet in self.player1.bullets: self.player1.bullets.remove(bullet)
					if bullet in self.player2.bullets: self.player2.bullets.remove(bullet)
					continue
				
				if not bullet.exploded:

					# Destroy the bullet after the defined period of time
					if bullet.lifespan <= -bullet.decay:
						if bullet in self.player1.bullets: self.player1.bullets.remove(bullet)
						if bullet in self.player2.bullets: self.player2.bullets.remove(bullet)
						continue

					# Check if the bullet has collided with Player 1
					if bullet.detectCollision(self.player1) and self.player1.timeout <= 0:
						self.player2.score += 1
						self.player1.explode()
						bullet.explode()

					# Check if the bullet has collided with Player 2
					if bullet.detectCollision(self.player2) and self.player2.timeout <= 0:
						self.player1.score += 1
						self.player2.explode()
						bullet.explode()

			# Display the score, flashing it when the game is about to end
			if (self.tick < self.gameDuration - 20) or (self.tick*60 // 30 % 2):
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

		# End of game
		if self.tick > self.gameDuration:

			# Stop music when game first ends
			if self.isMusicPlaying:
				sound.stop("music0")
				self.isMusicPlaying = False

			# Beeping every 30 ticks
			if self.tick - self.previousBeepTime >= 0.5:
				self.previousBeepTime = self.tick
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
		if self.tick >= self.gameDuration + 3:
			return 0
		
		self.tick += deltaTime

