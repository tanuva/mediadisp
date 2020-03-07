from datetime import datetime
from plexapi.myplex import MyPlexAccount
import paho.mqtt.client as mqtt
import traceback
import widget as gd

class PlexDataProvider:
    def __init__(self, settings):
        self.__settings = settings
        try:
            account = MyPlexAccount(settings.plex["user"], settings.plex["password"])
            self.__plex = account.resource(settings.plex["servername"]).connect()
        except:
            print("Could not connect to Plex API")

    def __getLocalMedium(self):
        # sessions() seems to return plexapi.audio.Track instances when playing
        # music. Maybe other classes for different media.
        if not self.__plex:
            raise "No Plex API connection"

        for medium in self.__plex.sessions():
            if len(medium.session) < 1:
                continue
            if medium.session[0].location == "lan":
                return medium
        return None

    def getPlayers(self):
        # medium.type element [movie, track, episode]
        medium = None
        try:
            medium = self.__getLocalMedium()
        except Exception as e:
            print("getPlayers(): Exception occurred. Probably Plex server offline?")
            traceback.format_exc()

        if medium == None:
            return []

        if medium.type == "movie" or medium.type == "episode":
            return ["video"]
        elif medium.type == "track":
            return ["audio"]
        else:
            print("Unexpected medium type: " + medium.type)
            return []

    def getPlayingAudio(self):
        medium = self.__getLocalMedium()
        if not medium:
            return {
                "artist": "",
                "album": "",
                "title": ""
            }

        return {
            "artist": medium.artist().title,
            "album": medium.parentTitle,
            "title": medium.title
        }

    def getAudioPlayerPosition(self):
        medium = self.__getLocalMedium()
        if not medium:
            return 0

        duration = float(medium.duration)
        current = float(medium.viewOffset)
        return current / duration


def on_connect(client, provider, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe("shairport-sync/idefix/#")

def on_message(client, provider, msg):
    #print("Unhandled topic: %s" % (msg.topic))
    pass

def on_album(client, provider, msg):
    provider.metadata["album"] = msg.payload.decode("utf-8")

def on_artist(client, provider, msg):
    provider.metadata["artist"] = msg.payload.decode("utf-8")

def on_title(client, provider, msg):
    provider.metadata["title"] = msg.payload.decode("utf-8")

def on_play_start(client, provider, msg):
    provider.playing = True

def on_play_end(client, provider, msg):
    provider.playing = False


class ShairportDataProvider:
    def __init__(self, settings):
        self.__settings = settings
        self.metadata = {
            "artist": "",
            "album": "",
            "title": ""
        }
        self.playing = False
        self.__initMQTT()

    def __initMQTT(self):
        self.__client = mqtt.Client()
        self.__client.user_data_set(self)
        self.__client.on_connect = on_connect
        self.__client.on_message = on_message
        # TODO Make the topics configurable
        self.__client.message_callback_add("shairport-sync/idefix/album", on_album)
        self.__client.message_callback_add("shairport-sync/idefix/artist", on_artist)
        self.__client.message_callback_add("shairport-sync/idefix/title", on_title)
        self.__client.message_callback_add("shairport-sync/idefix/play_start", on_play_start)
        self.__client.message_callback_add("shairport-sync/idefix/play_resume", on_play_start)
        self.__client.message_callback_add("shairport-sync/idefix/play_end", on_play_end)
        self.__client.connect("localhost")
        self.__client.loop_start()

    def getPlayers(self):
        return ["audio"] if self.playing else []

    def getPlayingAudio(self):
        return self.metadata

    def getAudioPlayerPosition(self):
        # Shairport doesn't seem to report progress
        return 0


class MusicScreen:
    def __init__(self, disp, settings, args):
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

        self.dataProviders = [
            ShairportDataProvider(settings),
            PlexDataProvider(settings)
        ]

        self.devMode = False

    def hasContent(self):
        if self.devMode:
            return True

        for provider in self.dataProviders:
            return len(provider.getPlayers()) > 0

    def update(self):
        # TODO Breaks if no provider has data. Shouldn't happen though since
        # this screen shouldn't be active then anyway.
        tags = None
        progress = 0

        for provider in self.dataProviders:
            if "audio" in provider.getPlayers():
                tags = provider.getPlayingAudio()
                progress = provider.getAudioPlayerPosition()
                break

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
