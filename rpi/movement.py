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

# def tohex(val, nbits):
#     return hex((val + (1 << nbits)) % (1 << nbits))


# def tobyte(val):
#     htxt = val[2:].zfill(4)
#     msb = "0x" + htxt[0:2]
#     lsb = "0x" + htxt[2:4]
#     # return msb, lsb
#     return int(msb, 16), int(lsb, 16)


# def convert(val):
#     valhex = tohex(val, 16)
#     return tobyte(valhex)


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


def checklist():
    # CONFIG
    ip = "192.168.1.9"
    port = 12345

    for i in range(0, 4):
        # TODO: Move

        # Capture
        cam = Camera()
        filename = cam.capture("../../../../shared/")
        time.sleep(2)
        iclient = ImageClient(ip, port)
        result = iclient.send(bytes(filename, "utf-8"))
        img_id = bytes.decode(result)
        print("Detected image #" + img_id)

        if result == b"15":
            continue
        else:
            break
