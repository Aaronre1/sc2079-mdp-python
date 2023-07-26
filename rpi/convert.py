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
    "15": "0",
}


def toimageid(img: str):
    return image_map[img]


def flatten_command(data):
    commands = data["commands"]
    paths = data["path"]
    print(paths)
    f_cmds = []

    step = 0  # do not increment if action == "SN"

    for i in range(len(commands)):
        cmd = tocommand(commands[i])
        action, value = cmd[0], cmd[1]
        if action == "FI":
            break
        path = paths[step]
        step += 1
        direction = path["d"]

        if action == "FW":
            for i in range(value):
                p = path.copy()

                if direction == 0:
                    p["y"] += i
                elif direction == 2:
                    p["x"] += i
                elif direction == 4:
                    p["y"] -= i
                elif direction == 6:
                    p["x"] -= i

                f = {"command": action, "position": p}
                f_cmds.append(f)
        elif action == "BW":
            for i in range(value):
                p = path.copy()
                if direction == 0:
                    p["y"] -= i
                elif direction == 2:
                    p["x"] -= i
                elif direction == 4:
                    p["y"] += i
                elif direction == 6:
                    p["x"] += i
                f = {"command": action, "position": p}
                f_cmds.append(f)
        elif action == "SN":
            f = {"command": action, "position": path}
            f_cmds.append(f)
            step -= 1
        else:
            path = paths[step]
            f_cmds.append({"command": action, "position": path})
        print(f_cmds[i])

    return f_cmds


if __name__ == "__main__":
    cmd = {
        "data": {
            "commands": [
                "FW10",
                "FR00",
                "FW90",
                "FW10",
                "BL00",
                "BL00",
                "SNAP1_C",
                "FIN",
            ],
            "distance": 50.0,
            "path": [
                {"d": 0, "s": -1, "x": 1, "y": 1},
                {"d": 0, "s": -1, "x": 1, "y": 2},
                {"d": 2, "s": -1, "x": 4, "y": 3},
                {"d": 2, "s": -1, "x": 13, "y": 3},
                {"d": 2, "s": -1, "x": 14, "y": 3},
                {"d": 4, "s": -1, "x": 11, "y": 4},
                {"d": 6, "s": 1, "x": 12, "y": 7},
            ],
        },
    }

    data = cmd["data"]
    result = flatten_command(data)
    print(str(result))
