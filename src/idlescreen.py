from datetime import datetime

class IdleScreen:
	def __init__(self, disp):
		self.disp = disp

	def update(self):
		curTime = datetime.now()
		self.disp.drawText([0,0], "{:%H:%M}".format(curTime), (255), "center", "center", 52)
