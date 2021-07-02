logic_operators = (r"\/", "/\\", "=>", "<=>", "(", ")")

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

    return split_formel_arr

def my_join(lst, item):
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return "".join(result)

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


"""
binary tree for the formel

"""

class operatorNode():
    def __init__(self, operator, function):
        self.operator = operator
        self.function = function
        self.node1 = None
        self.node2 = None

class atomNode():
    def __init__(self, atom, value):
        pass

class tree():
    def __init__(self, formel, functionArray):
        self.formel = formel
    
    def generate_tree(self):
        split_formel_arr = split_formel(self.formel)
        if split_formel_arr == None:
            return atomNode(self.formel, 0)
        node0 = operatorNode(split_formel_arr[1], None)
        subTree1 = tree(split_formel_arr[0], None)
        subTree2 = tree(split_formel_arr[2], None)
        node0.node1 = subTree1.generate_tree()
        node0.node1 = subTree2.generate_tree()


    def __str__(self):
        pass
    