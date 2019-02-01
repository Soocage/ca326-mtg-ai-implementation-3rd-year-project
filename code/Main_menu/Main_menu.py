import pygame

pygame.init()

display_info = pygame.display.Info()
display_size =(display_width, display_height)= (display_info.current_w, display_info.current_h)
gameDisplay = pygame.display.set_mode((display_size))
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)



pygame.display.set_caption("Magic The Gathering")
clock = pygame.time.Clock()

bg = pygame.image.load("Menu_background.png")
bg = pygame.transform.scale(bg, display_size)
cardImage = pygame.image.load("cursor.png")
cardImage = pygame.transform.scale(cardImage, (200, 200))


x = (display_width * 0.4)
y = (display_height * 0.55)
mx, my = pygame.mouse.get_pos()

running = True


def card(x,y):
    gameDisplay.blit(cardImage, (x,y))


while running:
    mx, my = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
                
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

    gameDisplay.blit(bg, (0,0))
    card(mx,my)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
