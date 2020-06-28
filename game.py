from player import Player
from setup import *
from vector import Vector2
from interface import InterfaceTools

class Game:
	"""
	The container for the game.
	Stores the players, responds to events in the game and controls inputs.
	"""

	def __init__(self, player1AI, player2AI, colour1, colour2, training = False, graphics = True):
		"""
		Starts the game.

		Arguments:
			player1AI (bool): If Player 1 should be controlled by AI.
			player2AI (bool): If Player 2 should be controlled by AI.
			colour1 (str): Tkinter format colour applied on Player 1.
			colour2 (str): Tkinter format colour applied on Player 2.
		"""
		self.training = training
		self.graphics = graphics
		self.tick = 0
		self.player1 = Player(Vector2(-0.5, -0.5), 90, player1AI, colour1, training = self.training)
		self.player2 = Player(Vector2(0.5, 0.5), -90, player2AI, colour2, training = self.training)
		self.gameDuration = 2 * 60 * fps
		if not self.training: sound.play("music0")

	def update(self):
		"""
		Updates all events in the game.
		Should be called every frame.
		"""
		# Game is not over
		if self.tick < self.gameDuration:
			# Register keypresses and act accordingly if the player is not an AI
			if not self.player1.computer:
				if inputs.key(*binds["p1-accelerate"]): self.player1.accelerate()
				if inputs.key(*binds["p1-decelerate"]): self.player1.decelerate()
				if inputs.key(*binds["p1-left"]):       self.player1.steerLeft()
				if inputs.key(*binds["p1-right"]):      self.player1.steerRight()
				if inputs.key(*binds["p1-shoot"]):      self.player1.shoot()
			if not self.player2.computer:
				if inputs.key(*binds["p2-accelerate"]): self.player2.accelerate()
				if inputs.key(*binds["p2-decelerate"]): self.player2.decelerate()
				if inputs.key(*binds["p2-left"]):       self.player2.steerLeft()
				if inputs.key(*binds["p2-right"]):      self.player2.steerRight()
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
			self.player1.update(canvas, self.player2, graphics = self.graphics)
			self.player2.update(canvas, self.player1, graphics = self.graphics)

			# Loop over all bullets in the game
			for bullet in self.player1.bullets + self.player2.bullets:
				bullet.update(canvas, self.graphics)
				
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
			if ((self.tick < self.gameDuration - 20 * 60) or (self.tick // 30 % 2)) and self.graphics:
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

		# Stop the music at the end of the game (skipped when training)
		if self.tick == self.gameDuration and not self.training:
			sound.stop("music0")

		# End of game (skipped when training)
		if self.tick > self.gameDuration and not self.training:

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
		if self.tick == self.gameDuration + 180 and not self.training:
			return 0

		# Instantly exit the game if training upon completion
		if self.tick == self.gameDuration and self.training:
			print(f"P1: {self.player1.score} P2: {self.player2.score}")
			return 0

		self.tick += 1

