import picamera
import picamera.array
import time 


#camera = picamera.PiCamera()

def hundra(camera):
    for i in range(100):
        camera.capture(str(i) + '.jpg') #Sparar en bild
        sleep(1)    
def test(camera, numberof):

    start=time.time()
    for i in range(numberof):
        with picamera.array.PiRGBArray(camera) as output:
            camera.capture(output, 'rgb', use_video_port=True)
    end=time.time()
    taken=(time.time()-start)/numberof
    print('Att ta en bild: ' + str(taken) + ' s')
#test(camera, 10)
    
def restest(numberof, width, height):
    """Ska test hur långtid det tar (i genomsnitt) för numberof bilder med given width och eight"""
    with picamera.PiCamera() as camera:
        with picamera.array.PiRGBArray(camera) as output:
            camera.resolution = (width, height)
            camera.framerate = 10
            start=time.time()
            for i in range(numberof):
                #camera.capture('file.jpeg')
                camera.capture(output, 'rgb',use_video_port=True) #Use_video_port = True, innebär att bilder tas snabbare som att det vore en video
                #Gör något med output här
                output.truncate(0)
            end=time.time()
            taken=(time.time()-start)/numberof
            print('Att ta en ' + str(width) + 'x' + str(height) + ' bild: ' + str(taken) + ' s')


def tabild(name, width, height,uvp=True):
    with picamera.PiCamera() as camera:
        with picamera.array.PiRGBArray(camera) as output:
            camera.resolution = (width, height)
            camera.framerate = 10
            camera.capture(name+'.jpeg',use_video_port=uvp)
            #camera.capture(output, 'rgb',use_video_port=True) #Use_video_port = True, innebär att bilder tas snabbare som att det vore en video
            #Gör något med output här
            output.truncate(0)    
#Tiden är ungefär densamma för olika storlekar
#restest(10, 1920, 720)
#restest(10, 224, 112)

#Samma bild (hela bilden) fast i den givna storleken
#tabild('small',224, 112)
tabild('big',1920,720)
tabild('bigi',1920,720,False)

#Lite länkar:
#http://picamera.readthedocs.io/en/release-1.10/api_array.html
#http://picamera.readthedocs.io/en/release-1.10/api_camera.html
