from datetime import datetime
from plexapi.myplex import MyPlexAccount
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
        return self.plex.getPlayers()

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
