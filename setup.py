import time
import tkinter as tk

from inputs import InputListener
from sound import SoundManager
from vector import Vector2

# Initialize Tkinter
width = 800
height = 800
fullscreen = False
root = tk.Tk()
root.config(bg = "#000", width = width, height = height)
root.minsize(400, 400)
root.title("Jet Fighter")
iconPhotoImage = tk.PhotoImage(file = "assets/icon.png")
root.iconphoto(False, iconPhotoImage)

# Create the canvas
canvas = tk.Canvas(
    root,
    width = width,
    height = height,
    bg = "#444",
    highlightthickness = 0
)
canvas.pack()

# Resize the canvas manually to ensure the aspect ratio stays locked
def scaleCanvas(event):
	size = min(event.width, event.height)
	canvas.configure(width = size, height = size)
root.bind("<Configure>", scaleCanvas)

# Initialize all sounds
sound = SoundManager({
	"beep": "assets/beep.wav",
	"explosion": "assets/explosion.wav",
	"music0": "assets/music0.wav",
	"music1": "assets/music1.wav",
	"shoot": "assets/shoot.wav"
})

# Initialize the input manager
inputs = InputListener(root)

# Dictionary of all keybindings
binds = {
	# Modifiers .......................
	"shift": (16, "press"),
	"ctrl": (17, "press"),
	"alt": (18, "press"),
	# Function ........................
	"f1": (112, "trigger"),
	"f2": (113, "trigger"),
	"f3": (114, "trigger"),
	"f4": (115, "trigger"),
	"f5": (116, "trigger"),
	"f6": (117, "trigger"),
	"f7": (118, "trigger"),
	"f8": (119, "trigger"),
	"f9": (120, "trigger"),
	"f10": (121, "trigger"),
	"f11": (122, "trigger"),
	"f12": (123, "trigger"),
	# Gameplay ........................
	"p1-accelerate": (87, "press"),
	"p1-decelerate": (83, "press"),
	"p1-left": (65, "press"),
	"p1-right": (68, "press"),
	"p1-shoot": (32, "trigger"),
	"p2-accelerate": (38, "press"),
	"p2-decelerate": (40, "press"),
	"p2-left": (37, "press"),
	"p2-right": (39, "press"),
	"p2-shoot": (13, "trigger"),
	# Interface .......................
	"ui-select": (32, "trigger"),
	"ui-up": (38, "trigger"),
	"ui-down": (40, "trigger"),
	"ui-escape": (27, "trigger"),
	"ui-p1-up": (87, "trigger"),
	"ui-p1-down": (83, "trigger"),
	"ui-p1-select": (32, "trigger"),
	"ui-p2-up": (38, "trigger"),
	"ui-p2-down": (40, "trigger"),
	"ui-p2-select": (13, "trigger"),
}

# Force show the window
root.focus_force()

class Direction:
	LEFT = 0
	RIGHT = 1
	FORWARD = UP = 2 
	BACKWARD = DOWN = 3

def loop(function, fpsLimit, previousTime):
	"""
	Wrapper function for the main update.
	Calls the supplied function every frame.
	"""
	# Get time when function call begins
	startTime = time.time()
	# Call the function, find delta time
	function(startTime - previousTime)
	# Get the amount of time which the function call took
	wait = time.time() - startTime
	# Amount of time one frame takes
	frameTime = 1000 // fpsLimit
	# Adjusted delay for how long the function took to run
	delay = max(int(frameTime - wait), 1)
	# Run the function again after the set delay time
	canvas.after(delay, lambda: loop(function, fpsLimit, startTime))

def pixelFromPosition(position):
	"""
	Converts a position into a pixel coordinate.

	Arguments:
		position (Vector2): The position to convert.

	Returns:
		tuple:float: Pixel coordinates.
	"""
	# Get the size of the window
	width = canvas.winfo_width()
	height = canvas.winfo_height()
	# Get the coordinates in pixels based on the window width and height
	# This should let the window be stretchable
	x = (width/2)  + (height/2) * position.x
	y = (height/2) + (height/2) * position.y
	return x, y
	
def positionFromPixel(x, y):
	"""
	Converts a pixel coordinate into a position.

	Arguments:
		tuple:float: The pixel coordinate to convert.

	Returns:
		Vector2: The position.
	"""
	# Get the size of the window
	width = canvas.winfo_width()
	height = canvas.winfo_height()
	return Vector2((x - width/2) / (height/2), (y - height/2) / (height/2))

def onWindowClose():
	sound.quit()
	root.destroy()
	quit()

root.protocol("WM_DELETE_WINDOW", onWindowClose)