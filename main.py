from picamzero import Camera
import serial
import RPi.GPIO as GPIO
import ColorDetectV4
import sys
import select

# ----------------------------------------------------------------------
# Function Defs
# ----------------------------------------------------------------------
def setLow4():
	GPIO.output(led4Red, GPIO.LOW)
	GPIO.output(led4Blue, GPIO.LOW)
	GPIO.output(led4Green, GPIO.LOW)

def setLow3():
	GPIO.output(led3Red, GPIO.LOW)
	GPIO.output(led3Blue, GPIO.LOW)
	GPIO.output(led3Green, GPIO.LOW)

def setLow2():
	GPIO.output(led2Red, GPIO.LOW)
	GPIO.output(led2Blue, GPIO.LOW)
	GPIO.output(led2Green, GPIO.LOW)

def setLow1():
	GPIO.output(led1Red, GPIO.LOW)
	GPIO.output(led1Blue, GPIO.LOW)
	GPIO.output(led1Green, GPIO.LOW)

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------
# LEDS
led1Red = 16
led1Green = 18
led1Blue = 22
led2Red = 36
led2Green = 37
led2Blue = 33
led3Red = 31
led3Green = 29
led3Blue = 15
led4Red = 13
led4Green = 11
led4Blue = 7

GPIO.setmode(GPIO.BOARD)
GPIO.setup(led4Red, GPIO.OUT)
GPIO.setup(led4Green, GPIO.OUT)
GPIO.setup(led4Blue, GPIO.OUT)
GPIO.setup(led3Red, GPIO.OUT)
GPIO.setup(led3Green, GPIO.OUT)
GPIO.setup(led3Blue, GPIO.OUT)
GPIO.setup(led2Red, GPIO.OUT)
GPIO.setup(led2Green, GPIO.OUT)
GPIO.setup(led2Blue, GPIO.OUT)
GPIO.setup(led1Red, GPIO.OUT)
GPIO.setup(led1Green, GPIO.OUT)
GPIO.setup(led1Blue, GPIO.OUT)

setLow4()
setLow3()
setLow2()
setLow1()

#ser = serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=1)


try:
    cam = Camera()
    cam.still_size = (648, 486) # Change aspect ratio of camera
    camera_ok = True
except SystemExit as e:
    print("[WARN] Prevented system exit:", e)
    GPIO.setup(led1Red, GPIO.OUT)
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
		setLow1();
		if color == 'R':
			GPIO.output(led1Red, GPIO.HIGH)
		elif color == 'G':
			GPIO.output(led1Green, GPIO.HIGH)
		elif color == 'B':
			GPIO.output(led1Blue, GPIO.HIGH)
		elif color == 'P':
			GPIO.output(led1Blue, GPIO.HIGH)
			GPIO.output(led1Red, GPIO.HIGH)
			
	elif line == '2':
		color = ColorDetectV4.detect_color(cam)
		setLow2();
		if color == 'R':
			GPIO.output(led2Red, GPIO.HIGH)
		elif color == 'G':
			GPIO.output(led2Green, GPIO.HIGH)
		elif color == 'B':
			GPIO.output(led2Blue, GPIO.HIGH)
		elif color == 'P':
			GPIO.output(led2Blue, GPIO.HIGH)
			GPIO.output(led2Red, GPIO.HIGH)
			
	elif line == '3':
		color = ColorDetectV4.detect_color(cam)
		setLow3();
		if color == 'R':
			GPIO.output(led3Red, GPIO.HIGH)
		elif color == 'G':
			GPIO.output(led3Green, GPIO.HIGH)
		elif color == 'B':
			GPIO.output(led3Blue, GPIO.HIGH)
		elif color == 'P':
			GPIO.output(led3Blue, GPIO.HIGH)
			GPIO.output(led3Red, GPIO.HIGH)
			
	elif line == '4':
		color = ColorDetectV4.detect_color(cam)
		setLow4();
		if color == 'R':
			GPIO.output(led4Red, GPIO.HIGH)
		elif color == 'G':
			GPIO.output(led4Green, GPIO.HIGH)
		elif color == 'B':
			GPIO.output(led4Blue, GPIO.HIGH)
		elif color == 'P':
			GPIO.output(led4Blue, GPIO.HIGH)
			GPIO.output(led4Red, GPIO.HIGH)
			
	elif line == 'h':
		GPIO.output(led4Red, GPIO.HIGH)
		GPIO.output(led4Blue, GPIO.HIGH)
		GPIO.output(led4Green, GPIO.HIGH)
		GPIO.output(led3Red, GPIO.HIGH)
		GPIO.output(led3Blue, GPIO.HIGH)
		GPIO.output(led3Green, GPIO.HIGH)
		GPIO.output(led2Red, GPIO.HIGH)
		GPIO.output(led2Blue, GPIO.HIGH)
		GPIO.output(led2Green, GPIO.HIGH)
		GPIO.output(led1Red, GPIO.HIGH)
		GPIO.output(led1Blue, GPIO.HIGH)
		GPIO.output(led1Green, GPIO.HIGH)
	elif line == 'l':
		setLow4()
		setLow3()
		setLow2()
		setLow1()
	else:
		print("Try another input!")
		
		
	line = 0

