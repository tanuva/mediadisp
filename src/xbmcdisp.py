"""
Copyright 2014-2015 Marcel 'tanuva' Brueggebors
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
import requests
import json
from settings import Settings
from pyserdisp import Serdisp
from musicscreen import MusicScreen
from idlescreen import IdleScreen

class XbmcDisp:
	def __init__(self, serdisp):
		self.__serdisp = serdisp
		self.__wasDisplayOn = True
		self.__screens = {}
		self.__screens["music"] = MusicScreen(self.__serdisp)
		self.__screens["idle"] = IdleScreen(self.__serdisp)
		self.__headers = {'content-type': 'application/json'}
		# Will contain player ids with player type as key (audio/video)
		# { "audio": 1, "video": 2 }
		self.__players = {}

	def __request(self, data):
		try:
			url = Settings.xbmcHost
			if not url[-1] == "/":
				url = url + "/"
			url = url + "jsonrpc"
			r = requests.post(url, json.dumps(data), headers=self.__headers)
		except Exception, e:
			print e
			print "Couldn't connect to XBMC. Retrying..."
			return None
		return r.json()

	def __getPlayers(self):
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

	def __getPlayingAudio(self):
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
		
		item = result["result"]["item"]
		item["artist"] = item["artist"][0] # artist is a list. wtf.
		return item

	def __getAudioPlayerPosition(self):
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

	def run(self):
		# isDisplayOn needs the currently active players
		if not self.__getPlayers():
			self.__players = {}

		isDisplayOn = self.isDisplayOn()

		if self.__wasDisplayOn and not isDisplayOn:
			self.__serdisp.quit()
			self.__wasDisplayOn = False
		elif not self.__wasDisplayOn and isDisplayOn:
			self.__serdisp.init()
			self.__serdisp.clear()
			self.__wasDisplayOn = True

		if not isDisplayOn:
			return

		if "audio" in self.__players.keys():
			# Audio is playing
			# Due to race condition the player might be invalid till now
			tags = self.__getPlayingAudio()
			progress = self.__getAudioPlayerPosition()
			if tags:
				self.__screens["music"].update(tags, progress)
		else:
			# Display something useful :)
			self.__screens["idle"].update()

		self.__serdisp.update()

	def isDisplayOn(self):
		curTime = datetime.now()
		isOn = False

		# rule priority increasing downward (obviously)
		if curTime.hour >= 9 and curTime.hour < 23:
			isOn = True
		if "audio" in self.__players.keys():
			isOn = True
		if "video" in self.__players.keys():
			isOn = False

		return isOn

if __name__ == "__main__":
	with Serdisp(Settings.dispDevice, Settings.dispModel) as serdisp:
		disp = XbmcDisp(serdisp)
		while True:
			disp.run()
			sleep(3)
