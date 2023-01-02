from shared_use import read_file
from shared_use import Huge
from shared_use import get_aoc_data as gd


class Monkey():

    def __init__(self):
        self.name = None
        self.my_items = None
        self.worry_change = None
        self.test = None
        self.true_act = None
        self.false_act = None
        self.counter = 0

    def pick_lice(self):
        # clean the name
        self.name = self.name.split(' ')[1]
        self.name = int(self.name[:-1])

        # clean starting items
        self.my_items = [item for item in self.my_items.split('items:')]
        self.my_items = self.my_items[1]

        if ',' in self.my_items:
            self.my_items = [Huge(item) for item in self.my_items.split(',')]
        else:
            self.my_items = [Huge(self.my_items)]

        # clean worry rules
        self.worry_change = [item for item in self.worry_change.split('new = old')]
        self.worry_change = self.worry_change[1].strip()
        self.worry_change = [item for item in self.worry_change.split(' ')]

        # clean test rules
        self.test = [item for item in self.test.split(' ')]
        self.test = int(self.test[-1])

        # clean true test action
        self.true_act = [item for item in self.true_act.split(' ')]
        self.true_act = int(self.true_act[-1])

        # clean false test action
        self.false_act = [item for item in self.false_act.split(' ')]
        self.false_act = int(self.false_act[-1])

def make_monkies(input):
    new_list = []

    while input:
        new_monkey = Monkey()
        new_monkey.false_act = input.pop()
        new_monkey.true_act = input.pop()
        new_monkey.test = input.pop()
        new_monkey.worry_change = input.pop()
        new_monkey.my_items = input.pop()
        new_monkey.name = input.pop()

        try:
            input.pop()
        except IndexError:
            pass

        new_monkey.pick_lice()

        new_list.append(new_monkey)

    new_list.reverse()
    return new_list


def monkey_around(monkies):

    for monkey in monkies:
        # print(f'Monkey {monkey.name}s turn')
        while monkey.my_items:
            current = monkey.my_items.pop(0)
            monkey.counter += 1
            # print(f'\t examining item with worry {current}')
            if 'old' in monkey.worry_change:
                change = current
            else:
                change = int(monkey.worry_change[1])

            if monkey.worry_change[0] == '+':
                current += change
            elif monkey.worry_change[0] =='*':
                current *= change

            # print(f'\t\t you are now {current} worried!')
            # current = int(current / 3)
            # print(f'\t\t safe! you are {current} worried.')

            if current % monkey.test == 0:
                # print(f'\t\t\t {current} is divisable by {monkey.test}')
                # print(f'\t\t\t passing to monkey {monkey.true_act}')
                monkies[monkey.true_act].my_items.append(current)
            else:
                # print(f'\t\t\t {current} is not divisable by {monkey.test}')
                # print(f'\t\t\t passing to monkey {monkey.false_act}')
                monkies[monkey.false_act].my_items.append(current)



if __name__ == '__main__':


    huge = Huge(59)
    print(huge)
    huge = Huge(60)
    print(huge)
    huge = Huge(65865198612)
    print(huge)

    # test = gd(11)
    test = read_file('test')

    print(test)

    monkey_list = make_monkies(test)



    interested = [1, 20, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]

    for i in range(10000):
        monkey_around(monkey_list)
        if i+1 in interested:
            print(f'Round {i}')
            for monkey in monkey_list:
                print(f'Monkey {monkey.name}: {monkey.counter}')

    big_list = []
    for monkey in monkey_list:
        big_list.append(monkey.counter)
        print(f'Monkey {monkey.name}: {monkey.counter}')
    big_list.sort(reverse=True)
    print(big_list[0] * big_list[1])


