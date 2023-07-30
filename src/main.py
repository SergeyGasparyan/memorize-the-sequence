import pygame as pg
from pygame.locals import MOUSEBUTTONDOWN, Color, MOUSEBUTTONDOWN, QUIT, K_RETURN, MOUSEBUTTONDOWN
from button import Button
from circle import Circle
from input_box import InputBox


class Game:
    def __init__(self, fps=30, width=500, height=500):
        # main settings
        pg.init()
        pg.display.set_caption("Memorize the sequence")
        
        self.fps = fps
        self.num_circles = 0
        self.width, self.height = width, height
        self.screen = pg.display.set_mode((width, height))
        self.bg_color = (15, 15, 15)
        self.clock = pg.time.Clock()

        # Game settings
        self.circles = []
        self.current_circle = 0
        self.pushed_numbers = []
        self.X = set()
        self.Y = set()

    def restart_game_settings(self):
        self.circles = []
        self.current_circle = 0
        self.pushed_numbers = []
        self.X = set()
        self.Y = set()
        
        self.play()

    def win_screen(self):
        next_level_button = Button(81, 251, 178, 41, self.bg_color)
        quit_button = Button(331, 251, 78, 41, self.bg_color)

        while True:
            self.screen.fill(self.bg_color)
            self.render_text("You Won!", Color("green"), 150, 100, font_size=60)

            next_level_button.draw(self.screen, "Next Level", color=Color("dodgerblue2"))
            quit_button.draw(self.screen, "Quit", color=Color("dodgerblue2"))

            for e in pg.event.get():
                if e.type == QUIT:
                    pg.quit()
                    quit()
                elif e.type == MOUSEBUTTONDOWN:
                    if next_level_button.rect.collidepoint(e.pos):
                        self.num_circles += 1
                        self.restart_game_settings()
                    elif quit_button.rect.collidepoint(e.pos):
                        pg.quit()
                        quit()

            pg.display.update()
            self.clock.tick(self.fps)

    def lose_screen(self):
        replay_button = Button(60, 250, 190, 43, self.bg_color)
        quit_button = Button(320, 250, 80, 43, self.bg_color)

        while True:
            self.screen.fill(self.bg_color)
            self.render_text("You Lost!", Color("red"), 150, 100, font_size=60)

            replay_button.draw(self.screen, "Play Again", color=Color("dodgerblue2"))
            quit_button.draw(self.screen, "Quit", color=Color("dodgerblue2"))
            
            for e in pg.event.get():
                if e.type == QUIT:
                    pg.quit()
                    quit()
                elif e.type == MOUSEBUTTONDOWN:
                    if replay_button.rect.collidepoint(e.pos):
                        self.restart_game_settings()
                    elif quit_button.rect.collidepoint(e.pos):
                        pg.quit()
                        quit()

            pg.display.update()
            self.clock.tick(self.fps)

    def game_result(self):
        # lost the game
        if self.current_circle != self.num_circles:
            return False
        
        for c in self.circles:
            if int(c.number) != c.clicked_number:
                # lost the game
                return False
            
        # won the game
        return True
    
    def check(self, pos):
        for c in self.circles:
            if c.rect.collidepoint(pos):
                if not c.clicked:
                    if self.pushed_numbers:
                        c.clicked_number = min(self.pushed_numbers)
                        self.pushed_numbers.remove(c.clicked_number)
                    else:
                        self.current_circle += 1
                        c.clicked_number = self.current_circle
                    c.clicked = True
                elif c.clicked:
                    self.pushed_numbers.append(c.clicked_number)
                    c.clicked_number = 0
                    c.clicked = False
                break

        for c in self.circles:
            c.draw(self.screen)

        pg.display.flip()
        self.clock.tick(self.fps)

    def create_circles(self, n):
        for i in range(n):
            c = Circle(self.width, self.height, i + 1)

            while c.x in self.X and c.y in self.Y:
                c = Circle(self.width, self.height, i + 1)

            for j in range(c.x - 2 * c.radius, c.x + 2 * c.radius + 1):
                self.X.add(j)

            for j in range(c.y - 2 * c.radius, c.y + 2 * c.radius + 1):
                self.Y.add(j)
            
            self.circles.append(c)

    def play(self):
        game_over = False
        drawn = False

        self.create_circles(self.num_circles)

        while not game_over:
            self.screen.fill(self.bg_color)
            if not drawn:
                # Drawing circles
                for c in self.circles:
                    c.draw(self.screen)

                    pg.display.update()
                    pg.time.wait(2000)
                
                pg.display.update()
                drawn = True
          
            for e in pg.event.get():
                if e.type == QUIT:
                    game_over = True
                    pg.quit()
                    quit()
                # When finished clicking
                elif e.type == pg.KEYDOWN:
                    if e.key == K_RETURN:
                        won = self.game_result()
                        if won:
                            self.win_screen()
                        else:
                            self.lose_screen()
                elif e.type == MOUSEBUTTONDOWN:
                    self.check(e.pos)

            self.clock.tick(self.fps)

    def render_text(self, txt, color, x, y, font_size=40):
        font = pg.font.SysFont("None", font_size)
        text = font.render(txt, True, color)
        self.screen.blit(text, (x, y))

    def menu(self):
        waiting = True
        input_box = InputBox(185, 240, 40, 32)

        enter_button_out = Button(230, 240, 82, 32, Color('lightskyblue3'))
        enter_button_in = Button(231, 241, 80, 30, self.bg_color)

        while waiting:
            for e in pg.event.get():
                if e.type == QUIT:
                    pg.quit()
                    quit()
                elif e.type == pg.KEYDOWN:
                    if e.key == K_RETURN:
                        self.num_circles = input_box.return_text()
                        self.play()
                elif e.type == MOUSEBUTTONDOWN:
                    if enter_button_in.rect.collidepoint(e.pos) or enter_button_out.rect.collidepoint(e.pos):
                        self.num_circles = input_box.return_text()
                        self.play()
                
                input_box.handle_event(e)
            
            self.screen.fill(self.bg_color)
            self.render_text("Enter the number of circles!", Color("dodgerblue2"), x=70, y=120)
            enter_button_out.draw(self.screen, "", font_size=40, dx=3, dy=3, color=Color("dodgerblue2"))
            enter_button_in.draw(self.screen, "Enter", font_size=40, dx=3, dy=3, color=Color("dodgerblue2"))
            input_box.draw(self.screen)
            
            pg.display.flip()
            self.clock.tick(self.fps)


if __name__ == "__main__":
    Game(fps=30, width=500, height=500).menu()
