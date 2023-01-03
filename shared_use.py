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
        self.__base = int(base)
        if input_number:
            self.set(input_number)
        else:
            self.__number = [0]


    def __str__(self):
        return f'base {self.__base}: {int(self)}'


    def __int__(self):
        my_int = 0
        for i in range(len(self.__number)-1, -1, -1):
            my_int += self.__number[i]*(self.__base**i)
        return my_int


    def set(self, input_number):
        # if we are attempting to set this Huge to another Huge:
        if type(input_number) is Huge:
            # just copy the data over, no conversion needed
            self.__number = input_number.__number
            self.__base = input_number.__base
            return

        # if we got passed a list we'll construt the new Huge and return it
        if type(input_number) is list:
            self.__number = input_number
            return

        # otherwise we are attempting to set this Huge to an int, it needs converting
        input_number = int(input_number)
        if input_number == 0:
            self.__number = [0]
        while input_number:
            self.__number.append(int(input_number % self.__base))
            input_number //= self.__base

    def divides(self, other):
        # convert our self to the base of the other

        # start by figuring out our largest place value needed in our new (lower) base
        # lets make a place value list
        ceiling = int(self)
        place_value = [1]
        while place_value[-1] < ceiling:
            place_value.append(other*place_value[-1])

        # now we have a list of the needed place values, lets start filling it in starting
        # with the biggest value we need, moving down

        # take off the last item, it's too big
        place_value.pop()

        """I THINK WE ARE CRASHING AT A CLEAN DIVIDE (NO REMAINDER) CHECK AND FIX"""
        # start chunking off parts of our int (the ceiling) and converting to new base
        new_base = []
        while ceiling:
            this_digit = 0
            this_place_value = place_value.pop()
            # if we are in the 'ones place' just tack it on
            if ceiling < other:
                this_digit = ceiling
                ceiling = 0
            # otherwise start subtracting (to avoid divide and float overflows)
            while ceiling > this_place_value:
                this_digit += 1
                ceiling -= this_place_value
            # we got how many of this digit, insert to new base at left side of list
            new_base.insert(0, this_digit)


        # if the 'ones' place is a 0, we divide evenly,
        # otherwise there will be a remainder
        if new_base[0] == 0:
            return True
        else:
            return False

    """YOU CAN SHORTEN THIS BY NOT CONVERTING TO HUGE TO ADD, JUST ADD THEN REGROUP IF NEEDED"""
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
