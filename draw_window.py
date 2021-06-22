import pygame


def draw_window(win, track, cars, gen):
    '''This function draws the window used to display all the images.'''
    win.blit(track, (0, 0))
    for car in cars:
        car.draw(win)
    
    generation_font = pygame.font.SysFont("Arial", 70)

    text = generation_font.render("Generation: {}".format(gen), True, (255, 255, 0))
    text_rect = text.get_rect()
    text_rect.center = (1500/2, 100)
    win.blit(text, text_rect)

    pygame.display.flip()
