import formel_tree as ft

formel = "a => ( ( ( a \/ b ) <=> ( -c /\ d ) ) \/ c )"
formel1 = "( ( ( a \\/ b ) <=> ( -c /\\ d ) ) \\/ c )"
formel2 = "a \\/ b /\\ c" #hier stimmt die auswertungsreihenfolge nicht (wenn man sie von links nach rechts auswertet)

t = ft.tree(formel)

node = t.top_node

dict = {"a": 0, "b": 0, "c": 0, "d": 0}

print(t.formel)
print(node.get_value())
print(t.evaluate(node))
exit()


def print_tree(node):
    try:
        if isinstance(node, ft.operationNode):
            print(f"{node.operation} has function: {node.function}")
            print_tree(node.left_child)
            print_tree(node.right_child)
    except Exception:
        return

print_tree(node)
