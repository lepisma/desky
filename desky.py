"""
Desky
-----

Wrap your web app in desktop frame
"""

import sys, subprocess
import socket
import time

from PyQt4.Qt import *

import json

MAX_PORT_SCAN_TRIES = 10 # 20 secs


def print_help():
	"""
	Prints help for commands
	"""

	print "Usage : `python desky.py` for running app"
	print "`python desky.py pack` for packing"
	print "`python desky.py packupx <upx-dir-path>` for packing with upx compression"

def port_check(port, host = '127.0.0.1'):
	"""
	Checks whether the port is open or not

	Parameters
	----------
	port : int
		The port to check for
	host : string
		The port to check for
	"""

	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(1)
		s.connect((host, port))
		s.close()
	except:
		return False

	return True

class Desky(QWidget):
	"""
	The GUI Class
	Opens the url in qt webview
	"""

	def __init__(self, url, name, server_process):
		"""
		Parameters
		----------
		url : string
			The url to load in the frame
		name : string
			The name of frame (to be shown as window title)
		server_process : subprocess.Popen or bool
			The process which is handling the webpage
		"""

		QWidget.__init__(self)
		self.setWindowTitle(name)
		self.layout = QGridLayout(self)
		self.layout.setMargin(0)
		self.layout.setSpacing(0)

		self.view = QWebView(self)
		self.view.setUrl(QUrl(url))

		self.layout.addWidget(self.view, 0, 0, 1, 1)

		self.server_process = server_process

	def closeEvent(self, event):
		"""
		Kills the server process and quits
		"""
		
		if self.server_process != False:
			self.server_process.kill()

		event.accept()
		
def main():
	"""
	Main function
	Scans directory for desky_config.json
	Runs server (if needed)
	Passes URL to qt webkit
	"""

	# Loading config
	try:
		config = json.load(open('desky_config.json', 'rb'))
	except IOError as e:
		if e.errno == 2:
			print "Config file not found"
		else:
			print "Something wicked happened while reading config"
		sys.exit()
		
	try:
		url = config['url']
	except KeyError:
		print "No url specified, exiting"
		sys.exit()

	try:
		cmd = config['cmd']
		server_process = subprocess.Popen(cmd)
	except KeyError:
		cmd = False
		server_process = False
		print "No command to run, opening frame now"

	if cmd != False:
		try:
			check_port = config['check_port']
		except KeyError:
			print "No check port specified, exiting"
			sys.exit()
	else:
		check_port = False

	try:
		name = config['name']
	except KeyError:
		print "No name specified, using 'Desky'"
		name = "Desky"
	
	if check_port != False:
		# Checking if server is up
		tries = 0
		while port_check(check_port) == False:
			time.sleep(2)
			tries += 1
			if tries > MAX_PORT_SCAN_TRIES:
				break

	app = QApplication(sys.argv)
	frame = Desky(url, name, server_process)
	frame.show()
	app.exec_()

def pack(upx = False):
	"""
	Packs the app using pyinstaller

	Parameters
	----------
	upx : string / bool
		Path to upx directory for compression or False for no upx
	"""

	try:
		config = json.load(open('desky_config.json', 'rb'))
	except IOError as e:
		if e.errno == 2:
			print "Config file not found"
		else:
			print "Something wicked happened while reading config"
		config = False

	if config != False:
		try:
			name = config['name']
		except KeyError:
			name = 'Desky'
	else:
		name = 'Desky'

	command = "pyinstaller desky.py --name=" + name + " --onefile --noconsole --distpath=./"

	if upx != False:
		command += " --upx-dir=" + upx

	subprocess.call(command)

if __name__ == '__main__':
	if len(sys.argv) == 1:
		main()
	elif len(sys.argv) == 2:
		if sys.argv[1] == "pack":
			pack()
		else:
			print_help()
	elif len(sys.argv) == 3:
		if sys.argv[1] == "packupx":
			pack(sys.argv[2])
		else:
			print_help()
	else:
		print_help()