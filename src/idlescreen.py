from datetime import datetime

class IdleScreen:
	def __init__(self, disp):
		self.disp = disp

	def update(self, tags):
		curTime = datetime.now()
		self.graphDisp.drawText([0,0], "{:%H:%M}".format(curTime), (255), "center", "center", 52)