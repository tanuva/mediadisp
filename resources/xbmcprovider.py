import xbmc
import xbmcaddon

class XbmcProvider:
	self.player = xbmc.Player()

	def __init__(self):
		self.player.onPlaybackEnded = XbmcProvider.onPlaybackEnded

	def getMediaTag(self):
		if player.isPlayingAudio():
			return player.getMusicInfoTag()
		if player.isPlayingVideo():
			return player.getVideoInfoTag()

	def getTime(self):
		return self.player.getTime()

	def getTotalTime(self):
		return self.player.getTotalTime()

	def onPlaybackEnded(self):
		print "playback ended"