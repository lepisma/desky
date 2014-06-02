"""
Desky
-----

Wrap your web app in desktop frame
"""

import sys, subprocess

from PyQt4.Qt import *

import json

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

	try:
		config = json.load(open('desky_config.json', 'rb'))
	except IOError as e:
		if e.errno == 2:
			print "Config file not found"
		else:
			print "Something wicked happened while reading config"
		sys.exit()

	try:
		cmd = config['cmd']
		server_process = subprocess.Popen(cmd)
	except KeyError:
		server_process = False
		print "No command to run, opening frame now"

	try:
		url = config['url']
	except KeyError:
		print "No url specified, exiting"
		sys.exit()

	try:
		name = config['name']
	except KeyError:
		print "No name specified, using 'Desky'"
		name = "Desky"
	
	app = QApplication(sys.argv)
	frame = Desky(url, name, server_process)
	frame.show()
	app.exec_()

if __name__ == '__main__':
	main()