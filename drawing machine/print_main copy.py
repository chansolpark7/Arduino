import serial
import time

ser = serial.Serial('COM14')
# ser.open()
def main(n):
    ser.write(str(n).encode())
    for i in range(n):
        string = file.readline().rstrip()
        ser.write(string.encode())
    print('end')
    try:
        while True:
            pass
    except:
        pass
    ser.close()

if __name__ == "__main__":
    path = 'C:/Users/chans/OneDrive/python/step/movement/test.data'
    with open(path, 'rt', encoding='utf-8') as file:
        n = int(file.readline().rstrip())
        main(n)