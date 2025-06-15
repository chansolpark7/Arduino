import pygame
import time

import algorithm

MM_SCALE = True
MM_PER_STEP = algorithm.MM_PER_STEP

def to_screen(pos): # step
    if MM_SCALE:
        return (int(pos[0]*MM_PER_STEP*6000/135), int(pos[1]*MM_PER_STEP*6000/135))
    else:
        return (int(pos[0]*MM_PER_STEP*600/135), int(pos[1]*MM_PER_STEP*600/135))

def main(timestamp):
    global MM_SCALE

    t = time.time()
    index = 0
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # index = (index+1)%len(timestamp)
                    t = time.time()
                    index = 0
                    pass
                elif event.key == pygame.K_TAB:
                    MM_SCALE = not MM_SCALE
        screen.fill((255, 255, 255))
        for i in range(len(path)-1):
            pygame.draw.line(screen, (0, 0, 0), to_screen(path[i]), to_screen(path[i+1]), 1)
        while True:
            if index < len(timestamp)-1 and (time.time()-t)*1000 > timestamp[index][0]:
                index += 1
            else:
                break
        pygame.draw.circle(screen, (255, 0, 0), to_screen(timestamp[index][1:]), 2)
        pygame.display.flip()

if __name__ == "__main__":
    pygame.init()

    size = (600, 600) # 135mm * 135mm
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)

    # path = [(5, 5), (20, 30), (55, 5)] # step
    path = [(110, 61), (336, 30), (502, 60), (585, 189), (631, 365), (605, 470), (524, 553), (415, 570), (227, 554), (156, 487), (73, 267), (126, 171), (259, 108), (421, 124), (515, 249), (520, 399), (346, 498), (211, 421), (190, 285), (250, 196), (361, 192), (447, 301), (364, 379), (275, 326), (281, 274), (367, 311), (427, 421), (496, 558), (538, 636), (605, 595), (651, 450), (644, 333), (628, 258), (627, 141), (610, 87), (565, 49), (505, 25), (434, 16), (297, 28), (149, 39), (66, 46), (15, 148), (10, 298), (33, 432), (33, 532), (77, 600), (240, 604), (411, 610), (537, 605), (597, 583)]
    max_v = 60 # mm/s
    max_a = 600 # mm/s^2
    jerk = 20 # mm/s

    timestamp = algorithm.loose(path, max_v, max_a, jerk)

    print(timestamp)
    print(len(timestamp))
    main(timestamp)