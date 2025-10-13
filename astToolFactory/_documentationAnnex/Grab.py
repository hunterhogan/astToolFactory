"""A warehouse for docstrings added to manufactured ast tools.

NOTE Use special indentation in this file.
    1. The generated files use spaces, not tabs, so use spaces here.
    2. As of this writing, I only know how to _manually_ align the indentation of the docstrings with the associated code. So,
        indent one or two levels as appropriate.
"""
from astToolFactory import getElementsDocstringGrab, settingsManufacturing
from astToolFactory.documentation import aDocument, diminutive2etymology, Docstring, docstrings, make1docstring
from astToolkit import Make

identifierToolClass: str = settingsManufacturing.identifiers['Grab']
identifierClass = identifierMethod = settingsManufacturing.identifiers[identifierToolClass]

docstrings[identifierClass][identifierMethod] = Make.Expr(Make.Constant(
    """Modify specific attributes of AST nodes while preserving the node structure.

    The Grab class provides static methods that create transformation functions to modify specific attributes of AST
    nodes. Unlike DOT which provides read-only access, Grab allows for targeted modifications of node attributes without
    replacing the entire node.

    Each method returns a function that takes a node, applies a transformation to a specific attribute of that node, and
    returns the modified node. This enables fine-grained control when transforming AST structures.
    """
))

# A new function, `getElementsDocstringGrab`, will return a dictionary for each `Grab` method. {'attribute': parameters,
# return, etc.} The function can use column 'type_astSuperClasses' to make sure TypeVar symbols are explained. The function should use
# logic similar to `getElementsTypeAlias`: if 'attribute' has more than one type, such as the annotation attribute, then the
# function should segregate the subclasses by the attribute type. The information from the function should be modular so we can
# arrange the docstring in different ways.

"""NOTE docstring contents
Classes with the attribute
Type of the attribute for each class, e.g.:
	type hasDOTannotation_expr = ast.AnnAssign
	type hasDOTannotation_exprOrNone = ast.arg
TypeVar summary line

Parameters
Returns
"""


	# docstrings[identifierToolClass][data.identifier] = Make.Expr(Make.Constant(make1docstring(data)))
