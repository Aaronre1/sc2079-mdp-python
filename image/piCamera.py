from picamera import piCamera
from time import sleep

# camera preview
camera = PiCamera()
camera.start_preview()
sleep(10)
camera.stop_preview()

# camera testing
from picamera.array import PiGRBArray

camera.resolution = (640,480) # change camera resolution
output = PiGRBArray(camera)
camera.capture(output, 'bgr') # capture image
src = output.array
print('Capture %d%d image' %(src.shape[1], src.shape[0])) #access to selected pixels

for i in range(1,10):
        s=''
        for j in range(1,10):
                s=s+repr(src[i,j,1])+' '
        print(s)
