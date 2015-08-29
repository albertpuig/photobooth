
#!/usr/bin/env python

#-------------------------------------------------------------------#
# Photobooth.py : Program for weeding photobooth running on 
# Raspberry Pi with Raspbian OS.
#-------------------------------------------------------------------#

__author__ = "Albert Puig"
__copyright__ = "Copyright 2015, Tomatitosoft"
__credits__ = ["Albert Puig"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Albert Puig"
__email__ = "albertpuig@gmail.com"
__status__ = "Development"

import os
import atexit
import pygame
import time
import random
import subprocess
import picamera
import yuv2rgb
import io
import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont


class photobooth :

	screen = None;  #variable for FB screen managament

	sizeData = [ # Camera parameters for different size settings
 	 # Full res      Viewfinder  Crop window
 	 [(2592, 1944), (320, 240), (0.0   , 0.0   , 1.0   , 1.0   )], # Large
 	 [(1920, 1080), (320, 180), (0.1296, 0.2222, 0.7408, 0.5556)], # Med
 	 [(1440, 1080), (320, 240), (0.2222, 0.2222, 0.5556, 0.5556)]] # Small


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

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	

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
	def introimg(self):
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
		
		self.take_picamera(file_path)

		print "Done"
		filename = "/home/pi/ftp/files/test/finished2.png"
		print filename
		img=pygame.image.load(filename).convert()
		img=pygame.transform.scale(img,(1824,984))	
		self.screen.blit(img,(0,0))
		pygame.display.update()
		time.sleep(4)

		filename = "/home/pi/ftp/files/test/intro.png"
		print filename
		img=pygame.image.load(filename).convert()
		img=pygame.transform.scale(img,(1824,984))	
		self.screen.blit(img,(0,0))
		# Update the display
		pygame.display.update()





	def take_picamera(self,file_path):

		now = time.strftime("%Y%m%d%H%M%S") #get the current date and time for the start of the filename
		file_name = file_path + now+ '.jpg'
		print file_name
		# Load the arbitrarily sized image
		img5 = Image.open('5.png')
		img4 = Image.open('4.png')
		img3 = Image.open('3.png')
		img2 = Image.open('2.png')
		img1 = Image.open('1.png')
		img0 = Image.open('sonrie.png')
		# Create an image padded to the required size with
		# mode 'RGB'
		pad5 = Image.new('RGB', (((img5.size[0] + 31) // 32) * 32,((img5.size[1] + 15) // 16) * 16,))
		# Paste the original image into the padded one
		pad5.paste(img5, (0, 0))

		pad4 = Image.new('RGB', (((img4.size[0] + 31) // 32) * 32,((img4.size[1] + 15) // 16) * 16,))
		pad4.paste(img4, (0, 0))
		pad3 = Image.new('RGB', (((img3.size[0] + 31) // 32) * 32,((img3.size[1] + 15) // 16) * 16,))
		pad3.paste(img3, (0, 0))
		pad2 = Image.new('RGB', (((img2.size[0] + 31) // 32) * 32,((img2.size[1] + 15) // 16) * 16,))
		pad2.paste(img2, (0, 0))
		pad1 = Image.new('RGB', (((img1.size[0] + 31) // 32) * 32,((img1.size[1] + 15) // 16) * 16,))
		pad1.paste(img1, (0, 0))
		pad0 = Image.new('RGB', (((img0.size[0] + 31) // 32) * 32,((img0.size[1] + 15) // 16) * 16,))
		pad0.paste(img0, (0, 0))
		#subprocess.call(["raspistill","-f","-vf","-o",file_name,"-sa","0","-w","1824","-h","984"])
		
		
		with picamera.PiCamera() as camera:

			#camera.resolution = (1824, 984)
			atexit.register(camera.close)
			camera.resolution = (1824,984)
			camera.crop       = (0.0, 0.0, 1.0, 1.0)
			'''
			# Buffers for viewfinder data
			rgb = bytearray(320 * 240 * 3)
			rgb = bytearray(camera.resolution[0] * camera.resolution[1] * 3)
			yuv = bytearray(320 * 240 * 3 / 2)
			#camera.annotate_text = 'Tatiana y Albert - 4 Sept 2015'
			sizeMode = 0
			while (True):
				stream = io.BytesIO() # Capture into in-memory stream
				camera.capture(stream, use_video_port=True, format='rgb')
				stream.seek(0)
				stream.readinto(rgb)  # stream -> YUV buffer
				stream.close()
				#yuv2rgb.convert(yuv, rgb, sizeData[sizeMode][1][0],sizeData[sizeMode][1][1])
				#img = pygame.image.frombuffer(rgb[0:(self.sizeData[sizeMode][1][0] * self.sizeData[sizeMode][1][1] * 3)],self.sizeData[sizeMode][1], 'RGB')
				#funciona
				#img = pygame.image.frombuffer(rgb[0:(320 * 240 * 3)], (320, 240), 'RGB')
				img = pygame.image.frombuffer(rgb[0:(camera.resolution[0] * camera.resolution[1] * 3)], (camera.resolution[0], camera.resolution[1]), 'RGB')
				if img:
					#self.screen.blit(img,((320 - img.get_width() ) / 2,(240 - img.get_height()) / 2))
					self.screen.blit(img, (0,0))
				
				pygame.display.update()
			'''

			# inicio de previsualizacion
			camera.start_preview(alpha=128)

			#titulo en la camara
			camera.annotate_text = 'Tatiana y Albert - 4 Sept 2015'

			# Fill background
			background = pygame.Surface(self.screen.get_size())
			background = background.convert()
			background.fill(pygame.Color('black'))

			# Display some text
			font = pygame.font.Font(None, 250)
			text5 = font.render("5 - pygame", 1, (255, 10, 10))
			textpos5 = text5.get_rect()
			textpos5.centerx = background.get_rect().centerx
			background.blit(text5, textpos5)

			# Blit everything to the screen
			self.screen.blit(background, (0, 0))
			pygame.display.flip()


			time.sleep(1)

			# Fill background
			background = pygame.Surface(self.screen.get_size())
			background = background.convert()
			background.fill(pygame.Color('black'))

			text4 = font.render("4 - pygame", 1, (255, 10, 10))
			textpos4 = text4.get_rect()
			textpos4.centerx = background.get_rect().centerx
			background.blit(text4, textpos4)

			# Blit everything to the screen
			self.screen.blit(background, (0, 0))
			pygame.display.flip()

			time.sleep(1)





			# Add the overlay with the padded image as the source,
			# but the original image's dimensions
			'''
			o = camera.add_overlay(pad5.tostring(), size=img5.size)
			
			# By default, the overlay is in layer 0, beneath the
			# preview (which defaults to layer 2). Here we make
			# the new overlay semi-transparent, then move it above
			# the preview
			o.alpha = 50
			o.layer = 3
			time.sleep(1)

			camera.remove_overlay(o)
			o = camera.add_overlay(pad4.tostring(), size=img4.size)
			o.alpha = 50
			o.layer = 3
			time.sleep(1)

			camera.remove_overlay(o)
			o = camera.add_overlay(pad3.tostring(), size=img3.size)
			o.alpha = 50
			o.layer = 3	
			time.sleep(1)

			camera.remove_overlay(o)
			o = camera.add_overlay(pad2.tostring(), size=img2.size)
			o.alpha = 50
			o.layer = 3
			time.sleep(1)

			camera.remove_overlay(o)
			o = camera.add_overlay(pad1.tostring(), size=img1.size)
			o.alpha = 50
			o.layer = 3
			time.sleep(1)
			camera.remove_overlay(o)
'''
			
			#intento fallido de pintar texto sobre camera 
			#se pinta con opacidad
			#img_text = Image.new("RGB", (1024, 768))
			#draw = ImageDraw.Draw(img_text)
			#draw.font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSerif.ttf",25)
			#draw.text((760,325), 'Smile', fill=(255, 255, 255))
			#o = camera.add_overlay(img_text.tostring(),size=img_text.size)
			#o.alpha = 128
			#o.layer = 3
			

			#intento de sobreimpresionar texto
			#font = pygame.font.Font(None, 30)
			#text_surface = font.render('pyScope (%s)' % "0.1", True, (255, 255, 255))
			#pyScope = photobooth()
			#pyScope.screen.blit(text_surface, (10, 0))
			#pygame.display.update()
			#camera.remove_overlay(o)

			# Camera warm-up time
			#metodo de picamera para capturar imagen
			o = camera.add_overlay(pad0.tostring(), size=img0.size)
			o.alpha = 50
			o.layer = 3
			time.sleep(0.5)
			camera.remove_overlay(o)


			# Fill background
			background = pygame.Surface(self.screen.get_size())
			background = background.convert()
			background.fill(pygame.Color('black'))

			# Display some text
			font = pygame.font.Font(None, 150)
			text = font.render("Hello There", 1, (255, 10, 10))
			textpos = text.get_rect()
			textpos.centerx = background.get_rect().centerx
			background.blit(text, textpos)

			# Blit everything to the screen
			self.screen.blit(background, (0, 0))
			pygame.display.flip()

			time.sleep(15)
			
			camera.capture(file_name)
			camera.close()

			
		
		



# exec of photoboth program test
print ("Photobooth startup")
wedding = photobooth()
wedding.introimg()
count=0;
# missed button trigger and while loop
while True:
    input_state = GPIO.input(18)
    time.sleep(0.3)
    if input_state == False:
        count=count+1
        wedding.takepic()
	print "Button Pressed %d " %(count)
    
#time.sleep(2)

#time.sleep(6)


