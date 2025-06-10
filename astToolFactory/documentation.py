"""A warehouse for docstrings added to manufactured ast tools.
NOTE Use special indentation in this file.
    1. The generated files use spaces, not tabs, so use spaces here.
    2. As of this writing, I only know how to _manually_ align the indentation of the docstrings with the associated code. So, indent one or two levels as appropriate."""
from astToolFactory import settingsManufacturing
from astToolkit import Make
from collections import defaultdict
import ast

docstrings: dict[str, dict[str, ast.Expr]] = defaultdict(lambda: defaultdict(lambda: Make.Expr(Make.Constant(''))))
diminutive2etymology: dict[str, str] = {}

docstringWarning = Make.Expr(Make.Constant("""This file is generated automatically, so changes to this file will be lost."""))

def getMoreDocstrings():
    import astToolFactory.documentationBe
    import astToolFactory.documentationClassIsAndAttribute
    import astToolFactory.documentationDOT
    import astToolFactory.documentationGrab
    import astToolFactory.documentationMake

getMoreDocstrings()