import warnings

logic_operators = (r"\/", "/\\", "=>", "<=>")

#TODO: description for split_formel
def split_formel(formel):
    """
    |   insert description here
    """
    #remove unnecessary brackets
    formel = remove_outer_brackets(formel)
    split_formel_arr = []
    arr = formel.split(" ")

    #smallest split formel is something like a /\ b
    #if the length is smaller then 3, then you dont have a left and right term and an operation between them
    if len(arr) < 3:
        return None
    
    if arr[0] != "(":
        #thats the easy case
        #just get the first atom, the operator after it and the rest is the right subterm
        split_formel_arr.append(arr[0])
        split_formel_arr.append(arr[1])
        split_formel_arr.append(my_join(arr[2:], " "))
    else:
        #find the end of the subterm which the brackets encloses, which is the left term
        #assume formel is valid, so I dont have to check if get_subterm_indices returns None
        #if formel is valid and formel starts with (, which means there has to be a closing bracket
        end_index_of_subterm = get_subterm_indices(formel)[1] + 1
        split_formel_arr.append(my_join(arr[0:end_index_of_subterm], " "))
        split_formel_arr.append(arr[end_index_of_subterm])
        split_formel_arr.append(my_join(arr[end_index_of_subterm + 1:], " "))

    split_formel_arr = list(map(remove_outer_brackets, split_formel_arr))
    
    return split_formel_arr

def remove_outer_brackets(formel):
    """
    |   remove the outermost brackets
    |   if the bracket at the first formel position (formel[0]) closes at the end of the formel (formel[-1])
    """

    while True:
        arr = formel.split(" ")
        indices = get_subterm_indices(formel)
        #subterm does not close, which means, with the assumption that the formel is valid that all outer brackets are removed
        if indices == None:
            break

        if indices[0] == 0 and indices[1] == len(arr) - 1:
            formel = formel[2:len(formel) - 2]
        else:
            break

    return formel

def my_join(lst, item):
    """
    |   same as "".join(lst), just insert item between every lst element
    """
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
                continue
        if f == ")":
            bracket -= 1
            #prevent the case ") ...some stuff... ("
            if bracket < 0:
                return False

    if bracket != 0:
        return False

    #verify atoms and quantors
    for index, f in enumerate(arr):
        #check that either an atom or an bracket is before and after an logic operator
        #brackets are correctly placed, so I dont have to check that again
        if f in logic_operators:
            if index == 0 or index == len(arr) - 1:
                return False
            if arr[index - 1] in logic_operators or arr[index + 1] in logic_operators:
                return False
        #check that between every atom is either a logic operator or a bracket
        elif is_atom(f):
            if index == 0 or index == len(arr) - 1:
                continue
            elif is_atom(arr[index - 1]) or is_atom(arr[index + 1]):
                return False
    return True

def get_subterm_indices(formel, start=None):
    """
    |   Returns a tuple with the start and end index of the innermost first subterm after the start index
    |   if there is no subterm or it does not close, return None
    |   This method returns indices of the formel.split(" ") array!
    """
    if start == None:
        start = 0

    arr = formel.split(" ")

    #move start to first opening bracket
    while start < len(arr) and arr[start] != "(":
        start += 1
    
    end_index = 0
    bracket = 0

    for i in range(start, len(arr)):
        if arr[i] == "(":
            bracket += 1
        elif arr[i] == ")":
            bracket -= 1
        if bracket == 0:
            end_index = i
            break
    
    if end_index == 0:
        return None
        
    return (start, end_index)

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
    def __init__(self, operation, function):
        self.operation = operation
        self.function = function
        self.left_child = None
        self.right_child = None
        self.up_to_date_value = False
        self.string = None
        self.value = 0

    def get_value(self):
        if not self.up_to_date_value:
            self.value = self.function(self.left_child.get_value(), self.right_child.get_value())
            self.up_to_date_value = True
        return self.value 

    def __str__(self):
        if self.string == None:
            self.string = f"( {str(self.left_child)} {self.operation} {self.right_child} )"
        return self.string

