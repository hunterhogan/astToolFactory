"""A warehouse for docstrings added to manufactured ast tools.

NOTE Use special indentation in this file.
    1. The generated files use spaces, not tabs, so use spaces here.
    2. As of this writing, I only know how to _manually_ align the indentation of the docstrings with the associated code. So,
        indent one or two levels as appropriate.
"""
from astToolFactory import settingsManufacturing
from astToolFactory.documentation import docstrings
from astToolkit import Make

identifierToolClass: str = 'DOT'
identifierClass = identifierMethod = settingsManufacturing.identifiers[identifierToolClass]

docstrings[identifierClass][identifierMethod] = Make.Expr(Make.Constant(
    """Access attributes and sub-nodes of AST elements via consistent accessor methods.

    The DOT class provides static methods to access specific attributes of different types of AST nodes in a consistent
    way. This simplifies attribute access across various node types and improves code readability by abstracting the
    underlying AST structure details.

    DOT is designed for safe, read-only access to node properties, unlike the grab class which is designed for modifying
    node attributes.

    """
))

