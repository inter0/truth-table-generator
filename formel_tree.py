logic_operators = (r"\/", "/\\", "=>", "<=>")

def split_formel(formel):
    if len(formel) < 3:
        return None

    split_formel_arr = []
    arr = formel.split(" ")

    if arr[0] != "(":
        split_formel_arr.append(arr[0])
        split_formel_arr.append(arr[1])
        split_formel_arr.append(my_join(arr[2:], " "))
    else:
        bracket = 0
        end_index_of_subterm = 0
        for index, f in enumerate(arr):
            if f == "(":
                bracket += 1
            if f == ")":
                bracket -= 1
            if bracket == 0:
                end_index_of_subterm = index + 1
                break
        split_formel_arr.append(my_join(arr[0:end_index_of_subterm], " "))
        split_formel_arr.append(arr[end_index_of_subterm])
        split_formel_arr.append(my_join(arr[end_index_of_subterm + 1:], " "))

    split_formel_arr = list(map(remove_outer_brackets, split_formel_arr))
    
    return split_formel_arr

def remove_outer_brackets(formel):
    arr = formel.split(" ")
    bracket = 0
    end_index = 0

    for index, f in enumerate(arr):
        if f == "(":
            bracket += 1
        if f == ")":
            bracket -= 1
        if bracket == 0:
            end_index = index
            break

    if end_index == len(arr) - 1 and end_index != 0:
        return formel[2:len(formel) - 2]
    else:
        return formel

def my_join(lst, item):
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return "".join(result)

#verify_formel has errors, it states a formel is not valid if an operator like <=> has a subterm like ( a /\ b) before or after it 
def verify_formel(formel):
    arr = formel.split(" ")

    #verify brackets
    bracket = 0
    for f in arr:
        if f == "(":
                bracket += 1
        if f == ")":
            bracket -= 1
    if bracket != 0:
        return False

    #verify atoms and quantors
    #TODO: subterms before and after a logical operator return false
    for index, f in enumerate(arr):
        if f in logic_operators:
            if index == 0:
                return False
            if not (is_atom(arr[index - 1]) and is_atom(arr[index + 1])):
                return False
    return True
               
def is_atom(chr):
    atom = True
    if chr in logic_operators:
        atom = False
    if chr == "(" or chr == ")":
        atom = False
    return atom

def implies(a, b):
    a ^= 1
    return a | b

def equivalence(a, b):
    if a == b:
        return 1
    else:
        return 0

def negate(a):
    a ^= 1
    return a

def my_and(a, b):
    return a & b

def my_or(a, b):
    return a | b

class operationNode():
    def __init__(self, operator, function):
        self.operator = operator
        self.function = function

    def __str__(self):
        return self.operator

class atomNode():
    def __init__(self, atom, value, negated=False):
        self.atom = atom
        self.value = value
        self.negated = negated
    
    def __str__(self):
        return self.atom

class tree():
    functions = [my_or, my_and, implies, equivalence, negate]

    def __init__(self, formel):
        self.formel = formel
        self.top_node = self.__generate_tree()
        self.atomNodes_arr = self.__get_atomNodes()
    
    #TODO: test this
    def __generate_tree(self):
        split_formel_arr = split_formel(self.formel)

        if split_formel_arr == None:
            if self.formel[0] == "-":
                return atomNode(self.formel, 0, True)
            else:
                return atomNode(self.formel, 0)

        node0 = operationNode(split_formel_arr[1], tree.functions[logic_operators.index(split_formel_arr[1])])
        node0.node1 = tree(split_formel_arr[0])
        node0.node2 = tree(split_formel_arr[2])

        return node0

    #TODO: test this and check if every atom is in dict
    def update_values(self, value_dict):
        for key, new_value in value_dict.items():
            index = self.atomNodes_arr.index(key)
            self.atomNodes_arr[index].value = new_value

    #TODO: test this
    def __get_atomNodes(self):
        atom_node_arr = []

        if isinstance(self.top_node, atomNode):
            atom_node_arr.append(self.top_node)
        else:
            atomNode1 = self.top_node.node1.__get_atomNodes()
            atomNode2 = self.top_node.node2.__get_atomNodes()
            if atomNode1 not in atom_node_arr:
                atom_node_arr += atomNode1
            if atomNode2 not in atom_node_arr:
                atom_node_arr += atomNode2
        return atom_node_arr
