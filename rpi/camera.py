from picamera import PiCamera
from time import sleep, gmtime
import calendar
from communication import ImageClient


class Camera(object):
    def __init__(self, resolution=(640, 480)):
        self.resolution = resolution

    def capture(self, directory=""):
        cam = PiCamera()
        cam.start_preview()

        timestamp = calendar.timegm(gmtime())
        filename = "obstacle_" + str(timestamp) + ".jpg"
        path = directory + filename
        cam.capture(path)

        cam.stop_preview()
        print("camera.py capture() to " + path)
        return filename
        # cam.resolution = self.resolution
        # output = PiGRBArray(cam)
        # cam.capture(output, 'bgr')
        # src = output.array
        # print(src)


if __name__ == "__main__":
    cam = Camera()
    filename = cam.capture("../../../shared/")
    print(filename)
    ip = "192.168.1.9"
    port = "12345"
    iclient = ImageClient(ip, port)
    result = iclient.send(bytes(filename))
    print(result)
