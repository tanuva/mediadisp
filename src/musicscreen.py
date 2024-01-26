from datetime import datetime
import paho.mqtt.client as mqtt
import traceback
import widget as gd

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
        self.title  = gd.Text(disp, [0,0], font, 18, "PpJjÄäPpJjÄä Title")
        self.artist = gd.Text(disp, [0,24], font, 16, "PpJjÄä Artist")
        self.time   = gd.Text(disp, [0,51], font, 18, "00:00", halign = "right")

        self.dataProviders = [
            ShairportDataProvider(settings),
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
