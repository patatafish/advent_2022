from shared_use import read_file


def process(my_data):
    total = 0

    for line in my_data:
        score = 0
        [opp, me] = line.split(' ')

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




if __name__ == '__main__':
    print('Running day 2 directly.')
    main()
