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
			pressKey(keystrokes[i])
		else:
			releaseKey(keystrokes[i])
	time.sleep(key_timing[len(key_timing)-1])

#scan codes https://www.qb64.org/wiki/Scancodes
#to windows virtual key codes https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes

# C struct redefinitions
######################################
###this defines scan code inputs######
#####instead of virtual key codes####
######################################

PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def pressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def releaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0,
ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

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
keyboard.wait('esc')




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
