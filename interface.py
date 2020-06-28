from random import randrange
from math import inf

from setup import *
from vector import Vector2

class InterfaceTools:
	"""
	Container class for tools.
	Contains tools for Interface scalability and consistency.
	"""
	
	@staticmethod
	def getCanvasSize():
		"""
		Returns the canvas size in pixels.

		Example:
			>>> InterfaceTools.getCanavasSize()
			(800, 800)
		"""
		return canvas.winfo_width(), canvas.winfo_height()

	@staticmethod
	def fontSize(size):
		"""
		Returns a negative integer which scales with the window size.
		Useful for scaling font size with different window configurations.
		"""
		return int(-size * (InterfaceTools.getCanvasSize()[0] / height))

	@staticmethod
	def imageScale(scale):
		"""
		Returns an integer, with a minimum of 1, which scales with the window size.
		Useful for scaling images with different window configurations.
		"""
		return max(1, int(scale * (InterfaceTools.getCanvasSize()[0] / height)))

	@staticmethod
	def drawKeybind(position, text, anchor = "center"):
		"""
		Draw an object in the shape of a key.
		Useful for displaying keybinds and tips.
		"""
		# Draw the text
		textObject = canvas.create_text(
			pixelFromPosition(Vector2(0, 0) + position),
			text = text,
			fill = "black",
			font = ("Fixedsys", InterfaceTools.fontSize(40), ""),
			anchor = anchor
		)
		# Get the bounding box of the text object in pixels
		boundingBox = canvas.bbox(textObject)
		# Convert the bounding box into position coordinates
		boundsMin = positionFromPixel(boundingBox[0], boundingBox[1])
		boundsMax = positionFromPixel(boundingBox[2], boundingBox[3])
		center = Vector2((boundsMin.x + boundsMax.x) / 2, (boundsMin.y + boundsMax.y) / 2)
		# Minimum rectangle size
		boundsMin.x = min(boundsMin.x - 0.05, -0.075 + center.x)
		boundsMin.y = min(boundsMin.y - 0.01, -0.075 + center.y)
		boundsMax.x = max(boundsMax.x + 0.05,  0.075 + center.x)
		boundsMax.y = max(boundsMax.y + 0.01,  0.075 + center.y)
		# Draw the rectangle
		canvas.create_rectangle(
			*pixelFromPosition(boundsMin),
			*pixelFromPosition(boundsMax),
			fill = "white",
			outline = "gray",
			width = InterfaceTools.imageScale(5)
		)
		# Position the text in front of the rectangle
		canvas.tag_raise(textObject)

class InterfaceTitleLogo:
	"""
	Class used across sevel interfaces to draw the title logo.
	"""

	def __init__(self):
		self.title = tk.PhotoImage(file = "assets/title.png")
		self.scaledTitle = self.title

	def draw(self, position):
		self.scaledTitle = self.title.zoom(InterfaceTools.imageScale(8))
		return canvas.create_image(
			pixelFromPosition(position),
			image = self.scaledTitle
		)

class InterfaceMusic:
	"""
	Controls the music and ensures it is looped.
	"""

	def __init__(self, music):
		self.music = music
		self.playing = False

	def play(self):
		self.playing = True
		self.startTime = time.time()
		sound.play(self.music)

	def stop(self):
		self.playing = False
		sound.stop(self.music)

	def update(self):
		if self.playing:
			# Ignore KeyError exception on systems which cannot load the music
			try:
				musicDuration = float(sound.index[self.music]["duration"]) / 1000
			except:
				musicDuration = inf
			# If the music is over
			if (time.time() - self.startTime) > musicDuration:
				sound.play(self.music)
				self.startTime = time.time()

class InterfaceStartup:

	def __init__(self):
		self.tick = 0

	def update(self):
		if self.tick == 60:
			sound.play("beep")
		if self.tick >= 60:
			canvas.create_text(
				pixelFromPosition(Vector2(0, 0)),
				text = "Alexander Kaminsky",
				fill = "white",
				font = ("Fixedsys", InterfaceTools.fontSize(40), "")
			)
		if self.tick == 180:
			return 0
		self.tick += 1

