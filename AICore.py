__author__ = 'Duncan'

RIGHT = 0
LEFT = 1
DOWN = 2
UP = 3
from three import *
import random

defaultbcweight = -1
defaultbiweight = -1

def true_random(max):
    return random.randrange(max)


def true_shuffle(lst):
    copy = list(lst)
    random.shuffle(copy)
    return copy


class NotListException(Exception):
    pass


class AspectWeightLengthMismatchException(Exception):
    pass


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




# ASPECTS

class AIAspectBC():
    def evaluateBoard(self, board):
        value = 0
        for i in board:
            for h in i:
                if h != 0:
                    value += 1
        return value


class AIAspectBI():
    def evaluateBoard(self, board):
        value = 0
        for row_index in range(len(board)):
            row = board[row_index]
            for col_index in range(len(row)):
                current = board[row_index][col_index]
                penalty = 0
                if row_index != len(board)-1:
                    below = board[row_index+1][col_index]
                    if isinstance(below, list):
                        print "below"
                    if current != 0 and below != 0:
                        penalty += abs(current-below)
                if col_index != len(row)-1:
                    right = board[row_index][col_index+1]
                    if current != 0 and right != 0:
                        penalty += abs(current-right)
                value += penalty
        return value




#   EVALUATOR

class AIEvaluator():
    def __init__(self, aspects, weights):
        if not isinstance(aspects, list) or not isinstance(weights, list):
            raise NotListException("Error: aspects or weights is not list")
        if len(aspects) != len(weights):
            raise AspectWeightLengthMismatchException("Error: aspect/weight dimension mismatch")
        self.aspects = aspects
        self.weights = weights

    def evaluateBoard(self, board):
        total = 0
        for pos in range(len(self.aspects)):
            total += self.aspects[pos].evaluateBoard(board)*self.weights[pos]
        return total

    def checkMove(self, board, direction):
        AIBoard = Board(board)
        if AIBoard.shift(direction).cells == board:
            return False
        return True

    def evaluateMove(self, board, incoming, direction):
        firstBoard = Board(board)
        values = []
        find_shift, length = firstBoard.shift(direction, incoming, not_random_function, True)
        for i in range(length):
            newBoard = firstBoard.shift(direction, incoming, lambda x: i)
            values.append(self.evaluateBoard(newBoard.cells))
        if len(values) == 0:
            return None
        return sum(values)*1.0/len(values)





#  THINKER


class AIThinker():
    def __init__(self, evaluator):
        if isinstance(evaluator, AIEvaluator):
            self.evaluator = evaluator
        else:
            raise Exception("Thinker got an evaluator that was not an evaluator")

    def suggestMove(self, board, incoming, pkg_used = []):
        if isinstance(incoming, int):
            new_val = [incoming]
        else:
            new_val = incoming
        firstBoard = Board(board)
        values = [0] * 4
        for i in range(len(values)):
            x = self.evaluator.evaluateMove(firstBoard.cells, new_val[0], i)
            values[i] = x
        if max(values) == values[0]:
            return RIGHT
        elif max(values) == values[1]:
            return LEFT
        elif max(values) == values[2]:
            return DOWN
        else:
            return UP





#     PLAYER


class AIPlayer():
    def __init__(self, evaluator):
        if isinstance(evaluator, AIEvaluator):
            self.evaluator = evaluator
        else:
            raise Exception("AI Player got an evaluator that was not an evaluator")
        self.thinker = AIThinker(self.evaluator)

    def play_game(self):
        game = ThreeGame(true_random, true_shuffle)
        num_moves = 0
        while game.isEnded() is False:
            game = game.shift(self.thinker.suggestMove(game.board, game.peek()))
            num_moves += 1
        highest = 0
        for i in game.board:
            if max(i) > highest:
                highest = max(i)
        return num_moves, highest, game.board