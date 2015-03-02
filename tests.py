
import unittest
from three import *

def max_rand(max):
    return max-1

def test_generator(random_function, largest_value = 0):
    return ThreePackage([6])

def no_shuffle_function(items):
    return items

def also_not_random_function(max):
    return 1


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

        b = [
            [0, 1],
            [0, 1],
        ]
        self.assertEqual(Board(b).shift(RIGHT), Board([[0, 1],
                                                       [0, 1]]))

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
        removed_item, remaining_package = package.remove_first()
        self.assertEqual(removed_item, 1)
        self.assertEqual(set(remaining_package.items), set([1] * 3 + [2] * 4 + [3] * 4))
        package = ThreePackage()
        for i in range(12):
            v, package = package.remove_first()
        result = package.remove_first()
        self.assertIsNone(result)

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
        self.assertFalse(game.isEnded())

    def testGameEnd(self):
        game = ThreeGame(not_random_function, no_shuffle_function, generatePackage, [[3, 6, 3, 6],
                                                                                    [6, 3, 6, 3],
                                                                                    [3, 6, 3, 6],
                                                                                    [6, 3, 6, 3],
                                                                                    ])
        self.assertTrue(game.isEnded())


    def testBonusTile(self):
        package = generatePackage(not_random_function, 48)
        self.assertSetEqual(set(package.items), set(default_package + [6]))
        package = generatePackage(not_random_function)
        self.assertSetEqual(set(package.items), set([1]*4 + [2]*4 + [3]*4))

    def testGameGeneratePackage(self):
        game = ThreeGame(not_random_function, no_shuffle_function, test_generator)
        self.assertEqual(game.board, [[6,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])

    #Pro tip: You have to put "test" before a UnitTestCase method or else it doesn't run when you run all your tests
    def testNewPackageAfterShift(self):
        game = ThreeGame(not_random_function, no_shuffle_function, generatePackage, [[0, 0, 0, 0],
                                                                              [1, 0, 0, 0],
                                                                              [0, 0, 0, 0],
                                                                              [48, 0, 0, 0],
                                                                              ], ThreePackage([1]))
        game = game.shift(DOWN)
        self.assertIn(6, game.remaining_pkg.items)
        self.assertEqual(game.board, [[1, 0, 0, 0],
                                      [0, 0, 0, 0],
                                      [1, 0, 0, 0],
                                      [48, 0, 0, 0],
                                      ])

        game = ThreeGame(not_random_function, no_shuffle_function, generatePackage, [[0, 0, 0, 0],
                                                                                  [1, 0, 0, 0],
                                                                                  [0, 0, 0, 0],
                                                                                  [1, 0, 0, 0],
                                                                                  ], ThreePackage([1]))
        game = game.shift(DOWN)
        self.assertNotIn(6, game.remaining_pkg.items)

    def testFindLargest(self):
        self.assertEqual(find_largest_value([[0, 0, 0, 0],
                                             [1, 0, 0, 0],
                                             [0, 0, 0, 0],
                                             [1, 0, 0, 0],
                                             ]), 1)

        self.assertEqual(find_largest_value([[0, 0, 0, 0],
                                             [14, 0, 0, 0],
                                             [0, 0, 0, 0],
                                             [28, 0, 0, 0],
                                             ]), 28)

        self.assertEqual(find_largest_value([[0, 0, 0, 0],
                                             [0, 0, 0, 0],
                                             [0, 0, 0, 0],
                                             [0, 0, 0, 0],
                                             ]), 0)

    def testFindReasonableValues(self):
        self.assertEqual(find_reasonable_values(6, 48, not_random_function), [6])
        self.assertEqual(find_reasonable_values(6, 96, not_random_function), [6, 12])
        self.assertEqual(find_reasonable_values(6, 192, not_random_function), [6, 12, 24])
        self.assertEqual(find_reasonable_values(48, 768, not_random_function), [48, 96])

    def testPeek(self):
        game = ThreeGame(not_random_function, no_shuffle_function, generatePackage, [[0, 0, 0, 0],
                                                                              [1, 0, 0, 0],
                                                                              [0, 0, 0, 0],
                                                                              [48, 0, 0, 0],
                                                                              ], ThreePackage([1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]))
        self.assertEqual(game.peek(), [1])
        game = ThreeGame(not_random_function, no_shuffle_function, generatePackage, [[0, 0, 0, 0],
                                                                              [1, 0, 0, 0],
                                                                              [0, 0, 0, 0],
                                                                              [48, 0, 0, 0],
                                                                              ], ThreePackage([3]))
        self.assertEqual(game.peek(), [3])
        game = ThreeGame(not_random_function, no_shuffle_function, generatePackage, [[0, 0, 0, 0],
                                                                              [1, 0, 0, 0],
                                                                              [0, 0, 0, 0],
                                                                              [999999, 0, 0, 0],
                                                                              ], ThreePackage([48]))
        self.assertEqual(game.peek(), [48, 96, 192])
        game = ThreeGame(not_random_function, no_shuffle_function, generatePackage, [[0, 0, 0, 0],
                                                                              [1, 0, 0, 0],
                                                                              [0, 0, 0, 0],
                                                                              [48, 0, 0, 0],
                                                                              ], ThreePackage([6]))
        self.assertEqual(game.peek(), [6])
        game = ThreeGame(not_random_function, no_shuffle_function, generatePackage, [[0, 0, 0, 0],
                                                                              [1, 0, 0, 0],
                                                                              [0, 0, 0, 0],
                                                                              [96, 0, 0, 0],
                                                                              ], ThreePackage([6]))
        self.assertEqual(game.peek(), [6, 12])

    def testNoRemoveOnShift(self):
        game = ThreeGame(not_random_function, no_shuffle_function, generatePackage, [[0, 0, 0, 0],
                                                                              [1, 0, 0, 0],
                                                                              [0, 0, 0, 0],
                                                                              [96, 0, 0, 0],
                                                                              ], ThreePackage([6]))
        game.shift(LEFT)
        self.assertEqual(game.remaining_pkg.items, [6])