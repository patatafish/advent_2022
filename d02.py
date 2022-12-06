import sys
import random
import pygame as pg
from shared_use import read_file


# create an image cache for quick loading
image_cache = {}


def get_img(key):
    # load image, will not attempt re-load if already in memory
    if key not in image_cache:
        image_cache[key] = pg.image.load(key)
    return image_cache[key]


class Elf(pg.sprite.Sprite):
    """
    class Elf
    defines the sprite, rect, and behavior of the elf

    on init--
        invert - 0 to face right, 1 to face left
        x_size - the size of the sprite in width
        y_size - the size of the sprite in height
    """
    def __init__(self, enemy=False, boss=False, x_size=200, y_size=200):
        pg.sprite.Sprite.__init__(self)
        # load image, convert for transparent BG
        self.image = get_img('IMG/common/elf.png')
        # self.image = pg.image.load('IMG/common/elf.png').convert_alpha()
        self.image.convert_alpha()
        # resize img from passed params
        self.image = pg.transform.smoothscale(self.image, (x_size, y_size))
        # if invert flag, flip on x
        self.enemy = enemy
        if self.enemy:
            self.image = pg.transform.flip(self.image, True, False)
        # define rect for sprite, on load create rect off-screen
        self.rect = self.image.get_rect()
        self.rect.center = (-500, -500)

        # internal values to control movement
        self.enter = False  # to control walk-up
        self.newborn = True  # for positioning pre-walk-up
        self.my_choice = None  # our choice in game (rock, paper, scissors)

    def update(self):
        # if we are initializing, show walk-up
        if self.enter:
            self.walk_up()

    def choose(self):
        # init new random seed
        random.seed()
        my_choice = random.randrange(3)
        if my_choice == 0:
            return 'rock'
        elif my_choice == 1:
            return 'paper'
        else:
            return 'scissors'

    def walk_up(self):
        # first motion, move to just off-screen
        if self.newborn:
            if self.enemy:
                self.rect.center = (1100, 700)
            else:
                self.rect.center = (-100, 700)
            self.newborn = False

        move_speed = 10
        # make enemy walk right to left
        if self.enemy:
            move_speed *= -1
        self.rect = self.rect.move(move_speed, 0)

        # check when to stop
        if self.enemy:
            if self.rect.left <= 550:
                self.enter = False
        else:
            if self.rect.right >= 450:
                self.enter = False


class Rock(pg.sprite.Sprite):

    def __init__(self, size=(250, 250), pos=(100, 100), rot=0):
        pg.sprite.Sprite.__init__(self)
        self.image = get_img('IMG/d02/rock.webp')
        self.image.convert_alpha()
        self.image = pg.transform.smoothscale(self.image, size)
        self.image = pg.transform.rotate(self.image, rot)
        self.rect = self.image.get_rect()
        self.rect.center = pos


class Paper(pg.sprite.Sprite):

    def __init__(self, size=(250, 250), pos=(100, 100), rot=0):
        pg.sprite.Sprite.__init__(self)
        self.image = get_img('IMG/d02/paper.png')
        self.image.convert_alpha()
        self.image = pg.transform.smoothscale(self.image, size)
        self.image = pg.transform.rotate(self.image, rot)
        self.rect = self.image.get_rect()
        self.rect.center = pos


class Scissors(pg.sprite.Sprite):

    def __init__(self, size=(250, 250), pos=(100, 100), rot=0):
        pg.sprite.Sprite.__init__(self)
        self.image = get_img('IMG/d02/scissor.webp')
        self.image.convert_alpha()
        self.image = pg.transform.smoothscale(self.image, size)
        self.image = pg.transform.rotate(self.image, rot)
        self.rect = self.image.get_rect()
        self.rect.center = pos


def process(my_data, part2_flag=0):
    total = 0

    for line in my_data:
        score = 0
        [opp, me] = line.split(' ')

        if part2_flag:
            if me == 'X':
                if opp == 'A':
                    me = 'Z'
                if opp == 'B':
                    me = 'X'
                if opp == 'C':
                    me = 'Y'
            elif me == 'Y':
                if opp == 'A':
                    me = 'X'
                if opp == 'B':
                    me = 'Y'
                if opp == 'C':
                    me = 'Z'
            else:
                if opp == 'A':
                    me = 'Y'
                if opp == 'B':
                    me = 'Z'
                if opp == 'C':
                    me = 'X'

        if me == 'X':
            score += 1
            if opp == 'A':
                score += 3
            if opp == 'C':
                score += 6
        if me == 'Y':
            score += 2
            if opp == 'B':
                score += 3
            if opp == 'A':
                score += 6
        if me == 'Z':
            score += 3
            if opp == 'C':
                score += 3
            if opp == 'B':
                score += 6
        total += score

        print(opp, me, score, total)

    return total


