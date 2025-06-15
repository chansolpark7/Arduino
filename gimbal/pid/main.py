import pygame
import math

class text:
    def __init__(self, font, text, color):
        self.text = text
        self.surface = font.render(str(text), True, color)
        self.color = color
    
    def draw_bottomleft(self, pos):
        rect = self.surface.get_rect()
        rect.bottomleft = pos
        screen.blit(self.surface, rect)
    
    def draw_bottomright(self, pos):
        rect = self.surface.get_rect()
        rect.bottomright = pos
        screen.blit(self.surface, rect)

    def collidepoint(self, pos, mouse_pos):
        rect = self.surface.get_rect()
        rect.center = pos
        return rect.collidepoint(mouse_pos)

def main():
    global size

    min_y = 50
    y = min_y
    v = 0
    a = 0
    Si = 0
    dd = 0

    pause = False

    Kp = 3 # 1.4
    Ki = 0.0005 # 0.0001
    Kd = 150 # -10
    
    # Kp = 3 # 1.4
    # Ki = 0.0 # 0.0001
    # Kd = 150 # -10

    queue = []
    max_length = size[0]
    k = 1
    color = ((255, 0, 0), (0, 255, 0), (0, 0, 255),  (127, 127, 0), (0, 127, 127))
    show = [True, True, True, True, True]
    name = ['p', 'i', 'd', 'a', 'v']
    t = []
    for i in range(5):
        t.append(text(fontobj, name[i], color[i]))

    while True:
        clock.tick(60)
        pos = pygame.mouse.get_pos()
        target_y = size[1] - pos[1]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.VIDEORESIZE:
                size = event.size
                max_length = size[0]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause = not pause
                elif event.key == pygame.K_ESCAPE:
                    y = min_y
                    v = 0
                    a = 0
                    Si = 0
                    dd = 0
                    queue = []
                elif pygame.K_1 <= event.key <= pygame.K_5:
                    show[event.key-pygame.K_1] = not show[event.key-pygame.K_1]
            elif event.type == pygame.MOUSEWHEEL:
                k *= (1-1/30)**-event.y
                print(k)
        if not pause:
            dy = target_y-y
            Si += dy

            if y <= min_y:
                y = min_y
                v = max(v, 0)
                a = max(Kp*dy+Ki*Si+Kd*dd-9.8, 0)
            else:
                a = Kp*dy+Ki*Si+Kd*dd-9.8

            v += a / 60
            dd = -v / 60
            y -= dd

            queue.append((Kp*dy, Ki*Si, Kd*dd, Kp*dy+Ki*Si+Kd*dd-9.8, v))
            while len(queue) > max_length:
                queue.pop(0)

        screen.fill((255, 255, 255))
        pygame.draw.line(screen, (0, 0, 0), (0, pos[1]), (size[0], pos[1]), 3)
        pygame.draw.line(screen, (0, 0, 0), (0, size[1]-min_y), (size[0], size[1]-min_y), 3)
        if len(queue) > 0:
            for i in range(5):
                if show[i]:
                    for j in range(len(queue)-1):
                        pygame.draw.aaline(screen, color[i], (j, size[1]//2 - queue[j][i]*k), (j+1, size[1]//2 - queue[j+1][i]*k))
                    t[i].draw_bottomright((max(20, len(queue)-10), size[1]//2 - queue[-1][i]*k))
        for i in range(-size[1]//70-1, size[1]//70+2):
            scale = 10**-math.floor(math.log10(k)+0.5)
            pygame.draw.aaline(screen, (10, 10, 10) if i%5==0 else (200, 200, 200), (0, size[1]//2 + 100*scale*i*k), (size[0],size[1]//2 + 100*scale*i*k), 1)
            scale_t = text(scalefontobj, f'{-i} X 10^{-math.floor(math.log10(k)+0.5)}', (200, 200, 200))
            scale_t.draw_bottomleft((10, size[1]//2 + 100*scale*i*k))
        pygame.draw.circle(screen, 0, (size[0]//2, size[1]-y), 10)
        pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    size = (600, 700)
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    pygame.display.set_caption("PID")
    clock = pygame.time.Clock()

    fontobj = pygame.font.SysFont('맑은 고딕', 25)
    scalefontobj = pygame.font.SysFont('맑은 고딕', 15)

    main()