
#!/usr/bin/env python

#-------------------------------------------------------------------#
# Photobooth.py : Program for weeding photobooth running on 
# Raspberry Pi with Raspbian OS.
#-------------------------------------------------------------------#

__author__ = "Albert Puig"
__copyright__ = "Copyright 2015, Tomatitosoft"
__credits__ = ["Albert Puig"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Albert Puig"
__email__ = "albertpuig@gmail.com"
__status__ = "Development"

import os
import pygame
import time
import random
import subprocess
import time
import picamera

class photobooth :

	screen = None;  #variable for FB screen managament

	##############################################################
	# __init__(a)
	# This function starts program
	# inputs: Only sefl variable
	# returns: nothing
	def __init__(self):
		"Ininitializes a new pygame screen using the framebuffer"
	        # Based on "Python GUI in Linux frame buffer"
	        # http://www.karoltomala.com/blog/?p=679
		disp_no = os.getenv("DISPLAY")
		if disp_no:
			print "I'm running under X display = {0}".format(disp_no)

	        # Check which frame buffer drivers are available
		# Start with fbcon since directfb hangs with composite output
		drivers = ['fbcon', 'directfb', 'svgalib']
		found = False
		for driver in drivers:
		# Make sure that SDL_VIDEODRIVER is set
			if not os.getenv('SDL_VIDEODRIVER'):
				os.putenv('SDL_VIDEODRIVER', driver)
			try:
				pygame.display.init()
			except pygame.error:
				print 'Driver: {0} failed.'.format(driver)
				continue
			found = True
			break
	    
		if not found:
			raise Exception('No suitable video driver found!')

		size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
		print "Framebuffer size: %d x %d" % (size[0], size[1])
		self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
		# Clear the screen to start
		self.screen.fill((0, 0, 0))        
 		# Initialise font support
		pygame.font.init()
		# Hide the mouse cursor
		pygame.mouse.set_visible(False)
		# Set caption
		pygame.display.set_caption('Tatiana y Albert')
		# Render the screen
		pygame.display.update()

	##############################################################
	# __del__(a)
	# This function starts program
	# inputs: self
	# returns: nothing, destructor class
	def __del__(self):
        	"Destructor to make sure pygame shuts down, etc."

	##############################################################
	# __test__(a)
	# This function starts program
	# inputs: self
	# returns: display an image on FB
	def test(self):
        	# Fill the screen with red (255, 0, 0)
        	#red = (255, 0, 0)
        	#self.screen.fill(red)
        	filename = "/home/pi/ftp/files/test/intro.png"
		print filename
		img=pygame.image.load(filename).convert()
		img=pygame.transform.scale(img,(1824,984))	
		self.screen.blit(img,(0,0))
		# Update the display
		pygame.display.update()

	def takepic(self):
		print "Take a picture smile"
		filename = "/home/pi/ftp/files/test/blank.png"
		print filename
		img=pygame.image.load(filename).convert()
		img=pygame.transform.scale(img,(1824,984))	
		self.screen.blit(img,(0,0))
		pygame.display.update()
		
		file_path = '/home/pi/ftp/files/test/' #where do you want to save the photos

		now = time.strftime("%Y%m%d%H%M%S") #get the current date and time for the start of the filename
		file_name = file_path + now+ '.jpg'
		print file_name
		#subprocess.call(["raspistill","-f","-vf","-o",file_name,"-sa","0","-w","1824","-h","984"])
		with picamera.PiCamera() as camera:
			camera.resolution = (1824, 984)
			camera.start_preview()
			camera.annotate_text = 'Tatiana y Albert - 4 Sept 2015'
			# Camera warm-up time
			time.sleep(2)
			camera.capture(file_name)
		
		print "Done"
		filename = "/home/pi/ftp/files/test/finished2.png"
		print filename
		img=pygame.image.load(filename).convert()
		img=pygame.transform.scale(img,(1824,984))	
		self.screen.blit(img,(0,0))
		pygame.display.update()

# exec of photoboth program test
print ("Photobooth startup")
wedding = photobooth()
wedding.test()
# missed button trigger and while loop
time.sleep(2)
wedding.takepic()
time.sleep(6)


