import pygame
from collections import deque

# def is_edge(array, x, y):
#     dx = [-1, 0, 1, -1, 1, -1, 0, 1]
#     dy = [-1, -1, -1, 0, 0, 1, 1, 1]
#     for i in range(8):
#         nx = x+dx[i]
#         ny = y+dy[i]
#         if not(0<=nx<img_x and 0<=ny<img_y):
#             continue
#         if array[nx][ny] == False:
#             return True
#     return False

# def get_connection_num(array, x, y):
#     dx = [0, -1, 1, 0]
#     dy = [-1, 0, 0, 1]
#     count = 0
#     for i in range(4):
#         nx = x+dx[i]
#         ny = y+dy[i]
#         if not(0<=nx<img_x and 0<=ny<img_y):
#             continue
#         if array[nx][ny] == True:
#             count += 1
#     return count

# right 0
# down 1
# left 2
# up 3
# def find_path(array, x, y):
#     global visited
#     point = [(x, y)]
#     visited[x][y] = True
#     direction = 0
#     dx = [1, 0, -1, 0]
#     dy = [0, -1, 0, 1]
#     while True:
#         flag = False
#         for i in range(3):
#             n_direction = (direction+i-1)%4
#             nx = x+dx[n_direction]
#             ny = y+dy[n_direction]
#             if not(0<=nx<img_x and 0<=ny<img_y):
#                 continue
#             if array[nx][ny] == False:
#                 if visited[nx][ny] == True:
#                     break
#                 x, y, direction = nx, ny, n_direction
#                 flag = True
#                 visited[x][y] = True
#                 point.append((x, y))
#                 break
#         if not flag:
#             break
#     return point

def find_path(img_array, x, y):
    global visited_line

    point = [(x, y)]
    visited_line[x][y] = True
    direction = 0
    dx = [1, 0, -1, 0]
    dy = [0, -1, 0, 1]
    start_x, start_y = x, y
    while True:
        for i in range(4):
            n_direction = (direction+i-1)%4
            nx = x+dx[n_direction]
            ny = y+dy[n_direction]
            if not(0<=nx<img_x and 0<=ny<img_y):
                continue
            if img_array[nx][ny] == False:
                x, y, direction = nx, ny, n_direction
                visited_line[x][y] = True
                point.append((x, y))
                break

        if start_x == x and start_y == y:
            break
    return point

def infill(img_array, img_x, img_y, x, y):
    global visited_line
    global visited_infill

    pen_width = 4
    max_jump_dist = 2
    queue = deque((x, y))
    visited_infill[x][y] = True
    lines = [] # (y, start x, end x)
    # while queue:
    #     x, y = queue.popleft()    

def save(img_array):
    file_path = 'C:/Users/chans/OneDrive/python/drawing machine/img.data'
    with open(file_path, 'wt', encoding='utf-8') as file:
        file.write(f'{img_x} {img_y}\n')
        for j in range(img_y):
            for i in range(img_x):
                if img_array[i][j] == True:
                    file.write('1')
                else:
                    file.write('0')
            file.write('\n')

def save_draw_data(point_list):
    file_path = 'C:/Users/chans/OneDrive/python/drawing machine/draw.data'
    with open(file_path, 'wt', encoding='utf-8') as file:
        file.write(f'{len(point_list)}\n')
        for point in point_list:
            file.write(f'{len(point)}\n')
            for x, y in point:
                file.write(f'{x} {y}\n')

# w True
# b False
if __name__ == "__main__":
    pygame.init()
    img = "C:/Users/chans/OneDrive/python/drawing machine/4.png"

    surface = pygame.image.load(img)
    img_x, img_y = surface.get_size()
    img_array = [[False]*img_y for _ in range(img_x)]
    for i in range(img_x):
        for j in range(img_y):
            color = sum(surface.get_at((i, j)))/3
            if color > 150:
                img_array[i][j] = True

    # for i in range(img_x):
    #     for j in range(img_y):
    #         if img_array[i][j] == True and is_edge(img_array, i, j):
    #             edge_array[i][j] = True

    visited_line = [[False]*img_y for _ in range(img_x)]
    visited_infill = [[False]*img_y for _ in range(img_x)]
    point_list = []
    for j in range(img_y):
        for i in range(img_x):
            if img_array[i][j] == False and visited_line[i][j] == False:
                visited_line[i][j] = True
                point = find_path(img_array, i, j)
                point_list.append(point)
                # point = infill(img_array, img_x, img_y, i, j)
                # point_list.append(point)
            # if i == 0 and j == 0 and img_array[i][j] == False:
            #     if visited[0][0]:
            #         continue
            #     point = find_path(img_array, 0, 0)
            # elif i == 0 and img_array[i][j-1] != img_array[i][j]:
            #     if img_array[i][j] == False and not visited[i][j]:
            #         point = find_path(img_array, i, j)
            #     else:
            #         continue
            # elif img_array[i-1][j] != img_array[i][j]:
            #     if img_array[i][j] == False and not visited[i][j]:
            #         point = find_path(img_array, i, j)
            #     else:
            #         continue
            # else:
            #     continue

    # edge_array = [[True] * img_y for _ in range(img_x)]
    # for i in range(img_x):
    #     for j in range(img_y):
    #         if img_array[i][j] == False and not visited_line[i][j]:
    #             edge_array[i][j] = False

    # pen_width = 5
    # point = []
    # for j in range(0, img_y, pen_width):
    #     for i in range(img_x):
    #         if edge_array[i][j] == False:
    #             point.append((i, j))
    #         elif len(point) != 0:
    #             point_list.append(point)
    #             point = []

    # save(edge_array)
    # save(edge_array)
    save_draw_data(point_list)