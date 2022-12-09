from shared_use import read_file
from shared_use import flatten

class Forest():

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
            new_forest = []
            for i in range(self.rows):
                self.forest[i] = [x for x in self.forest[i]]

    def show(self):
        print('\nMap:')
        for row in self.forest:
           print(row)
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

        print(f'considering view from {self.forest[my_y][my_x]} at ({my_y},{my_x})')

        # if we are an edge tree, exit with score of 0
        if my_x == 0 or my_y == 0 or my_x == self.cols - 1 or my_y == self.rows - 1:
            print('Edge tree, 0 score')
            return 0

        # look up (we know we can see at least 1 tree, so pre-load)
        this_view = 1
        y_offset = -1
        this_height = int(self.forest[my_y + y_offset][my_x])
        print(f'above us is {self.forest[my_y + y_offset][my_x]} at {this_height}m')
        while True:
            y_offset -= 1
            if my_y + y_offset >= 0:
                # if there exists a tree above the current one
                print(f'looking at {self.forest[my_y + y_offset][my_x]} compared to {this_height}')
                if int(self.forest[my_y + y_offset][my_x]) >= this_height:
                    # this tree is taller or equal than ours, so we can see it
                    # increase the score
                    this_view += 1
                    # make this tree the new highest in view
                    this_height = int(self.forest[my_y + y_offset][my_x])
                else:
                    # special case, we are in the distance and we've seen two trees the same height
                    if int(self.forest[my_y + y_offset][my_x]) == this_height and y_offset < -1:
                        this_view += 1
                        print('two equal trees, marking both')
                    print(f'cannnot see whats behind this tree, score up is {this_view}')
                    # this tree is NOT in view, sum the score, and exit
                    view_score *= this_view
                    break
            else:
                # if we've exited the forest
                print(f'we exited the forest, score up is {this_view}')
                # sum all our scores and exit
                view_score *= this_view
                break

        # look right
        this_view = 1
        x_offset = 1
        this_height = int(self.forest[my_y][my_x + x_offset])
        print(f'right of us is {self.forest[my_y][my_x + x_offset]} at {this_height}m')
        while True:
            x_offset += 1
            if my_x + x_offset < self.cols:
                # if there exists a tree to the right of the current one
                print(f'looking at {self.forest[my_y][my_x + x_offset]} compared to {this_height}')
                if int(self.forest[my_y][my_x + x_offset]) >= this_height:
                    # this tree is taller or equal than ours, so we can see it
                    # increase the score
                    this_view += 1
                    # make this tree the new highest in view
                    this_height = int(self.forest[my_y][my_x + x_offset])
                else:
                    # special case, we are in the distance and we've seen two trees the same height
                    if int(self.forest[my_y][my_x + x_offset]) == this_height and x_offset > 1:
                        this_view += 1
                        print('two equal trees, marking both')
                    print(f'cannnot see whats behind this tree, score up is {this_view}')
                    # this tree is NOT in view, sum the score, and exit
                    view_score *= this_view
                    break
            else:
                # if we've exited the forest
                print(f'we exited the forest, score right is {this_view}')
                # sum all our scores and exit
                view_score *= this_view
                break

        # look down
        this_view = 1
        y_offset = 1
        this_height = int(self.forest[my_y + y_offset][my_x])
        print(f'below us is {self.forest[my_y + y_offset][my_x]} at {this_height}m')
        while True:
            y_offset += 1
            if my_y + y_offset < self.rows:
                # if there exists a tree below the current one
                print(f'looking at {self.forest[my_y + y_offset][my_x]} compared to {this_height}')
                if int(self.forest[my_y + y_offset][my_x]) >= this_height:
                    # this tree is taller or equal than ours, so we can see it
                    # increase the score
                    this_view += 1
                    # make this tree the new highest in view
                    this_height = int(self.forest[my_y + y_offset][my_x])
                else:
                    # special case, we are in the distance and we've seen two trees the same height
                    if int(self.forest[my_y + y_offset][my_x]) == this_height and y_offset > 1:
                        this_view += 1
                        print('two equal trees, marking both')
                    print(f'cannnot see whats behind this tree, score down is {this_view}')
                    # this tree is NOT in view, sum the score, and exit
                    view_score *= this_view
                    break
            else:
                # if we've exited the forest
                print(f'we exited the forest, score down is {this_view}')
                # sum all our scores and exit
                view_score *= this_view
                break

        # look left
        this_view = 1
        x_offset = -1
        this_height = int(self.forest[my_y][my_x + x_offset])
        print(f'left of us is {self.forest[my_y][my_x + x_offset]} at {this_height}m')
        while True:
            if my_x + x_offset >= 0:
                # if there exists a tree to the left of the current one
                print(f'looking at {self.forest[my_y][my_x + x_offset]} compared to {this_height}')
                if int(self.forest[my_y][my_x + x_offset]) > this_height:
                    # this tree is taller or equal than ours, so we can see it
                    # increase the score
                    this_view += 1
                    # make this tree the new highest in view
                    this_height = int(self.forest[my_y][my_x + x_offset])
                    x_offset -= 1
                else:
                    # special case, we are in the distance and we've seen two trees the same height
                    if int(self.forest[my_y][my_x + x_offset]) == this_height and x_offset < -1:
                        this_view += 1
                        print('two equal trees, marking both')
                    print(f'cannnot see whats behind this tree, score left is {this_view}')
                    # this tree is NOT in view, sum the score, and exit
                    view_score *= this_view
                    break
            else:
                # if we've exited the forest
                print(f'we exited the forest, score left is {this_view}')
                # sum all our scores and exit
                view_score *= this_view
                break

        print(f'************ tree score of {view_score}\n')
        return view_score

def main():
    raw_data = read_file('test')
    print(raw_data)
    my_forest = Forest(raw_data)
    my_forest.show()
    my_forest.for_the_trees()
    my_forest = Forest(raw_data)
    my_forest.show()
    tallest = -1
    print(my_forest.get_tree_score(3, 2))
"""
    for y in range(my_forest.cols):
        for x in range(my_forest.rows):
            tallest = max(my_forest.get_tree_score(y, x), tallest)
    print(f'Best treehouse score is {tallest}')
"""

if __name__ == '__main__':
    print('running day 8')
    main()
