import movement as move
from communication import BluetoothServer, ImageClient, AlgoClient
from camera import Camera

UUID = "00001101-0000-1000-8000-00805F9B34FB"
ALGO_URL = ""
IMAGE_IP = "192.168.192."
IMAGE_PORT = 12345
IMAGE_DIR = ""

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
    cmd = []
    while True:
        # LOOP
        
        # move
        # ping back location (BT)
        # if SNAP: detect image (TCP)
        
        img_name = cam.capture(IMAGE_DIR)
        img_client = ImageClient(IMAGE_IP, IMAGE_PORT)
        img_result = img_client.send(bytes(img_name, "utf-8"))
        if img_result != "15":
            # ping back image_id (BT)
            bt.send(img_result)
            # update image_count
            img_count += 1
            # if image_count >= 5: break
            if img_count >= 5:
                print('all image found. terminating')
                break
