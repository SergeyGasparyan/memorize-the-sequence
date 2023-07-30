import pygame as pg


class Button:
    def __init__(self, x, y, width, height, color=(211, 211, 211)):
        pg.init()
        self.color = color
        self.rect = pg.Rect(x, y, width, height)

    def draw(self, win, txt, font_size=50, dx=5, dy=5, color=(15, 15, 15)):
        font = pg.font.SysFont("None", font_size)
        pg.draw.rect(win, self.color, self.rect)
        text = font.render(txt, True, color)
        win.blit(text, (self.rect.x + dx, self.rect.y + dy))
