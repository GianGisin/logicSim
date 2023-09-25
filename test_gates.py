import unittest
from gates.gates import *


class Gates_test(unittest.TestCase):
    def test_not(self):
        gate = Not_Gate()

        gate.A.trigger(False)
        self.assertEqual(gate.Q.state, True)

        gate.A.trigger(True)
        self.assertEqual(gate.Q.state, False)

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

    def test_xor(self):
        gate = Xor_Gate()

        gate.A.trigger(False)
        gate.B.trigger(False)
        self.assertEqual(gate.Q.state, False)

        gate.A.trigger(True)
        gate.B.trigger(False)
        self.assertEqual(gate.Q.state, True)

        gate.A.trigger(True)
        gate.B.trigger(True)
        self.assertEqual(gate.Q.state, False)

    def test_nand(self):
        gate = Nand_Gate()

        gate.A.trigger(False)
        gate.B.trigger(False)
        self.assertEqual(gate.Q.state, True)

        gate.A.trigger(True)
        gate.B.trigger(False)
        self.assertEqual(gate.Q.state, True)

        gate.A.trigger(True)
        gate.B.trigger(True)
        self.assertEqual(gate.Q.state, False)

    def test_nor(self):
        gate = Nor_Gate()

        gate.A.trigger(False)
        gate.B.trigger(False)
        self.assertEqual(gate.Q.state, True)

        gate.A.trigger(True)
        gate.B.trigger(False)
        self.assertEqual(gate.Q.state, False)

        gate.A.trigger(True)
        gate.B.trigger(True)
        self.assertEqual(gate.Q.state, False)

    def test_xnor(self):
        gate = Xnor_Gate()

        gate.A.trigger(False)
        gate.B.trigger(False)
        self.assertEqual(gate.Q.state, True)

        gate.A.trigger(True)
        gate.B.trigger(False)
        self.assertEqual(gate.Q.state, False)

        gate.A.trigger(True)
        gate.B.trigger(True)
        self.assertEqual(gate.Q.state, True)

    def test_half_adder(self):
        g_xor = Xor_Gate()  # sum bit
        g_and = And_Gate()  # carry bit

        A = Connector("input A")
        A.connect(g_xor.A)
        A.connect(g_and.A)

        B = Connector("input B")
        B.connect(g_xor.B)
        B.connect(g_and.B)

        A.send(True)
        B.send(True)

        self.assertEqual(g_xor.Q.state, False)
        self.assertEqual(g_and.Q.state, True)

        A.send(False)

        self.assertEqual(g_xor.Q.state, True)
        self.assertEqual(g_and.Q.state, False)

        B.send(False)
        self.assertEqual(g_xor.Q.state, False)
        self.assertEqual(g_and.Q.state, False)

    def test_full_adder(self):
        # initialize gates
        g_xor = Xor_Gate()
        g_sum = Xor_Gate()
        g_carry = Or_Gate()
        g_and1 = And_Gate()
        g_and2 = And_Gate()

        # initialize Inputs
        A = Connector("Input A")
        B = Connector("Input B")
        C = Connector("Input Cin")

        # setup connections from inputs
        A.connect(g_xor.A)
        A.connect(g_and1.A)
        B.connect(g_xor.B)
        B.connect(g_and1.B)
        C.connect(g_sum.B)
        C.connect(g_and2.B)

        # setup connections to output
        g_xor.Q.connect(g_sum.A)
        g_xor.Q.connect(g_and2.A)
        g_and1.Q.connect(g_carry.B)
        g_and2.Q.connect(g_carry.A)

        # truth table  A      B      Cin    Sum    Carry
        truth_table = [
            [False, False, False, False, False],
            [False, False, True, True, False],
            [False, True, False, True, False],
            [False, True, True, False, True],
            [True, False, False, True, False],
            [True, False, True, False, True],
            [True, True, False, False, True],
            [True, True, True, True, True],
        ]

        for row in truth_table:
            A.send(row[0])
            B.send(row[1])
            C.send(row[2])

            self.assertEqual(g_sum.Q.state, row[3])
            self.assertEqual(g_carry.Q.state, row[4])


if __name__ == "__main__":
    unittest.main()
