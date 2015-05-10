__author__ = 'Duncan'

RIGHT = 0
LEFT = 1
DOWN = 2
UP = 3
from three import *
import random

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

#--------------ASPECTS----------------------------------------------------------

def evaluateBoardCombination(board):
        value = 0
        for i in board:
            for h in i:
                if h != 0:
                    value += 1
        return value


def evaluateBoardImbalance(board):
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

#-------------------------------------------------------------------------------


class MoreSmartAI():
    def evaluateBoard(self, board, aspects = [evaluateBoardCombination, evaluateBoardImbalance], weights = [-1, -1]):
        if len(aspects) != len(weights):
            raise Exception('Error: Dimension Mismatch in evaluateBoard')
        results = []
        for i in aspects:
            for n in weights:
                results.append(i(board)*n)
        return sum(results)

    def checkMove(self, board, direction):
        AIBoard = Board(board)
        if AIBoard.shift(direction).cells == board:
            return False
        return True

    def evaluateMoveValue(self, board, incoming, direction, aspects = [evaluateBoardCombination, evaluateBoardImbalance], weights = [-1, -1]):
        firstBoard = Board(board)
        values = []
        ignore_board, length = firstBoard.shift(direction, incoming, not_random_function, True)
        for i in range(length):
            newBoard = firstBoard.shift(direction, incoming, lambda x: i)
            values.append(self.evaluateBoard(newBoard.cells, aspects, weights))
        if len(values) == 0:
            return -666
        return sum(values)*1.0/len(values)

    def suggestMove(self, board, incoming, aspects = [evaluateBoardCombination, evaluateBoardImbalance], weights = [-1, -1]):
        firstBoard = Board(board)
        values = [0] * 4
        for i in range(len(values)):
            x = self.evaluateMoveValue(firstBoard.cells, incoming, i, aspects, weights)
            values[i] = x
        if max(values) == values[RIGHT]:
            return RIGHT
        elif max(values) == values[LEFT]:
            return LEFT
        elif max(values) == values[DOWN]:
            return DOWN
        else:
            return UP

    def play_game(self, aspects = [evaluateBoardCombination, evaluateBoardImbalance], weights = [-1, -1]):
        game = ThreeGame(true_random, true_shuffle)
        num_moves = 0
        while game.isEnded() is False:
            game = game.shift(self.suggestMove(game.board, game.peek()[true_random(len(game.peek()))], aspects, weights))
            num_moves += 1
        each_max = []
        for x in (game.board):
            each_max.append(max(x))
        return num_moves, max(each_max), game.board