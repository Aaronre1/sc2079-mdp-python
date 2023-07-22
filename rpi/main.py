import movement as move
from communication import BluetoothServer, ImageClient, AlgoClient
from camera import Camera, Camera2
import json
from convert import tocommand

UUID = "00001101-0000-1000-8000-00805F9B34FB"
ALGO_URL = "http://192.168.1.9:5000/path"

IMAGE_IP = "192.168.1.16"
IMAGE_PORT = 12345
IMAGE_DIR = "../../../../shared/"

IMAGE_RETRY = 1
img_count = 0
# start bluetooth server
with BluetoothServer(UUID) as bt:
    print("running...")
    # device connected
    # setup
    bt_msg = ""
    bt_client, bt_info = bt.accept()
    while True:
        bt_msg = bytes.decode(bt_client.recv(1024), "utf-8")
        if len(bt_msg) < 6:
            continue
        if bt_msg[0:6] == "Device":
            continue
        else:
            # bt_client.close()
            break

    # receive arena info (BT)
    algo_arena = json.loads(bt_msg)
    algo_arena["retrying"] = False
    print("Receive arena info (BT)")
    print(str(bt_msg))
    # send arena info to algo server(REST)
    algo_client = AlgoClient(ALGO_URL)
    # receive algo solution(REST)=
    algo_solution = algo_client.send(algo_arena)
    print("Receive algo solution")
    print(str(algo_solution))

    # execute algo path
    cam = Camera()
    # with Camera2() as cam:
    cmds = algo_solution.data.commands

    for i in range(len(cmds)):
        cmd = tocommand(cmds[i])
        print("Executing command: " + str(cmd))
        action = cmd[0]
        val = cmd[1]

        move.idle(5)  # idle between commands
        if action == "FW":
            for j in range(0, val):
                move.FW(1)
                bt_client.send("FW")
        elif action == "FR":
            move.FR00()
            bt_client.send("FR")
        elif action == "FL":
            move.FL00()
            bt_client.send("FL")
        elif action == "BR":
            move.BR00()
        elif action == "BL":
            move.BL00()
        elif action == "BW":
            for j in range(0, val):
                move.backward(1)
                bt_client.send("BW")
        elif action == "SN":
            for j in range(0, IMAGE_RETRY):
                bt_client.send("SN")
                img_name = cam.capture(IMAGE_DIR)
                img_client = ImageClient(IMAGE_IP, IMAGE_PORT)
                img_result = img_client.send(bytes(img_name, "utf-8"))
                if img_result != "15":
                    # ping back image_id (BT)
                    # obstacle:,<obs id>,<img id>
                    bt_client.send("obstacle:," + str(val) + img_result)
                    # update image_count
                    img_count += 1
                    break
            # if image_count >= 5: break
            if img_count >= 5:
                print("all image found. terminating")
                break