class InterfaceSplash:

	def __init__(self, titleLogo):
		self.tick = 0
		self.titleLogo = titleLogo

	def update(self):
		self.titleLogo.draw(Vector2(0, -0.25))

		# Flash subtitle text every 30 ticks
		if self.tick // 30 % 2:
			canvas.create_text(
				pixelFromPosition(Vector2(0, 0.25)),
				text = "PRESS SPACE TO START",
				fill = "white",
				font = ("Fixedsys", InterfaceTools.fontSize(40), "")
			)

		# Input response
		if inputs.key(*binds["ui-select"]):
			sound.play("beep")
			return 0

		self.tick += 1

class InterfaceMainMenu:

	def __init__(self, titleLogo, animated = False):
		self.tick = 0
		self.animated = animated
		self.titleLogo = titleLogo
		self.selections = ["Player vs. Player", "Player vs. AI", "How to Play", "Credits"]
		self.selectionIndex = 0
		self.selectionSpacing = 0.15

	def update(self):

		if self.animated:
			# Slide animation
			self.titleLogo.draw(Vector2(0, -0.25 - (0.01 * min(self.tick, 30))))
		else:
			self.titleLogo.draw(Vector2(0, -0.55))

		# Wait 180 ticks before displaying help
		if self.tick > 180:
			# Flashing rectangle around hint
			if self.tick // 30 % 2:
				canvas.create_rectangle(
					*pixelFromPosition(Vector2(-0.75, 0.35)),
					*pixelFromPosition(Vector2( 0.75, 0.75)),
					fill = "",
					outline = "yellow",
					width = InterfaceTools.imageScale(4)
				)
			# Hint text
			canvas.create_text(
				*pixelFromPosition(Vector2(0, 0.55)),
				text = "HINT: Use the UP ARROW, DOWN\nARROW and SPACE keys to make\nyour selection...",
				fill = "white",
				font = ("Fixedsys", InterfaceTools.fontSize(25), ""),
				anchor = "center"
			)

		# Wait 30 ticks before drawing the options
		if self.tick > (30 if self.animated else 0):
			# Draw selection list
			for i, selection in enumerate(self.selections):
				canvas.create_text(
					pixelFromPosition(Vector2(-0.5, -0.25 + i * self.selectionSpacing)),
					text = self.selections[i],
					fill = "white",
					font = ("Fixedsys", InterfaceTools.fontSize(40), ""),
					anchor = "w"
				)

			# Draw cursor
			shape = [
				*pixelFromPosition(Vector2(-0.025 - 0.65, -0.275 + self.selectionIndex * self.selectionSpacing)),
				*pixelFromPosition(Vector2(-0.025 - 0.65, -0.225 + self.selectionIndex * self.selectionSpacing)),
				*pixelFromPosition(Vector2( 0.025 - 0.65, -0.250 + self.selectionIndex * self.selectionSpacing)),
			]
			canvas.create_polygon(shape, fill = "lightgrey")

			# Input response
			if inputs.key(*binds["ui-up"]):
				sound.play("beep")
				self.selectionIndex = (self.selectionIndex - 1) % len(self.selections)
			if inputs.key(*binds["ui-down"]): 
				sound.play("beep")
				self.selectionIndex = (self.selectionIndex + 1) % len(self.selections)
			if inputs.key(*binds["ui-select"]): 
				sound.play("beep")
				return self.selectionIndex
			if inputs.key(*binds["f1"]):
				if "AI vs. AI" not in self.selections:
					self.selections.append("AI vs. AI")

		self.tick += 1

