import random

max_rpm = 100

# a, b 0일 경우 예외 처리

# a = random.randint(5000, 10000)
# b = random.randint(5000, 10000)
a = 1200
b = 7

i = 0
j = 0
# if a > b:
#     a_rpm = max_rpm
#     b_rpm = max_rpm*b/a
# else:
#     a_rpm = max_rpm*a/b
#     b_rpm = max_rpm
a_rpm = max_rpm*a//max(a, b)
b_rpm = max_rpm*b//max(a, b)

print(a_rpm, b_rpm)

# a_delay = 150000//a_rpm
# b_delay = 150000//b_rpm

# set a, b low
while i<a*2 or j<b*2:
    now = max(i*150000*max(a, b)//(max_rpm*a), j*150000*max(a, b)//max_rpm*b)
    if (i+1)*b < (j+1)*a:
        next = (i+1)*150000*max(a, b)//(max_rpm*a)
        #delay next-now
        i += 1
        print('i', next)
    elif (i+1)*b == (j+1)*a:
        next = (i+1)*150000*max(a, b)//(max_rpm*a)
        i += 1
        j += 1
        print('i j', next)
    else:
        next = (j+1)*150000//b_rpm
        j += 1
        print('j', next)

if i != a*2 or j != b*2:
    print(a, b)