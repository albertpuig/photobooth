# photobooth
Wedding photobooth project

tomatitosoft.com




/test

cameratest – take a photo using python but not picamera

videotest – likewise with a camera

previewtest – using picamera, put a live preview on the screen

continuoustest – it’s too slow to take photos one-by-one, each with a new focus and light level test. Instead, try 
shooting in continuous mode using picamera.

displayjpg – after taking the photos and uploading the animated gif, it’s nice to show it on the screen. I couldn’t get the pi to show the animated gif, but we could cheat by showing the jpgs. This code starts that. It’s a bit tricky.

gpio_test – once you get all the pieces put together, try running this to see if they all work.

gpio_buttons – here I was testing using the buttons–two of them with a event detection

gpio_cleanup – when I was testing, I sometimes that the code quite unexpectedly. I used this code to cleanup the GPIO for the next time I try running something.

internettest – I had an issue where the python program quit when my iPhone hotspot momentarily dropped it’s internet connection. This code tests if there there is an internet connection before uploading and has some error handling. It could probably use some more work.

tumblr_test – here I’m testing uploading to tumblr directly. It works, but it takes a about two minutes to complete even on a good internet connection. That’s not a useful timeframe with a line of people waiting to use the device. I could have built a queue system on a different thread that uploads files one-by-one. Instead I decided to send the file to post via email. Then Tumblr can take the time to process the files and post them.

email_test – here I’m testing sending an email with an attachment
