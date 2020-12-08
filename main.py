import pygame as pg
from pygame.locals import *
from circle import Circle
from inputbox import InputBox
from button import Button

# Main settings
pg.init()
circles_amount = 0
width, height = 500, 500
screen = pg.display.set_mode((width, height))
pg.display.set_caption('Guess the circles!')
bg_color = (15, 15, 15)
clock = pg.time.Clock()

# Game settings
current_circle = 0
circles = []
pushed_numbers = []
X = set()
Y = set()


def restart_game_settings():
    global current_circle, circles, pushed_numbers, X, Y
    current_circle = 0
    circles = []
    pushed_numbers = []
    X = set()
    Y = set()
    play()


def won_the_game():
    global circles_amount
    won = True
    while won:
        screen.fill(bg_color)
        render_text('You Won!', Color('green'), 150, 100, font_size=60)

        next_level_button = Button(60, 250, 180, 43)
        next_level_button.draw(screen, 'Next Level')

        quit_button = Button(320, 250, 80, 43)
        quit_button.draw(screen, 'Quit')
        for e in pg.event.get():
            if e.type == QUIT:
                pg.quit()
                quit()
            if e.type == MOUSEBUTTONDOWN:
                if next_level_button.rect.collidepoint(e.pos):
                    circles_amount += 1
                    restart_game_settings()
                if quit_button.rect.collidepoint(e.pos):
                    pg.quit()
                    quit()
        pg.display.update()
        clock.tick(30)


def lost_the_game():
    lost = True
    while lost:
        screen.fill(bg_color)
        render_text('You Lost!', Color('red'), 150, 100, font_size=60)

        replay_button = Button(60, 250, 190, 43)
        replay_button.draw(screen, 'Play Again')
        quit_button = Button(320, 250, 80, 43)
        quit_button.draw(screen, 'Quit')
        for e in pg.event.get():
            if e.type == QUIT:
                pg.quit()
                quit()
            if e.type == MOUSEBUTTONDOWN:
                if replay_button.rect.collidepoint(e.pos):
                    lost = False
                    restart_game_settings()
                if quit_button.rect.collidepoint(e.pos):
                    pg.quit()
                    quit()
        pg.display.update()
        clock.tick(30)


def game_result():
    if current_circle != circles_amount:
        # Lost the game
        return False
    for c in circles:
        if int(c.number) != c.clicked_number:
            # Lost the game
            return False
    # Won the game
    return True


def check(pos):
    global current_circle, pushed_numbers
    for c in circles:
        if c.rect.collidepoint(pos):
            if not c.clicked:
                if pushed_numbers:
                    c.clicked_number = min(pushed_numbers)
                    pushed_numbers.remove(c.clicked_number)
                else:
                    current_circle += 1
                    c.clicked_number = current_circle
                c.clicked = True
            elif c.clicked:
                pushed_numbers.append(c.clicked_number)
                c.clicked_number = 0
                c.clicked = False
            break
    for c in circles:
        c.draw(screen)
    pg.display.flip()
    clock.tick(30)


def create_circles(n):
    for i in range(n):
        c = Circle(width, height, i + 1)
        while c.x in X and c.y in Y:
            c = Circle(width, height, i + 1)
        for j in range(c.x - 2 * c.radius, c.x + 2 * c.radius + 1):
            X.add(j)
        for j in range(c.y - 2 * c.radius, c.y + 2 * c.radius + 1):
            Y.add(j)
        circles.append(c)


def play():
    game_over = False
    drawn = False
    create_circles(circles_amount)
    while not game_over:
        screen.fill(bg_color)
        if not drawn:
            # Drawing circles
            for c in circles:
                c.draw(screen)
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
            if e.type == pg.KEYDOWN:
                if e.key == K_RETURN:
                    won = game_result()
                    if won:
                        won_the_game()
                    else:
                        lost_the_game()
            if e.type == MOUSEBUTTONDOWN:
                check(e.pos)
        clock.tick(30)


def render_text(txt, color, x, y, font_size=40):
    font = pg.font.SysFont('None', font_size)
    text = font.render(txt, True, color)
    screen.blit(text, (x, y))


def menu():
    global circles_amount
    waiting = True
    input_box = InputBox(210, 220, 40, 30)
    while waiting:
        for e in pg.event.get():
            if e.type == QUIT:
                pg.quit()
                quit()
            if e.type == pg.KEYDOWN:
                if e.key == K_RETURN:
                    circles_amount = input_box.return_text()
                    play()
            input_box.handle_event(e)
        screen.fill(bg_color)
        render_text('Enter the number of circles!', Color('dodgerblue2'), 70, 150)
        input_box.draw(screen)
        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    menu()
