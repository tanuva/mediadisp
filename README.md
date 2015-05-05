xbmcdisp
========

A piece of code that displays information from Kodi (formerly XBMC) on an external display connected via serdisplib.
Connects to XBMC via json-rpc, therefore a configuration file will be needed at some point... :)
It shows music metadata while playing music and a clock in idle. Apart from that the backlight is turned off while playing movies - we don't want to disturb.

Just to have it said: this works with Kodi as well as XBMC. The relevant parts of the JSON interface don't seem to have changed (yet).

Dependencies
============

Packages from pip: freetype-py, pillow, requests

Pillow requires Python headers to be installed (python-dev on Debian Wheezy).

Customization
=============

Adjust `musicscreen.py` and/or `idlescreen.py` to your needs. I have included the background images I currently use for reference. Depending on your display you'll want to draw your own.

