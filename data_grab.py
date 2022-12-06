from urllib.request import urlopen, Request
import os
import sys


if __name__ == '__main__':

    print('Building File Tree...')
    # try opening the project directory, exit prog if read error
    try:
        files = os.scandir('.')
    except FileNotFoundError:
        print('Error reading directory for file tree!')
        sys.exit(1)

    print('Identifying .py content...')
    # create empty list for relevant files
    clean_file_list = []
    # loop items looking for d##.py patters
    """                   use RE here later?"""
    for item in files:
        if 'd' in item.name and item.name.endswith('.py'):
            clean_file_list.append(item.name)
    # remove extra matched items
    clean_file_list.remove('shared_use.py')
    clean_file_list.remove('data_grab.py')

    print('Checking for DAT files...')
    for item in clean_file_list:
        print(item, end='... ')
        name, extension = item.split('.')
        if os.path.exists(f'DAT/{name}'):
            print('DAT file found!')
        else:
            print('DAT FILE DOES NOT EXIST!')

    menu = True
    while menu:
        print('\n\nMenu:')
        for item in clean_file_list:
            print(' ' * 3, end='')
            print(clean_file_list.index(f'{item}') +1, end=')')
            print(f' {item}')
        print(f'   {len(clean_file_list)+1}) Make new file')
        print(f'   {len(clean_file_list)+2}) Exit')

        foo = input('   :')
        try:
            foo = int(foo)
        except ValueError:
            print('Invalid Choice.')

        if foo == len(clean_file_list)+2:
            print('exiting...')
            menu = False
            continue

        if foo == len(clean_file_list)+1:
            print('checking if data is available...')
            new_day = len(clean_file_list)+1
            # url = 'http://google.com/'
            url = f'https://adventofcode.com/2022/day/{new_day}/input'
            req = Request(f'{url}', headers={'User-Agent': 'Mozilla/5.0'})
            print(f'Opening URL for day {url}...')
            with urlopen(f'{url}') as response:
                html = response.read()
                print(html)