#!/usr/bin/python

#preample

#import relevant
import time
import random
import subprocess
import board
import neopixel
import threading 
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library


# Setup neopixels
# Pin 18
pixel_pin = board.D12

# The number of NeoPixels
num_pixels = 16

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False,
                           pixel_order=ORDER)

#Setup GPIO for button
#GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
buttonPin = 10
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set


#define time inteval
minTime = 10*60
maxTime = 15*60

################# class section ##############3

class PakkelegThread(threading.Thread):
	"""Pakkeleg Thread class to start pakkeleg while able to stop if switch is flipped using the stop() method to stop pakkeleg. """

    #initialize pakkelegThread with time
	def __init__(self, tid):
		super(PakkelegThread, self).__init__()
		self._stop_event = threading.Event()
		self._tid = tid

	def stop(self):
		self._stop_event.set()

	def stopped(self):
		return self._stop_event.is_set()

	def run(self):
		threading.Thread(target = self.play, args = ['./lyde/Sleigh.wav']).start()        
		for j in range(self._tid):
			self.timedLights(1)
			if(self.stopped()):
				self.stopLights()
				break
		if(not self.stopped()):
			self.faerdig()

	def faerdig(self):
		threading.Thread(target = self.play, args =['./lyde/Boxing.wav']).start()
		self.flashingLights(2)
		print('DING-DING-DING-DING-DING')

	def play(self,audio_file_path):
		subprocess.run(["ffplay", "-nodisp", "-autoexit", "-hide_banner", audio_file_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

	def timedLights(self,tid):
		red = (130,0,0)
		green = (0,200,0)
		for j in range(tid):
			for i in range(1,num_pixels,2):
				pixels[i] = red
			for i in range(0,num_pixels,2):
				pixels[i] = green
			pixels.show()
			time.sleep(.5)

			for i in range(1,num_pixels,2):
				pixels[i] = green
			for i in range(0,num_pixels,2):
				pixels[i] = red
			pixels.show()
			time.sleep(.5)

	def flashingLights(self,tid):
		red = (204,0,0)
		green = (0,255,0)
		for j in range(tid*10):
			pixels.fill(red)
			pixels.show()
			time.sleep(0.1)
			pixels.fill((0,0,0))
			pixels.show()
			time.sleep(0.1)

	def stopLights(self):
		green = (0,255,0)
		pixels.fill(green)
		pixels.show()
		time.sleep(1)
		pixels.fill((0,0,0))
		pixels.show()


################## set min max time section ############

def setMinMaxTime():
	#define colors
	green = (0,255,0)
	red = (255,0,0)
	#make a red circle running
	for i in range(num_pixels):
		if i > 0:
			pixels[i-1] = (0,0,0)
		pixels[i] = red
		pixels.show()
		time.sleep(.1)
	pixels.fill((0,0,0))
	pixels.show()

	#define counters
	minKliks = 0
	maxKliks = 0
	minDone = False
	maxDone = False
	prev_input = GPIO.input(buttonPin)
	#loop to get number of minutes
	while (not minDone) or (not maxDone):
		#first set minimum time
		if ((not minDone) and (not maxDone)):
			input = GPIO.input(buttonPin)
			#switch turned from off to on
			if ((not prev_input) and input):
				time.sleep(.5)
				input2 = GPIO.input(buttonPin)
				if (input and (not input2)):
					#The switch has been turned on and off fast, we count one klik.
					minKliks = minKliks + 1
					for i in range(0,minKliks):
						pixels[i] = green
					pixels.show()
				else:
					print('Minimum tid sat.')
					minDone = True
					maxKliks = minKliks

		if minDone and (not maxDone):
			input = GPIO.input(buttonPin)
			#switch turned from on to off
			if (prev_input and (not input)):
				time.sleep(.5)
				input2 = GPIO.input(buttonPin)
				if ((not input) and input2):
					#The switch has been turned off and on fast, we count one klik.
					maxKliks = maxKliks + 1
					for i in range(minKliks,maxKliks):
						pixels[i] = red
					pixels.show()
				else:
					maxDone = True
					print('Maksimum tid sat.')

		#update previous input
		prev_input = input
		#slight pause to debounce
		time.sleep(0.05)
		

	global minTime, maxTime
	minTime = 2*60*minKliks
	maxTime = 2*60*maxKliks	

	for i in reversed(range(num_pixels)):
		if i < num_pixels - 1:
			pixels[i+1] = (0,0,0)
		pixels[i] = green
		pixels.show()
		time.sleep(.1)
	pixels.fill((0,0,0))
	pixels.show()




################## main section ###############

def main():
	prev_input = GPIO.input(buttonPin)
	print("Saa skal vi te'et igen!")
	try:
		while True: # Run for ever
			#get position of switch
			input = GPIO.input(buttonPin)
			#switch has been turned on
			if ((not prev_input) and input):
				time.sleep(.5)
				input2 = GPIO.input(buttonPin)
				if (input and (not input2)):
					print("Indstiller min og max tid...")
					setMinMaxTime()
					print("Tiden er sat til mellem {0} og {1} minutter".format(int(minTime/60),int(maxTime/60)))
				else:
					print("Starter pakkeleg ...")
					tid = random.randint(minTime, maxTime)
					print("Psst - klokken ringer om {0} min og {1} sekunder".format(int(tid/60),tid % 60))
					thePakkeleg = PakkelegThread(tid)
					thePakkeleg.start()
			#switch has been turned off
			if (prev_input and (not input)):
				print("Pakkeleg afbrudt.")
				if('thePakkeleg' in locals()):
					thePakkeleg.stop()

			#update previous input
			prev_input = input
			#slight pause to debounce
			time.sleep(0.05)

	# End program cleanly with keyboard
	except KeyboardInterrupt:
		# Reset GPIO settings
		GPIO.cleanup()

		# turn off LEDs
		pixels.fill((0,0,0))
		pixels.show()
		print(" Exiting...")


if __name__== "__main__":
  main()

