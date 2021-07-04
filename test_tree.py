import formel_tree

formel = "a => ( ( ( a \/ b ) <=> ( -c /\ d ) ) \/ c )"

formel1 = "( ( ( a \\/ b ) <=> ( -c /\\ d ) ) \\/ c )"

t = formel_tree.tree(formel)

node = t.top_node

print(node)
exit()


def print_tree(node):
    try:
        if isinstance(node, formel_tree.operationNode):
            print(f"{node} has function: {node.function}")
            print_tree(node.left_child)
            print_tree(node.right_child)
    except Exception:
        return

print_tree(node)
