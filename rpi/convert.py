def tohex(val, nbits):
    return hex((val + (1 << nbits)) % (1 << nbits))


def tobyte(val):
    htxt = val[2:].zfill(4)
    msb = "0x" + htxt[0:2]
    lsb = "0x" + htxt[2:4]
    # return msb, lsb
    return int(msb, 16), int(lsb, 16)


def convert(val):
    valhex = tohex(val, 16)
    return tobyte(valhex)


def tocommand(command: str):
    # FW90
    # 0123

    # SNAP3_C
    # 0123456
    action = command[0:2]
    if action == "SN":
        snapid = command[4]
        return (action, int(snapid))
    elif action == "FI":
        return (action, 0)
    else:
        val = command[2]
        return (action, int(val))


image_map = {
    "0": "10",
    "1": "6",
    "2": "7",
    "3": "8",
    "4": "9",
    "5": "11",
    "6": "12",
    "7": "13",
    "8": "14",
    "9": "15",
    "10": "2",
    "11": "4",
    "12": "3",
    "13": "1",
    "14": "5",
    "15": "15",
}


def toimageid(img: str):
    return image_map[img]
