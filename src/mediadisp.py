"""
Copyright 2014-2017 Marcel 'tanuva' Kummer
For license information, see the LICENSE file that must have come with this file.
"""

# =====================
# Source: http://stackoverflow.com/questions/279237/import-a-module-from-a-relative-path
import os, sys, inspect
# realpath() with make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

# use this if you want to include modules from a subfolder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0],"../pyserdisp/PySerdisp")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
# ======================

from time import sleep
from datetime import datetime
from settings import Settings
from pyserdisp import Serdisp
from musicscreen import MusicScreen
from idlescreen import IdleScreen

class MediaDisp:
    def __init__(self, serdisp, args):
        self.__serdisp = serdisp
        self.__args = args
        self.__wasDisplayOn = True
        self.__screens = {
            "music": MusicScreen(self.__serdisp, Settings, args),
            "idle": IdleScreen(self.__serdisp, Settings, args)
        }

    def __s(self, name):
        return self.__screens[name]

    def run(self):
        musicRunning = self.__s("music").hasContent()
        isDisplayOn = self.isDisplayOn(musicRunning)

        if self.__wasDisplayOn and not isDisplayOn:
            self.__serdisp.quit()
            self.__wasDisplayOn = False
        elif not self.__wasDisplayOn and isDisplayOn:
            self.__serdisp.init()
            self.__serdisp.clear()
            self.__wasDisplayOn = True

        if not isDisplayOn:
            return

        if musicRunning:
            self.__s("music").update()
        else:
            # Display something useful :)
            self.__s("idle").update()

        self.__serdisp.update()

    def isDisplayOn(self, musicRunning):
        curTime = datetime.now()
        isOn = False

        def isNewYearsEve():
            return ((curTime.day == 31 and curTime.month == 12 and curTime.hour >= 7)
                or (curTime.day == 1 and curTime.month == 1 and curTime.hour < 2))

        # rule priority increasing downward (obviously)
        if curTime.hour >= 7 and curTime.hour < 23:
            isOn = True
        if isNewYearsEve():
            isOn = True
        if musicRunning:
            isOn = True

        return isOn

def parseArgs():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-network", "-n", dest="network", action="store_const",
        const=False, default=True,
        help='Disable network requests')
    parser.add_argument("--tlimit", "-t", dest="tlimit", default=None, type=int,
        help='Quit after the specified time limit (seconds). Also disables the frame limiter.')

    return parser.parse_args()

if __name__ == "__main__":
    args = parseArgs()
    starttime = datetime.now()
    frames = 0

    with Serdisp(Settings.dispDevice, Settings.dispModel) as serdisp:
        disp = MediaDisp(serdisp, args)
        while True:
            disp.run()

            if args.tlimit:
                frames += 1
                if (datetime.now() - starttime).seconds >= args.tlimit:
                    break
            else:
                sleep(5)

        if args.tlimit:
            diff = datetime.now() - starttime
            print("Frames: %i FPS: %s" % (frames, frames / diff.seconds))
