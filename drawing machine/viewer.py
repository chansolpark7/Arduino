import pygame

file_path = 'C:/Users/chans/OneDrive/python/drawing machine/img.data'
draw_path = 'C:/Users/chans/OneDrive/python/drawing machine/draw.data'

pygame.init()

with open(file_path, 'rt', encoding='utf-8') as file:
    x, y = map(int, file.readline().split())
    surface = pygame.Surface((x, y))
    for j in range(y):
        string = file.readline()
        for i in range(x):
            if string[i] == '0':
                surface.set_at((i, j), 0)
            else:
                surface.set_at((i, j), (255, 255, 255))

with open(draw_path, 'rt', encoding='utf-8') as file:
    n = int(file.readline())
    point_list = []
    for i in range(n):
        m = int(file.readline())
        point = []
        for j in range(m):
            x, y = map(int, file.readline().split())
            point.append((x, y))
        point_list.append(point)

surface2 = pygame.transform.smoothscale_by(surface, 1)
screen = pygame.display.set_mode((1000, 700))
clock = pygame.time.Clock()
for i in point_list:
    print(len(i))

index = 0
while True:
    clock.tick(60)
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                index = (index+1)%len(point_list)

    screen.fill(0)
    screen.blit(surface2, (0, 0))
    if len(point_list[index]) > 2:
        pygame.draw.lines(screen, (255, 0, 0), False, point_list[index])
    pygame.display.flip()