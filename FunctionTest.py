def openPacketStream(APPId : int, priority, SCLCKStart : int, SCLCKEnd : int):
    with open("0x54e.bin", "rb") as f:
        contents = f.readlines()

f = open("0x54e.bin", "rb")

print(f)