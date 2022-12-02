
# flatten will take a 2-d or greater list and flatten to a 1-d list preserving the order of all items
def flatten(my_list):
    # print(f'starting to flatten {my_list}')
    # empty list to return
    my_clean_list = []
    # loop items in list
    for item in my_list:
        # print(f'looking at {item}', end=' ')
        # if item is a list itself, recursive call to flatten
        if type(item) is list:
            # print(f'is a list!')
            sub_list = flatten(item)
            for word in sub_list:
                # print(f'{word} is flat, appending')
                # loop one word at a time, since we are returned a list,
                # we don't simply append that list as it would re-create
                # the 2-d nature.
                my_clean_list.append(word)
        else:
            # print(f'is flat, appending {item}')
            # if item is not a list, (i.e. char/string) append it directly
            my_clean_list.append(item)

    # return the clean, 1-d list
    # print(f'I think im flat, returning {my_clean_list}')
    return my_clean_list

# file i/o
def read_file(filename, read_type='l'):
    # append directory for read
    filename = '/home/mendoncapatrick/PycharmProjects/advent2022/DAT/' + filename
    with open(filename, 'r') as inf:

        # import file line by line, splittng on newline
        if read_type == 'l':
            my_raw_data = [line for line in inf.read().split('\n')]
            return my_raw_data

        # import file reading word by word, splitting on empty space
        if read_type == 'w':
            my_raw_data = [line for line in inf.read().split(' ')]
            return my_raw_data

        # import file char by char, splitting each char
        if read_type == 'c':
            my_raw_data = [line for line in inf.read()]
            return my_raw_data

        # if we are passed another char or string to split on, do that
        my_raw_data = [line for line in inf.read().split(read_type)]
        return my_raw_data