class InterfaceGameSetup:

	def __init__(self, player1AI = False, player2AI = False):
		"""
		player1, player2 are boolean values that determine if the player is controlled by a human or not.
		"""
		self.tick = 0
		self.player1AI = player1AI
		self.player2AI = player2AI
		self.selectionIndex = [0, 0]
		self.colours = ["#ff6363", "#ffc163", "#88de68", "#63c6ff", "#ffffff", "#000000"]
		self.playerReady = [False, False]
		self.playerKeys = {0: ["W", "S", "SPACE"], 1: ["⭡", "⭣", "ENTER"]}
		self.timeSinceReady = 0
		self.headings = [
			"Player 1:" if not self.player1AI else "Computer:",
			"Player 2:" if not self.player2AI else "Computer:"
		]
		self.itemSpacing = 0.15

	def update(self):

		# Draw headings
		for i, heading in enumerate(self.headings):
			canvas.create_text(
				pixelFromPosition(Vector2(-0.4 + i * 0.8, -0.8)),
				text = heading,
				fill = "white",
				font = ("Fixedsys", InterfaceTools.fontSize(40), ""),
			)

		# Draw two columns (for player 1 and player 2)
		for i in range(2):
			# Draw colour selections:
			for j, colour in enumerate(self.colours):
				canvas.create_rectangle(
					*pixelFromPosition(Vector2(-0.8 + i * 0.9, -0.65 + j * self.itemSpacing)),
					*pixelFromPosition(Vector2(-0.1 + i * 0.9, -0.55 + j * self.itemSpacing)),
					fill = colour,
					width = 0
				)

			# If the player is not a computer
			if (i == 0 and not self.player1AI) or (i == 1 and not self.player2AI):
				# Draw keybinds
				InterfaceTools.drawKeybind(Vector2(-0.75 + i * 0.9, 0.35), self.playerKeys[i][0], anchor = "w")
				InterfaceTools.drawKeybind(Vector2(-0.55 + i * 0.9, 0.35), self.playerKeys[i][1], anchor = "w")
				InterfaceTools.drawKeybind(Vector2(-0.75 + i * 0.9, 0.55), self.playerKeys[i][2], anchor = "w")
				# Draw keybind captions
				canvas.create_text(
					pixelFromPosition(Vector2(-0.1 + i * 0.9, 0.35)),
					text = "Select",
					fill = "white",
					font = ("Fixedsys", InterfaceTools.fontSize(24), ""),
					anchor = "e"
				)
				canvas.create_text(
					pixelFromPosition(Vector2(-0.1 + i * 0.9, 0.55)),
					text = "Ready",
					fill = "white",
					font = ("Fixedsys", InterfaceTools.fontSize(24), ""),
					anchor = "e"
				)
			# Draw cursors, yellow and flashing every 15 ticks if ready
			if not self.playerReady[i] or self.tick // 15 % 2:
				canvas.create_rectangle(
					pixelFromPosition(Vector2(-0.825 + i * 0.9, -0.675 + self.selectionIndex[i] * self.itemSpacing)),
					pixelFromPosition(Vector2(-0.075 + i * 0.9, -0.525 + self.selectionIndex[i] * self.itemSpacing)),
					fill = "",
					outline = "yellow" if self.playerReady[i] else "white",
					width = InterfaceTools.imageScale(5)
				)		

		if not (self.playerReady[0] and self.playerReady[1]):
			self.timeSinceReady = 0
			# Flash hint text every 30 ticks
			if self.tick // 30 % 2:
				canvas.create_text(
					pixelFromPosition(Vector2(0, 0.8)),
					text = "PRESS ESC TO RETURN TO MAIN MENU",
					fill = "white",
					font = ("Fixedsys", InterfaceTools.fontSize(24), "")
				)

			# Exit to main menu
			if inputs.key(*binds["ui-escape"]):
				sound.play("beep")
				return 0
		else:
			self.timeSinceReady +=1
			# Flash game starting text every 30 ticks
			if self.tick // 30 % 2:
				canvas.create_text(
					pixelFromPosition(Vector2(0, 0.8)),
					text = "GAME STARTING...",
					fill = "white",
					font = ("Fixedsys", InterfaceTools.fontSize(24), "")
				)


		if not self.player1AI:
			if inputs.key(*binds["ui-p1-select"]):
				# Prevent both players from selecting the same colour
				if not (self.playerReady[1] and self.selectionIndex[0] == self.selectionIndex[1]):
					sound.play("beep")
					self.playerReady[0] = not self.playerReady[0]
			if not self.playerReady[0]:
				if inputs.key(*binds["ui-p1-up"]):
					sound.play("beep")
					self.selectionIndex[0] = (self.selectionIndex[0] - 1) % len(self.colours)
				if inputs.key(*binds["ui-p1-down"]):
					sound.play("beep")
					self.selectionIndex[0] = (self.selectionIndex[0] + 1) % len(self.colours)
		else:
			if self.playerReady[1] or self.player2AI:
				if not self.playerReady[0]:
					selection = randrange(0, len(self.colours))
					while selection == self.selectionIndex[1]:
						selection = randrange(0, len(self.colours))
					self.selectionIndex[0] = selection
					self.playerReady[0] = True
			else:
				self.playerReady[0] = False

		if not self.player2AI:
			if inputs.key(*binds["ui-p2-select"]):
				# Prevent both players from selecting the same colour
				if not (self.playerReady[0] and self.selectionIndex[0] == self.selectionIndex[1]):
					sound.play("beep")
					self.playerReady[1] = not self.playerReady[1]
			if not self.playerReady[1]:
				if inputs.key(*binds["ui-p2-up"]):
					sound.play("beep")
					self.selectionIndex[1] = (self.selectionIndex[1] - 1) % len(self.colours)
				if inputs.key(*binds["ui-p2-down"]):
					sound.play("beep")
					self.selectionIndex[1] = (self.selectionIndex[1] + 1) % len(self.colours)
		else:
			if self.playerReady[0] or self.player1AI:
				if not self.playerReady[1]:
					selection = randrange(0, len(self.colours))
					while selection == self.selectionIndex[0]:
						selection = randrange(0, len(self.colours))
					self.selectionIndex[1] = selection
					self.playerReady[1] = True
			else:
				self.playerReady[1] = False

		# Start the game
		if self.timeSinceReady > 120:
			return 1

		self.tick += 1

