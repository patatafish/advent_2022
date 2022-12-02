from shared_use import read_file


def process(my_data):


def main():
    raw_data = read_file('d02', 'l')
    print(raw_data)
    clean = process(raw_data)
    print(clean)




if __name__ == '__main__':
    print('Running day 2 directly.')
    main()
