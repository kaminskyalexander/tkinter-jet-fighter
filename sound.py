# This is unoriginal code modified to work with the game.
# Sound will only work on Windows.
# Source: https://github.com/TaylorSMarks/playsound/blob/master/playsound.py

from ctypes import c_buffer, windll
from sys import getfilesystemencoding

def winCommand(*command):
    buf = c_buffer(255)
    command = ' '.join(command).encode(getfilesystemencoding())
    errorCode = int(windll.winmm.mciSendStringA(command, buf, 254, 0))
    if errorCode:
        errorBuffer = c_buffer(255)
        windll.winmm.mciGetErrorStringA(errorCode, errorBuffer, 254)
        raise Exception(f"Error {str(errorCode)} for command:\n {command.decode()} \n\n {errorBuffer.value.decode()}")
    return buf.value

class SoundManager:

    def __init__(self, sounds):
        self.sounds = sounds
        self.index = {}

        for sound in self.sounds:
            alias = f"sound_{sound}"
            winCommand("open \"" + self.sounds[sound] + "\" alias", alias)
            winCommand("set", alias, "time format milliseconds")
            duration = winCommand("status", alias, "length")

            self.index[sound] = {
                "alias": alias,
                "duration": duration.decode()
            }

    def play(self, sound):
        try:
            alias = self.index[sound]["alias"]
            duration = self.index[sound]["duration"]
            winCommand("play", alias, "from 0 to", duration)
        except:
            raise Exception("Sound unable to play. (Incorrect index name?)")

    def stop(self, sound):
        try:
            alias = self.index[sound]["alias"]
            winCommand("stop", alias)
        except:
            raise Exception("Sound unable to stop. (Incorrect index name?)")

if __name__ == "__main__":
    import time
    sound = SoundManager(sounds = {"beep": "assets/beep.wav"})
    sound.play("beep")