__author__ = 'Duncan'
import unittest
from AICore import *


class AIUnitTests(unittest.TestCase):
    def testFunctionDiscrimination(self):
        ai = dumbAI()
        self.assertNotEqual(ai.evaluateBoard([[0, 1], [0, 0]]), ai.evaluateBoard([[1, 1], [0, 0]]))
        ai = AIAspectBC()
        self.assertNotEqual(ai.evaluateBoard([[0, 1], [0, 0]]), ai.evaluateBoard([[1, 1], [0, 0]]))
        ai = AIAspectBI()
        self.assertNotEqual(ai.evaluateBoard([[0, 1], [0, 0]]), ai.evaluateBoard([[1, 256], [0, 0]]))

    def testevaluatorAI(self):
        with self.assertRaises(NotListException):
            ai = AIEvaluator([AIAspectBI(), AIAspectBI()], 4)
        with self.assertRaises(AspectWeightLengthMismatchException):
            ai =AIEvaluator([AIAspectBC(), AIAspectBI()], [1, 1, 1, 1])
        ai = AIEvaluator([AIAspectBC(), AIAspectBI()], [-1, -1])
        self.assertEqual(ai.evaluateBoard([[1, 0], [0, 0]]), -1)
        self.assertEqual(ai.evaluateBoard([[1, 3], [0, 256]]), 3)
        self.assertFalse(ai.checkMove([[0, 1], [0, 0]], RIGHT))
        self.assertTrue(ai.checkMove([[0, 1], [0, 0]], LEFT))
        self.assertFalse(ai.checkMove([[1, 3], [3, 1]], RIGHT))
        self.assertEqual(ai.evaluateMove([[0, 1], [0, 0]], 2, LEFT), -3)
        self.assertEqual(ai.evaluateMove([[0, 1], [0, 2]], 2, LEFT), -4.5)
        self.assertEqual(ai.evaluateMove([[0, 1], [0, 2]], 2, UP), -3)
        self.assertEqual(ai.evaluateMove([[2, 3], [3, 2]], 123, RIGHT), -666)

    def testImbalanceAI(self):
        ai = AIAspectBI()
        self.assertEqual(ai.evaluateBoard([[0, 0], [1, 2]]), 1)
        self.assertEqual(ai.evaluateBoard([[0, 3], [1, 3]]), 2)

    def testHighestValueAI(self):
        ai = AIAspectHV()
        self.assertEqual(ai.evaluateBoard([[0, 0], [1, 2]]), 2)
        self.assertEqual(ai.evaluateBoard([[0, 96], [1, 2]]), 96)

    def testAIWeighting(self):
        ai = AIEvaluator([AIAspectBC(), AIAspectBI()], [1, -1])
        self.assertEqual(ai.evaluateBoard([[0, 3], [1, 3]]), 1)
        ai = AIEvaluator([AIAspectBC(), AIAspectBI()], [1, -2])
        self.assertEqual(ai.evaluateBoard([[0, 3], [1, 3]]), -1)

    def testAIDecideDirection(self):
        aievaluator = AIEvaluator([AIAspectBC(), AIAspectBI()], [-1, -1])
        aithinker = AIThinker(aievaluator)
        self.assertEqual(aithinker.suggestMove([[1, 0], [0, 0]], 2), RIGHT)
        self.assertEqual(aithinker.suggestMove([[1, 1], [0, 0]], 2), DOWN)

    def testAIRunGame(self):
        aievaluator = AIEvaluator([AIAspectBC(), AIAspectBI()], [-1, -1])
        aiplayer = AIPlayer(aievaluator)
        num_moves, highest, final = aiplayer.play_game()
        self.assertGreater(num_moves, 8)

    def testRepeatedRun(self):
        finalresn = []
        for bc in range(-10, 11):
            for bi in range(-10, 11):
                evaluator = AIEvaluator([AIAspectBC(), AIAspectBI()], [bc, bi])
                player = AIPlayer(evaluator)
                results = []
                for i in range(20):
                    num_moves, highest, final = player.play_game()
                    results.append(highest)
                print str(bc) + ", " + str(bi)
                print results
                print sum(results)/len(results)
                finalresn.append((sum(results)/len(results), str(bc) + ", " + str(bi)))
                print " "
        print reversed_list(sorted(finalresn))
