import sys
import pygame
import pygame as pg
from shared_use import read_file


def count_inventory(my_data):
    inventory = []
    elf_has = 0

    for line in my_data:
        if line:
            elf_has += int(line)
        else:
            inventory.append(elf_has)
            elf_has = 0

    inventory.sort()
    inventory.reverse()
    return inventory


def game_loop(my_data):
    black = (0, 0, 0)
    wait_delay = 3500
    move_speed = 10

    pygame.init()
    clock = pygame.time.Clock()
    window = width, height = 1000, 1000
    screen = pygame.display.set_mode(window)
    font = pygame.font.Font('freesansbold.ttf', 32)

    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((170, 238, 187))

    screen.blit(background, (0, 0))
    pg.display.flip()

    elf = pygame.image.load('IMG/d01/elf.png').convert_alpha()
    elf = pygame.transform.smoothscale(elf, (200, 200))
    elf_rect = elf.get_rect()
    start_rect = (-200, 500)
    elf_rect.center = start_rect

    desk = pygame.image.load('IMG/d01/desk.png').convert_alpha()
    desk = pygame.transform.smoothscale(desk, (300, 300))
    desk_rect = desk.get_rect()
    desk_rect.center = (600, 500)

    in_game = True

    approach = True
    tally = False
    leave = False

    top_3 = [0, 0, 0]

    while in_game:
        clock.tick(60)
        screen.blit(background, (0, 0))
        screen.blit(desk, desk_rect)

        top1 = font.render(f'{top_3[0]}', True, black)
        top1_rect = top1.get_rect()
        top1_rect.topright = (975, 25)
        top2 = font.render(f'{top_3[1]}', True, black)
        top2_rect = top2.get_rect()
        top2_rect.topright = (975, 55)
        top3 = font.render(f'{top_3[2]}', True, black)
        top3_rect = top3.get_rect()
        top3_rect.topright = (975, 85)
        top_total = int(top_3[0]) + int(top_3[1]) + int(top_3[2])
        top_total_font = font.render(f'{top_total}', True, black)
        top_total_font_rect = top_total_font.get_rect()
        top_total_font_rect.bottomright = (975, 975)

        screen.blit(top1, top1_rect)
        screen.blit(top2, top2_rect)
        screen.blit(top3, top3_rect)
        screen.blit(top_total_font, top_total_font_rect)

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                in_game = False

        if approach:
            elf_rect = elf_rect.move((move_speed, 0))
            if elf_rect.right >= desk_rect.left:
                approach = False
                tally = True
        elif tally:
            if wait_delay:
                wait_delay -= 100

            move_speed += 1

            i = 0
            try:
                while my_data[i]:
                    i += 1
            except IndexError:
                approach = False
                tally = False
                leave = False
                continue

            my_pocket = my_data[0:i]
            del(my_data[0:i+1])
            print(my_pocket, my_data)
            tally = False
            leave = True

            locx, locy = desk_rect.topleft

            total = 0
            for items in my_pocket:
                total += int(items)
                text = font.render(f'{items}', True, black)
                text_rect = text.get_rect()
                text_rect.topleft = (locx, locy)
                screen.blit(text, text_rect)
                locy += 50

            total_score = font.render(f'{total}', True, black)
            total_rect = total_score.get_rect()
            total_rect.topleft = desk_rect.topright
            screen.blit(total_score, total_rect)

            screen.blit(elf, elf_rect)
            pygame.display.flip()
            pygame.time.wait(wait_delay)

            print(top_3)
            top_3.append(int(total))
            top_3.sort()
            top_3.reverse()
            del(top_3[-1])

        elif leave:
            elf_rect = elf_rect.move((0, -move_speed))
            if elf_rect.bottom < screen.get_rect().top:
                elf_rect.center = start_rect
                leave = False
                approach = True

        screen.blit(elf, elf_rect)
        pygame.display.flip()

    pygame.quit()
    sys.exit()



def main():
    raw_data = read_file('d01', 'l')

    print(raw_data)

    elf_food = count_inventory(raw_data)
    print(elf_food[0], elf_food[1], elf_food[2])
    print(elf_food[0] + elf_food[1] + elf_food[2])
    game_loop(raw_data)


if __name__ == '__main__':
    print('Running day 1 directly')

    main()
