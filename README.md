mediadisp
========

A piece of code that displays information from [shairport-sync](https://github.com/mikebrady/shairport-sync) and/or Plex (earlier: Kodi/XBMC) on an external display connected via serdisplib.
For setup details, copy `settings.default.py` and adapt. You have all the power of the snake. :)
It shows music metadata while playing music and a clock in idle. Apart from that the backlight is turned off while playing movies - we don't want to disturb.

![running on a c't includ USB display](https://github.com/tanuva/xbmcdisp/blob/master/running.jpg)

Dependencies
============

Debian packages: 
```
aptitude install python-dev libjpeg-dev
```

Packages from pip:
```
pip install -r requirements.txt`
```

Running
=======

```
python src/mediadisp.py
```

Customization
=============

Adjust `settings.py`, `musicscreen.py` and/or `idlescreen.py` to your needs. I have included the background images I currently use for reference. Depending on your display you'll want to draw your own.

