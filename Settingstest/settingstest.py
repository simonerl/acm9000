import picamera
import picamera.array
import time

def restest():
    """Ska test hur långtid det tar (i genomsnitt) för numberof bilder med given width och eight"""
    with picamera.PiCamera() as camera:
        with picamera.array.PiRGBArray(camera) as output:
            ######################################
            #SETTINGS
            #Ovissentliga är utkommenterade
            ###
            #camera.resolution = (width, height)
            #camera.framerate = 10
            #camera_num=0 
            #stereo_mode='none'
            #stereo_decimate=False
            #camera.sensor_mode=0 #Automatiskt av resolution och framerate
            #led_pin=None #GPIO pin som ska styra kamerans led
            ###
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
            #Specifikt för camera.capture:
            uvp = False # use_video_port #Use_video_port = True, innebär att bilder tas snabbare som att det vore en video
            ######################################
            #sensor_vektor = [0, 1, 2, 3, 4, 5, 6, 7]
            #awb_vektor=['off','auto','sunlight','cloudy','shade','tungsten','fluorescent','incandescent','flash','horizon']
            meter_vektor=['average','spot','backlit','matrix']
            for i in meter_vektor:
                try:
                    start=time.time()
                    camera.meter_mode=i
                    camera.capture(output, 'rgb',use_video_port=uvp) 
                    #Gör något med output här
                    
                    end=time.time()
                    taken=(time.time()-start)
                    print('Att ta bild med sensor_mode ' + str(i) + ': ' + str(taken) + ' s')
                except:
                    print('sensor_mode' + str(i) + ' fungerade inte!')
                output.truncate(0)
restest()
