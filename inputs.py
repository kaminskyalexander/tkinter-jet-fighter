# Tkinter Input Listener

# Initializing .................................................................
# Start the input listener by initializing this class. The root argument must be
# an instance of Tkinter's Tk() class.

# Refreshing Inputs ............................................................
# To refresh the inputs dictionary, the refresh() method must be called every
# main loop. This should be called once before checking for input states to
# minimize input lag/delay.

# Input Format .................................................................
# The inputs dictionary stores values in the following format:
# Keyboard presses:     (keycode, state)
# Mouse button presses: (button, state)
# Mouse motion:         (x, y)
# * A keycode is a numerical value unique for every key. A good reference for
#   finding a keycode for a certain key is the website https://keycode.info.
# * Mouse button corresponds to a numerical value of a certain mouse button
#   (left click is 1, middle click is 2, right click is 3).
# * Mouse motion is a coordinate with the origin at the top right of the window.
# * Valid states are: "trigger", "press", "release" and "*" (wildcard).

# Retrieving Keyboard and Mouse Button Presses..................................
# A list of tuples is returned via the properties self.keys and self.buttons.
# Each tuple follows the formats specified in the input format section.

# Retrieving Mouse Motion.......................................................
# Use the self.motion property to get a (x, y) tuple of the mouse position.

# Verifying if a Keyboard or Mouse Button is Pressed ...........................
# You can check if a key or mouse button is pressed with the keys() and
# buttons() methods. Both functions take two arguments corresponding to the
# format specified in the input format section. By default, state is set to
# wildcard. The functions returns the key if it matches the arguments; it
# otherwise returns None.


class InputListener:

	def __init__(self, root):
		self.listening = True
		self.reset()

		root.bind("<KeyPress>",      lambda event: self.queue.append(event))
		root.bind("<KeyRelease>",    lambda event: self.queue.append(event))
		root.bind("<ButtonPress>",   lambda event: self.queue.append(event))
		root.bind("<ButtonRelease>", lambda event: self.queue.append(event))
		root.bind("<Motion>",        lambda event: self.queue.append(event))
		root.bind("<FocusIn>",       lambda event: self.focus(event))
		root.bind("<FocusOut>",      lambda event: self.focus(event))

	def focus(self, event):
		# Focus In
		if event.type == "9":
			self.reset()
			self.listening = True
		# Focus Out
		elif event.type == "10":
			self.reset()
			self.listening = False
			
	def reset(self):
		self.inputs = {"keys": [], "buttons": [], "motion": (0, 0)}
		self.queue = []

	@property
	def keys(self): return self.inputs["keys"]
	@property
	def buttons(self): return self.inputs["buttons"]
	@property
	def motion(self): return self.inputs["motion"]

	def key(self, keycode, state = "*"):
		if state == "*":
			keycodes = [i[0] for i in self.keys]
			if keycode in keycodes:
				return self.keys[keycodes.index(keycode)]
		else:
			if (keycode, state) in self.keys:
				return (keycode, state)

	def button(self, button, state = "*"):
		if state == "*":
			buttons = [i[0] for i in self.buttons]
			if button in buttons:
				return self.buttons[buttons.index(button)]
		else:
			if (button, state) in self.buttons:
				return (button, state)

	def refresh(self):

		if self.listening:

			for key in self.keys:
				if key[1] == "trigger":
					self.keys.remove(key)
				if key[1] == "release":
					self.keys.remove(key)

			for button in self.buttons:
				if button[1] == "trigger":
					self.buttons.remove(button)
				if button[1] == "release":
					self.buttons.remove(button)

			for event in self.queue:

				# Key Press
				if event.type == "2":
					instance = self.key(event.keycode)
					if not instance:
						self.keys.append((event.keycode, "trigger"))
						self.keys.append((event.keycode, "press"))

				# Key Release
				if event.type == "3":
					instance = self.key(event.keycode)
					if instance:
						self.keys.remove(instance)
						self.keys.append((event.keycode, "release"))

				# Mouse Button Press
				if event.type == "4":
					instance = self.button(event.num)
					if not instance:
						self.buttons.append((event.num, "trigger"))
						self.buttons.append((event.num, "press"))

				# Mouse Button Release
				if event.type == "5":
					instance = self.button(event.num)
					if instance:
						self.buttons.remove(instance)
						self.buttons.append((event.num, "release"))

				# Motion
				if event.type == "6":
					self.inputs["motion"] = event.x, event.y
			
			self.queue.clear()