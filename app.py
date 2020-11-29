from time import sleep

import RPi.GPIO as GPIO
from rpi_TM1638 import TMBoards

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(26,GPIO.OUT)

STB = 22
CLK = 21
DIO = 17

TM = TMBoards(DIO, CLK, STB, 0)
TM.clearDisplay()

num_left = 0
num_right = 9999

global led
led = False


def num_update():
    TM.segments[0] = '{:04d}'.format(abs(num_left)%10000)
    TM.segments[4] = '{:04d}'.format(abs(num_right)%10000)
    return


def toggle_led(tmLed):
	global led
	print('Led Status: {led}, tmLed: {tmLed}'.format(led = led, tmLed = tmLed))
	if led == False:
		GPIO.output(26, GPIO.HIGH)
		TM.segments[tmLed] = '1'
		TM.leds[tmLed] = True
		led = True
		sleep(0.4)
	elif led == True:
		GPIO.output(26, GPIO.LOW)
		TM.segments[tmLed] = '0'
		TM.leds[tmLed] = False
		led = False
		sleep(0.4)
	return


def switchPressLedFeedback(tmSwitch):
	TM.leds[tmSwitch] = True if TM.switches[tmSwitch] else False
	sleep(0.2)
  TM.leds[tmSwitch] = True if TM.switches[tmSwitch] else False


while True:
	if TM.switches[0]:
		toggle_led(0)
	if TM.switches[1]:
                switchPressLedFeedback(1)
		num_left += 1
		num_update()
	if TM.switches[2]:
                switchPressLedFeedback(2)
		num_left -= 1
		num_update()
	if TM.switches[3]:
                switchPressLedFeedback(3)
		num_left = 0
		num_update()
	if TM.switches[4]:
                switchPressLedFeedback(4)
		print("4")
	if TM.switches[5]:
                switchPressLedFeedback(5)
		num_left = 0123
		num_right = 4567
		num_update()
	if TM.switches[6]:
                switchPressLedFeedback(6)
		print('Number left: {num_left} \n Number right: {num_right}'.format(num_left = num_left, num_right = num_right))
	if TM.switches[7]:
		switchPressLedFeedback(7)
		TM.clearDisplay()
		GPIO.cleanup()
		break