class InterfaceHelp:

	def __init__(self):
		self.tick = 0
		self.objective = (
			"Welcome to JET FIGHTER! Your objective is to\n"
			"destroy and explode your enemy as many times\n"
			"within the time given. The more, the better!\n"
			"The player with the higher score wins."
		)
		self.controls = {
			"Player 1": {
				"Accelerate": "W",
				"Decelerate": "S",
				"Turn Left": "A",
				"Turn Right": "D",
				"Shoot": "SPACE"
			},
			"Player 2": {
				"Accelerate": "⭡",
				"Decelerate": "⭣",
				"Turn Left": "⭠",
				"Turn Right": "⭢",
				"Shoot": "ENTER"
			}
		}
		self.itemSpacing = 0.2

	def update(self):
		# Draw objective help
		canvas.create_text(
			pixelFromPosition(Vector2(0, -0.85)),
			text = self.objective,
			fill = "white",
			font = ("Fixedsys", InterfaceTools.fontSize(24), ""),
			anchor = "n"
		)

		# Draw the controls
		for i, player in enumerate(self.controls):
			# Heading text
			canvas.create_text(
				pixelFromPosition(Vector2(-0.4 + i * 0.8, -0.4)),
				text = player + ":",
				fill = "white",
				font = ("Fixedsys", InterfaceTools.fontSize(40), ""),
			)
			for j, keybind in enumerate(self.controls[player]):
				# Draw keybind
				InterfaceTools.drawKeybind(
					Vector2(-0.75 + i * 0.85, -0.2 + j * self.itemSpacing),
					self.controls[player][keybind],
					anchor = "w"
				)
				# Draw text
				canvas.create_text(
					pixelFromPosition(Vector2(-0.1 + i * 0.85, -0.2 + j * self.itemSpacing)),
					text = keybind,
					fill = "white",
					font = ("Fixedsys", InterfaceTools.fontSize(24), ""),
					anchor = "e"
				)

		# Flash hint text every 30 ticks
		if self.tick // 30 % 2:
			canvas.create_text(
				pixelFromPosition(Vector2(0, 0.8)),
				text = "PRESS ESC TO RETURN TO MAIN MENU",
				fill = "white",
				font = ("Fixedsys", InterfaceTools.fontSize(24), "")
			)

		# Input response
		if inputs.key(*binds["ui-escape"]):
			sound.play("beep")
			return 0
			
		self.tick += 1

