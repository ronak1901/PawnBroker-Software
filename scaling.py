import pyautogui

def scaling(widgetlist):

	compwidth, compheight = pyautogui.size()

	widthratio = compwidth / 1920
	heightratio = compheight / 1080
	if (widthratio != 1 and heightratio != 1):

		for widget in widgetlist:
			w = widget.width()
			h = widget.height()
			x = widget.x()
			y = widget.y()
			newx = int(x * widthratio)
			newy = int(y * heightratio)
			nw = int(w * widthratio)
			nh = int(h * heightratio)
			widget.resize(nw, nh)
			widget.move(newx, newy)
			font = widget.font()
			font.setPointSize(12)
			font.setFamily("SansSerif")
			widget.setFont(font)
