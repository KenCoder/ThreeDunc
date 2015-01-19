RIGHT = 0
LEFT = 1
DOWN = 2
UP = 3
from random import *


def can_combine(a, b):
    if b == 0:
        return True
    elif a in [1,2]:
        return a+b == 3
    else:
        return a == b


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

    def shift(self, direction, new_value = -1, random_function = not_random_function):
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
        return Board(out)

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
    def __init__(self, randomfunction, shufflefunction, board = None, remaining_pkg = None):
        self.randomfunction = randomfunction
        self.shufflefunction = shufflefunction
        if board is None:
            initial_pkg = ThreePackage()
            initial_items = []
            for i in range(9):
                v, initial_pkg = initial_pkg.remove_random(randomfunction)
                initial_items.append(v)
            # Fill rest with zeros
            initial_items = initial_items + [0] * (16 - len(initial_items))
            # Shuffle
            initial_items = shufflefunction(initial_items)
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
        if self.remaining_pkg.remove_random(self.randomfunction) != None:
            new_value, new_pkg = self.remaining_pkg.remove_random(self.randomfunction)
        else:
            self.remaining_pkg = ThreePackage(default_package)
            new_value, new_pkg = self.remaining_pkg.remove_random(self.randomfunction)
        new_board = board.shift(direction, new_value, self.randomfunction)
        return ThreeGame(self.randomfunction, self.shufflefunction, new_board.cells, new_pkg)

    def isEnded(self):
        board = Board(self.board)
        if board.shift(LEFT) == board and board.shift(RIGHT) == board and board.shift(UP) == board and board.shift(DOWN) == board:
            return True
        else:
            return False



