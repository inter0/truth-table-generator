from pylatex import Document
from pylatex.utils import NoEscape
import argparse
import formel_tree as ft


def models(vars):
    """
    This function iterates over every model of this formel,
    it yields an array of the new values and updates the vars dictionary
    """
    for i in range(2**len(vars)):
        bin_str = bin(i)[2:]
        if len(bin_str) < len(vars):
            bin_str = "0"*(len(vars) - len(bin_str)) + bin_str
        new_values = [int(t) for t in bin_str]
        for value, var in zip(new_values, vars):
            vars[var] = value
        yield new_values

def main(in_file, doc):
    variables = {}
    logic_operators = (r"\/", "/\\", "=>", "<=>", "(", ")")

    try:
        with open(in_file, "r") as file:
            formular = file.read()
    except Exception as e:
        print(f"Error opening/reading the input file: {e}")
        exit()

    for var in formular.split(" "):
        if var not in logic_operators:
            var = var.replace("-", "")
            variables.update({var: 0})

    init_table(doc, len(variables))
    #with \\land /\ and \\lor \/

    for model in models(variables):
        #models should return an dic with the updated values for the variables
        #so just updated values in the tree
        #evaluate
        #write line to doc
        pass

def init_table(doc, size):
    center = "|".join(["c"]*size)
    start_table = r"\begin{tabular}{" + center + "}"
    doc.append(NoEscape(start_table))

def table_write_line(doc, arr, last_line=False):
    arg_str = ""
    #if we write values to the table
    if not isinstance(arr[0], str):
        arg_str = " & ".join(map(str, arr))
    else:
        #if we write atoms and subformules
        #just put a & between every element of arr
        arg_str = " & ".join(arr)
    line = arg_str + r"\\"

    if not last_line:
        line += r" \hline"
    doc.append(NoEscape(line))

def end_table(doc):
    doc.append(NoEscape(r"\end{tabular}"))

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("input", help="The file with the logic you want the truth table for", type=str)
    p.add_argument("output", help="The filename were you want to save the pdf with the truth table", type=str)
    #p.add_argument("-v", "--verbose", help="If a variable occurs negated in the formular, print the negated and non negated value to the table. Default is to not print the negated value", type=bool, default=False)
    args = p.parse_args()

    doc = Document(args.output.replace(".pdf", ""))

    main(args.input, doc)

    end_table(doc)
    doc.generate_pdf()