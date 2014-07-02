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

# use this if you want to include modules from a subfolder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0],"../pyserdisp")))
if cmd_subfolder not in sys.path:
	sys.path.insert(0, cmd_subfolder)
# ======================

from datetime import datetime
from time import sleep
import requests
import json
from graphdisp import GraphDisp

class XbmcDisp:
	def __init__(self, graphDisp):
		self.graphDisp = graphDisp
		self.graphDisp.drawText([0, 0], "Bananaa!", (255), "center", "center")
		self.graphDisp.flip()

		self.headers = {'content-type': 'application/json'}

		# Will contain player ids with player type as key (audio/video)
		self.players = {}

	def __request(self, data):
		r = requests.post("http://pi:8080/jsonrpc", json.dumps(data), headers=self.headers)
		return r.json()

	def __getPlayers(self):
		query = {"jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": 1}
		result = self.__request(query)
		#{
		#	"id":1,
		#	"jsonrpc":"2.0",
		#	"result": [{
		#		"playerid": 0,
		#		"type": "audio"
		#	}]
		#}
		self.players = {}
		for player in result["result"]:
			self.players[player["type"]] = player["playerid"]
		return self.players

	def __getPlayingAudio(self):
		try:
			query = {
				'params': {
					'playerid': self.players["audio"],
					'properties': [
					'title', 'album', 'artist', 'duration'
					]
				},
				'jsonrpc': '2.0',
				'method': 'Player.GetItem',
				'id': 'AudioGetItem'
			}
		except KeyError:
			print "getPlayingAudio: No audio player known!"
			return

		result = self.__request(query)
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
		
		item = result["result"]["item"]
		item["artist"] = item["artist"][0]
		return item

	def run(self):
		self.__getPlayers()
		if "audio" in self.players.keys():
			# Audio is playing
			# Due to race condition the player might be invalid till now
			tags = self.__getPlayingAudio()
			if tags:
				self.graphDisp.drawText([0,0], tags["title"], (255), "left", "", 12)
				self.graphDisp.drawText([0,13], tags["artist"], (255), "left", 10)
				self.graphDisp.drawText([0,23], tags["album"], (255), "left", 10)
				self.graphDisp.drawProgressBar([0,59], [128,5], .3)
		else:
			# Display something useful :)
			curTime = datetime.now()
			self.graphDisp.drawText([0,0], "{:%H:%M}".format(curTime), (255), "center", "center", 52)

		self.graphDisp.flip()

if __name__ == "__main__":
	with GraphDisp("USB:7c0/1501", "CTINCLUD") as disp:
		server = XbmcDisp(disp)
		while True:
			server.run()
			sleep(3)
