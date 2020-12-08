import random as rd
import pygame as pg


class Circle:
    def __init__(self, width, height, number):
        pg.init()
        self.font = pg.font.SysFont('None', 40)
        self.radius = 20
        self.color = pg.Color('white')
        self.number = str(number)
        self.clicked = False
        self.clicked_number = 0
        self.x = rd.randint(self.radius, width - self.radius)
        self.y = rd.randint(self.radius, height - self.radius)
        self.rect = pg.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)

    def draw(self, win):
        pg.draw.circle(win, self.color, (self.x, self.y), self.radius)
        if not self.clicked:
            text = self.font.render('?', True, pg.Color('black'))
            win.blit(text, (self.x - 9, self.y - 12))
        else:
            text = self.font.render(str(self.clicked_number), True, pg.Color('black'))
            win.blit(text, (self.x - 8, self.y - 12))

