from shared_use import read_file


def find_start(my_data):

    found = False
    i = 0
    while not found:
        chunk = my_data[i:i+14]
        score = 0
        print(chunk, end=' ')
        for j in range(14):
            for k in range(14):
                if chunk[j] == chunk[k]:
                    score += 1
        if score <= 14:
            found = True
        else:
            print(score)
            i += 1

    print(f'\n{i+14}')


def main():
    raw_data = read_file('d06', 'c')
    print(raw_data)

    find_start(raw_data)


if __name__ == '__main__':
    print('Running day 6')
    main()
