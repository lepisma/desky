"""
Packs the app in an executable using pyinstaller
"""

import subprocess

import json

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

subprocess.call(command)