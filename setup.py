import tkinter as tk
import time

root = tk.Tk()
width = 800
height = 800
fps = 60

canvas = tk.Canvas(
    root,
    width = width,
    height = height,
    bg = "#000",
    highlightthickness = 0
)
canvas.pack(fill = "both", expand = True)

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
	"f12": (133, "trigger"),
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
	"p2-shoot": (13, "trigger")
}

# Force show the window
root.focus_force()

def loop(function):
	# Get time when function call begins
	startTime = time.time()
	# Call the function
	function()
	# Get the amount of time which the function call took
	wait = time.time() - startTime
	# Amount of time one frame takes
	frameTime = 1000 // fps
	# Adjusted delay for how long the function took to run
	delay = max(int(frameTime - wait), 1)
	# Run the function again after the set delay time
	canvas.after(delay, lambda: loop(function))
	
