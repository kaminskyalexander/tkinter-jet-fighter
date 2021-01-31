from game import Game
from interface import InterfaceManager, InterfaceStartup
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
		if game.update(deltaTime) == 0:
			game = None
			ui.currentInterface = InterfaceStartup()

loop(main, 120, time.time())
tk.mainloop()
