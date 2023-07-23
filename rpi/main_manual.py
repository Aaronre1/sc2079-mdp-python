import movement as move
from navigation import Navigator
from communication import BluetoothServer, ImageClient
from camera import Camera
import json
from convert import tocommand, toimageid, flatten_command

UUID = "00001101-0000-1000-8000-00805F9B34FB"
ALGO_URL = "http://192.168.1.9:5000/path"

IMAGE_IP = "192.168.1.9"
IMAGE_PORT = 12345
IMAGE_DIR = "../../../../shared/"


def main():
    print("running...")
    with BluetoothServer(UUID) as bts, Camera() as cam:
        img_client = ImageClient(IMAGE_IP, IMAGE_PORT)
        obs_id = 1
        detected = {}

        while True:
            cmd = bts.recv()
            move.idle(2)
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
                img_name = cam.capture(IMAGE_DIR)
                result = img_client.send(bytes(img_name, "utf-8"))
                img_id = toimageid(bytes.decode(result, "utf-8"))
                print("detected obstacle #" + str(obs_id) + " as image #" + img_id)
                detected[str(obs_id)] = img_id
                obs_id += 1
                move.idle(5)  # idle between snaps

                bt_msg = "0,0,0,0,|" 
                for k in detected.keys():
                    obs_id_str = k
                    img_id = detected[k]
                    bt_msg += obs_id_str + "," + img_id + ","
                
                bts.send(bt_msg)

if __name__ == "__main__":
    main()