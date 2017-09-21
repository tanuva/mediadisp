from datetime import datetime
import json
import requests
import widget as gd

# This file is unmaintained and will probably not work!

class XbmcDataProvider:
	def __init__(self, settings):
		self.__settings = settings
		self.__headers = {'content-type': 'application/json'}
		# Will contain player ids with player type as key (audio/video)
		# { "audio": 1, "video": 2 }
		self.__players = {}

	def __request(self, data):
		try:
			url = self.__settings.xbmcHost
			if not url[-1] == "/":
				url = url + "/"
			url = url + "jsonrpc"
			r = requests.post(url, json.dumps(data), headers=self.__headers)
		except Exception, e:
			print e
			print "Couldn't connect to XBMC. Retrying..."
			return None
		if not r.status_code == 200:
			print "JSON RPC failed:", r
			return None
		return r.json()

	def getPlayers(self):
		query = {"jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": 1}
		result = self.__request(query)
		if not result:
			return None

		#{
		#	"id":1,
		#	"jsonrpc":"2.0",
		#	"result": [{
		#		"playerid": 0,
		#		"type": "audio"
		#	}]
		#}
		self.__players = {}
		for player in result["result"]:
			self.__players[player["type"]] = player["playerid"]
		return self.__players

	def getPlayingAudio(self):
		try:
			query = {
				'jsonrpc': '2.0',
				'method': 'Player.GetItem',
				'id': 'AudioGetItem',
				'params': {
					'playerid': self.__players["audio"],
					'properties': [
						'title', 'album', 'artist', 'duration'
					]
				}
			}
		except KeyError:
			print "getPlayingAudio: No audio player known!"
			return

		result = self.__request(query)
		if not result:
			return None
		#{	u'jsonrpc': u'2.0',
		#	u'id': u'AudioGetItem',
		#	u'result': {
		#		u'item': {
		#			u'album': u'Fu\xdfball, WWDC-Nachlese und Google I/O',
		#			u'artist': [u'Freak Show'],
		#			u'title': u'FS135 Das Update ist jetzt freigegeben',
		#			u'duration': 0
		#		}
		#	}
		#}

		if "error" in result:
			return { 'album': "",
				'artist': result["error"]["message"],
				'title': "Error" }
		item = result["result"]["item"]

		# Kodi seldomly served weird results here. This didn't crash for quite a while though,
		# so either the workaround is actually working around or Kodi was fixed. Was never able
		# to track this down completely. :)
		try:
			if "artist" in item.keys() and len(item["artist"]) > 0:
				item["artist"] = item["artist"][0] # artist is a list. wtf.
			else:
				item["artist"] = ""
				item["album"] = ""
		except:
			# something strange is happening
			print "ERROR: len(item[\"artist\"]) failed on this data:", result
		return item

	def getAudioPlayerPosition(self):
		try:
			query = {
				'jsonrpc': '2.0',
				'method': 'Player.GetProperties',
				'id': 'GetPercentage',
				'params': {
					'playerid': self.__players["audio"],
					'properties': [
						'percentage'
					]
				}
			}
		except KeyError:
			print "getPlayerPosition: No audio player known!"
			return

		result = self.__request(query)
		if not result or not "result" in result.keys():
			return None

		return result["result"]["percentage"] / 100.0

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

		self.xbmc = XbmcDataProvider(settings)

	def getPlayers(self):
		players = self.xbmc.getPlayers()
		return [] if not players else players.keys()

	def update(self):
		tags = self.xbmc.getPlayingAudio()
		progress = self.xbmc.getAudioPlayerPosition()
		if not tags:
			return # Possible race condition

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
