'''
XBMCdisp plugin for XBMC >= 12.0
Copyright 2014 Marcel 'tanuva' Brueggebors
For license information, see the LICENSE file that must have come with this file.
'''

# =====================
# Source: http://stackoverflow.com/questions/279237/import-a-module-from-a-relative-path
import os, sys, inspect
# realpath() with make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
	sys.path.insert(0, cmd_folder)

# use this if you want to include modules from a subforder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0],"resources")))
if cmd_subfolder not in sys.path:
	sys.path.insert(0, cmd_subfolder)
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0],"resources/pyserdisp")))
if cmd_subfolder not in sys.path:
	sys.path.insert(0, cmd_subfolder)
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0],"resources/freetype-py")))
if cmd_subfolder not in sys.path:
	sys.path.insert(0, cmd_subfolder)

# Info:
# cmd_folder = os.path.dirname(os.path.abspath(__file__)) # DO NOT USE __file__ !!!
# __file__ fails if script is called in different ways on Windows
# __file__ fails if someone does os.chdir() before
# sys.argv[0] also fails because it doesn't not always contains the path
# =====================

from time import sleep # Sounds quite relaxed.
import xbmc
import xbmcaddon
from graphdisp import GraphDisp
from lcdmode import LcdMode

__settings__   = xbmcaddon.Addon(id='script.tanuva.xbmcdisp')
#__cwd__        = __settings__.getAddonInfo('path')

# Needed for notifications
__icon__       = os.path.join(__settings__.getAddonInfo("path"), "icon.png")
__scriptname__ = "XBMCdisp"

class XbmcDisp:
	def __init__(self, device, model, options = ""):
		if not xbmc.abortRequested:
			self.disp = GraphDisp(device, model, options)
			self.disp.showText([0, 0], "Hello!")
			self.disp.update()

	def __enter__(self):
		self.disp.__enter__()

	def __exit__(self, type, value, traceback):
		self.disp.__exit__(type, value, traceback)

	def __showDisplayConnectResult(self):
		print "showDisplayConnectResult"

		# Review this before use!
		#if not g_failedConnectionNotified:
		#	text = __settings__.getLocalizedString(32500)
		#	xbmc.executebuiltin("XBMC.Notification(%s,%s,%s,%s)" % (__scriptname__, text, 10, __icon__))
		#else:
		#	text = __settings__.getLocalizedString(32501)
		#if not g_initialConnectAttempt:
		#	xbmc.executebuiltin("XBMC.Notification(%s,%s,%s,%s)" % (__scriptname__, text, 10, __icon__))

	'''
	def __getPlaybackMode(self):
		result = LcdMode.GENERAL

		if navActive:
			result = LcdMode.NAVIGATION
		elif screenSaver:
			result = LcdMode.SCREENSAVER
		elif playingPVRTV:
			result = LcdMode.PVRTV
		elif playingPVRRadio:
			result = LcdMode.PVRRADIO
		elif playingTVShow:
			result = LcdMode.TVSHOW
		elif playingVideo:
			result = LcdMode.VIDEO
		elif playingMusic:
			result = LcdMode.MUSIC

		return result
	'''

	def update(self):
		print "update"
		self.disp.update()

if __name__ == "__main__":
	# Surround this with try/catch and notify user
	#with XbmcDisp("USB:7c0/1501", "CTINCLUD") as disp:
	#	# Enter our main loop
	#	while not xbmc.abortRequested:
	#		disp.update()
	#		sleep(1) # seconds

	lastOut = ""

	while not xbmc.abortRequested:
		player = xbmc.Player()
		output = "XBMCdisp "
		if player.isPlayingVideo():
			output += "Video: "
			print "turning off backlight"
		elif player.isPlayingAudio():
			# check for playing/paused state
			# show state icon
			output += "Audio: "
			tag = player.getMusicInfoTag()
			output += tag.getArtist() + " - " + tag.getTitle() + " (" + tag.getAlbum() + ")"
		if player.isPlaying() and not lastOut == output:
			print output
			lastOut = output

		sleep(1)
