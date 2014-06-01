ui.py: design.ui
	pyuic4 design.ui -o ui.py
	
clean:
	rm ui.py