import sys
import math
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

    def __init__(self, input_number=None):
        self.factors = [1]
        if input_number:
            self.set(int(input_number))

    def set(self, input_number):
        # fill with factors list
        # if the passed number is 1 or 2, just set it now
        if input_number == 1:
            return
        if input_number == 2:
            self.factors.append(input_number)
            return
        self.factor(input_number)

    def primes(self, n):
        """ Returns  a list of primes < n """
        sieve = [True] * n
        for i in range(3, int(n ** 0.5) + 1, 2):
            if sieve[i]:
                sieve[i * i::2 * i] = [False] * ((n - i * i - 1) // (2 * i) + 1)
        return [2] + [i for i in range(3, n, 2) if sieve[i]]


    def factor(self, input_number):
        # this function works in place, altering the self.factors list

        # generate the list of primes to input+1 to check against
        check_list = self.primes(input_number+1)

        # before anything else, check if the input IS prime, if so return it immediately
        if input_number == check_list[-1]:
            self.factors.append(input_number)
            return

        # loop across the factoring, until we are forced to put the input into the factor list
        # we really only need to check the bottom half of the factors list
        while True:
            if check_list[-1] > int(input_number/2):
                check_list.pop()
            else:
                break

        i = 0
        while input_number != 1:


            # is the input itself the prime?
            if input_number == check_list[-1]:
                self.factors.append(input_number)
                continue

            # what item in the check list are we at?
            is_factor = check_list[i]

            # check if the current is a factor of input
            if input_number % is_factor == 0:
                # if so, append current to factor list
                self.factors.append(is_factor)
                # divide the input by the factor
                input_number = int(input_number  / is_factor)
                # return to the start of out check list for next factorization
                i = 0
                # break the 'prime number' check loop, return to top
                continue

            if i < len(check_list):
                # if the number didn't factor, increase the check
                i += 1


    def __str__(self):
        return str(math.prod(self.factors))


    def __add__(self, other):
        return
    def __sub__(self, other):
        return

    def __mul__(self, other):
        return

    def __eq__(self, other):
        return

    def __lt__(self, other):
        return

    def __gt__(self, other):
        return

    def __mod__(self, other):
        return
