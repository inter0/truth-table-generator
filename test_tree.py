import formel_tree

formel = "a => ( ( ( a \/ b ) <=> ( -c /\ d ) ) \/ c )"

formel1 = "( ( ( a \\/ b ) <=> ( -c /\\ d ) ) \\/ c )"

tree = formel_tree.tree(formel)
tree.generate_tree()

node = tree.top_node

def print_tree(node):
    try:
        print(node)
        print(f"{node.node1}\t{node.node2}")
        print_tree(node.node1)
        print_tree(node.node2)
    except Exception:
        return

print_tree(node)
