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

    def test_half_adder(self):
        g_xor = Xor_Gate() # sum bit
        g_and = And_Gate() # carry bit

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

        

unittest.main()