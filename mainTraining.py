from game import Game
from setup import *

gameArguments = {
	"player1AI": True,
	"player2AI": True,
	"colour1": "white",
	"colour2": "black",
	"training": True,
	"graphics": True
}

game = Game(**gameArguments)
startTime = time.time()

def main():
	"""
	The main loop of the process.
	Called every frame.
	"""
	global game, fullscreen, startTime

	# Clear all objects from the screen
	canvas.delete("all")

	# Update input dictionary
	inputs.refresh()

	# Fullscreen
	if inputs.key(*binds["f11"]):
		fullscreen = not fullscreen
		root.attributes("-fullscreen", fullscreen)

	# Graphics toggle
	if inputs.key(*binds["f12"]):
		game.graphics = gameArguments["graphics"] = not game.graphics

	# Restart game on completion
	if game.update() == 0:
		game = Game(**gameArguments)
		print(f"Game completed in: {time.time() - startTime}s")
		startTime = time.time()
	
	canvas.after(1, main)

main()

tk.mainloop()