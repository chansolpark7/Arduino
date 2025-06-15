MM_PER_STEP = 0.2

def loose(path, max_v, max_a, jerk): # step, mm/s, mm/s^2, mm/s
    x, y = path[0]
    t = 0
    timestamp = [(t, x, y)] # time, x, y
    for i in range(len(path)-1):
        x1, y1 = path[i]
        x2, y2 = path[i+1]
        dx = abs(x2-x1)
        dy = abs(y2-y1)
        dir_x = 1 if x2 >= x1 else -1
        dir_y = 1 if y2 >= y1 else -1

        # total_t = max(dx, dy)/max_v # step*s/mm
        # total_t = max(dx, dy)*0.2/max_v # s
        # total_t = max(dx, dy)*MM_PER_STEP*1000/(jerk/2) # ms
        total_t = int((dx**2 + dy**2)**0.5)*MM_PER_STEP*1000/(jerk)
        i, j = 0, 0
        while i < dx or j < dy:
            if (i+1)*dy <= (j+1)*dx:
                i += 1
                x += dir_x
                if (i+1)*dy == (j+1)*dx:
                    j += 1
                    y += dir_y
                timestamp.append((t + i*total_t/dx, x, y))
            else:
                j += 1
                y += dir_y
                timestamp.append((t + j*total_t/dy, x, y))
        t += total_t

    return timestamp

def acceleration(path, max_v, max_a, jerk): # step, mm/s, mm/s^2, mm/s
    x, y = path[0]
    t = 0
    timestamp = [(t, x, y)] # time, x, y
    for i in range(len(path)-1):
        x1, y1 = path[i]
        x2, y2 = path[i+1]
        dx = abs(x2-x1)
        dy = abs(y2-y1)
        dir_x = 1 if x2 >= x1 else -1
        dir_y = 1 if y2 >= y1 else -1

        # total_t = max(dx, dy)/max_v # step*s/mm
        # total_t = max(dx, dy)*0.2/max_v # s
        total_t = max(dx, dy)*MM_PER_STEP*1000/max_v#(jerk/2) # ms
        i, j = 0, 0
        while i < dx or j < dy:
            if (i+1)*dy <= (j+1)*dx:
                i += 1
                x += dir_x
                if (i+1)*dy == (j+1)*dx:
                    j += 1
                    y += dir_y
                timestamp.append((t + i*total_t/dx, x, y))
            else:
                j += 1
                y += dir_y
                timestamp.append((t + j*total_t/dy, x, y))
        t += total_t

    return timestamp