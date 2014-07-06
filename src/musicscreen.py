from datetime import datetime

class MusicScreen:
	def __init__(self, disp):
		self.disp = disp
		# draw layout only once

	def update(self, tags, progress):
		self.disp.drawPixmap("layout-music.png")
		curTime = datetime.now()
		self.disp.drawText([0,2], "{:%H:%M}".format(curTime), (255), "center", "", 12)
		self.disp.drawText([1,14], tags["title"], (255), "left", "", 14)
		self.disp.drawText([1,35], tags["artist"], (255), "left", "", 12)
		self.disp.drawText([1,50], tags["album"], (255), "left", "", 12)
		self.disp.drawProgressBar([0,29], [128,6], progress)
