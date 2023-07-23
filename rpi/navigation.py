import movement as move
from camera import Camera2
from communication import ImageClient
from convert import toimageid


class Navigator(object):
    """
    Move robot base on command given.
    Keeps track of robot position after movement.
    N,E,S,W
    0,2,4,6
    """

    def __init__(
        self, x, y, d, cam: Camera2, img_client: ImageClient, img_directory, retries=1
    ):
        self.x = x
        self.y = y
        self.d = d
        self.cam = cam
        self.retries = retries
        self.image_client = img_client
        self.image_directory = img_directory

        self.detected = {}

    def __snap(self):
        for x in range(self.retries):
            img_name = self.cam.capture(self.image_directory)
            result = self.image_client.send(bytes(img_name, "utf-8"))
            img_id = toimageid(bytes.decode(result, "utf-8"))
            
            if img_id != "0":
                print("detected image #" + img_id)
                return img_id
        print("no image detected")
        return "0"

    def execute(self, data):
        print("executing command: " + str(data))
        cmd = data["command"]
        pos = data["position"]

        self.x = pos["x"]
        self.y = pos["y"]
        self.d = pos["d"]
        self.s = pos["s"]

        if cmd == "FW":
            move.FW(1)
        elif cmd == "BW":
            move.BW(1)
        elif cmd == "FR":
            move.FR00()
        elif cmd == "FL":
            move.FL00()
        elif cmd == "BL":
            move.BL00()
        elif cmd == "BR":
            move.BR00()
        elif cmd == "SN":
            obs_id = str(pos["s"])
            img_id = self.__snap()
            print("detected obstacle #" + obs_id + " as image #" + img_id)
            self.detected[obs_id] = img_id
            move.idle(5)  # idle between snaps
