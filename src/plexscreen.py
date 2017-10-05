from datetime import datetime
from plexapi.myplex import MyPlexAccount
import widget as gd

class PlexDataProvider:
	def __init__(self, settings):
		self.__settings = settings
		account = MyPlexAccount(settings.plex["user"], settings.plex["password"])
		self.__plex = account.resource(settings.plex["servername"]).connect()

	def getPlayers(self):
		sessions = self.__plex.sessions()
		return ["audio"] if len(sessions) > 0 else []

	def getPlayingAudio(self):
		sessions = self.__plex.sessions()
		if len(sessions) == 0:
			return {
				"artist": "",
				"album": "",
				"title": ""
			}

		session = sessions[0]
		return {
			"artist": session.artist().title,
			"album": session.parentTitle,
			"title": session.title
		}

	def getAudioPlayerPosition(self):
		sessions = self.__plex.sessions()
		if len(sessions) == 0:
			return 0

		duration = float(sessions[0].duration)
		current = float(sessions[0].viewOffset)
		return current / duration

class MusicScreen:
	def __init__(self, disp, settings):
		self.disp = disp
		# draw layout only once
		self.bg = gd.Pixmap(disp, "layout-music.png", [0, 0])
		# text slots
		font = "DroidSans.ttf"
		self.time   = gd.Text(disp, [0,2], font, 12, "00:00", halign = "center")
		self.title  = gd.Text(disp, [0,14], font, 14, "Title", halign = "center")
		self.artist = gd.Text(disp, [3,35], font, 12, "Artist")
		self.album  = gd.Text(disp, [3,50], font, 12, "Album")
		# progress bar
		self.progress = gd.Progressbar(disp, [0,30], [128,4], border=False)

		self.plex = PlexDataProvider(settings)

	def getPlayers(self):
		players = self.plex.getPlayers()
		return players

	def update(self):
		tags = self.plex.getPlayingAudio()
		progress = self.plex.getAudioPlayerPosition()

		self.bg.draw()
		curTime = datetime.now()
		self.time.setText("{:%H:%M}".format(curTime))
		self.time.draw()
		self.title.setText(tags["title"])
		self.title.draw()
		self.artist.setText(tags["artist"])
		self.artist.draw()
		self.album.setText(tags["album"])
		self.album.draw()
		self.progress.setState(progress)
		self.progress.draw()
