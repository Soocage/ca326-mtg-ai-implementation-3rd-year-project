import pygame
import time

#initializing pygame module
pygame.init()

#make the window and taking dimentions of your display
display_info = pygame.display.Info()
display_size =(display_width, display_height)= (display_info.current_w, display_info.current_h)
gameDisplay = pygame.display.set_mode((display_size))

#define button dimentions
button_length = (display_width/5)
button_height = (display_height/8)

#define button orientation
start_game_button_x = (display_width/2)- (button_length + (display_width/10))
start_game_button_y = (display_height/3)*2

exit_game_button_x = (display_width/2) + (display_width/10)
exit_game_button_y = (display_height/3)*2

#colors
button_blue = (125,137,240)
hover_button_blue = (175, 183, 245)
grey = (205,205,205)
black = (0,0,0)
white = (255,255,255)
dark_red = (200,0,0)
dark_green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)
blue = (0,0,255)



pygame.display.set_caption("Magic The Gathering")
clock = pygame.time.Clock()

bg = pygame.image.load("Menu_background.png")
bg = pygame.transform.scale(bg, display_size)

logo = pygame.image.load("logo.png")
logo_width = int(display_width/2)
logo_height = int(display_height/4)
logo = pygame.transform.scale(logo, (logo_width, logo_height))

cardImage = pygame.image.load("cursor.png")
cardImage = pygame.transform.scale(cardImage, (200, 200))


x = (display_width * 0.4)
y = (display_height * 0.55)
mx, my = pygame.mouse.get_pos()

def text_object(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font("freesansbold.ttf", 115)
    TextSurf, TextRect = text_object(text, largeText)
    TextRect.center = ((display_width/2), (display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()

    time.sleep(2)

    game_loop()


def lose():
    message_display("goodbye")


def cursor(x,y):
    gameDisplay.blit(cardImage, (x,y))

def game_loop():
    running = True
    while running:
        mx, my = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
                

                if event.key == pygame.K_P:
                    lose()
                    
        gameDisplay.blit(bg, (0,0))
        cursor(mx,my)
        pygame.display.update()
        clock.tick(60)
        
#This will create buttons an position them
def button(msg,x,y,w,h,ic,ac,action = None):
    #Take in the co-ordinates of the mouse
    mouse = pygame.mouse.get_pos()
    #Check what buttons have been pressed by the mouse
    click = pygame.mouse.get_pressed()
    #Check if mouse position is within the boundry of the button
    if (x + w) > mouse[0] > x and (y + h) > mouse[1] > y:
        #Highlight the button with a lighter shad of blue
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            #If we clicked on play launch the game_loop
            if action == "play":
                game_loop()
            #If we clicked quit run the exit function
            elif action == "quit":
                pygame.quit()
                quit()
    #Else we are not over the button so it stays as it is
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))
    #This will display whatever message we provided in freesansbold on the centre of the button
    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_object(msg, smallText)
    textRect.center = ((x +(w/2)), (y + (h/2)))
    gameDisplay.blit(textSurf, textRect)
        

#This will run the initial screen you will see before you get to the game screen
def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()


        #preparing background
        gameDisplay.fill(grey)
        
        #preparing logo
        gameDisplay.blit(logo, ((display_width/2 -(logo_width/2)),(display_height/8)))
        
        #creating buttons
        button("start",start_game_button_x, start_game_button_y, button_length, button_height, button_blue, hover_button_blue, "play")
        button("End", exit_game_button_x, exit_game_button_y, button_length, button_height, button_blue, hover_button_blue, "quit")

        #printing to screen
        pygame.display.update()
        clock.tick(5)

game_intro()
pygame.quit()
quit()
