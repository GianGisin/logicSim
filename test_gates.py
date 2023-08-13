import unittest
from gates.gates import *

class Gates_test(unittest.TestCase):
    def test_and(self):
        gate = And_Gate()

        gate.A.trigger(False)
        gate.B.trigger(False)
        self.assertEqual(gate.Q.state, False)

        gate.A.trigger(True)
        gate.B.trigger(False)
        self.assertEqual(gate.Q.state, False)

        gate.A.trigger(True)
        gate.B.trigger(True)
        self.assertEqual(gate.Q.state, True)

    def test_or(self):
        gate = Or_Gate()

        gate.A.trigger(False)
        gate.B.trigger(False)
        self.assertEqual(gate.Q.state, False)

        gate.A.trigger(True)
        gate.B.trigger(False)
        self.assertEqual(gate.Q.state, True)

        gate.A.trigger(True)
        gate.B.trigger(True)
        self.assertEqual(gate.Q.state, True)

        


unittest.main()