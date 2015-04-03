RIGHT = 0
LEFT = 1
DOWN = 2
UP = 3
from random import *
from copy import *


def generatePackage(random_function, largest_value = 0):
    if random_function(2) != 0 or largest_value == 0:
        new_package = ThreePackage(default_package)
        print default_package
    else:
        all_below = range(1, largest_value/8 + 1)
        possibilities = []
        for i in all_below:
            if i % 3 == 0 and i != 3:
                possibilities.append(i)
        package_items = deepcopy(default_package)
        if possibilities != []:
            extra_val = possibilities[random_function(len(possibilities))]
            package_items.append(extra_val)
        new_package = ThreePackage(package_items)
    return new_package


def can_combine(a, b):
    if b == 0:
        return True
    elif a in [1,2]:
        return a+b == 3
    else:
        return a == b

def find_largest_value(board):
    largest_val = 0
    for row in board:
        for idx in row:
            if idx > largest_val:
                largest_val = idx
    return largest_val

def shift_row(row):
    # item_pos = -1
    # while item_pos == -1:
    #     for i in range(len(row)).reverse():
    #         if i > 0 and row[i] != 0:
    #             if row[i] == 1 or row[i] == 2:
    #                 if row[i-1] + row[i] == 3:
    #                     item_pos = i
    #             else:
    #                 if row[i] == row[i-1] or row[i-1] == 0:
    #                     item_pos = i
    result = []
    moving = False
    for i in range(len(row) - 1, 0, -1):
        if moving:
            result.append(row[i-1])
        elif i > 0 and can_combine(row[i-1], row[i]):
            result.append(row[i] + row[i-1])
            moving = True
        else:
            result.append(row[i])
    if moving:
        result.append(0)
    else:
        result.append(row[0])
    result.reverse()
    return result


def swap_rows_and_cols(array):
    columns = []
    for cnum in range(len(array[0])):
        columns.append([])
        for row in array:
            columns[cnum].append(row[cnum])
    return columns


def reversed_list(lst):
    return list(reversed(lst))

def not_random_function(max):
    return 0

class Board():
    def __init__(self, array):
        self.cells = array

    def __eq__(self, other):
        return self.cells == other.cells

    def shift(self, direction, new_value=-1, random_function=not_random_function, return_moved=False):
        in_board = self.cells
        if direction in [DOWN, UP]:
            in_board = swap_rows_and_cols(in_board)
        if direction in [LEFT, UP]:
            in_board = [reversed_list(x) for x in in_board]
        new_board = []
        moved = []
        for row_idx in range(len(in_board)):
            row = in_board[row_idx]
            new_row = shift_row(row)
            if new_row != row:
                moved.append(row_idx)
            new_board.append(new_row)
        if len(moved) > 0 and new_value != -1:
            insertion_point = random_function(len(moved))
            new_board[moved[insertion_point]][0] = new_value

        out = new_board
        if direction in [LEFT, UP]:
            out = [reversed_list(x) for x in out]
        if direction in [DOWN, UP]:
            out = swap_rows_and_cols(out)
        if return_moved == False:
            return Board(out)
        return Board(out), len(moved)



default_package = [1] * 4 + [2] * 4 + [3] * 4


class ThreePackage():
    def __init__(self, items = default_package):
        self.items = list(items)

    def remove_random(self, random_function):
        if self.items != []:
            after = list(self.items)
            pos = random_function(len(after))
            v = after[pos]
            after.pop(pos)
            return v, ThreePackage(after)
        else:
            return None


class ThreeGame():
    #pro tip: passing a function as a default argument, it has to appear before the argument
    def __init__(self, random_function, shuffle_function, package_generator = generatePackage, board = None, remaining_pkg = None):
        self.randomfunction = random_function
        self.shufflefunction = shuffle_function
        if board is None:
            initial_pkg = package_generator(random_function)
            initial_items = []
            if len(initial_pkg.items) < 9:
                for i in range(len(initial_pkg.items)):
                    v, initial_pkg = initial_pkg.remove_random(random_function)
                    initial_items.append(v)
            else:
                for i in range(9):
                    v, initial_pkg = initial_pkg.remove_random(random_function)
                    initial_items.append(v)
            # Fill rest with zeros
            initial_items = initial_items + [0] * (16 - len(initial_items))
            # Shuffle
            initial_items = shuffle_function(initial_items)
            # Break into two d array
            self.board = []
            for i in range(4):
                self.board.append(initial_items[i*4:i*4+4])
            self.remaining_pkg = initial_pkg
        else:
            self.board = board
            self.remaining_pkg = remaining_pkg


    def shift(self, direction):
        board = Board(self.board)
        new_value, new_pkg = self.remaining_pkg.remove_random(self.randomfunction)
        new_board = board.shift(direction, new_value, self.randomfunction)
        if len(self.remaining_pkg.items) is 1:
            self.remaining_pkg = generatePackage(self.randomfunction, find_largest_value(board.cells))
            new_value, new_pkg = self.remaining_pkg.remove_random(self.randomfunction)
        #Pro tip: Always check each of the places where you return a new class after changing the default argument order or adding a new default argument.
        return ThreeGame(self.randomfunction, self.shufflefunction, generatePackage, new_board.cells, new_pkg)

    def isEnded(self):
        board = Board(self.board)
        if board.shift(LEFT) == board and board.shift(RIGHT) == board and board.shift(UP) == board and board.shift(DOWN) == board:
            return True
        else:
            return False

    def peek(self):
        next_item = self.remaining_pkg.items[0]
        final = []
        if next_item <= 3:
            return [next_item]
        else:
            return find_reasonable_values(next_item, find_largest_value(self.board), self.randomfunction)


def find_reasonable_values(next_item, max, random_function):
    pos = random_function(3)
    if pos == 0:
        final = next_item, next_item*2, next_item*4
    elif pos == 1:
        final = next_item/2, next_item, next_item*2
    elif pos == 2:
        final = next_item/4, next_item/2, next_item
    else:
        raise Exception("find reasonable values found an unknown position")
    final = [i for i in final if i >= 6]
    final = [i for i in final if i <= max/8]
    return final







