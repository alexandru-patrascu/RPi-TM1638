from time import sleep

import RPi.GPIO as GPIO
from rpi_TM1638 import TMBoards

# Tell RPi that we're using GPIO board
GPIO.setmode(GPIO.BCM)

# Hide console warnings from GPIO
GPIO.setwarnings(False)

# The GPIO pin used for LED
GPIO.setup(26,GPIO.OUT)

STB = 22 # The GPIO pin used for STB
CLK = 21 # The GPIO pin used for CLK
DIO = 17 # The GPIO pin used for DIO

TM = TMBoards(DIO, CLK, STB, 0)
TM.clearDisplay()

num_left = 0
num_right = 9999

global led
led = False


# Update the LED Display
def num_update():
	TM.segments[0] = '{:04d}'.format(abs(num_left)%10000)
	TM.segments[4] = '{:04d}'.format(abs(num_right)%10000)
	return


# Toggle the GPIO LED
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


# Toggle ON / OFF the correspondent LED of the pressed TM Board switch
def switch_press_led_feedback(tmSwitch):
	TM.leds[tmSwitch] = True if TM.switches[tmSwitch] else False
	sleep(0.2)
	TM.leds[tmSwitch] = True if TM.switches[tmSwitch] else False


while True:
	if TM.switches[0]:
		toggle_led(0)
	if TM.switches[1]:
		switch_press_led_feedback(1)
		num_left += 1
		num_update()
	if TM.switches[2]:
		switch_press_led_feedback(2)
		num_left -= 1
		num_update()
	if TM.switches[3]:
		switch_press_led_feedback(3)
		num_left = 0
		num_update()
	if TM.switches[4]:
		switch_press_led_feedback(4)
		print("4")
	if TM.switches[5]:
		switch_press_led_feedback(5)
		num_left = 0123
		num_right = 4567
		num_update()
	if TM.switches[6]:
		switch_press_led_feedback(6)
		print('Number left: {num_left} \n Number right: {num_right}'.format(num_left = num_left, num_right = num_right))

	# Exit / Close the program
	if TM.switches[7]:
		switch_press_led_feedback(7)
		TM.clearDisplay()
		GPIO.cleanup()
		break
