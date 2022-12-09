from shared_use import read_file
from shared_use import flatten


class Forest:

    def __init__(self, trees):

        # if trees is not a list, can't seed the forest
        if not type(trees) == list:
            print('cant make a forest without trees')
            return

        print('Seeding new forest...')
        self.rows = 0
        self.cols = 0
        self.forest = trees.copy()
        self.seen = None
        self.seed()

    def seed(self):
        # checks how many rows and cols, then validates the data as a rectangle
        self.rows = len(self.forest)
        self.cols = len(self.forest[0])

        # make sure the forest is rectangular
        for row in self.forest:
            if len(row) != self.cols:
                print('non-rectangular forest, exiting!')
                return None

        # if there is no seen map established, we have a brand new forest,
        # make sure we are dealing with 2-d lists, not strings
        if not self.seen:
            # create the seen map
            self.seen = []
            seen_row = []
            for i in range(self.cols):
                seen_row.append('.')
            for i in range(self.rows):
                self.seen.append(seen_row.copy())
            # move the forest to a 2-d list
            for i in range(self.rows):
                self.forest[i] = [x for x in self.forest[i]]

    def show(self, seen_flag=True):
        print('\nMap:')
        for row in self.forest:
           print(row)
        if seen_flag:
            print('Seen Map:')

            for row in self.seen:
                print(row)


    def rotate(self):

        new_forest = []
        new_seen = []
        for i in range(self.cols):
            new_row = []
            new_seen_row = []
            for j in range(self.rows-1, -1, -1):
                new_row.append(self.forest[j][i])
                new_seen_row.append(self.seen[j][i])
            new_forest.append(new_row)
            new_seen.append(new_seen_row)
        self.forest = new_forest.copy()
        self.seen = new_seen.copy()
        # if the forest rows or cols swapped, redefine
        self.seed()

    def for_the_trees(self):

        print('\nobserving from outside...')

        # do this operation 4 times, once for each side
        for sides in range(4):

            for i in range(self.rows):
                tallest = self.forest[i][0]
                self.seen[i][0] = '*'
                for j in range(self.cols):
                    if int(self.forest[i][j]) > int(tallest):
                        tallest = self.forest[i][j]
                        self.seen[i][j] = '*'

            self.show()
            self.rotate()

        # count how many * are in seen array
        print(f'\nI think I saw {flatten(self.seen).count("*")} trees.')

    def get_tree_score(self, my_y=0, my_x=0):
        view_score = 1
        x_offset = 0
        y_offset = 0

        # if we are an edge tree, exit with score of 0
        if my_x == 0 or my_y == 0 or my_x == self.cols - 1 or my_y == self.rows - 1:
            print('   Edge tree, 0 score')
            return 0

        show = []
        for i in range(my_y-5, my_y+5, 1):
            string = ''
            for j in range(my_x-5, my_x+5, 1):
                if i >= 0 and j >= 0:
                    if i < self.rows and j < self.cols:
                        if i == my_y or j == my_x:
                            string += self.forest[i][j]
                        else:
                            string += ' '
            show.append(string)

        for line in show:
            print(line)

        print(f'considering view from {self.forest[my_y][my_x]} at ({my_y},{my_x})')

        # look up
        current_score = 0
        current_height = int(self.forest[my_y][my_x])
        y_offset = -1
        print(f'   up: ', end='')
        while True:
            # first check if we've exited the forest
            if my_y + y_offset < 0:
                # if we have, total the score and exit
                print('(x)', end='')
                view_score *= current_score
                break
            print(f'({self.forest[my_y + y_offset][my_x]})', end='')
            # if the next tree is of equal height to this tree, score 1 and exit
            if current_height == int(self.forest[my_y + y_offset][my_x]):
                current_score += 1
                y_offset -= 1
                continue
            # if the next tree is shorter than this tree, exit without scoring ONLY if we are
            # not at the origin
            if current_height > int(self.forest[my_y + y_offset][my_x]):
                # if we are at the origin, score this tree, mark height, and move to next
                if y_offset == -1:
                    current_score += 1
                    # current_height = int(self.forest[my_y + y_offset][my_x])
                    y_offset -= 1
                    continue
                # if we are away from origin, this view is blocked, do not score and exit
                view_score *= current_score
                break
            # if the next tree is taller than this tree, score tree, mark height, and move to next
            if current_height < int(self.forest[my_y + y_offset][my_x]):
                current_score += 1
                current_height = int(self.forest[my_y + y_offset][my_x])
                y_offset -= 1
                continue
        print(f' {current_score}')

        # look down
        current_score = 0
        current_height = int(self.forest[my_y][my_x])
        y_offset = 1
        print(f'   down: ', end='')
        while True:
            # first check if we've exited the forest
            if my_y + y_offset >= self.rows:
                # if we have, total the score and exit
                print('(x)', end='')
                view_score *= current_score
                break
            print(f'({self.forest[my_y + y_offset][my_x]})', end='')
            # if the next tree is of equal height to this tree, score 1 and exit
            if current_height == int(self.forest[my_y + y_offset][my_x]):
                current_score += 1
                y_offset += 1
                continue
            # if the next tree is shorter than this tree, exit without scoring ONLY if we are
            # not at the origin
            if current_height > int(self.forest[my_y + y_offset][my_x]):
                # if we are at the origin, score this tree, mark height, and move to next
                if y_offset == 1:
                    current_score += 1
                    current_height = int(self.forest[my_y + y_offset][my_x])
                    y_offset += 1
                    continue
                # if we are away from origin, this view is blocked, do not score and exit
                view_score *= current_score
                break
            # if the next tree is taller than this tree, score tree, mark height, and move to next
            if current_height < int(self.forest[my_y + y_offset][my_x]):
                current_score += 1
                current_height = int(self.forest[my_y + y_offset][my_x])
                y_offset += 1
                continue
        print(f' {current_score}')

        # look right
        current_score = 0
        current_height = int(self.forest[my_y][my_x])
        x_offset = 1
        print('   right: ', end='')
        while True:
            # first check if we've exited the forest
            if my_x + x_offset >= self.cols:
                # if we have, total the score and exit
                print('(x)', end='')
                view_score *= current_score
                break
            print(f'({self.forest[my_y][my_x + x_offset]})', end='')
            # if the next tree is of equal height to this tree, score 1 and exit
            if current_height == int(self.forest[my_y][my_x + x_offset]):
                current_score += 1
                x_offset += 1
                continue
            # if the next tree is shorter than this tree, exit without scoring ONLY if we are
            # not at the origin
            if current_height > int(self.forest[my_y][my_x + x_offset]):
                # if we are at the origin, score this tree, mark height, and move to next
                if x_offset == 1:
                    current_score += 1
                    current_height = int(self.forest[my_y][my_x + x_offset])
                    x_offset += 1
                    continue
                # if we are away from origin, this view is blocked, do not score and exit
                view_score *= current_score
                break
            # if the next tree is taller than this tree, score tree, mark height, and move to next
            if current_height < int(self.forest[my_y][my_x + x_offset]):
                current_score += 1
                current_height = int(self.forest[my_y][my_x + x_offset])
                x_offset += 1
                continue
        print(f' {current_score}')

        # look left
        current_score = 0
        current_height = int(self.forest[my_y][my_x])
        x_offset = -1
        print('   left: ', end='')
        while True:
            # first check if we've exited the forest
            if my_x + x_offset < 0:
                # if we have, total the score and exit
                print('(x)', end='')
                view_score *= current_score
                break
            print(f'({self.forest[my_y][my_x + x_offset]})', end='')
            # if the next tree is of equal height to this tree, score 1 and exit
            if current_height == int(self.forest[my_y][my_x + x_offset]):
                current_score += 1
                x_offset -= 1
                continue
            # if the next tree is shorter than this tree, exit without scoring ONLY if we are
            # not at the origin
            if current_height > int(self.forest[my_y][my_x + x_offset]):
                # if we are at the origin, score this tree, mark height, and move to next
                if x_offset == -1:
                    current_score += 1
                    current_height = int(self.forest[my_y][my_x + x_offset])
                    x_offset -= 1
                    continue
                # if we are away from origin, this view is blocked, do not score and exit
                view_score *= current_score
                break
            # if the next tree is taller than this tree, score tree, mark height, and move to next
            if current_height < int(self.forest[my_y][my_x + x_offset]):
                current_score += 1
                current_height = int(self.forest[my_y][my_x + x_offset])
                x_offset -= 1
                continue
        print(f' {current_score}')


        print(f'   total: {view_score}')
        return view_score

def main():
    raw_data = read_file('d08')
    print(raw_data)
    my_forest = Forest(raw_data)
    # my_forest.show()
    my_forest.for_the_trees()
    my_forest = Forest(raw_data)
    my_forest.show(False)
    tallest = -1
    """for y in range(my_forest.rows):
        for x in range(my_forest.cols):
            mine = my_forest.get_tree_score(y, x)
            if mine > tallest:
                tallest = mine
                print(f'\n\n\n{"*"*500}\nFOUND NEW TALLEST {tallest}\n****************\n\n\n')
        print(f'{"#"*150}')
        print(f'{"#" * 150}')
        print(f'{"#" * 150}')
    print(f'Best treehouse score is {tallest}')"""

if __name__ == '__main__':
    print('running day 8')
    main()
