import pygame as pg


pg.init()
color_inactive = pg.Color('lightskyblue3')
color_active = pg.Color('dodgerblue2')
font = pg.font.Font(None, 32)


class InputBox:
    def __init__(self, x, y, w, h):
        self.rect = pg.Rect(x, y, w, h)
        self.color = color_inactive
        self.text = ''
        self.txt_surface = font.render(self.text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = color_active if self.active else color_inactive
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = font.render(self.text, True, self.color)

    def draw(self, win):
        # Blit the text.
        win.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pg.draw.rect(win, self.color, self.rect, 2)

    def return_text(self):
        return int(self.text)
