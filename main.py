from pylatex import Document
from pylatex.utils import NoEscape
import argparse

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
    table_write_line(doc, list(variables.keys()))

    for i in range(2**len(variables)):
        if i == 0:
            table_write_line(doc, list(variables.values()))
            continue
        index = 0
        for key, value in variables.items():
            rythm = 2**(len(variables)-index-1)
            index += 1
            if i % rythm == 0:
                value ^= 1
                variables.update({key: value})
        if i == 2**len(variables) - 1:
            table_write_line(doc, list(variables.values()), True)
            continue
        table_write_line(doc, list(variables.values()))


def init_table(doc, size):
    center = "|".join(["c"]*size)
    start_table = r"\begin{tabular}{" + center + "}"
    doc.append(NoEscape(start_table))

def table_write_line(doc, arr, last_line=False):
    arg_str = ""
    if not isinstance(arr[0], str):
        arg_str = " & ".join(map(str, arr))
    else:
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