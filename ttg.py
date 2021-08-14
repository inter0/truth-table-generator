from pylatex import Document
from pylatex.package import Package
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
            formel = file.read()
    except Exception as e:
        print(f"Error opening/reading the input file: {e}")
        exit()

    for var in formel.split(" "):
        if var not in logic_operators:
            var = var.replace("-", "")
            variables.update({var: 0})
    
    t = ft.tree(formel)
    evaluated = t.evaluate()
    init_table(doc, len(variables) + len(evaluated))
    #write header of table
    table_write_line(doc, list(variables.keys()) + list(evaluated.keys()))

    for model in models(variables):
        last_line = True if sum(model) == len(variables) else False 
        t.update_values(variables)
        evaluated = t.evaluate() 
        table_write_line(doc, model + list(evaluated.values()), last_line)
    
    return

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
        for index, ele in enumerate(arr):
            ele = ele.replace("-", " \\neg ")
            ele = ele.replace(" /\\ ", " \\land ")
            ele = ele.replace(" \\/ ", " \\lor ")
            #implies requires to use a math package and i dont know how to include it
            ele = ele.replace(" => ", " \\implies ")
            ele = ele.replace(" <=> ", " \\iff ")
            arr[index] = "$" + ele + "$"
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
    p.add_argument("-k", "--keep-tex", help="Keep the .tex file after the pdf got created", default=True, action="store_false")
    args = p.parse_args()

    geometry_options = {"lmargin": "0.5cm", "tmargin": "2cm"}

    doc = Document(default_filepath=args.output.replace(".pdf", ""), indent=False, page_numbers=False, geometry_options=geometry_options)
    doc.packages.append(Package("amsmath"))

    main(args.input, doc)

    end_table(doc)
    doc.generate_pdf(clean_tex=args.keep_tex)