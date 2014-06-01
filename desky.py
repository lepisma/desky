import sys
import cv2
from PyQt4 import QtGui, QtCore, Qt
from ui import Ui_MainWindow

class Gui(QtGui.QMainWindow):
	def __init__(self, url = "http://localhost", parent=None):
		QtGui.QWidget.__init__(self,parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.update
		self.ui.webView.setUrl(QtCore.QUrl(url))
		
	def close(self):
		sys.exit()
		
def main():
	app = QtGui.QApplication(sys.argv)
	ex = Gui()
	ex.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()