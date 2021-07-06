import formel_tree as ft
import unittest

formel1 = "a => ( ( ( a \/ b ) <=> ( -c /\ d ) ) \/ c )"
formel2= "( ( ( ( a \/ b ) <=> ( -c /\ d ) ) \/ c ) )"
formel3 = "a \/ b /\ c"
formel4 = "a \/"
formel5 = "( ( a \/ b ) ) )"
formel6 = "( -a => b ) \/ ( b <=> c )"
formel7 = "( c -a => b ) \/ ( b <=> c )"

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
        self.assertEqual(ft.remove_outer_brackets(formel1), formel1)

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
        self.assertTrue(ft.verify_formel(formel1))
        self.assertTrue(ft.verify_formel(formel2))
        self.assertFalse(ft.verify_formel(formel4))
        self.assertFalse(ft.verify_formel(formel5))
        self.assertTrue(ft.verify_formel(formel6))
        self.assertFalse(ft.verify_formel(formel7))

    def test_generateTree(self):
        self.assertRaises(Exception, ft.tree, formel7)
        self.assertRaises(Exception, ft.tree, formel4)

        t3 = ft.tree(formel3)

        top_node = t3.top_node
        l_node = top_node.left_child
        r_node = top_node.right_child
        rl_node = r_node.left_child
        rr_node = r_node.right_child

        #test if nodes have the right type
        self.assertTrue(isinstance(top_node, ft.operationNode))
        self.assertTrue(isinstance(r_node, ft.operationNode))
        self.assertTrue(isinstance(l_node, ft.atomNode))
        self.assertTrue(isinstance(rl_node, ft.atomNode))
        self.assertTrue(isinstance(rr_node, ft.atomNode))
        #test if nodes have the right name/operation and function
        self.assertEqual(top_node.operation, "\/")
        self.assertEqual(top_node.function, ft.my_or)
        self.assertEqual(r_node.operation, "/\\")
        self.assertEqual(r_node.function, ft.my_and)
        self.assertEqual(l_node.name, "a")
        self.assertEqual(rl_node.name, "b")
        self.assertEqual(rr_node.name, "c")

        t1 = ft.tree(formel1)

        #just draw the tree to verify this
        top_node = t1.top_node
        l_node = top_node.left_child
        r_node = top_node.right_child
        rr_node = r_node.right_child
        rl_node = r_node.left_child
        rll_node = rl_node.left_child
        rlr_node = rl_node.right_child
        rlll_node = rll_node.left_child
        rllr_node = rll_node.right_child
        rlrl_node = rlr_node.left_child
        rlrr_node = rlr_node.right_child

        #test if nodes have the right type
        self.assertTrue(isinstance(top_node, ft.operationNode))
        self.assertTrue(isinstance(r_node, ft.operationNode))
        self.assertTrue(isinstance(rl_node, ft.operationNode))
        self.assertTrue(isinstance(rll_node, ft.operationNode))
        self.assertTrue(isinstance(rlr_node, ft.operationNode))
        self.assertTrue(isinstance(rlll_node, ft.atomNode))
        self.assertTrue(isinstance(rllr_node, ft.atomNode))
        self.assertTrue(isinstance(rlrl_node, ft.atomNode))
        self.assertTrue(isinstance(rlrr_node, ft.atomNode))
        self.assertTrue(isinstance(l_node, ft.atomNode))
        self.assertTrue(isinstance(rr_node, ft.atomNode))
        #test if nodes have the right name/operation and function
        self.assertEqual(top_node.operation, "=>")
        self.assertEqual(top_node.function, ft.implies)
        self.assertEqual(r_node.operation, "\/")
        self.assertEqual(r_node.function, ft.my_or)
        self.assertEqual(rl_node.operation, "<=>")
        self.assertEqual(rl_node.function, ft.equivalence)
        self.assertEqual(rll_node.operation, "\/")
        self.assertEqual(rll_node.function, ft.my_or)
        self.assertEqual(rlr_node.operation, "/\\")
        self.assertEqual(rlr_node.function, ft.my_and)
        self.assertEqual(l_node.name, "a")
        self.assertEqual(rr_node.name, "c")
        self.assertEqual(rllr_node.name, "b")
        self.assertEqual(rlrl_node.name, "-c")
        self.assertEqual(rlrr_node.name, "d")

        self.assertEqual(l_node, rlll_node)
        self.assertNotEqual(rlrl_node, rr_node)
        self.assertTrue(rlrl_node.negated)
        self.assertFalse(rlrr_node.negated)
        self.assertFalse(l_node.negated)

    def test_getSubtermIndices(self):
        indices6 = ft.get_subterm_indices(formel6)
        self.assertEqual(indices6, (0, 4))
        indices6 = ft.get_subterm_indices(formel6, start=4)
        self.assertEqual(indices6, (6, 10))
        indices1 = ft.get_subterm_indices(formel1)
        self.assertEqual(indices1, (2, 18))
        indices3 = ft.get_subterm_indices(formel3)
        self.assertEqual(indices3[1], -1)

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
