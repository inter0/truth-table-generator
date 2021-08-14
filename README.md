# Truth Table Generator
A Python program that evaulates propositional calculus and writes it into an pdf file.
## Installation
You need to have LaTeX and perl installed. `pip install -r requirements.txt` will install all other dependencies. This program only depends on pylatex and argparse. PyLaTeX requires a Python version of 3.3+ and Perl.
## Usage
`python ttg.py [-k] logic.txt output.pdf` will read the propositional calculus from the first positional argument logic.txt, evaluates it, creates a LaTeX table and generates a pdf out of it. The second positional argument is the name of the pdf file. With the -k keyword argument, you keep the generated .tex file. 
### logic.txt
This is the file that contains the propostional calculus. You can name this file however you like but it is important that you have a space between every proposition like /\\, a, -b, etc and brackets. 
* Or: \\/
* And: /\\
* Implies: =>
* Equvalence: <=>
* Negation: -a

This program will evaluate negation first, then propositions between brackets and then the rest.
__Note that the evaluation order is not automaticly left to right__ 
a /\\ b \\/ c will evaluate as a /\\ ( b \\/ c ). If you want to make sure the evaluation order is correct, use brackets.
# Output
a => ( ( ( a \/ b ) <=> ( -c /\ d ) ) \/ c ) will generate the table below

![alt resulting table](https://github.com/inter0/truth-table-generator/blob/main/readme/result.png)
