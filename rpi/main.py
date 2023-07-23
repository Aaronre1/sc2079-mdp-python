import movement as move
from navigation import Navigator
from communication import BluetoothServer, ImageClient, AlgoClient, BluetoothServer
from camera import Camera
import json
from convert import toimageid, flatten_command

UUID = "00001101-0000-1000-8000-00805F9B34FB"
ALGO_URL = "http://192.168.1.9:5000/path"

IMAGE_IP = "192.168.1.9"
IMAGE_PORT = 12345
IMAGE_DIR = "../../../../shared/"

IMAGE_RETRY = 1
img_count = 0


def get_arena_info(bts: BluetoothServer):
    while True:
        bt_msg = bts.recv()
        if len(bt_msg) < 1:
            continue
        elif bt_msg[0] == "{":  # only process json strings
            try:
                print("parsing arena_info")
                arena_info = json.loads(bt_msg)
                arena_info["retrying"] = False
                print("received arena info (BT)")
                print(str(arena_info))
                return arena_info
            except:
                print("parse arena_info failed")
                continue


def get_algo_solution(arena_info):
    algo_client = AlgoClient(ALGO_URL)
    algo_solution = algo_client.send(arena_info)
    print("received algo solution")
    print(str(algo_solution))
    return algo_solution


def snap(bts: BluetoothServer, cam: Camera):
    for x in range(IMAGE_RETRY):
        bts.send("SN")
        img_name = cam.capture(IMAGE_DIR)
        client = ImageClient(IMAGE_IP, IMAGE_PORT)
        result = client.send(bytes(img_name, "utf-8"))
        img_id = toimageid(bytes.decode(result, "utf-8"))
        if img_id != "15":
            return img_id
    return "15"

def main():
    print("running...")
    with BluetoothServer(UUID) as bts, Camera() as cam:
        arena_info = get_arena_info(bts)

        algo_solution = get_algo_solution(arena_info)

        commands = flatten_command(algo_solution["data"])
        img_client = ImageClient(IMAGE_IP, IMAGE_PORT)

        nav = Navigator(1, 1, 0, cam, img_client, IMAGE_DIR, IMAGE_RETRY)

        move.idle(5)
        for i in range(len(commands)):
            nav.execute(commands[i])
            # ping back to android
            # d,x,y,s|id,img,id,img,id,img,id,img,
            bt_msg = str(nav.d) + "," + str(nav.x) + "," + str(nav.y) +","+ str(nav.s)+ ",|"
            for k in nav.detected.keys():
                obs_id = k
                img_id = nav.detected[k]
                bt_msg += obs_id + "," + img_id + ","
                
            bts.send(bt_msg)
            
    print("terminating...")
        
if __name__ == "__main__":
    main()

