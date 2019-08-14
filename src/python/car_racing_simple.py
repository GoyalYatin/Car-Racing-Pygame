import pygame as pg
import random

pg.init()

# crash_sound = pg.mixer.Sound("crash.wav")

white = (255, 255, 255)
black = (0, 0, 0)
red = (155, 0, 0)
green = (0, 155, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)

display_width = 800
display_height = 600
# define surface as gameDisplay
gameDisplay = pg.display.set_mode((display_width, display_height))
# set title of the game window
pg.display.set_caption("Car Racing")

# set icon
icon = pg.image.load('../resources/car.png')
pg.display.set_icon(icon)  # size is 32x32

# intialize frames per second
clock = pg.time.Clock()

FPS = 60
pause = False

small_font = pg.font.SysFont("comicsansms", 25)
med_font = pg.font.SysFont("comicsansms", 50)
large_font = pg.font.SysFont("comicsansms", 75)

car_img = pg.image.load("../resources/car.png")
car_width = 60


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pg.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()         
    else:
        pg.draw.rect(gameDisplay, ic, (x, y, w, h))
    smallText = pg.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)


def game_intro():
    """
    Welcome Window or entry to the game
    """
    intro = True

    while intro:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        gameDisplay.fill(white)
        largeText = pg.font.SysFont("comicsansms", 115)
        TextSurf, TextRect = text_objects("Car Race", largeText)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(TextSurf, TextRect)

        button("GO!", 150, 450, 100, 50, green, bright_green, game_loop)
        button("Quit", 550, 450, 100, 50, red, bright_red, quit_game)

        pg.display.update()
        clock.tick(5)


def quit_game():
    pg.quit()
    quit()


def unpause():
    global pause
    # pg.mixer.music.unpause()
    pause = False


def paused():
    # pg.mixer.music.pause()
    largeText = pg.font.SysFont("comicsansms",115)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    while pause:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        button("Continue", 150, 450, 100, 50, green, bright_green, unpause)
        button("Quit", 550, 450, 100, 50, red, bright_red, quit_game)

        pg.display.update()
        clock.tick(15)


def crash():
    # pg.mixer.Sound.play(crash_sound)
    # pg.mixer.music.stop()
    largeText = pg.font.SysFont("comicsansms", 115)
    TextSurf, TextRect = text_objects("You Crashed", largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        button("Play Again", 150, 450, 100, 50, green, bright_green, game_loop)
        button("Quit", 550, 450, 100, 50, red, bright_red, quit_game)

        pg.display.update()
        clock.tick(15)


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def blocks_dodged(count):
    text = small_font.render("Dodged: "+str(count), True, black)
    gameDisplay.blit(text, (0, 0))


def blocks(block_x, block_y, block_w, block_h, color):
    pg.draw.rect(gameDisplay, color, [block_x, block_y, block_w, block_h])
    

def car(x, y):
    gameDisplay.blit(car_img, (x, y))


def game_loop():
    """
    Main game loop
    """
    global pause
    # pg.mixer.music.load('jazz.wav')
    # pg.mixer.music.play(-1)
    game_exit = False

    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0

    block_startx = random.randrange(0, display_width)
    block_starty = -600
    block_speed = 7
    block_width = 100
    block_height = 100

    block_count = 1
    dodged = 0

    # game loop
    while not game_exit:

        # event loop
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_exit = True

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    x_change = -5
                elif event.key == pg.K_RIGHT:
                    x_change = 5
                if event.key == pg.K_p:
                    pause = True
                    paused()

            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                    x_change = 0

        x += x_change
        gameDisplay.fill(white)

        blocks(block_startx, block_starty, block_width, block_height, black)
        block_starty += block_speed
        car(x, y)
        blocks_dodged(dodged)

        if x > display_width - car_width or x < 0:
            crash()

        if block_starty > display_height:
            block_starty = 0 - block_height
            block_startx = random.randrange(0, display_width)
            dodged += 1
            block_speed += 1
            block_width += (dodged * 1.2)

        if y < block_starty + block_height:
            if block_startx < x < block_startx + block_width or block_startx < x + car_width < block_startx + block_width:
                crash()

        # render the display with new updates
        pg.display.update()
        # frames per second
        clock.tick(FPS)
    pg.quit()
    quit()


game_intro()
game_loop()
