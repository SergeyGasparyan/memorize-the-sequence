import pygame as pg

pg.init()
font = pg.font.SysFont('None', 50)


class Button:
    def __init__(self, x, y, width, height):
        self.color = (211, 211, 211)
        self.rect = pg.Rect(x, y, width, height)

    def draw(self, win, txt):
        pg.draw.rect(win, self.color, self.rect)
        text = font.render(txt, True, (15, 15, 15))
        win.blit(text, (self.rect.x + 5, self.rect.y + 5))
