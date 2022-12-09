from shared_use import read_file


def show_rope(rope):

    min_y = min(x[1] for x in rope) - 2
    max_y = max(x[1] for x in rope) + 3
    min_x = min(x[0] for x in rope) - 2
    max_x = max(x[0] for x in rope) + 3

    if min_y > -2:
        min_y = -2
    if min_x > -2:
        min_x = -2
    if max_y < 3:
        max_y = 3
    if max_x < 3:
        max_x = 3

    map = {}
    for i in range(min_x, max_x):
        for j in range(min_y, max_y):
            if i == 0:
                map[f'{i}, {j}'] = '|'
            elif j == 0:
                map[f'{i}, {j}'] = '-'
            else:
                map[f'{i}, {j}'] = ' '
            if [i, j] in rope:
                map[f'{i}, {j}'] = str(rope.index([i, j]))

    for i in range(max_y-1, min_y-1, -1):
        for j in range (min_x, max_x):
            print(f' {map[f"{j}, {i}"]}', end='')
        print('\n')


def main():
    raw_data = [l.split(' ') for l in read_file('d09')]
    print(raw_data)


    # make a rope of n length
    n = 10
    rope = []
    for i in range(n):
        rope.append([0,0])

    visited = []
    moves = {'R': [1, 0], 'L': [-1, 0], 'U': [0, 1], 'D': [0, -1]}


    for instruction in raw_data:
        print(instruction)
        dir = instruction[0]
        num = int(instruction[1])

        for move in range(num):
            rope[0][0] += moves[dir][0]
            rope[0][1] += moves[dir][1]


            segment = len(rope) - 1
            while True:
                # left/right
                horz_diff = rope[segment-1][0] - rope[segment][0]
                vert_diff = rope[segment-1][1] - rope[segment][1]
                if abs(horz_diff) > 1:
                    if vert_diff:
                        rope[segment][0] += int(horz_diff / abs(horz_diff))
                        rope[segment][1] += int(vert_diff / abs(vert_diff))
                    else:
                        rope[segment][0] = int((rope[segment-1][0] + rope[segment][0])/2)
                    segment = len(rope) - 1
                    continue

                # up/down
                if abs(vert_diff) > 1:
                    if horz_diff:
                        rope[segment][0] += int(horz_diff / abs(horz_diff))
                        rope[segment][1] += int(vert_diff / abs(vert_diff))
                    else:
                        rope[segment][1] = int((rope[segment-1][1] + rope[segment][1])/2)
                    segment = len(rope) - 1
                    continue

                segment -= 1
                if segment == 0:
                    break

            if rope[-1] not in visited:
                visited.append(rope[-1].copy())

        # show_rope(rope)
        print('\n')

    print(len(visited))

if __name__ == '__main__':
    print('running day 09')
    main()
