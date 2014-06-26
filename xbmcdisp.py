'''
XBMCdisp plugin for XBMC >= 12.0
Copyright 2014 Marcel 'tanuva' Brueggebors
For license information, see the LICENSE file that must have come with this file.
'''

from time import sleep # Sounds quite relaxed.
import xbmc
import xbmcaddon
from lcdmode import LcdMode

#__settings__   = xbmcaddon.Addon(id='script.tanuva.xbmcdisp')
#__cwd__        = __settings__.getAddonInfo('path')

# Needed for notifications
#__icon__       = os.path.join(__settings__.getAddonInfo("path"), "icon.png")
#__scriptname__ = "XBMCdisp"

class XbmcDisp:

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
		#from datetime import datetime
		#curTime = datetime.now()
		#self.graphdisp.drawText([0,0],
		#	"{:%H:%M:%S}".format(curTime),
		#	self.graphdisp.serdisp.BLACK,
		#	"center", "top")
		#self.graphdisp.drawText([0, 0], "Let the sun shine!", self.graphdisp.serdisp.BLACK, "center", "center")
		#self.graphdisp.drawProgressBar([0, 60], [128, 4], curTime.second / 60.0)
		#import timeit
		#print timeit.timeit(self.graphdisp.flip, "gc.enable()", number=1)

		player = xbmc.Player()
		if player.isPlayingAudio():
			# check for playing/paused state
			tag = player.getMusicInfoTag()
			self.graphdisp.drawText([0,0], tag.getArtist(), "left", "top")
			self.graphdisp.drawText([0,0], tag.getTitle(), "right", "center")
			self.graphdisp.drawText([0,0], tag.getAlbum(), "left", "bottom")
		else:
			self.graphdisp.clear()
		self.graphdisp.flip()

if __name__ == "__main__":
	