import time
import pyautogui
from pywinauto.application import Application
import ctypes
from ctypes import wintypes
import win32gui
import win32ui
from ctypes import windll
from PIL import Image
import keyboard

key_press = 258
key_down = 256
key_up = 257

############################################
###############Functions####################
############################################

def takePicture(hwnd, int):
	left, top, right, bot = win32gui.GetWindowRect(hwnd)
	w = right - left
	h = bot - top

	hwndDC = win32gui.GetWindowDC(hwnd)
	mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
	saveDC = mfcDC.CreateCompatibleDC()

	saveBitMap = win32ui.CreateBitmap()
	saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

	saveDC.SelectObject(saveBitMap)

	# Change the line below depending on whether you want the whole window
	# or just the client area.
	#result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
	result = ctypes.windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)

	bmpinfo = saveBitMap.GetInfo()
	bmpstr = saveBitMap.GetBitmapBits(True)

	im = Image.frombuffer(
	    'RGB',
	    (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
	    bmpstr, 'raw', 'BGRX', 0, 1)

	win32gui.DeleteObject(saveBitMap.GetHandle())
	saveDC.DeleteDC()
	mfcDC.DeleteDC()
	win32gui.ReleaseDC(hwnd, hwndDC)

	if result == 1:
	    #PrintWindow Succeeded
		if int == 0:
			im.save('base' + str(hwnd) + '.png')
		else:
			im.save("current" + str(hwnd) + ".png")

def playback(keystrokes, key_timing, key_pressed):
	for i in range(len(keystrokes)-1):
		if key_timing[i] < 0.1:
			key_timing[i] = 0.1
		time.sleep(key_timing[i])
		if key_pressed[i] == 'down':
			dlg.send_message(key_down, switch_keys(keystrokes[i]), 0)
		else:
			dlg.send_message(key_up, switch_keys(keystrokes[i]), 0)
	time.sleep(key_timing[len(key_timing)-1])

#convert scan codes https://www.qb64.org/wiki/Scancodes
#to windows virtual key codes https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
def switch_keys(argument):
    switcher = {
        14: 0x08, #backspace
		15: 0x09, #tab
        28: 0x0D, #enter
        44: 0x5A, #z
        45: 0x58, #x
        72: 0x26, #up
        75: 0x25, #left
        77: 0x27, #right
        80: 0x28 #down
    }
    return switcher.get(argument, 0x4C) #default to L

############################################
###########Main Function####################
############################################

#SAVE IMMEDIATE DATA, handle and window position
pyautogui.click()
handle = win32gui.GetForegroundWindow()
MOUSE_X, MOUSE_Y = pyautogui.position()
r = win32gui.GetWindowRect(handle);
takePicture(handle, 0)

#GET PID
user32 = ctypes.windll.user32
pid = wintypes.DWORD()
user32.GetWindowThreadProcessId(handle, ctypes.byref(pid))

#GET WINDOW DIALOG TO SEND KEYSTROKES
app = Application().connect(process=pid.value)
dlg = app.top_window()

#INIT VARIABLES
start_time = time.time()
last_time = start_time
relative_x = MOUSE_X-r[0]
relative_y = MOUSE_Y-r[1]
im1 = Image.open('base' + str(handle) + '.png')
Normal_Color = im1.getpixel( (relative_x,relative_y) )
im1.close()
print("Base color = " + str(Normal_Color))
keystrokes = [];
key_timing = [];
key_pressed = [];
found_shiny = False;
sr_count = 0;

#Record SR process
recorded = keyboard.record(until='esc')
for button_event in recorded:
	keystrokes.append(button_event.scan_code)
	key_timing.append(button_event.time-last_time)
	key_pressed.append(button_event.event_type)
	last_time = button_event.time

print(keystrokes)

while (not found_shiny):
	playback(keystrokes,key_timing,key_pressed)
	takePicture(handle, 1)

	#get color of new screenshot at same pixel as base screenshot
	im2 = Image.open("current" + str(handle) + ".png")
	New_Color = im2.getpixel( (relative_x,relative_y) )
	im2.close()

	print("SR: " + str(sr_count) + ' Duration ' + time.strftime("%d:%H:%M:%S", time.gmtime(time.time() - start_time)))
	if New_Color != Normal_Color:
		found_shiny = True;
	sr_count += 1;

print('Found shiny at ' + str(sr_count) + ' soft resets.')
print('Duration ' + time.strftime("%d:%H:%M:%S", time.gmtime(time.time() - start_time)))




#INSTRUCTIONS - READ ME
#Only works on windows 10
#This is currently only working to soft reset for a shiny torchic on pokemon Emerald
#Only known Emulator that this works with is mGBA (way that the keys are passed in)
#Can be used for as many instances you can fit on your screen
#Need python32 + pip + all the libraries
#pip install pyautogui
#pip install pywinauto
#
#1. Go to first encounter with torchic
#2. Start program while mouse is hovering over torchic to grab color (must do this for each instance)
#3. It will stop when it finds a shiny (hopefully)
#
#Note: You may not close/minimise the emulator, but it doesn't have to be visible
