import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
time.sleep(2)

for i in range(50):
    line = ser.readline()   # read a byte
    while(ser.in_waiting > 0):
        line = ser.readline()
    if len(line) > 5:
        x = int(line[0]) + (int(line[1]) << 8)
        y = int(line[2]) + (int(line[3]) << 8)
        z = int(line[4]) + (int(line[5]) << 8)
        print( str(x) + "," + str(y) + "," + str(z) )
    time.sleep(1)

ser.close()