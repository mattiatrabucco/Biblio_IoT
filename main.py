import serial


# s = serial.Serial("/dev/serial/port1", 115200)
# s.write(b"Hello from serial port")

stringNFC=b"AA 73 95 19"

#s = serial.Serial('COM3')
s = serial.Serial('/dev/tty.usbmodem101')
while True:
    res = s.readline()
    print(res)
    if b"Card UID" in res:
        if stringNFC in res:
            print("OK")
            s.write(b"OK\n")
        else:
            print("ERROR: non puoi entrare")
            s.write(b"ERROR: non puoi entrare\n")
