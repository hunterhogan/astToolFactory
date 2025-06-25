"""A warehouse for docstrings added to manufactured ast tools.

NOTE Use special indentation in this file.
    1. The generated files use spaces, not tabs, so use spaces here.
    2. As of this writing, I only know how to _manually_ align the indentation of the docstrings with the associated code. So,
        indent one or two levels as appropriate.
"""
from astToolFactory import settingsManufacturing
from astToolFactory.documentation import docstrings
from astToolkit import Make

identifierToolClass: str = 'Grab'
identifierClass = identifierMethod = settingsManufacturing.identifiers[identifierToolClass]

docstrings[identifierClass][identifierMethod] = Make.Expr(Make.Constant(
    """
    Modify specific attributes of AST nodes while preserving the node structure.

    The Grab class provides static methods that create transformation functions to modify specific attributes of AST
    nodes. Unlike DOT which provides read-only access, Grab allows for targeted modifications of node attributes without
    replacing the entire node.

    Each method returns a function that takes a node, applies a transformation to a specific attribute of that node, and
    returns the modified node. This enables fine-grained control when transforming AST structures.
    """
))
