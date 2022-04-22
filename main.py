import serial


# s = serial.Serial("/dev/serial/port1", 115200)
# s.write(b"Hello from serial port")

stringNFC=b"Reader 0: Card UID: AA 73 95 19\r\n"

s = serial.Serial('COM3')
while True:
    res = s.readline()
    print(res)
    if stringNFC == res:
        print("OK")
        s.write(b"OK\n")
