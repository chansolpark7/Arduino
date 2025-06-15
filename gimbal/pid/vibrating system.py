import pygame
import math
import threading

m = 1 # kg
k = 1 # N/m
c = 1 # Ns/m

def user_input():
    global m
    global k
    global c

    while True:
        try:
            exec(input(), globals())
            print(f'm : {m}  k : {k}  c : {c}')
        except Exception as reason:
            print(reason)

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

    x = 0
    v = 0

    pause = False

    queue = []
    max_length = size[0]
    dragging = False

    while True:
        clock.tick(60)
        pos = pygame.mouse.get_pos()
        rect_x = 100
        rect_y = 50
        x_k = 60
        spring = 20
        box_color = (0, 0, 0)
        spring_color = (80, 80, 80)
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
                    x = 0
                    v = 0
                    queue = []
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
                    v = 0
                    queue = []
        if dragging:
            x = (pos[0]-size[0]//2)/x_k
        elif not pause:
            _F = -k*x - c*v
            v += _F / m / 60
            x += v / 60

            if len(queue) < max_length:
                queue.append(x)

        spring_x = (size[0]/2+x*x_k)/spring
        spring_y = 40
        line_color = (30, 30, 30)
        screen.fill((255, 255, 255))

        # 그래프
        if len(queue) > 0:
            for j in range(len(queue)-1):
                pygame.draw.aaline(screen, (20, 20, 20), (j, size[1]//2 - queue[j]*x_k/2), (j+1, size[1]//2 - queue[j+1]*x_k/2))

        # 격자
        pygame.draw.line(screen, line_color, (size[0]//2, 0), (size[0]//2, size[1]))
        for i in range(1, int(size[0]/2/spring)+1):
            pygame.draw.line(screen, line_color, (size[0]//2-x_k*i, 0), (size[0]//2-x_k*i, size[1]))
            pygame.draw.line(screen, line_color, (size[0]//2+x_k*i, 0), (size[0]//2+x_k*i, size[1]))

        # 물체
        pygame.draw.rect(screen, box_color, (size[0]//2+x*x_k, size[1]//2-rect_y//2, rect_x, rect_y), 3)

        # 용수철
        for i in range(spring):
            pygame.draw.line(screen, spring_color, (int(spring_x*i), size[1]//2-spring_y//2), (int(spring_x*(i+0.5)), size[1]//2+spring_y//2), 2)
            pygame.draw.line(screen, spring_color, (int(spring_x*(i+0.5)), size[1]//2+spring_y//2), (int(spring_x*(i+1)), size[1]//2-spring_y//2), 2)

        mkc_text = text(fontobj, f'm : {m}kg    k : {k}N/m    c : {c}Ns/m    C : {2*(m*k)**0.5:.2f}    ζ : {c/(2*(m*k)**0.5):.2f}', (0, 0, 0))
        mkc_text.draw_bottomright((size[0]-20, size[1]-10))
        pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    size = (600, 700)
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    clock = pygame.time.Clock()

    fontobj = pygame.font.SysFont('맑은 고딕', 70)

    thread = threading.Thread(target=user_input)
    thread.daemon = True
    thread.start()

    main()