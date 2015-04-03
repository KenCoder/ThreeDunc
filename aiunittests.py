__author__ = 'Duncan'
import unittest
from AICore import *


class AIUnitTests(unittest.TestCase):
    def testFunctionDiscrimination(self):
        ai = dumbAI()
        self.assertNotEqual(ai.evaluateBoard([[0, 1], [0, 0]]), ai.evaluateBoard([[1, 1], [0, 0]]))
        ai = MoreSmartAI()
        self.assertNotEqual(ai.evaluateBoardCombination([[0, 1], [0, 0]]), ai.evaluateBoardCombination([[1, 1], [0, 0]]))
        self.assertNotEqual(ai.evaluateBoardImbalance([[0, 1], [0, 0]]), ai.evaluateBoardImbalance([[1, 256], [0, 0]]))

    def testCombinationAI(self):
        ai = MoreSmartAI()
        self.assertEqual(ai.evaluateBoardCombination([[1, 0], [0, 0]]), 1)
        self.assertEqual(ai.evaluateBoardCombination([[1, 3], [0, 256]]), 3)

    def testImbalanceAI(self):
        ai = MoreSmartAI()
        self.assertEqual(ai.evaluateBoardImbalance([[0, 0], [1, 2]]), 1)
        self.assertEqual(ai.evaluateBoardImbalance([[0, 3], [1, 3]]), 2)

    def testAIWeighting(self):
        ai = MoreSmartAI()
        self.assertEqual(ai.evaluateBoard([[0, 3], [1, 3]], 1, -1), 1)
        self.assertEqual(ai.evaluateBoard([[0, 3], [1, 3]], 1, -2), -1)
        self.assertEqual(ai.evaluateBoard([[1, 0], [0, 0]]), 1)

    def testAICheckValidMove(self):
        ai = MoreSmartAI()
        self.assertFalse(ai.checkMove([[0, 1], [0, 0]], RIGHT))
        self.assertTrue(ai.checkMove([[0, 1], [0, 0]], LEFT))
        self.assertFalse(ai.checkMove([[1, 3], [3, 1]], RIGHT))

    def testAIEvaluateDirection(self):
        ai = MoreSmartAI()
        self.assertEqual(ai.evaluateMoveValue([[0, 1], [0, 0]], 2, LEFT), 1)
        self.assertEqual(ai.evaluateMoveValue([[0, 1], [0, 2]], 2, LEFT), 1.5)
        self.assertEqual(ai.evaluateMoveValue([[0, 1], [0, 2]], 2, UP), 1)
        self.assertEqual(ai.evaluateMoveValue([[2, 3], [3, 2]], 123, RIGHT), -666)

    def testAIDecideDirection(self):
        ai = MoreSmartAI()
        self.assertEqual(ai.suggestMove([[1, 0], [0, 0]], 2), RIGHT)
        self.assertEqual(ai.suggestMove([[1, 1], [0, 0]], 2), DOWN)

    def testAIRunGame(self):
        ai = MoreSmartAI()
        num_moves, highest, final = ai.play_game()
        self.assertGreater(len(num_moves), 8)