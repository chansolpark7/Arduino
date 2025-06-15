import pygame

MM_SCALE = True
MM_PER_STEP = 0.2

# int?

# 10 pixel == 1mm
def to_screen(pos): # step
    if MM_SCALE:
        return (int(pos[0]*MM_PER_STEP*6000/135), int(pos[1]*MM_PER_STEP*6000/135))
    else:
        return (int(pos[0]*MM_PER_STEP*600/135), int(pos[1]*MM_PER_STEP*600/135))

def to_mm(pos): # pixel
    if MM_SCALE:
        return (int(pos[0]/MM_PER_STEP*135/6000), int(pos[1]/MM_PER_STEP*135/6000))
    else:
        return (int(pos[0]/MM_PER_STEP*135/600), int(pos[1]/MM_PER_STEP*135/600))

def main():
    global MM_SCALE

    pos_list = []

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and len(pos_list) != 0:
                    pos_list.pop()
                elif event.key == pygame.K_SPACE:
                    print(pos_list)
                elif event.key == pygame.K_TAB:
                    MM_SCALE = not MM_SCALE
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(event.button, event.pos)
                if event.button == 1:
                    pos_list.append(to_mm(event.pos))

        screen.fill((255, 255, 255))
        for i in range(len(pos_list)-1):
            pygame.draw.line(screen, (0, 0, 0), to_screen(pos_list[i]), to_screen(pos_list[i+1]), 1)
        pygame.display.flip()

if __name__ == "__main__":
    pygame.init()

    size = (600, 600) # 135mm * 135mm
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)

    # path = [(5, 5), (20, 30), (55, 5)]
    # max_v = 60 # mm/s
    # max_a = 600 # mm/s^2
    # jerk = 20 # mm/s

    main()