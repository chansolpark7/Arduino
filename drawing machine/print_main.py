import serial
import time

ser = serial.Serial('COM14')
# ser.open()
def main(n):
    print(1)
    max_command_length = 3
    command_length = 0
    count = 0
    # ser.write('down'.encode())
    try:
        while count < n:
            time.sleep(0.01) ########################################
            if command_length < max_command_length:
                string = file.readline().rstrip()
                print(count)
                ser.write(string.encode())
                count += 1
                command_length += 1
            if ser.in_waiting > 0:
                data = ser.readline().decode().strip()
                print(data)
                if data == 'complete':
                    command_length -= 1
                print('waiting end')
    except Exception as reason:
        print(reason)
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