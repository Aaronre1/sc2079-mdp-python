import movement as move
from communication import BluetoothServer, ImageClient, AlgoClient
from camera import Camera

UUID = "00001101-0000-1000-8000-00805F9B34FB"
ALGO_URL = "http://192.168.1.14:5000/path"

IMAGE_IP = "192.168.192."
IMAGE_PORT = 12345
IMAGE_DIR = "../../../../shared/"

img_count = 0
# start bluetooth server
with BluetoothServer(UUID) as bt:
    # receive arena info (BT)
    algo_arena = bt.accept()
    # send arena info to algo server(REST)
    algo_client = AlgoClient(ALGO_URL)
    # receive algo solution(REST)
    algo_solution = algo_client.send(algo_arena)

    # execute algo path
    cam = Camera()
    cmds = algo_solution.commands

    for i in range(len(cmds)):
        cmd = cmds[i]
        action = cmd[0]
        val = cmd[1]

        move.idle(5)  # idle between commands
        if action == "FW":
            for j in range(0,val):
                move.FW(1)
                bt.send("FW")
        elif action == "FR":
            move.FR00()
            bt.send("FR")
        elif action == "FL":
            move.FL00()
            bt.send("FL")
        elif action == "BR":
            move.BR00()
        elif action == "BL":
            move.BL00()
        elif action == "BW":
            for j in range(0,val):
                move.backward(1)
                bt.send("BW")
        elif action == "SN":
            for j in range(0, 1):
                bt.send("SN")
                img_name = cam.capture(IMAGE_DIR)
                img_client = ImageClient(IMAGE_IP, IMAGE_PORT)
                img_result = img_client.send(bytes(img_name, "utf-8"))
                if img_result != "15":
                    # ping back image_id (BT)
                    # obstacle:,<obs id>,<img id>
                    bt.send("obstacle:," + str(val) + img_result)
                    # update image_count
                    img_count += 1
                    break
            # if image_count >= 5: break
            if img_count >= 5:
                print("all image found. terminating")
                break
