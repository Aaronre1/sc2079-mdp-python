import serial
import time
from convert import convert

PORT = "/dev/ttyS0"
BAUDRATE = 115200
DELAY = 0.8
SER = serial.Serial(
    PORT, BAUDRATE, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE
)
# Header, Packet length, ID, Function,
# X MSB, X LSB, Y MSB, Y LSB, Z MSB, Z LSB
# Reserve byte, CRC byte
IDLE = [0x5A, 0x0C, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF]
# X -1000 to 1000
# Y do not change
# Z 1000 (left) to -1000 (right)


def send(x, z):
    xhex = convert(x)
    zhex = convert(z)
    packet = [
        0x5A,
        0x0C,
        0x01,
        0x01,
        xhex[0],
        xhex[1],
        0x00,
        0x00,
        zhex[0],
        zhex[1],
        0x00,
        0xFF,
    ]

    SER.write(bytearray(packet))
    time.sleep(DELAY)


def forward(x):
    for i in range(0, x):
        send(120, 0)


def backward(x):
    for i in range(0, x):
        send(-120, 0)


# turn right +1Y +3X
def right_13():
    for i in range(0, 6):
        send(90, -1000)
    for i in range(0, 5):
        send(-90, -1000)
    for i in range(0, 3):
        send(100, 0)
    send(50, -1000)
    for i in range(0, 3):
        send(100, 0)


def left_13():
    for i in range(0, 6):
        send(90, 1000)
    for i in range(0, 5):
        send(-90, 1000)
    for i in range(0, 3):
        send(100, 0)
    send(50, 1000)
    for i in range(0, 3):
        send(100, 0)


from camera import Camera
from communication import ImageClient


def idle(x):
    for i in range(0, x):
        send(0, 0)


def FW(x):
    for i in range(0, x):
        send(129, 0)


def BW(x):
    for i in range(0, x):
        send(-129, 0)


def FR00():
    for i in range(0, 2):
        send(-60, -700)
    for i in range(0, 6):
        send(85, -780)


def FL00():
    for i in range(0, 3):
        send(-50, 910)
    for i in range(0, 6):
        send(85, 710)


def BL00():  # Backward Left
    for i in range(0, 4):
        send(-120, -1000)
    for i in range(0, 1):
        send(150, -500)
    for i in range(0, 1):
        send(-70, -680)
    send(-20, 0)


def BR00():  # Backward Right
    for i in range(0, 4):
        send(-120, 980)
    for i in range(0, 1):
        send(140, 450)
    for i in range(0, 1):
        send(-60, 450)
    send(20, 0)


def bullseye():
    for i in range(0, 5):
        send(-120, 500)
    idle(1)
    for i in range(0, 8):
        send(130, 0)
    idle(1)
    for i in range(0, 6):
        send(250, -650)


def checklist():
    # CONFIG
    ip = "192.168.1.9"
    port = 12345

    for i in range(0, 4):
        # Capture
        cam = Camera()
        filename = cam.capture("../../../../shared/")
        time.sleep(2)
        iclient = ImageClient(ip, port)
        result = iclient.send(bytes(filename, "utf-8"))
        img_id = bytes.decode(result)
        print("Detected image #" + img_id)

        if result == b"15":
            idle(5)
            bullseye()
            continue
        else:
            break


if __name__ == "__main__":
    checklist()
