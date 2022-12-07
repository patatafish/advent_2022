from shared_use import read_file

def main():
    raw_data = read_file('test')
    print(raw_data)


if __name__ == '__main__':
    print('running day 7')
    main()
