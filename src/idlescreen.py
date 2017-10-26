from datetime import datetime
from icalendar.cal import Calendar
import requests
import widget as gd

class ICalPoller:
	def __init__(self, url):
		self.url = url
		self.lastCalendarPoll = datetime(1970, 1, 1)
		self.iCalText = ""

	def getCalendarText(self):
		if (datetime.now() - self.lastCalendarPoll).days < 1:
			return self.iCalText

		response = requests.get(self.url)
		if not response.status_code == 200:
			print("Error fetching calendar. HTTP status:", response.status_code)
			return self.iCalText

		self.iCalText = response.text
		self.lastCalendarPoll = datetime.now()
		return self.iCalText

	def getEvent(self, title):
		cal = Calendar.from_ical(self.getCalendarText())
		countdownEvent = None
		for component in cal.subcomponents:
			if "SUMMARY" in component.keys() and component["SUMMARY"] == title:
				countdownEvent = component
		return countdownEvent

class IdleScreen:
	def __init__(self, disp, settings):
		self.disp = disp
		self.settings = settings
		self.poller = ICalPoller(self.settings.countdown["ical"])
		self.bg = gd.Pixmap(disp, "layout-idle.png", [0, 0])
		self.time = gd.Text(disp, [0,6], "DroidSans.ttf", 50, "00:00", halign = "center", valign = "top")
		self.days = gd.Text(disp, [0,3], "DroidSans.ttf", 12, "000 Tage", halign = "center", valign = "bottom")

	def daysLeft(self):
		event = self.poller.getEvent(self.settings.countdown["eventTitle"])
		interval = event['DTSTART'].dt - datetime.now().date()
		return interval.days

	def update(self):
		self.bg.draw()
		curTime = datetime.now()
		self.time.setText("{:%H:%M}".format(curTime))
		self.time.draw()
		if self.settings.countdown["enabled"]:
			self.days.setText("{0} Tage".format(self.daysLeft()))
			self.days.draw()
