from datetime import datetime
from icalendar.cal import Calendar
import paho.mqtt.client as mqtt
import requests
import widget as gd


def on_connect(client, provider, flags, rc):
    print(f"MQTT: Subscribing to {provider.settings.mqtt['charge_average_topic']}")
    client.subscribe(provider.settings.mqtt["charge_average_topic"])
    print(f"MQTT: Subscribing to {provider.settings.mqtt['battery_soc_topic']}")
    client.subscribe(provider.settings.mqtt["battery_soc_topic"])


def on_message(client, provider, msg):
    #print("Unhandled topic: %s" % (msg.topic))
    pass


def on_charge_average(client, provider, msg):
    payload_str = msg.payload.decode("utf-8")
    try:
        provider.state["charge_average"] = float(payload_str)
    except ValueError as e:
        print(f"MQTT: {provider.settings.mqtt['charge_average_topic']}: Unexpected value: {payload_str}")
        provider.state["charge_average"] = 0.0


def on_soc(client, provider, msg):
    payload_str = msg.payload.decode("utf-8")
    try:
        provider.state["soc_percent"] = float(payload_str)
    except ValueError as e:
        print(f"MQTT: {provider.settings.mqtt['battery_soc_topic']} Unexpected value: {payload_str}")
        provider.state["soc_percent"] = 0.0


class MQTTDataProvider:
    def __init__(self, settings):
        self.settings = settings
        self.state = {
            "charge_average": 0.0,
            "soc_percent": 0.0,
        }

        self.__client = mqtt.Client()
        self.__client.user_data_set(self)
        self.__client.on_connect = on_connect
        self.__client.on_message = on_message
        self.__client.message_callback_add(settings.mqtt["charge_average_topic"], on_charge_average)
        self.__client.message_callback_add(settings.mqtt["battery_soc_topic"], on_soc)
        self.__client.connect("idefix")
        self.__client.loop_start()


    def soc(self):
        """ Returns battery SOC in percent """
        return self.state["soc_percent"]


    def charge_average(self):
        """ Returns average battery charge rate in W """
        return self.state["charge_average"]


class ICalPoller:
    def __init__(self, url):
        self.url = url
        self.lastCalendarPoll = datetime(1970, 1, 1)
        self.iCalText = ""

    def __getCalendarText(self):
        if (datetime.now() - self.lastCalendarPoll).days < 1:
            return self.iCalText

        response = requests.get(self.url)
        response.raise_for_status()

        self.iCalText = response.text
        self.lastCalendarPoll = datetime.now()
        return self.iCalText

    def getEvent(self, title):
        calendarText = self.__getCalendarText()
        cal = Calendar.from_ical(calendarText)
        countdownEvent = None
        for component in cal.subcomponents:
            if "SUMMARY" in component.keys() and component["SUMMARY"] == title:
                countdownEvent = component
        return countdownEvent

class IdleScreen:
    def __init__(self, disp, settings, args):
        self.disp = disp
        self.settings = settings
        self.args = args
        self.bg = gd.Pixmap(disp, "layout-idle.png", [0, 0])
        self.time = gd.Text(disp, [0,6], "DroidSans.ttf", 50, "00:00", halign = "center", valign = "top")

        if settings.countdown["enabled"]:
            self.poller = ICalPoller(self.settings.countdown["ical"])
            self.days = gd.Text(disp, [0,3], "DroidSans.ttf", 12, "000 Tage", halign = "center", valign = "bottom")

        if settings.mqtt["enabled"]:
            self.__mqtt = MQTTDataProvider(settings)
            self.__battery_icon = gd.Pixmap(self.disp, "battery_6x10.png", [0, 54])
            self.__battery_soc = gd.Progressbar(self.disp, [8, 54], [112, 10], border=True)
            self.__arrow_discharge = gd.Pixmap(self.disp, "triangle_left_6x10.png", [122, 54])
            self.__arrow_charge = gd.Pixmap(self.disp, "triangle_right_6x10.png", [122, 54])
            self.__dot = gd.Pixmap(self.disp, "dot_6x10.png", [122, 54])

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
            if self.args.network:
                try:
                    count = self.daysLeft()
                    template = "{0} Tag" if abs(count) == 1 else "{0} Tage"
                    self.days.setText(template.format(count))
                except requests.exceptions.RequestException as e:
                    print(e)
                    # Display something remotely useful to the user
                    self.days.setText(type(e).__name__)
            else:
                self.days.setText("Network Disabled")
            self.days.draw()

        if self.settings.mqtt["enabled"]:
            self.__battery_icon.draw()
            self.__battery_soc.setState(self.__mqtt.soc() / 100.0)
            self.__battery_soc.draw()

            if self.__mqtt.charge_average() > 10:
                self.__arrow_charge.draw()
            elif self.__mqtt.charge_average() < -10:
                self.__arrow_discharge.draw()
            else:
                self.__dot.draw()
