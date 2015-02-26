#!/bin/bash

# On Debian, serdisplib needs to be built with libusb support for usb displays.
# Need to modify LD_LIBRARY_PATH for it to be found.
LD_LIBRARY_PATH=/usr/local/lib python src/xbmcdisp.py
