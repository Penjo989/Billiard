import pygame


class text:
    def __init__(self, msg, color, x, y, size, surface):
        self.font = pygame.font.SysFont(None, size)
        self.msg = msg
        self.color = color
        self.x = x
        self.y = y
        self.surface = surface
        self.size = size

    def display(self):
        self.text = self.font.render(self.msg, True, self.color)
        self.surface.blit(self.text, (self.x - 10, self.y - 10))
