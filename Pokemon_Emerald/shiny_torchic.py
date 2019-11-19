import time
import pyautogui
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
import ctypes
from ctypes import wintypes

key_press = 258
key_down = 256
key_up = 257
key_x = 0x58
key_z = 0x5A
key_entr = 0x0D
key_bkspce = 0x08

############################################
###############Functions####################
############################################
def getColor():
	PIXEL = pyautogui.screenshot(
	    region=(
	        MOUSE_X, MOUSE_Y, 1, 1
	    )
	)
	COLOR = PIXEL.getcolors()
	return COLOR

def softReset():
	dlg.send_message(key_down, key_x, 0)
	dlg.send_message(key_down, key_z, 0)
	dlg.send_message(key_down, key_entr, 0)
	dlg.send_message(key_down, key_bkspce, 0)
	time.sleep(.3)
	dlg.send_message(key_up, key_x, 0)
	dlg.send_message(key_up, key_z, 0)
	dlg.send_message(key_up, key_entr, 0)
	dlg.send_message(key_up, key_bkspce, 0)

def returnToBattle():
	for x in range(0,90):
		dlg.send_message(key_down, key_x, 0)
		time.sleep(.1)
		dlg.send_message(key_up, key_x, 0)
		time.sleep(.1)
	time.sleep(3)

############################################
###########Main Function####################
############################################

time.sleep(.3)
pyautogui.click()
MOUSE_X, MOUSE_Y = pyautogui.position()

#GET PID
user32 = ctypes.windll.user32
h_wnd = user32.GetForegroundWindow()
pid = wintypes.DWORD()
user32.GetWindowThreadProcessId(h_wnd, ctypes.byref(pid))
print(pid.value)

app = Application().connect(process=pid.value)
#print(app.windows())
dlg = app.top_window()

start_time = time.time()
Normal_Color = getColor()
# print("Mouse: (%d,%d)" % (MOUSE_X, MOUSE_Y))
#print("RGB: %s" % (Normal_Color[0][1].__str__()))

found_shiny = False;
sr_count = 0;

while (not found_shiny):
	softReset()
	returnToBattle()
	possible_shiny = getColor()
	print("RGB: %s" % (possible_shiny[0][1].__str__()) + " SR: " + str(sr_count) + ' Duration ' + time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time)))
	if possible_shiny[0][1] != Normal_Color[0][1]:
		found_shiny = True;
	sr_count += 1;

print('Found shiny at ' + str(sr_count) + ' soft resets.')
print('Duration ' + time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time)))




#INSTRUCTIONS - READ ME
#Only works on windows 10
#This is currently only working to soft reset for a shiny torchic on pokemon Emerald
#Only known Emulator that this works with is mGBA (way that the keys are passed in)
#Can be used for as maany instances you can fit on your screen
#Need python32 + pip + all the libraries
#pip install psutil
#pip install pyautogui
#pip install pywinauto
#
#1. Go to first encounter with torchic
#2. Start program while mouse is hovering over torchic to grab color (must do this for each instance)
