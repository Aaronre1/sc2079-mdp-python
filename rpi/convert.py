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
