import sys
from aocd import get_data
from os.path import exists

# flatten will take a 2-d or greater list and flatten to a 1-d list preserving the order of all items
def flatten(my_list):
    # empty list to return
    my_clean_list = []
    # loop items in list
    for item in my_list:
        # if item is a list itself, recursive call to flatten
        if type(item) is list:
            sub_list = flatten(item)
            for word in sub_list:
                # loop one word at a time, since we are returned a list,
                # we don't simply append that list as it would re-create
                # the 2-d nature.
                my_clean_list.append(word)
        else:
            # if item is not a list, (i.e. char/string) append it directly
            my_clean_list.append(item)

    # return the clean, 1-d list
    return my_clean_list


# file i/o
def read_file(filename, read_type='l'):
    """
    :param filename: the file to be read, this assumes in directory ../PycharmProjects/advent2022/DAT/
    :param read_type: how to read the file, default is 'l' - break at newline, ' ' break at empty space, 'c'
    break between characters
    :return: list() of data from file
    """
    # append directory for read
    filename = '/home/mendoncapatrick/PycharmProjects/advent2022/DAT/' + filename
    with open(filename, 'r') as inf:

        # import file line by line, splitting on newline
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


# session ID define for AOC download
def get_session_id():
    return '53616c7465645f5f04f997207e51ec1a892b2d71b1a91c54b1d75c4124f2ded20737280a7e55bba5009585cd8e3778bbbb831fb6c39795f523d000918b7334b6 '


# looks for data for specified day, if it doesn't exist then will try to
# grab data from AOC site and write new local file
def get_aoc_data(my_day=1, my_year=2022, read_type='l'):

    filename = 'd' + str(my_day)

    # if the file doesn't exist, grab data from site and write file
    if not exists('DAT/' + filename):

        # try the connection, exit if no data can be found on web
        try:
            raw_data = get_data(session=get_session_id(), day=my_day, year=my_year)
        except:
            print('Couldn\'t get the data!')
            sys.exit()

        # write the data to new file, error and exit if we can't
        with open('DAT/' + filename, 'x') as outf:
            outf.write(raw_data)

    # read the data from the local file, using the passed read-type to split the data into list
    new_data = read_file(filename, read_type)

    return new_data


class Huge():

    def __init__(self, input_number=None, base=750):
        self.__number = []
        self.__base = base
        if input_number:
            self.set(input_number)
        else:
            self.__number = [0]


    def __str__(self):
        my_string = f'base {self.__base}: '
        for i in range(len(self.__number)-1, -1, -1):
            my_string += f'{self.__number[i]}'
        return my_string




#### YOU NEED TO MAKE THE SET FUNCTION HANDLE LISTS ALA __ADD__ AND SUCH


    def set(self, input_number):
        input_number = int(input_number)
        if input_number == 0:
            self.__number = [0]
        while input_number:
            self.__number.append(int(input_number % self.__base))
            input_number //= self.__base


    def __add__(self, other):
        if type(other) != Huge:
            other = Huge(other, self.__base)

        my_total = [0]

        for i in range(max(len(self.__number), len(other.__number))):
            try:
                my_total[i] += self.__number[i]
            except IndexError:
                pass
            try:
                my_total[i] += other.__number[i]
            except IndexError:
                pass

            if my_total[i] >= self.__base:
                carry = my_total[i] // self.__base
                my_total[i] %= self.__base
                my_total.append(carry)
            else:
                my_total.append(0)

        if my_total[-1] == 0:
            my_total.pop()

        return Huge(my_total, self.__base)

    def __sub__(self, other):
        if type(other) != Huge:
            other = Huge(other, self.__base)

        if self == other:
            return [0]

        if self > other:
            remainder = self.__number
            subtrahend = other.__number
        else:
            remainder = other.__number
            subtrahend = self.__number

        for i in range(len(remainder)):
            if remainder[i] < subtrahend[i]:
                remainder[i+1] -= 1
                remainder[i] += self.__base
            remainder[i] -= subtrahend[i]

        return Huge(remainder, self.__base)


    def __mul__(self, other):
        if type(other) != Huge:
            other = Huge(other, self.__base)

        my_product = [0]

        if len(self.__number) >= len(other.__number):
            for i in range(len(other.__number)):
                for j in range(len(self.__number)):
                    my_product[j+i] += other.__number[i] * self.__number[j]
                    if my_product[j+i] >= self.__base:
                        carry = my_product[j+i] // self.__base
                        my_product[j+i] %= self.__base
                        try:
                            my_product[j+i+1] += carry
                        except IndexError:
                            my_product.append(carry)
                    else:
                        my_product.append(0)
        else:
            for i in range(len(self.__number)):
                for j in range(len(other.__number)):
                    my_product[j+i] += self.__number[i] * other.__number[j]
                    if my_product[j+i] >= self.__base:
                        carry = my_product[j+i] // self.__base
                        my_product[j+i] %= self.__base
                        try:
                            my_product[j+i+1] += carry
                        except IndexError:
                            my_product.append(carry)
                    else:
                        my_product.append(0)

        if my_product[-1] == 0:
            my_product.pop()

        return Huge(my_product, self.__base)

    def __eq__(self, other):
        for i in range(max(len(self.__number), len(other.__number))):
            try:
                if self.__number[i] == other.__number[i]:
                    continue
                else:
                    return False
            except IndexError:
                return False
        return True

    def __lt__(self, other):
        if len(other.__number) > len(self.__number):
            return False

        if self == other:
            return False

        for i in range(len(self.__number)-1, -1, -1):
            if self.__number[i] < other.__number[i]:
                return True
            else:
                return False

    def __gt__(self, other):
        return other < self

    def __mod__(self, other):
        return
