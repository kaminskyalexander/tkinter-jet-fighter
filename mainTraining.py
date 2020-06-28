from game import Game
from ml.agent import DQNAgent
from setup import *
import os

import numpy as np

gameArguments = {
	"player1AI": False,
	"player2AI": False,
	"colour1": "white",
	"colour2": "black",
	"training": True,
	"graphics": True
}

GLOBAL_TICK = 0
GAMES_PLAYED = 0
agent = DQNAgent(10, 5)

print("JET FIGHTER DQN TRAINING\nTo play the main game run **main.py**")
loadWeights = input("Load existing weights? [y/n]").lower()
while loadWeights not in ("y", "n"):
	loadWeights = input("Load existing weights? [y/n]").lower()
if loadWeights == "y":
	agent.load("ml-output/" + input("File name (excluding ml-output): "))

game = Game(**gameArguments)
startTime = time.time()

def getPlayerState(player):
	return [
		player.position.x / 2 + 0.5,
		player.position.y / 2 + 0.5,
		player.angle / 360,
		(player.speed - player.minimumSpeed) / (player.maximumSpeed - player.minimumSpeed),
		int(player.timeSinceLastShot > player.shootCooldown)
	]

def main():
	"""
	The main loop of the process.
	Called every frame.
	"""
	global game, fullscreen, startTime, GLOBAL_TICK, GAMES_PLAYED
	GLOBAL_TICK += 1

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

	player1Info = getPlayerState(game.player1)
	player2Info = getPlayerState(game.player2)

	state = np.array([player1Info + player2Info])
	action = agent.act(state)
	enemyAction = np.argmax(agent.policyNetwork.predict(np.array([player2Info + player1Info]))[0])

	if   action == 0: game.player1.steerLeft()
	elif action == 1: game.player1.steerRight()
	elif action == 2: game.player1.accelerate()
	elif action == 3: game.player1.decelerate()
	elif action == 4: game.player1.shoot()

	if   enemyAction == 0: game.player2.steerLeft()
	elif enemyAction == 1: game.player2.steerRight()
	elif enemyAction == 2: game.player2.accelerate()
	elif enemyAction == 3: game.player2.decelerate()
	elif enemyAction == 4: game.player2.shoot()

	# Restart game on completion
	result = game.update()
	reward = 0
	if game.player1.score == 1:
		game.player1.score = 0
		reward = 1
	elif game.player2.score == 1:
		game.player2.score = 0
		reward = -1
	done = True if result == 0 else False

	nextState = np.array([getPlayerState(game.player1) + getPlayerState(game.player2)])

	agent.remember(state, nextState, action, reward, done)
	if GLOBAL_TICK % 300 == 0:
		if len(agent.memory) > 32:
			agent.replay(32)

	if GLOBAL_TICK % 1500 == 0:
		print(f"Episode: {GAMES_PLAYED} Epsilon: {agent.epsilon}")
		agent.policyNetwork.set_weights(agent.targetNetwork.get_weights())

	if done:
		GAMES_PLAYED += 1
		if GAMES_PLAYED % 5 == 0:
			if not os.path.exists("ml-output"):
				os.mkdir("ml-output")
			agent.save(f"ml-output/weights_{GAMES_PLAYED}.hdf5")
			print("Agent saved to folder ml-output")
		game = Game(**gameArguments)
		print(f"Game completed in: {time.time() - startTime}s")
		startTime = time.time()
	
	canvas.after(1, main)

main()

tk.mainloop()