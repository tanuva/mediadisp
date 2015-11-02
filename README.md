xbmcdisp
========

A piece of code that displays information from Kodi/XBMC on an external display connected via serdisplib.
Connects to Kodi via json-rpc, tell `settings.py` where your Kodi is... :)
It shows music metadata while playing music and a clock in idle. Apart from that the backlight is turned off while playing movies - we don't want to disturb.

![xbmcdisp running on a c't includ USB display](https://github.com/tanuva/xbmcdisp/blob/master/running.jpg)

Dependencies
============

Packages from pip: freetype-py, pillow, requests

Pillow requires Python headers to be installed (python-dev on Debian Wheezy).

Customization
=============

Adjust `settings.py`, `musicscreen.py` and/or `idlescreen.py` to your needs. I have included the background images I currently use for reference. Depending on your display you'll want to draw your own.

