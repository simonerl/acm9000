#########################################
# RGB image shooting program for a      #
# Raspberry Pi 3 and a Raspberry Pi     #
# camera v.2                            #
# By Simon Erlandsson & Gustav Burman   #
# CMAST                                 #
# Version 1.0:2018-04-17                #
#########################################
import picamera
import picamera.array
import time
import numpy
def implementsettings(camera):
    """Will implement the settings below for a picamera object"""
    camera.sensor_mode=0 #Automatiskt av resolution och framerate
    camera.resolution= (112, 80)
    camera.sharpness = 0
    camera.contrast = 0
    camera.brightness = 50
    camera.saturation = 0
    camera.ISO = 50
    camera.video_stabilization = False
    camera.exposure_compensation = 0
    camera.exposure_mode = 'sports'
    camera.meter_mode = 'average'
    camera.awb_mode = 'auto'
    camera.image_effect = 'none'
    camera.color_effects = None
    camera.rotation = 0
    camera.hflip = True
    camera.vflip = True
    camera.crop = (0.0, 0.0, 1.0, 1.0)
    camera.image_denoise=False
  
def takejpgimage(name,camera):
    """Takes a jpeg image"""
    #Specific for camera.capture:
    uvp = True # use_video_port  
    camera.capture(name + '.jpeg')
        
def takeRGBimage(camera):
    """Takes an images and returns an RGB matrix in the form of a picamera.array.PiRGBArray"""
    output=picamera.array.PiRGBArray(camera)
    output.truncate(0)
    #Specific for camera.capture:
    uvp = True # use_video_port  
    camera.capture(output, 'rgb',use_video_port=uvp)
    return output

def camerastatus(camera):
    """Prints information about a picamera"""
    print('Resolution ' + str(camera.resolution))
    print('Exposure mode ' + str(camera.exposure_mode))
    print('Horizontol flip ' + str(camera.hflip))
    print('Vertical flip ' + str(camera.vflip))
    print('Current exposure speed ' + str(camera.exposure_speed) +' us')
    print('Image denoise: ' + str(camera.image_denoise))
    print('Image effect: ' + str(camera.image_effect))
    start=time.time()
    takeRGBimage(camera)
    end=time.time()
    taken=(time.time()-start)
    print('Time to shoot RGB image ' + str(taken) + 's')

if __name__=='__main__':
    camera=picamera.PiCamera()
    implementsettings(camera)
    takejpgimage('test', camera) #Takes a jpeg image
    output=takeRGBimage(camera) #Takes a rgb image
    camerastatus(camera)
    print('Captured %dx%d image' % (output.array.shape[1], output.array.shape[0]))
    start=time.time()
    output=takeRGBimage(camera)
    end=time.time()
    taken=(time.time()-start)
    print('Time to shoot RGB image ' + str(taken) + 's')
    print('Captured %dx%d image' % (output.array.shape[1], output.array.shape[0]))
