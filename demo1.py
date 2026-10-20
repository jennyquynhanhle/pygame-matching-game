import pygame

pygame.init()

#game variables and constants
WIDTH = 600
HEIGHT = 600
white = (255, 255, 255)
black = (0, 0, 0)

fps = 60
timer = pygame.time.Clock()

#create screen
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("THE MATCHING GAME!!!")

running = True
while running:
    timer.tick(fps)
    screen.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
pygame.quit()