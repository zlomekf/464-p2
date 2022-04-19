import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
time.sleep(2)

'''
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
'''
while(True):
    line = ser.readline()   # read a byte
    while(ser.in_waiting > 4):
        line = ser.readline() 
    print(len(line))
    print(line)
    if len(line) == 7:
        x = int(line[0]) | (int(line[1]) & 0x0F) << 8
        y = int(line[2]) | (int(line[3]) & 0x0F) << 8
        z = int(line[4]) | (int(line[5]) & 0x0F) << 8
        print((x,y,z))
    time.sleep(0.01)