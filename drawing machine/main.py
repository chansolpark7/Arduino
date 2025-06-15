import serial
import time

ser = serial.Serial('COM5')

def test():
    try:
        while True:
            while ser.in_waiting > 0:
                data = ser.readline().decode('ascii').strip()
                print('>', data)
            string = input('data : ')+'\n'
            ser.write(string.encode('ascii'))
    except:
        pass
    ser.close()

def control():
    is_waiting = True
    time.sleep(3)
    try:
        while True:
            while ser.in_waiting > 0:
                data = ser.readline().decode('ascii').strip()
                print('>', data)
                if data == 'complete':
                    is_waiting = True
            if is_waiting:
                is_waiting = False
                string = input('data : ')+'\n'
                ser.write(string.encode('ascii'))
    except:
        pass
    ser.close()

def auto():
    file_path = "C:/Users/chans/OneDrive/python/drawing machine/movement/Koch_curve.data"
    file = open(file_path, 'rt', encoding='utf-8')

    input('start?')
    time.sleep(5)

    count = 0
    complete_count = 0
    n = int(file.readline())
    max_stack_size = 10
    stack_size = 0
    try:
        while count < n:
            if stack_size < max_stack_size:
                string = file.readline()
                data = string.encode('ascii')
                # print('-----', data)
                # input('>')
                ser.write(data)
                stack_size += 1
                count += 1
            if ser.in_waiting > 0:
                data = ser.readline().decode('ascii').strip()
                if data == 'complete':
                    stack_size -= 1
                    complete_count += 1
                    print(f'{complete_count/n*100:.2f}%')
                else:
                    print('>', data)
    except Exception as reason:
        print(reason)
    ser.close()

# auto()
control()
# test()