class InterfaceCredits:

	def __init__(self):
		self.tick = 0
		self.credits = (
			"JET FIGHTER\n"
			"Inspired by the 1975 arcade game\n"
			"\n"
			"\n"
			"Game Developed by:\n"
			"Alexander Kaminsky\n"
			"Maxwell Hunt\n"
			"\n"
			"Music by:\n"
			"Kevin MacLeod (incompetech.com)\n"
			"Licensed under Creative Commons:\n" 
			"By Attribution 3.0\n"
			"creativecommons.org/licenses/by/3.0/\n"
		)

	def update(self):
		# Draw credits
		canvas.create_text(
			pixelFromPosition(Vector2(0, -0.85)),
			text = self.credits,
			fill = "white",
			font = ("Fixedsys", InterfaceTools.fontSize(24), ""),
			anchor = "n"
		)

		# Flash hint text every 30 ticks
		if self.tick // 30 % 2:
			canvas.create_text(
				pixelFromPosition(Vector2(0, 0.8)),
				text = "PRESS ESC TO RETURN TO MAIN MENU",
				fill = "white",
				font = ("Fixedsys", InterfaceTools.fontSize(24), "")
			)

		# Input response
		if inputs.key(*binds["ui-escape"]):
			sound.play("beep")
			return 0
			
		self.tick += 1

class InterfaceEmpty:
	"""
	Empty interface used while the game is running.
	"""

	def __init__(self):
		pass

	def update(self):
		pass

class InterfaceManager:
	"""
	Controls the state of the user interface and switches between states when necessary.
	Each state must have an __init__ method and an update method.
	The update method is called every frame and returns an integer to signal a change of state.
	"""

	def __init__(self):
		self.currentInterface = InterfaceStartup()
		self.titleLogo = InterfaceTitleLogo()
		self.music = InterfaceMusic("music1")

	def update(self):
		self.music.update()
		response = self.currentInterface.update()
		if response != None:

			if isinstance(self.currentInterface, InterfaceStartup):
				# Completed startup
				if response == 0:
					self.currentInterface = InterfaceSplash(self.titleLogo)
					self.music.play()

			elif isinstance(self.currentInterface, InterfaceSplash):
				# User pressed space
				if response == 0:
					self.currentInterface = InterfaceMainMenu(self.titleLogo, animated = True)

			elif isinstance(self.currentInterface, InterfaceMainMenu):
				# User selected "Player vs. Player"
				if response == 0:
					self.currentInterface = InterfaceGameSetup()
				# User selected "Player vs. AI"
				elif response == 1:
					self.currentInterface = InterfaceGameSetup(player2AI = True)
				# User selected "How to Play"
				elif response == 2:
					self.currentInterface = InterfaceHelp()
				# User selected "Credits"
				elif response == 3:
					self.currentInterface = InterfaceCredits()
				# User selected "AI vs. AI"
				elif response == 4:
					self.currentInterface = InterfaceGameSetup(player1AI = True, player2AI = True)

			elif isinstance(self.currentInterface, InterfaceGameSetup):
				# User pressed escape
				if response == 0:
					self.currentInterface = InterfaceMainMenu(self.titleLogo)
				# Game started
				elif response == 1:
					self.music.stop()
					gameSetup = {
						"player1AI": self.currentInterface.player1AI,
						"player2AI": self.currentInterface.player2AI,
						"colour1": self.currentInterface.colours[self.currentInterface.selectionIndex[0]],
						"colour2": self.currentInterface.colours[self.currentInterface.selectionIndex[1]]
					}
					self.currentInterface = InterfaceEmpty()
					return gameSetup

			elif isinstance(self.currentInterface, InterfaceHelp):
				# User pressed escape
				if response == 0:
					self.currentInterface = InterfaceMainMenu(self.titleLogo)

			elif isinstance(self.currentInterface, InterfaceCredits):
				# User pressed escape
				if response == 0:
					self.currentInterface = InterfaceMainMenu(self.titleLogo)
