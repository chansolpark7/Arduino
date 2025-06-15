import math
pi = math.pi
# def write_xy(file, x, y):
#     file.write(f'{x} {y}\n')

# 단위 step

# circle

# path = 'C:/Users/chans/OneDrive/python/step/movement/circle.data'
# r = 100
# a = 300
# b = 300
# circle_step = 60
# with open(path, 'wt', encoding='utf-8') as file:
#     file.write(f'{circle_step*2+7}\n')
#     file.write('1\n')
#     file.write('3\n')
#     file.write(f'{a+r} {b}\n')
#     file.write('2\n')
#     for i in range(circle_step):
#         file.write('3\n')
#         file.write(f'{int(a+math.cos(i*2*pi/circle_step)*r)} {int(b+math.sin(i*2*pi/circle_step)*r)}\n')
#     file.write('1\n')
#     file.write('3\n')
#     file.write('0 0\n')

# Koch_curve

def make(S, C, W):
    string = ""
    for i in W:
        if i in C:
            string += C[i]
        else:
            string += i
    return string

path = 'C:/Users/chans/OneDrive/python/step/movement/Koch_curve.data'
step = 3
length = 13 #################
x = 100
y = 400
degree = 0
S = {"F":'move', "+":'rotation', "-":'rotation'}
C = {"F":"F+F-F+F"}
W = "F-F-F"
VALUE = {"F":length, "+":60, "-":-120}
string = W
for _ in range(step):
    string = make(S, C, string)

min_x, min_y = 1e9, 1e9
max_x, max_y = -1e9, -1e9
with open(path, 'wt', encoding='utf-8') as file:
    file.write('1\n')
    file.write('3\n')
    file.write(f'{x} {y}\n')
    file.write('2\n')
    for i in string:
        if i in S:
            if S[i] == "move":
                x += math.cos(math.radians(degree))*length
                y += math.sin(math.radians(degree))*length
                file.write('3\n')
                file.write(f'{int(x)} {int(y)}\n')
                min_x = min(min_x, int(x))
                min_y = min(min_y, int(y))
                max_x = max(max_x, int(x))
                max_y = max(max_y, int(y))
            elif S[i] == "rotation":
                degree += VALUE[i]
    file.write('1\n')
    file.write('3\n')
    file.write('0 0\n')

print(min_x, min_y, max_x, max_y)