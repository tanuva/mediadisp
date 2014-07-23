from datetime import datetime
import graphdisp as gd

class MusicScreen:
	def __init__(self, disp):
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

	def update(self, tags, progress):
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
