from datetime import datetime
import widget as gd

class IdleScreen:
	def __init__(self, disp, _):
		self.disp = disp
		self.bg = gd.Pixmap(disp, "layout-idle.png", [0, 0])
		self.time = gd.Text(disp, [0,0], "DroidSans.ttf", 50, "00:00", halign = "center", valign = "center")

	def update(self):
		self.bg.draw()
		curTime = datetime.now()
		self.time.setText("{:%H:%M}".format(curTime))
		self.time.draw()
