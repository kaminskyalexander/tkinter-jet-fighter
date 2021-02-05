if __name__ == "__main__":

	from game import Game
	from player import PlayerComputer
	from interface import InterfaceManager, InterfaceStartup, InterfaceSplash
	from setup import *

	ui = InterfaceManager()
	game = None

	def main(deltaTime):
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
		response = ui.update(deltaTime)
		if response != None:
			# Start the game
			game = Game(**response)

		if game != None:
			# Return to title screen after game completion
			response = game.update(deltaTime)
			if response == 0:
				game = None
				ui.currentInterface = InterfaceStartup()
			# Quit to title
			elif response == 1:
				game = None
				ui.currentInterface = InterfaceSplash(ui.titleLogo)
				ui.music.play()
			elif response == 2:
				game = Game(isinstance(game.player1, PlayerComputer), isinstance(game.player2, PlayerComputer), game.player1.colour, game.player2.colour)

	loop(main, 120, time.time())
	tk.mainloop()
