# =====================
# Source: http://stackoverflow.com/questions/279237/import-a-module-from-a-relative-path
import os, sys, inspect
# realpath() with make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
	sys.path.insert(0, cmd_folder)

# use this if you want to include modules from a subfolder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0],"../pyserdisp")))
if cmd_subfolder not in sys.path:
	sys.path.insert(0, cmd_subfolder)
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0],"../freetype-py")))
if cmd_subfolder not in sys.path:
	sys.path.insert(0, cmd_subfolder)
# ======================

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from graphdisp import GraphDisp

class HTTPRequestHandler(BaseHTTPRequestHandler):
	def do_POST():
		print command, path

class DispServer:
	def __init__(self, graphDisp):
		self.graphDisp = graphDisp
		self.graphDisp.drawText([0, 0], "Bananaa!", (255), "center", "center")
		self.graphDisp.flip()

	def run(self):
	    address = ('', 6660)
	    httpd = HTTPServer(address, HTTPRequestHandler)
	    while True:
	    	httpd.handle_request()

if __name__ == "__main__":
	with GraphDisp("USB:7c0/1501", "CTINCLUD") as disp:
		server = DispServer(disp)
		server.run()
		