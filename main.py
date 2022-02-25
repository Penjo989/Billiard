import pygame
import socket
from board import Board, ball
import time

#CONSTANTS
WIN_WIDTH = 400
WIN_HEIGHT = 2*WIN_WIDTH
"""
THANKS TO BENPRO FOR HELPING MEpygame.draw.circle(self.surface, DARK_GREEN, (0,self.size[1]/2), self.balls[0].radius*3)
"""
#colors
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
DARK_GREEN = (34, 139, 34)

def main():
    pygame.init()
    win = pygame.display.set_mode((WIN_WIDTH , WIN_HEIGHT))
    pygame.display.set_caption("Billiard")
    run = True
    mouse_status = "free"
    board = Board(win, (WIN_WIDTH , WIN_HEIGHT), DARK_GREEN)
    while run:
        interval = time.time()
        pygame.time.delay(8)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_status = "pushed"
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_status = "free"
        mouse = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_EQUALS]:
            if board.show_holes:
                board.show_holes = False
            else:
                board.show_holes = True
        if keys[pygame.K_a]:
            board.balls[15].pos = [mouse[0], mouse[1]]
        #win.fill((255, 255, 255))
        #pygame.draw.rect(win, (0, 255, 0), (x, y, width, height))
        interval = time.time() - interval
        #print(f"fps {1/interval} /sec")
        board.update(interval)
        board.display(mouse_status, mouse)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
