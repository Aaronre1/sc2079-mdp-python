from picamera import PiCamera
from time import sleep, gmtime
import calendar
from communication import ImageClient

class Camera(object):
    def __init__(self, resolution=(640, 480)):
        self.resolution = resolution
        
    def __enter__(self):
        self.cam = PiCamera()
        self.cam.resolution = self.resolution
        self.cam.start_preview()
        sleep(1)
        return self
        
    def __exit__(self, *args):
        self.cam.stop_preview()
        self.cam.close()
        
    def capture(self,directory=""):
        timestamp = calendar.timegm(gmtime())
        filename = "obstacle_" + str(timestamp) + ".jpg"
        path = directory + filename
        self.cam.capture(path)
        print("camera.py capture() to " + path)
        return filename
    
# deprecated
class Camera2(object):
    def __init__(self, resolution=(640, 480)):
        self.resolution = resolution

    def capture(self, directory=""):
        print("capturing image")
        cam = PiCamera()
        cam.resolution = self.resolution
        cam.start_preview()
        sleep(2) #sleep to allow camera to focus
        timestamp = calendar.timegm(gmtime())
        filename = "obstacle_" + str(timestamp) + ".jpg"
        path = directory + filename
        cam.capture(path)
        cam.stop_preview()
        cam.close()
        print("camera.py capture() to " + path)
        return filename


if __name__ == "__main__":
    cam = Camera2()
    filename = cam.capture("../../../../shared/")
    sleep(2)
    print(filename)
    ip = "192.168.1.9"
    port = 12345
    iclient = ImageClient(ip, port)
    result = iclient.send(bytes(filename, "utf-8"))
    print(result)
