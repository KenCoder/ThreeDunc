__author__ = 'Duncan'

RIGHT = 0
LEFT = 1
DOWN = 2
UP = 3
from three import *


def true_random(max):
    return random.randrange(max)


def true_shuffle(lst):
    copy = list(lst)
    random.shuffle(copy)
    return copy


class dumbAI():
    def __init__(self):
        x = 1

    def evaluateBoard(self, board):
        array = []
        current = 0
        for i in board:
            for h in i:
                current += 1
                array.append(h*current)
        return sum(array)


class MoreSmartAI():
    def evaluateBoardCombination(self, board):
        value = 0
        for i in board:
            for h in i:
                if h != 0:
                    value += 1
        return value

    def evaluateBoardImbalance(self, board):
        value = 0
        for row_index in range(len(board)):
            row = board[row_index]
            for col_index in range(len(row)):
                current = board[row_index][col_index]
                penalty = 0
                if row_index != len(board)-1:
                    below = board[row_index+1][col_index]
                    if current != 0 and below != 0:
                        penalty += abs(current-below)
                if col_index != len(row)-1:
                    right = board[row_index][col_index+1]
                    if current != 0 and right != 0:
                        penalty += abs(current-right)
                value += penalty
        return value

    def evaluateBoard(self, board, bcweight=1, biweight=-1):
        bccalc = self.evaluateBoardCombination(board)*bcweight
        bicalc = self.evaluateBoardImbalance(board)*biweight
        return bccalc+bicalc

    def checkMove(self, board, direction):
        AIBoard = Board(board)
        if AIBoard.shift(direction).cells == board:
            return False
        return True

    def evaluateMoveValue(self, board, incoming, direction, bcweight=1, biweight=-1):
        firstBoard = Board(board)
        values = []
        find_shift, length = firstBoard.shift(direction, incoming, not_random_function, True)
        for i in range(length):
            newBoard = firstBoard.shift(direction, incoming, lambda x: i)
            values.append(self.evaluateBoard(newBoard.cells, bcweight, biweight))
        if len(values) == 0:
            return -666
        return sum(values)*1.0/len(values)

    def suggestMove(self, board, incoming, bcweight=1, biweight=-1):
        firstBoard = Board(board)
        values = [0] * 4
        for i in range(len(values)):
            x = self.evaluateMoveValue(firstBoard.cells, incoming, i, bcweight, biweight)
            values[i] = x
        if max(values) == values[0]:
            return RIGHT
        elif max(values) == values[1]:
            return LEFT
        elif max(values) == values[2]:
            return DOWN
        else:
            return UP

    def play_game(self, bcweight=1, biweight=-1):
        game = ThreeGame(true_random, true_shuffle)
        num_moves = 0
        while game.isEnded() is False:
            game.shift(self.suggestMove(game.board.cells, game.peek(), bcweight, biweight))
            num_moves += 1