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
        self.int_value = int(input_number)
        self.factors = [1]
        if input_number:
            self.set(int(input_number))

    def set(self, input_number):
        # fill with factors list
        self.factor(input_number)

    def factor(self, input_number=None):
        # this function works in place, altering the self.factors list

        # if we are asking to factor the number we already are...
        if (self.int_value == input_number) and (len(self.factors) > 1):
            # then don't do the work, just return
            return

        # we are creating a new list of factors here, we should reset the current list
        self.factors = [1]

        # if we aren't passed a number to factor, use the current int value
        if not input_number:
            input_number = self.int_value

        # loop across the factoring, until we are forced to put the input into the factor list
        while True:

            # if the input is 1, we've fully factored the input_number
            if input_number == 1:
                break

            # knock out a few quickies with tricks we can check easily
            seven_check = False
            # first check if the number is even
            if str(input_number)[-1] in ['0', '2', '4', '6', '8']:
                self.factors.append(2)
                input_number = int(input_number / 2)
                continue
            # check for % 3 quickly
            temp = input_number
            while True:
                # add all the individual digits of input number
                temp = sum([int(i) for i in list(str(temp))])
                # check if the number is a single digit or not
                if len(str(temp)) > 1:
                    # if it is, go back to the top
                    continue
                break

            # if we have a single digit, check for %3
            if temp % 3 == 0:
                self.factors.append(3)
                input_number = int(input_number / 3)
                continue

            # check for % 5 quickly
            if str(input_number)[-1] == '5':
                self.factors.append(5)
                input_number = int(input_number / 5)
                continue


            # if not even, start checking odd numbers all the way to (input/2)+1
            i = 13
            ceiling = math.sqrt(input_number) + 1

            while True:
                # does the guess go evenly?
                if input_number % i == 0:
                    self.factors.append(i)
                    input_number = int(input_number / i)
                    # if we found a factor, break this 'odd' while loop, start from top
                    break
                # if it didn't factor, check the next odd number
                i += 2

                # check to see if we've checked the whole set of possible
                # factors, if so the input is prime and we should record it as
                # it's own factor
                if i > ceiling:
                    print()
                    self.factors.append(input_number)
                    # set the exit flag for outer loop
                    input_number = 1
                    break

    def __str__(self):
        return str(self.int_value)

    def __add__(self, other):
        if type(other) is Huge:
            self.int_value += other.int_value
            self.factor()
        else:
            self.int_value += other
            self.factor()

        return self

    def __sub__(self, other):
        if type(other) is Huge:
            self.int_value -= other.int_value
            self.factor()
        else:
            self.int_value -= other
            self.factor()

        return self

    def __mul__(self, other):
        if type(other) is Huge:
            self.int_value *= other.int_value
            self.factors.extend(other.factors)
            self.factors.sort()
        else:
            self.int_value *= other
            other = Huge(other)
            self.factors.extend(other.factors)
            self.factors.sort()

        return self

    def __eq__(self, other):
        if type(other) is Huge:
            return self.int_value == other.int_value
        else:
            return self.int_value == other

    def __lt__(self, other):
        if type(other) is Huge:
            return self.int_value < other.int_value
        else:
            return self.int_value < other

    def __gt__(self, other):
        if type(other) is Huge:
            return self.int_value > other.int_value
        else:
            return self.int_value > other

    def __mod__(self, other):
        if type(other) is Huge:
            return other.factors in self.factors
        else:
            return self.factor(other) in self.factors
