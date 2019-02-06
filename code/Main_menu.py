import pygame
import time

#initializing pygame module
pygame.init()
pygame.mixer.init()

#make the window and taking dimentions of your display
display_info = pygame.display.Info()
display_size =(display_width, display_height)= (display_info.current_w, display_info.current_h)
gameDisplay = pygame.display.set_mode((display_size))

#define button dimentions
button_length = (display_width/4)
button_height = (display_height/8)

#define button orientation
start_game_button_x = (display_width/2)- (button_length + (display_width/10))
start_game_button_y = (display_height/2.5)

login_button_x = (display_width/2) + (display_width/10)
login_button_y= (display_height/2.5)

options_button_x = (display_width/2)- (button_length + (display_width/10))
options_button_y = (display_height/3)*1.75

deck_button_x = (display_width/2) + (display_width/10)
deck_button_y = (display_height/3)*1.75

exit_game_button_x = (display_width/2) - (button_length/2)
exit_game_button_y = (display_height/3)*2.25

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

bg_color = grey


#Creates the name of the window and initiates how were timing changes in the window
pygame.display.set_caption("Magic The Gathering")
clock = pygame.time.Clock()

cursor = pygame.image.load("cursor.png")
cursor = pygame.transform.scale(cursor, (200, 200))

#loads in the logo of the game and scales the image to appropriate size
logo = pygame.image.load("logo.png")
logo_width = int(display_width/2)
logo_height = int(display_height/4)
logo = pygame.transform.scale(logo, (logo_width, logo_height))


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


def cursor_pos(x,y):
    gameDisplay.blit(cursor, (x,y))

def game_loop():
    running = True
    while running:
        mx, my = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            if event.type == pygame.KEYDOWN:                

                if event.key == pygame.K_P:
                    lose() 

                if event.key == pygame.K_ESCAPE:
                    myquit()
                    
        cursor_pos(mx,my)
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
            if action == "play_vs_ai":
                game_loop()
                
            #If we clicked quit run the exit function   
            elif action == "quit":
                myquit()

            #run the options function
            elif action == "options":
                options()

            #run the login function
            elif action == "login":
                login()
                
    #Else we are not over the button so it stays as it is
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))
        
    #This will display whatever message we provided in freesansbold on the centre of the button
    smallText = pygame.font.Font("freesansbold.ttf", 40)
    textSurf, textRect = text_object(msg, smallText)
    textRect.center = ((x +(w/2)), (y + (h/2)))
    gameDisplay.blit(textSurf, textRect)
    
        


        

        
        

        
        

        
    
#This will run the initial screen you will see before you get to the game screen
def game_intro():
    in_intro = True
    while in_intro:
        (mx, my) = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                myquit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    myquit()

        #preparing background
        gameDisplay.fill(bg_color)

        #preparing logo
        gameDisplay.blit(logo, ((display_width/2 -(logo_width/2)),(display_height/15)))

        #creating buttons
        button("Fight Vs Ai",start_game_button_x, start_game_button_y, button_length, button_height, button_blue, hover_button_blue, "play_vs_ai")
        button("Quit", exit_game_button_x, exit_game_button_y, button_length, button_height, button_blue, hover_button_blue, "quit")
        button("Options",options_button_x, options_button_y, button_length, button_height, button_blue, hover_button_blue, "options")
        button("Deck Tools", deck_button_x, deck_button_y, button_length, button_height, button_blue, hover_button_blue, "deck_tools")
        button("Login",login_button_x, login_button_y, button_length, button_height, button_blue, hover_button_blue, "login")
        

        cursor_pos(mx, my)

        #printing to screen
        pygame.display.update()

def options():
    in_options = True
    while in_options:
        (mx, my) = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                myquit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    myquit()

        gameDisplay.fill(bg_color)
        
        pygame.draw.rect(gameDisplay, black, ((display_width/6) -10, (display_height/6)-10, ((display_width/3)*2)+20, ((display_height/3)*2)+20))
        pygame.draw.rect(gameDisplay, bright_red, (display_width/6, display_height/6, (display_width/3)*2, (display_height/3)*2))
        button("Change resolution",start_game_button_x, start_game_button_y, button_length, button_height, button_blue, hover_button_blue, "change resolution")
        button("Quit", exit_game_button_x, exit_game_button_y, button_length, button_height, button_blue, hover_button_blue, "quit")
        button("+",options_button_x, options_button_y, button_length, button_height, button_blue, hover_button_blue, "options")
        button("-",options_button_x, options_button_y, button_length, button_height, button_blue, hover_button_blue, "options")
        button("Background color",options_button_x, options_button_y, button_length, button_height, button_blue, hover_button_blue, "options")
        cursor_pos(mx,my)
        pygame.display.update()

def myquit():
    pygame.quit()
    quit()

game_intro()
pygame.quit()
quit()
