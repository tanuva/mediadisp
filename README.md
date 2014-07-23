xbmcdisp
========

A piece of code that displays information from XBMC on an external display connected via serdisplib.
Connects to XBMC via json-rpc, therefore a configuration file will be needed at some point... :)

Dependencies
============

Packages from pip: freetype-py, pillow, requests

Pillow requires Python headers to be installed (python-dev on Debian Wheezy).

Customization
=============

Adjust `musicscreen.py` and/or `idlescreen.py` to your needs. I haven't included my background images ("layouts") to keep the repository free from binary blobs, but I can publish them if requested.