def main():
    raw_data = read_file('d02', 'l')
    print(raw_data)
    clean = process(raw_data)
    print(clean)
    clean = process(raw_data, 1)
    print(clean)


def main_loop():

    # main init sequence for pygame
    pg.init()
    clock = pg.time.Clock()

    # define basic window
    window_size = window_width, window_height = 1000, 1000
    screen = pg.display.set_mode(window_size)

    # set background screen
    black = (0, 0, 0)
    background = pg.Surface(screen.get_size())
    background = background.convert()

    # flip screen and display loading during asset gather
    loading_img = pg.image.load('IMG/d02/loading.png').convert_alpha()
    loading_rect = loading_img.get_rect()
    loading_rect.center = screen.get_rect().center
    screen.blit(background, (0, 0))
    screen.blit(loading_img, loading_rect)
    pg.display.update()

    # define sprite groups
    all_sprites = pg.sprite.RenderUpdates()
    player_group = pg.sprite.RenderUpdates()
    enemy_group = pg.sprite.RenderUpdates()
    button_group = pg.sprite.RenderUpdates()

    # load sprites
    # player sprite
    player = Elf()
    # first enemy sprite
    enemy = Elf(enemy=True)
    # we are entering
    player.enter = True
    enemy.enter = True

    # button sprites
    rock_button = Rock((250, 250), (200, 300), 0)
    paper_button = Paper((250, 250), (500, 300), 0)
    scis_button = Scissors((250, 250), (800, 300), 0)

    button_group.add(rock_button, paper_button, scis_button)
    player_group.add(player)
    enemy_group.add(enemy)
    all_sprites.add(player_group, enemy_group)

    # loop and game control variables
    running = True  # game loop control flag
    new_enemy = False    # spawn a new enemy?
    click_list = []     # event list on mouse click

    # clear screen for game loop animation
    screen.blit(background, (0, 0))
    pg.display.update()

    while running:
        # begin each loop by placing down background
        screen.blit(background, (0, 0))

        # main loop, check for quit signal
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                continue
            if event.type == pg.MOUSEBUTTONUP:
                click_list = [s for s in button_group if s.rect.collidepoint(event.pos)]

        # if enemy needed, create it
        if new_enemy:
            print('Creating new enemy')
            # load enemy sprites
            enemy = Elf(True)
            # show is enemy
            enemy.enter = True
            # add to groups
            all_sprites.add(enemy)
            enemy_group.add(enemy)
            # change flag, we have an enemy
            new_enemy = False

        # if both player present, start game
        if not enemy.enter:
            # reset previous choice, if any
            player_choice = None
            all_sprites.add(button_group)

            # if the mouse has been click, check if it made a choice
            if click_list:
                if rock_button in click_list:
                    player_choice = 'rock'
                elif paper_button in click_list:
                    player_choice = 'paper'
                elif scis_button in click_list:
                    player_choice = 'scissors'

            # if the player made a choice, ask the computer to choose
            if player_choice:
                computer_choice = enemy.choose()

                print(player_choice, computer_choice)

                # after the computer chooses, show the play
                # where play icons will be centered
                p1_choice_pos = (475, 650)
                p2_choice_pos = (525, 650)
                choice_size = (100, 100)
                choice_rot = 30
                # define player icons
                if player_choice == 'rock':
                    p1_icon = Rock(choice_size, p1_choice_pos, choice_rot)
                elif player_choice == 'paper':
                    p1_icon = Paper(choice_size, p1_choice_pos, choice_rot)
                else:
                    p1_icon = Scissors(choice_size, p1_choice_pos, choice_rot)
                if computer_choice == 'rock':
                    p2_icon = Rock(choice_size, p2_choice_pos, -choice_rot)
                elif player_choice == 'paper':
                    p2_icon = Paper(choice_size, p2_choice_pos, -choice_rot)
                else:
                    p2_icon = Scissors(choice_size, p2_choice_pos, -choice_rot)

                player_group.add(p1_icon)
                enemy_group.add(p2_icon)
                all_sprites.add(player_group, enemy_group)

        # update sprite groups
        all_sprites.update()
        # player_group.update()
        # enemy_group.update()

        # render
        all_sprites.clear(screen, background)
        change_rect = all_sprites.draw(screen)
        pg.display.update(change_rect)

        # clear click event list
        click_list.clear()

        # frame rate control
        clock.tick(60)

    # outside main game loop, clean up and exit
    pg.quit()
    sys.exit()


if __name__ == '__main__':
    print('Running day 2 directly.')
    main()

    print('Starting pygame...')
    main_loop()