class atomNode():
    def __init__(self, name, value, negated):
        self.name = name
        self.value = value
        self.negated = negated
    
    def get_value(self):
        return self.value
    
    def __str__(self):
        return self.name

class tree():
    functions = [my_or, my_and, implies, equivalence, negate]

    def __init__(self, formel):
        if not verify_formel(formel):
           raise Exception("Not a valid formel")
        self.formel = formel
        self.atomNode_arr = []
        self.top_node = self.__generate_tree()

    def __generate_tree(self):
        split_formel_arr = split_formel(self.formel)

        #if formel cant be split more, this is an atom
        if split_formel_arr == None:
            negated = True if self.formel[0] == "-" else False
            value = 1 if negated else 0
            node = atomNode(self.formel, value, negated)
            self.atomNode_arr.append(node)
            return node

        #create new operationNode and recursively build tree
        #set childs of this operationNode
        node = operationNode(split_formel_arr[1], tree.functions[logic_operators.index(split_formel_arr[1])])
        left_subtree = tree(split_formel_arr[0])
        right_subtree = tree(split_formel_arr[2])
        self.atomNode_arr = left_subtree.atomNode_arr + right_subtree.atomNode_arr
        node.left_child = left_subtree.top_node
        node.right_child = right_subtree.top_node
        self.left_subtree = left_subtree
        self.right_subtree = right_subtree

        return node

    def update_values(self, value_dict):
        atom_names_arr = self.__get_atom_names(with_negated=False, sort_arr=False)

        #check if atom of value_dict is a atom in this tree and if it does assign new value to it
        #TODO: check if atom exists as negated atom in formel, because non negated atom that only exists as negated in formel gives a warning
        for atom_name, new_value in value_dict.items():
            if atom_name not in atom_names_arr:
                warning_msg = f"Atom {atom_name} is not a atom in this tree."
                if atom_name[0] == "-":
                    warning_msg += "\nNegated atoms are automaticly set to the negated value of the non negated value of the corresponding node"
                    warning_msg += "\nIf this atom only exists negated in this formel then you can ignore this warning"
                warnings.warn(warning_msg)
                continue
            nodes = self.__get_atomNodes_by_name(atom_name)
            for node in nodes:
                node.value = new_value
        
        for negated_atom in [atom for atom in self.atomNode_arr if atom.negated]:
            new_value = negate(value_dict[negated_atom.name[1:]])
            negated_atom.value = new_value

        #update operationNodes up_to_date_value to False
        self.__update_operationNodes()

    def __get_atomNodes_by_name(self, name):
        node_arr = []
        for node in self.atomNode_arr:
            if node.name == name:
                node_arr.append(node)
        return node_arr

    def __update_operationNodes(self):
        if isinstance(self.top_node, operationNode):
            self.top_node.up_to_date_value = False
            self.left_subtree.__update_operationNodes()
            self.right_subtree.__update_operationNodes()
        
    def __get_atom_names(self, with_negated=True, sort_arr=False):
        atom_names_arr = [atom.name for atom in self.atomNode_arr]

        if not with_negated:
            for atom in self.atomNode_arr:
                if atom.negated:
                    atom_names_arr.remove(atom.name)
            
        return atom_names_arr if not sort_arr else sorted(atom_names_arr)
    
    def evaluate(self):
        evaluated_dict = self.__evaluate_tree()
        sorted_dict = {key: value for key, value in sorted(evaluated_dict.items(), key= lambda item: len(item[0]))}

        return sorted_dict

    def __evaluate_tree(self):
        #evaluate actually recursivly evaluates all operationNodes via get_value
        if isinstance(self.top_node, atomNode):
            atomDict = {}
            if self.top_node.negated:
                atomDict = {str(self.top_node): self.top_node.get_value()}
            return atomDict

        dict = {}
        operation_dict = {str(self.top_node): self.top_node.get_value()}
        dict_of_left_child = self.left_subtree.__evaluate_tree()
        dict_of_right_child = self.right_subtree.__evaluate_tree()

        #update dict merges duplicate nodes together
        dict.update(dict_of_left_child)
        dict.update(dict_of_right_child)
        dict.update(operation_dict)

        return dict
