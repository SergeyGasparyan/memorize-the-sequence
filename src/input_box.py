import pygame as pg


class InputBox:
    def __init__(self, x, y, w, h):
        pg.init()
        self.color_inactive = pg.Color("lightskyblue3")
        self.color_active = pg.Color("dodgerblue2")
        self.rect = pg.Rect(x, y, w, h)
        self.font = pg.font.Font(None, 32)
        self.color = self.color_inactive
        self.num_circle_text = ""
        self.txt_surface = self.font.render(self.num_circle_text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # if the user clicked on the input_box rect
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            
            # change the current color of the input box
            self.color = self.color_active if self.active else self.color_inactive
        elif event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.num_circle_text = ""
                elif event.key == pg.K_BACKSPACE:
                    self.num_circle_text = self.num_circle_text[:-1]
                else:
                    self.num_circle_text += event.unicode
                
                # re-render the text
                self.txt_surface = self.font.render(self.num_circle_text, True, self.color)

    def draw(self, win):
        win.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pg.draw.rect(win, self.color, self.rect, 2)

    def return_text(self):
        return int(self.num_circle_text)
