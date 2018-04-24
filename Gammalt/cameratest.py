import picamera
from time import sleep

camera = picamera.PiCamera()



#Setting:
camera.resolution = 0
camera.sharpness = 0
camera.contrast = 0
camera.brightness = 50
camera.saturation = 0
camera.ISO = 50
camera.video_stabilization = False
camera.exposure_compensation = 0
camera.exposure_mode = 'auto'
camera.meter_mode = 'average'
camera.awb_mode = 'auto'
camera.image_effect = 'none'
camera.color_effects = None
camera.rotation = 0
camera.hflip = True
camera.vflip = True
camera.crop = (0.0, 0.0, 1.0, 1.0)
camera.capture('image8.jpg') #Sparar en bild

#camera.start_preview() #Avsluta med ctrl-D
#camera.stop_preview()


#Filma fem sekunder
#camera.start_recording('video.h264')
#sleep(5)
#camera.stop_recording()
