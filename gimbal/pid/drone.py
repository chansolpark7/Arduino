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

    margin = 50
    y = 0
    v = 0
    a = 0
    Si = 0
    dd = 0

    pause = False
    show_y = True

    # Kp = 30
    # Ki = 0.5
    # Kd = 800

    Kp = 30
    Ki = 0.1
    Kd = 800

    Kp = 30
    Ki = 0.1
    Kd = 800

    # 100 pixels 1ms/s^2
    force_scale = 1
    # 100 pixels = 1m
    y_scale = 1

    r = 1-1/30

    queue = []
    max_length = size[0]
    color = ((255, 0, 0), (0, 255, 0), (0, 0, 255),  (127, 127, 0), (0, 127, 127))
    show = [True, True, True, True, True]
    name = ['p', 'i', 'd', 'a', 'v']
    t = []
    for i in range(5):
        t.append(text(fontobj, name[i], color[i]))

    while True:
        clock.tick(60)
        pos = pygame.mouse.get_pos()
        target = ((size[1]-pos[1]-margin)/100)/y_scale
        key = pygame.key.get_pressed()
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
                elif event.key == pygame.K_BACKSPACE:
                    show_y = not show_y
                elif event.key == pygame.K_ESCAPE:
                    y = 0
                    v = 0
                    a = 0
                    Si = 0
                    dd = 0
                    queue = []
                elif pygame.K_1 <= event.key <= pygame.K_5:
                    show[event.key-pygame.K_1] = not show[event.key-pygame.K_1]
            elif event.type == pygame.MOUSEWHEEL:
                if key[pygame.K_LCTRL]:
                    y_scale *= r**-event.y
                    print('y scale :', y_scale)
                else:
                    force_scale *= r**-event.y
                    print('force scale :', force_scale)
        if not pause:
            error = target-y
            Si += error

            if y <= 0:
                y = 0
                v = max(v, 0)
                a = max(Kp*error+Ki*Si+Kd*dd-9.8, 0)
            else:
                a = Kp*error+Ki*Si+Kd*dd-9.8

            v += a / 60
            dd = -v / 60
            y -= dd

            queue.append((Kp*error, Ki*Si, Kd*dd, Kp*error+Ki*Si+Kd*dd-9.8, v))
            while len(queue) > max_length:
                queue.pop(0)

        screen.fill((255, 255, 255))

        # force
        pygame.draw.line(screen, (0, 0, 0), (0, pos[1]), (size[0], pos[1]), 3)
        y_t = text(scalefontobj, f'{target:.2f}m', (0, 0, 0))
        y_t.draw_bottomright((size[0]-10, pos[1]))
        for i in range(-size[1]//70-1, size[1]//70+2):
            scale = 10**-math.floor(math.log10(force_scale)+0.5)
            pygame.draw.aaline(screen, (10, 10, 10) if i%5==0 else (180, 180, 180), (0, size[1]//2 + 100*scale*i*force_scale), (size[0],size[1]//2 + 100*scale*i*force_scale))
            scale_t = text(scalefontobj, f'{-i} X 10^{-math.floor(math.log10(force_scale)+0.5)+2} m/s^2', (180, 180, 180))
            scale_t.draw_bottomleft((10, size[1]//2 + 100*scale*i*force_scale))

        # y
        pygame.draw.line(screen, (10, 10, 10), (0, size[1] - margin), (size[0], size[1] - margin), 1)
        scale_t = text(scalefontobj, f'0 m', (10, 10, 10))
        scale_t.draw_bottomright((min(size[0]-10, size[0]//2+100), size[1] - margin))
        if show_y:
            for i in range(1, size[1]//20+2):
                scale = 10**-math.floor(math.log10(y_scale)+0.5)
                pygame.draw.line(screen, (10, 10, 10), (size[0]//2-100, size[1] - 100*scale*i*y_scale - margin), (size[0]//2+100, size[1] - 100*scale*i*y_scale - margin), 1)
                scale_t = text(scalefontobj, f'{i} X 10^{-math.floor(math.log10(y_scale)+0.5)} m', (10, 10, 10))
                scale_t.draw_bottomright((min(size[0]-10, size[0]//2+100), size[1] - 100*scale*i*y_scale - margin))

        if len(queue) > 0:
            for i in range(5):
                if show[i]:
                    for j in range(len(queue)-1):
                        pygame.draw.aaline(screen, color[i], (j, size[1]//2 - queue[j][i]*force_scale), (j+1, size[1]//2 - queue[j+1][i]*force_scale))
                    t[i].draw_bottomright((max(20, len(queue)-10), size[1]//2 - queue[-1][i]*force_scale))

        pygame.draw.circle(screen, 0, (size[0]//2, size[1]-y*100*y_scale-margin), max(1, 10*y_scale))
        pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    size = (600, 700)
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    pygame.display.set_caption("PID")
    clock = pygame.time.Clock()

    fontobj = pygame.font.SysFont('맑은 고딕', 25)
    scalefontobj = pygame.font.SysFont('맑은 고딕', 18)

    main()