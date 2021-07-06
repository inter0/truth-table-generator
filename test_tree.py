import formel_tree as ft
import unittest

formel1 = "a => ( ( ( a \/ b ) <=> ( -c /\ d ) ) \/ c )"
formel2= "( ( ( ( a \/ b ) <=> ( -c /\ d ) ) \/ c ) )"
formel3 = "a \/ b /\ c"
formel4 = "a \/"

class testTree(unittest.TestCase):
    def test_splitFormel(self):
        split_formel3 = ft.split_formel(formel3)
        self.assertEqual(split_formel3, ["a", "\/", "b /\ c"])
        split_formel3 = ft.split_formel(split_formel3[2])
        self.assertEqual(split_formel3, ["b", "/\\", "c"])
        split_formel3 = ft.split_formel(split_formel3[2])
        self.assertIsNone(split_formel3)

        self.assertIsNone(ft.split_formel(formel4))

        split_formel1 = ft.split_formel(formel1)
        self.assertEqual(split_formel1, ["a", "=>", "( ( a \/ b ) <=> ( -c /\ d ) ) \/ c"])
        split_formel1 = ft.split_formel(split_formel1[2])
        self.assertEqual(split_formel1, ["( a \/ b ) <=> ( -c /\ d )", "\/", "c"])
        split_formel1 = ft.split_formel(split_formel1[0])
        self.assertEqual(split_formel1, ["a \/ b", "<=>", "-c /\ d"])
        split_formel1 = ft.split_formel(split_formel1[2])
        self.assertEqual(split_formel1, ["-c", "/\\", "d"])

    def test_removeOuterBrackets(self):
        outer_brackets_removed = ft.remove_outer_brackets(formel2)
        self.assertEqual(outer_brackets_removed, "( ( a \/ b ) <=> ( -c /\ d ) ) \/ c")
        nothing_to_do = ft.remove_outer_brackets(formel3)
        self.assertEqual(nothing_to_do, formel3)

    def test_implies(self):
        self.assertEqual(ft.implies(0, 0), 1)
        self.assertEqual(ft.implies(0, 1), 1)
        self.assertEqual(ft.implies(1, 0), 0)
        self.assertEqual(ft.implies(1, 1), 1)

    def test_equivalence(self):
        self.assertEqual(ft.equivalence(0, 0), 1)
        self.assertEqual(ft.equivalence(0, 1), 0)
        self.assertEqual(ft.equivalence(1, 0), 0)
        self.assertEqual(ft.equivalence(1, 1), 1)

    def test_negate(self):
        self.assertEqual(ft.negate(0), 1)
        self.assertEqual(ft.negate(1), 0)

    def test_myAnd(self):
        self.assertEqual(ft.my_and(0, 0), 0)
        self.assertEqual(ft.my_and(0, 1), 0)
        self.assertEqual(ft.my_and(1, 0), 0)
        self.assertEqual(ft.my_and(1, 1), 1)

    def test_myOr(self):
        self.assertEqual(ft.my_or(0, 0), 0)
        self.assertEqual(ft.my_or(0, 1), 1)
        self.assertEqual(ft.my_or(1, 0), 1)
        self.assertEqual(ft.my_or(1, 1), 1)

    def test_verifyFormel(self):
        pass

    def test_generateTree(self):
        pass

    def test_updateValues(self):
        pass

    def test_getAtomNodeByName(self):
        pass

    def test_updateOperationNode(self):
        pass

    def test_getAtomNames(self):
        pass

    def test_evaluate(self):
        pass


if __name__ == "__main__":
    unittest.main()
