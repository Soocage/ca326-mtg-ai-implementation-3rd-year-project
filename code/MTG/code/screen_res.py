import pygame
pygame.init()
pygame.mixer.init()


def get_screen_res():


	display_info = pygame.display.Info()
	display_size = (display_width, display_height)= (display_info.current_w, display_info.current_h)
	return(display_size)
	
