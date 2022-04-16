import serial
import time

ser = serial.Serial('/dev/ttyACM2', 9600, timeout=5)
time.sleep(2)

for i in range(50):
    line = ser.readline()   # read a byte
    while(ser.in_waiting > 0):
        line = ser.readline() 
    if len(line) > 2:
        print(line[0])
        print(line[1])
        print(line[2])
    time.sleep(0.01)

ser.close()