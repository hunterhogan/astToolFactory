"""A warehouse for docstrings added to manufactured ast tools.
NOTE Use special indentation in this file.
    1. The generated files use spaces, not tabs, so use spaces here.
    2. As of this writing, I only know how to _manually_ align the indentation of the docstrings with the associated code. So, indent one or two levels as appropriate."""
from astToolFactory import settingsManufacturing
from astToolFactory.documentation import docstrings
from astToolkit import Make
import ast

identifierToolClass: str = 'ClassIsAndAttribute'

docstrings[settingsManufacturing.identifiers[identifierToolClass]][settingsManufacturing.identifiers[identifierToolClass]] = Make.Expr(Make.Constant(
    """
    Create functions that verify AST nodes by type and attribute conditions.

    The ClassIsAndAttribute class provides static methods that generate conditional functions for determining if an AST
    node is of a specific type AND its attribute meets a specified condition. These functions return TypeIs-enabled
    callables that can be used in conditional statements to narrow node types during code traversal and transformation.

    Each generated function performs two checks:
    1. Verifies that the node is of the specified AST type
    2. Tests if the specified attribute of the node meets a custom condition

    This enables complex filtering and targeting of AST nodes based on both their type and attribute contents.
    """
))
