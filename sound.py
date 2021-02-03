# This is unoriginal code modified to work with the game.
# Sound will only work on Windows.
# Source: https://github.com/TaylorSMarks/playsound/blob/master/playsound.py

try:
	from ctypes import c_buffer, windll
	from sys import getfilesystemencoding
except:
	pass

import multiprocessing

class SoundCommand:
	PLAY = 0
	STOP = 1

class SoundProcessWorker(multiprocessing.Process):

	def __init__(self, taskQueue, sounds):

		multiprocessing.Process.__init__(self)
		self.taskQueue = taskQueue

		self.sounds = sounds
		self.index = {}

	def run(self):
		# Opens each sound and stores it in the index
		for sound in self.sounds:
			alias = f"sound_{sound}"
			self.winCommand("open \"" + self.sounds[sound] + "\" alias", alias)
			self.winCommand("set", alias, "time format milliseconds")
			duration = self.winCommand("status", alias, "length")

			self.index[sound] = {
				"alias": alias,
				"duration": duration.decode()
			}

		while True:
			nextTask = self.taskQueue.get()
			if nextTask:
				if nextTask[0] == SoundCommand.PLAY:
					self.play(nextTask[1])
				elif nextTask[0] == SoundCommand.STOP:
					self.stop(nextTask[1])

	def play(self, sound):
		try:
			alias = self.index[sound]["alias"]
			duration = self.index[sound]["duration"]
			self.winCommand("play", alias, "from 0 to", duration)
		except:
			raise Exception("Sound unable to play. (Incorrect index name?)")

	def stop(self, sound):
		try:
			alias = self.index[sound]["alias"]
			self.winCommand("stop", alias)
		except:
			raise Exception("Sound unable to stop. (Incorrect index name?)")

	def winCommand(self, *command):
		buf = c_buffer(255)
		command = ' '.join(command).encode(getfilesystemencoding())
		errorCode = int(windll.winmm.mciSendStringA(command, buf, 254, 0))
		if errorCode:
			errorBuffer = c_buffer(255)
			windll.winmm.mciGetErrorStringA(errorCode, errorBuffer, 254)
			raise Exception(f"Error {str(errorCode)} for command:\n {command.decode()} \n\n {errorBuffer.value.decode()}")
		return buf.value

class SoundManager:
	"""
	Controls sounds. 
	IMPORTANT: This tool only works on Windows.
	"""

	def __init__(self, sounds):
		"""
		Initialize the sound manager.

		Arguments:
			sounds (dict): List of sounds formatted name:filepath
		"""
		try:
			self.taskQueue = multiprocessing.JoinableQueue()
			self.processWorker = SoundProcessWorker(self.taskQueue, sounds)
			self.processWorker.start()
		except:
			print("Sound manager encountered an error! Sounds will not play.")

	def play(self, sound):
		"""
		Plays a sound.

		Arguments:
			sound (str): The sound index to play.
		"""
		try:
			self.taskQueue.put((SoundCommand.PLAY, sound))
		except:
			print("Sound manager encountered an error! Sounds will not play.")

	def stop(self, sound):
		"""
		Stops a sound.

		Arguments:
			sound (str): The sound index to stop.
		"""
		try:
			self.taskQueue.put((SoundCommand.STOP, sound))
		except:
			print("Sound manager encountered an error! Sounds will not play.")

	def quit(self):
		self.processWorker.terminate()

# Test the program.
if __name__ == "__main__":
	sound = SoundManager(sounds = {"beep": "assets/beep.wav"})
	sound.play("beep")