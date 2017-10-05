from datetime import datetime
import widget as gd

class IdleScreen:
	def __init__(self, disp, _):
		self.disp = disp
		self.bg = gd.Pixmap(disp, "layout-idle.png", [0, 0])
		self.time = gd.Text(disp, [0,6], "DroidSans.ttf", 50, "00:00", halign = "center", valign = "top")
		self.days = gd.Text(disp, [0,3], "DroidSans.ttf", 12, "000 Tage", halign = "center", valign = "bottom")

	def daysLeft(self, then):
		interval = then - datetime.now()
		return interval.days + (1 if interval.seconds > 0 else 0)

	def update(self):
		self.bg.draw()
		curTime = datetime.now()
		self.time.setText("{:%H:%M}".format(curTime))
		self.time.draw()
		self.days.setText("{0} Tage".format(self.daysLeft(datetime(2017, 10, 01, 0, 0, 0))))
		self.days.draw()
