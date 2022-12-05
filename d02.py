import pygame
import pygame as pg
from shared_use import read_file


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
    


if __name__ == '__main__':
    print('Running day 2 directly.')
    main()

    print('Starting pygame...')
    main_loop()
