
import unittest
from three import *

def max_rand(max):
    return max-1


def no_shuffle_function(items):
    return items


class ThreesUnitTests(unittest.TestCase):
    def testBoard(self):
        a = [
            [1, 2],
            [1, 0],
        ]
        self.assertEqual(Board(a).shift(RIGHT).cells, [[0, 3],
                                                       [0, 1]])
        b = [
            [1, 0],
            [1, 0],
        ]
        self.assertEqual(Board(b).shift(RIGHT).cells, [[0, 1],
                                                       [0, 1]])

        self.assertEqual(Board([[1, 1],
                                [3, 3]]).shift(RIGHT).cells, [[1, 1],
                                                              [0, 6]])

        self.assertEqual(Board([[2, 2],
                                [3, 3]]).shift(RIGHT).cells, [[2, 2],
                                                              [0, 6]])
        self.assertEqual(Board([[1, 0, 2],
                                [0, 1, 2]]).shift(RIGHT).cells, [[0, 1, 2],
                                                                 [0, 0, 3]])

        self.assertEqual(Board([[1, 0, 0, 2],
                                [0, 0, 1, 2]]).shift(RIGHT).cells, [[0, 1, 0, 2],
                                                                    [0, 0, 0, 3]])
        self.assertEqual(Board([[3, 6],
                                [12, 12]]).shift(RIGHT).cells, [[3, 6],
                                                                [0, 24]])

        self.assertEqual(Board([[1, 2],
                                [1, 0]]).shift(LEFT).cells, [[3, 0],
                                                             [1, 0]])

        self.assertEqual(Board([[3, 3],
                                [6, 6]]).shift(LEFT).cells, [[6, 0],
                                                             [12, 0]])

        self.assertEqual(Board([[3, 3],
                                [2, 2]]).shift(LEFT).cells, [[6, 0],
                                                             [2, 2]])

        self.assertEqual(Board([[1, 3],
                                [2, 3]]).shift(DOWN).cells, [[0, 0],
                                                             [3, 6]])

        self.assertEqual(Board([[2, 3],
                                [2, 3]]).shift(DOWN).cells, [[2, 0],
                                                             [2, 6]])

        self.assertEqual(Board([[2, 3, 0, 1],
                                [2, 3, 1, 2]]).shift(DOWN).cells, [[2, 0, 0, 0],
                                                                   [2, 6, 1, 3]])

        self.assertEqual(Board([[2, 3],
                                [1, 3]]).shift(UP).cells, [[3, 6],
                                                           [0, 0]])

        self.assertEqual(Board([[1, 0],
                                [1, 0]]).shift(RIGHT, new_value = 2, random_function=not_random_function)
                         .cells, [[2, 1],
                                  [0, 1]])

        self.assertEqual(Board([[0, 1],
                                [1, 0]]).shift(LEFT, new_value = 2, random_function=not_random_function)
                         .cells, [[1, 2],
                                  [1, 0]])

        self.assertEqual(Board([[1, 3],
                                [1, 3]]).shift(DOWN, new_value=2, random_function=not_random_function).cells,
                         [[1, 2],
                          [1, 6]])

        self.assertEqual(Board([[1, 1],
                                [1, 1]]).shift(LEFT, new_value=2, random_function=not_random_function)
                         .cells, [[1, 1],
                                  [1, 1]])

    all_items = [1] * 4 + [2] * 4 + [3] * 4
    all_set = set(all_items)

    def testPackage(self):
        package = ThreePackage()
        self.assertEqual(set(package.items), self.all_set)
        removed_item, remaining_package = package.remove_random(not_random_function)
        self.assertEqual(removed_item, 1)
        self.assertEqual(set(remaining_package.items), set([1] * 3 + [2] * 4 + [3] * 4))
        self.assertEqual(package.remove_random(max_rand)[0], 3)

        package = ThreePackage()
        for i in range(12):
            v, package = package.remove_random(not_random_function)
        self.assertIsNone(package.remove_random(not_random_function))

    def testGame(self):
        game = ThreeGame(not_random_function, no_shuffle_function)
        self.assertEqual(game.board, [ [1, 1, 1, 1],
                                       [2, 2, 2, 2],
                                       [3, 0, 0, 0],
                                       [0, 0, 0, 0]
                                        ])
        game = ThreeGame(not_random_function, reversed_list)
        self.assertEqual(game.board, [[0, 0, 0, 0],
                                      [0, 0, 0, 3],
                                      [2, 2, 2, 2],
                                      [1, 1, 1, 1],
                                      ])

        game = game.shift(DOWN)
        self.assertEqual(game.board, [[3, 0, 0, 0],
                                      [0, 0, 0, 0],
                                      [0, 0, 0, 3],
                                      [3, 3, 3, 3],
                                      ])

        game = game.shift(DOWN)
        self.assertEqual(game.board, [[3, 0, 0, 0],
                                      [3, 0, 0, 0],
                                      [0, 0, 0, 0],
                                      [3, 3, 3, 6],
                                      ])

        game = game.shift(DOWN)
        self.assertEqual(game.board, [[3, 0, 0, 0],
                                      [3, 0, 0, 0],
                                      [3, 0, 0, 0],
                                      [3, 3, 3, 6],
                                      ])
        game = game.shift(DOWN)
        self.assertEqual(game.board, [[1, 0, 0, 0],
                                      [3, 0, 0, 0],
                                      [3, 0, 0, 0],
                                      [6, 3, 3, 6],
                                      ])
