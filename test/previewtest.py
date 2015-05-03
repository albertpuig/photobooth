#!/usr/bin/env python

import time
import picamera

with picamera.PiCamera() as camera:
    #camera.resolution = (2592, 1944)
    # The following is equivalent
    #camera.resolution = camera.MAX_IMAGE_RESOLUTION	
    camera.vflip = True
    #camera.saturation = 0
    camera.start_preview()
    time.sleep(5)
    camera.capture('test_file.jpg')
