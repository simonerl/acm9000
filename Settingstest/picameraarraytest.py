import picamera
import picamera.array
def test():
    camera=picamera.PiCamera()
    output=picamera.array.PiRGBArray(camera) 
    camera.capture(output, 'rgb')
    return output
output=test()
print('Captured %dx%d image' % (output.array.shape[1], output.array.shape[0]))
print(output.array)
