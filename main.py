from picamzero import Camera
import serial
import RPi.GPIO as GPIO
import ColorDetectV4
import sys
import select

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------
#ser = serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=1)


try:
    cam = Camera()
    cam.still_size = (648, 486) # Change aspect ratio of camera
    camera_ok = True
except SystemExit as e:
    print("[WARN] Prevented system exit:", e)
    cam = None

readType = 'K' #K if I am reading over manual keyboard, S If I am reading serial input
nl = 0
#color = ColorDetectV	4.detect_color(cam)

# ----------------------------------------------------------------------
# Loop
# ----------------------------------------------------------------------
while True:
	# Take in an input
	# ------------------------------------------------------------------
	if readType == 'K':
		line = sys.stdin.read(1)
		# Clear the buffer
		if line != '\n':
			while nl != '\n':
					nl = sys.stdin.read(1)
	elif readType == 'S':
		line = ser.readline().decode('utf-8').strip()
	else:
		print("Mistake in the readType")
		break
	
	# Process that input
	# ------------------------------------------------------------------
	if line == 0:
		break
	elif line == '1':
		color = ColorDetectV4.detect_color(cam)
	else:
		print("Try another input!")
		
		
	line = 0
	
