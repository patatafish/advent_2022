import shared_use
from shared_use import get_aoc_data as gd

if __name__ == '__main__':

    test = gd(10)
    # test = shared_use.read_file('test')

    register = [[1, 1]]

    while test:

        current = test.pop(0)
        last = register[-1][-1]

        if current == 'noop':
            register.append([last, last])
            continue

        addend = current.split(' ')
        addend = int(addend[1])

        register.append([last, last])
        register.append([last, last + addend])


    interesting = [20, 60, 100, 140, 180, 220]

    signal_strength = 0

    for line_num in interesting:
        signal_strength += line_num * register[line_num][0]

    print(signal_strength)


    register.pop(0)
    pixel = 0

    while register:
        sprite = register.pop(0)[0]
        window = [pixel-1, pixel, pixel+1]
        if sprite in window:
            print('#', end=' ')
        else:
            print(' ', end=' ')

        pixel += 1

        if pixel == 40:
            print('\n')
            pixel = 0




