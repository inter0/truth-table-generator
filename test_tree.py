import formel_tree as ft

def test_splitFormel():
    pass

def test_removeOuterBrackets():
    pass

def test_verifyFormel():
    pass

def test_updateValues():
    pass

def test_getAtomNodeByName():
    pass

def test_updateOperationNode():
    pass

def test_getAtomNames():
    pass

def test_evaluate():
    pass

formel = "a => ( ( ( a \/ b ) <=> ( -c /\ d ) ) \/ c )"
formel1 = "( ( ( a \\/ b ) <=> ( -c /\\ d ) ) \\/ c )"
formel2 = "a \\/ b /\\ c" #hier stimmt die auswertungsreihenfolge nicht (wenn man sie von links nach rechts auswertet)

t = ft.tree(formel)
