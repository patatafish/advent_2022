from shared_use import read_file


def main():
    raw_data = read_file('d05')
    print(raw_data)

    # find split between stacks and instructions
    i = 0
    for line in raw_data:
        if line:
            i += 1
            continue
        break
    # split data into stacks and instructions, excluding '' line
    raw_stacks = raw_data[:i]
    instructions = raw_data[i+1:]

    clean_stacks = make_stacks(raw_stacks)
    # move_stacks() will alter clean_stacks as it is pass-by-ref
    move_stacks(clean_stacks, instructions)
    # show the top item in each stack
    for stack in clean_stacks:
        print(stack[-1][1], end='')
    print()


def disp(my_stacks):

    num_stacks = len(my_stacks)

    # checking for the tallest, -1 for indexing
    tallest = get_height(my_stacks) - 1

    # loop each height, counting down.
    # print newline for readability
    print()
    for i in range(tallest, -1, -1):
        # print leading space for readability
        print(' ', end='')
        for stack in my_stacks:
            try:
                print(stack[i], end=' ')
            except IndexError:
                # if there is no such item (the stack is shorter than what height
                # we are considering, then print 4 ' ' to keep stacks straight
                print(' ' * 4, end='')
        # end of row, print endl for next stack
        print()

    # label the stacks
    for i in range(num_stacks):
        print(f'  {i}', end=' ')
    print('\n\n')

def get_height(my_stacks):
    tallest = 0
    for stack in my_stacks:
        tallest = max(tallest, len(stack))
    return tallest


def move_stacks(my_stacks, my_moves, show_moves=True):
    # the amount of items our crane can grab at once.
    grasp = 99

    # look at each move individually
    for move in my_moves:
        # check if move contains data, if not break loops
        if not move:
            break

        # display stacks if flag
        if show_moves:
            disp(my_stacks)

        # First, we will reduce the move to just three numbers, since every move has the format
        # of: MOVE # FROM # TO #.
        # split the move into words
        move = move.split(' ')
        # look at each word to see if it is numbers or letters
        looking = True
        i = 0
        while looking:
            try:
                # if it is numbers, keep it and translate to int from str
                move[i] = int(move[i])
                i += 1
            except ValueError:
                # if it is not numbers, delete the item and adjust our index for looping
                del(move[i])
            except IndexError:
                looking = False

        # adjust move to correctly index from and to columns
        move[1] -= 1
        move[2] -= 1

        """ part 1 solution
        # Nw we can loop move[0] number of times, getting one stack from move[1] and putting it in move[2]
        print(move)
        for i in range(move[0]):
            my_stacks[move[2]].append(my_stacks[move[1]].pop())
        """

        print(move)

        moving = True
        i = move[0]
        while moving:
            # if we have 3 or fewer to move, grab them, move them, exit
            if i <= grasp:
                # put crates in claw
                claw = my_stacks[move[1]][-i:]
                # remove crates from current stack
                del(my_stacks[move[1]][-i:])
                moving = False
            # otherwise we have more than fit in claw, take a chunk and move them
            else:
                # put (grasp) crates in claw
                claw = my_stacks[move[1]][-grasp:]
                # remove crates from current stack
                del(my_stacks[move[1]][-grasp:])
                i -= grasp
            # place crates on target stack
            for crate in claw:
                my_stacks[move[2]].append(crate)

    # display stacks if flag once more on exit
    if show_moves:
        disp(my_stacks)


def make_stacks(my_data):
    # find the number of columns the stacks contain, save as an int
    num_stacks = int(max(my_data[-1].split(' ')))

    # create a clean list of the contents of each stack from top (in index 0) to bottom
    my_stack = []
    # start by making an empty list for each stack
    for i in range(num_stacks):
        my_stack.append([])
    # read each line of the raw stack data, adding items as found
    # we do not read the last line as it is not crate info but stack numbers
    for crates in my_data[:-1]:
        # to read the column content, the letter will be at index
        # (i*4)+1. this starts counting at column 0.
        for i in range(num_stacks):
            # if the item is in the list, record it
            try:
                if crates[(i*4)+1] != ' ':
                    my_stack[i].append(f'[{crates[(i*4)+1]}]')
            # if we look outside the list, stop looking
            except IndexError:
                break

    # reverse each stack to keep bottom at [0] and top at [-1]
    for i in range(len(my_stack)):
        my_stack[i].reverse()

    return my_stack


if __name__ == '__main__':
    print('running day 5')
    main()
