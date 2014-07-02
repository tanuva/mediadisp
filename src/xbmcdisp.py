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

from time import sleep
import requests
import json
from graphdisp import GraphDisp
from musicscreen import MusicScreen
from idlescreen import IdleScreen

class XbmcDisp:
	def __init__(self, graphDisp):
		self.graphDisp = graphDisp
		self.screens = {}
		self.screens["music"] = MusicScreen(self.graphDisp)
		self.screens["idle"] = IdleScreen(self.graphDisp)
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
		item["artist"] = item["artist"][0] # artist is a list. wtf.
		return item

	def run(self):
		self.__getPlayers()
		if "audio" in self.players.keys():
			# Audio is playing
			# Due to race condition the player might be invalid till now
			tags = self.__getPlayingAudio()
			if tags:
				self.screens["music"].update(tags)
		else:
			# Display something useful :)
			self.screens["idle"].update()

		self.graphDisp.flip()

if __name__ == "__main__":
	with GraphDisp("USB:7c0/1501", "CTINCLUD") as graphDisp:
		disp = XbmcDisp(graphDisp)
		while True:
			disp.run()
			sleep(3)
