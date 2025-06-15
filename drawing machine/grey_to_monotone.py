import pygame

# 210 mm x 297 mm
# no micro step : 1050 step x 1485 step

def randint(n, maximum):
    n = (n<<13) ^ n
    nn = (n * (n * n * 60493 + 19990303) + 1376312589) & 0x7fffffff
    return nn % maximum

def random(n):
    return 1 - randint(n, 0x80000000) / 0x40000000

def transform_grey_img_1(img, img_size, layer_num):
    filling_layer = [False]*(layer_num)
    filling_layer[0] = True
    filling_order = [0]*layer_num
    for i in range(1, layer_num):
        longest_blank_index = 0
        longest_blank_length = 0
        index = 0
        for j in range(layer_num):
            if filling_layer[j] == True:
                if j-index > longest_blank_length:
                    longest_blank_index = index
                    longest_blank_length = j-index
                index = j+1
        if layer_num-index > longest_blank_length:
            longest_blank_index = index
            longest_blank_length = layer_num-index

        index = longest_blank_index+(longest_blank_length-1)//2
        filling_layer[index] = True
        filling_order[index] = i

    transformed_img = pygame.Surface(img_size)
    transformed_img.fill((255, 255, 255))
    for x in range(img_size[0]):
        for y in range(img_size[1] // layer_num):
            color = 0
            for layer in range(layer_num):
                r, g, b = img.get_at((x, y*layer_num+layer))[:3]
                color += 0.2126*r + 0.7152*g + 0.0722*b
            color = max(min(int(color) // layer_num, 255), 0)
            level = min((255-color) // (255 // (layer_num+1)), layer_num)
            for layer in range(level):
                transformed_img.set_at((x, y*layer_num+filling_order[layer]), (0, 0, 0))
    
    return transformed_img

def transform_grey_img_2(img, img_size, layer_num, chunk_length):
    filling_layer = [False]*(layer_num)
    filling_layer[0] = True
    filling_order = [0]*layer_num
    for i in range(1, layer_num):
        longest_blank_index = 0
        longest_blank_length = 0
        index = 0
        for j in range(layer_num):
            if filling_layer[j] == True:
                if j-index > longest_blank_length:
                    longest_blank_index = index
                    longest_blank_length = j-index
                index = j+1
        if layer_num-index > longest_blank_length:
            longest_blank_index = index
            longest_blank_length = layer_num-index

        index = longest_blank_index+(longest_blank_length-1)//2
        filling_layer[index] = True
        filling_order[index] = i

    transformed_img = pygame.Surface(img_size)
    transformed_img.fill((255, 255, 255))
    for x in range(img_size[0]):
        for y in range(img_size[1] // layer_num):
            color = 0
            for layer in range(layer_num):
                r, g, b = img.get_at((x, y*layer_num+layer))[:3]
                color += 0.2126*r + 0.7152*g + 0.0722*b
            color = max(min(int(color) // layer_num, 255), 0)
            level = min((255-color) // (255 // (layer_num+1)), layer_num)
            box_num = int(chunk_length * layer_num * (255-color) / 255) - (level-1) * chunk_length
            for layer in range(level-1):
                transformed_img.set_at((x, y*layer_num+filling_order[layer]), (0, 0, 0))

            # shift = 
            if x % chunk_length < box_num:
                transformed_img.set_at((x, y*layer_num+filling_order[level-1]), (0, 0, 0))
    
    return transformed_img

def main():
    zooming = 0.5
    mode = 0 # 0 : original, 1 : transformed
    x, y = 0, 0 # view x, y
    speed = 10

    # transformed_img1 = transform_grey_img_1(img, img_size, 4)
    # transformed_img2 = transform_grey_img_1(img, img_size, 6)
    transformed_img3 = transform_grey_img_1(img, img_size, 8)
    transformed_img4 = transform_grey_img_1(img, img_size, 10)
    transformed_img1 = transform_grey_img_2(img, img_size, 8, 2)
    transformed_img2 = transform_grey_img_2(img, img_size, 8, 4)
    # transformed_img3 = transform_grey_img_2(img, img_size, 8, 6)
    # transformed_img4 = transform_grey_img_2(img, img_size, 8, 10)

    while True:
        clock.tick(30)
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT]:
            x += speed / zooming
        if key[pygame.K_LEFT]:
            x -= speed / zooming
        if key[pygame.K_UP]:
            y -= speed / zooming
        if key[pygame.K_DOWN]:
            y += speed / zooming
        
        x = min(max(x, -img_size[0]/2), img_size[0]/2)
        y = min(max(y, -img_size[1]/2), img_size[1]/2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    mode = (mode+1)%5
            elif event.type == pygame.MOUSEWHEEL:
                zooming = min(max(zooming * (1.05 ** event.y), 0.05), 1.5)
                print(zooming)
    
        screen.fill((255, 255, 255))
        if mode == 0:
            screen.blit(pygame.transform.smoothscale_by(img, zooming), (screen_size[0]/2 - zooming * (img_size[0]/2 + x), screen_size[1]/2 - zooming * (img_size[1]/2 + y)))
        elif mode == 1:
            screen.blit(pygame.transform.smoothscale_by(transformed_img1, zooming), (screen_size[0]/2 - zooming * (img_size[0]/2 + x), screen_size[1]/2 - zooming * (img_size[1]/2 + y)))
        elif mode == 2:
            screen.blit(pygame.transform.smoothscale_by(transformed_img2, zooming), (screen_size[0]/2 - zooming * (img_size[0]/2 + x), screen_size[1]/2 - zooming * (img_size[1]/2 + y)))
        elif mode == 3:
            screen.blit(pygame.transform.smoothscale_by(transformed_img3, zooming), (screen_size[0]/2 - zooming * (img_size[0]/2 + x), screen_size[1]/2 - zooming * (img_size[1]/2 + y)))
        elif mode == 4:
            screen.blit(pygame.transform.smoothscale_by(transformed_img4, zooming), (screen_size[0]/2 - zooming * (img_size[0]/2 + x), screen_size[1]/2 - zooming * (img_size[1]/2 + y)))

        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    img_path = "C:/Users/chans/OneDrive/python/drawing machine/10.jpg"
    img = pygame.image.load(img_path).convert(24, 0)
    img_size = img.get_size()
    print(img_size)

    clock = pygame.time.Clock()

    screen_size = (800, 600)
    screen = pygame.display.set_mode(screen_size)

    main()