"""A warehouse for docstrings added to manufactured ast tools.
NOTE Use special indentation in this file.
    1. The generated files use spaces, not tabs, so use spaces here.
    2. As of this writing, I only know how to _manually_ align the indentation of the docstrings with the associated code. So, indent one or two levels as appropriate."""
from astToolFactory import dictionaryIdentifiers
from astToolkit import Make
from collections import defaultdict
import ast

docstrings: dict[str, dict[str, ast.Expr]] = defaultdict(lambda: defaultdict(lambda: Make.Expr(Make.Constant(''))))

ImaDocstring: str = """This file is generated automatically, so changes to this file will be lost."""
docstringWarning = Make.Expr(Make.Constant(ImaDocstring))
del ImaDocstring

ImaDocstring: str = (
    """Type guard functions for safe AST node identification and type narrowing.
    (AI generated docstring)

    Provides static methods that perform runtime type checking for all AST node types
    while enabling compile-time type narrowing through `TypeIs` annotations. Forms
    the foundation of type-safe AST analysis and transformation throughout the toolkit.

    Each method takes an `ast.AST` node and returns a `TypeIs` that confirms both
    runtime type safety and enables static type checkers to narrow the node type in
    conditional contexts. This eliminates the need for unsafe casting while providing
    comprehensive coverage of Python's AST node hierarchy.

    Methods correspond directly to Python AST node types, following the naming convention
    of the AST classes themselves. Coverage includes expression nodes (`Add`, `Call`,
    `Name`), statement nodes (`Assign`, `FunctionDef`, `Return`), operator nodes
    (`And`, `Or`, `Not`), and structural nodes (`Module`, `arguments`, `keyword`).

    The class serves as the primary type-checking component in the antecedent-action
    pattern, where predicates identify target nodes and actions specify operations.
    Type guards from this class are commonly used as building blocks in `IfThis`
    predicates and directly as `findThis` parameters in visitor classes.

    Parameters:

        node: AST node to test for specific type membership

    Returns:

        typeIs: `TypeIs` enabling both runtime validation and static type narrowing

    Examples:

        Type-safe node processing with automatic type narrowing:

            if Be.FunctionDef(node):
                functionName = node.name  # Type-safe access to name attribute
                parameterCount = len(node.args.args)

        Building complex predicates for visitor patterns:

            NodeTourist(Be.Return, Then.extractIt(DOT.value)).visit(functionNode)

        Combining type guards in conditional logic:

            if Be.Call(node) and Be.Name(node.func):
                callableName = node.func.id  # Type-safe access to function name
    """
)
docstrings[dictionaryIdentifiers['Be']][dictionaryIdentifiers['Be']] = Make.Expr(Make.Constant(ImaDocstring))
del ImaDocstring

ImaDocstring: str = (
    """
    Access attributes and sub-nodes of AST elements via consistent accessor methods.

    The DOT class provides static methods to access specific attributes of different types of AST nodes in a consistent
    way. This simplifies attribute access across various node types and improves code readability by abstracting the
    underlying AST structure details.

    DOT is designed for safe, read-only access to node properties, unlike the grab class which is designed for modifying
    node attributes.
    """
)
docstrings[dictionaryIdentifiers['DOT']][dictionaryIdentifiers['DOT']] = Make.Expr(Make.Constant(ImaDocstring))
del ImaDocstring

ImaDocstring: str = (
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
)
docstrings[dictionaryIdentifiers['ClassIsAndAttribute']][dictionaryIdentifiers['ClassIsAndAttribute']] = Make.Expr(Make.Constant(ImaDocstring))
del ImaDocstring

ImaDocstring: str = (
    """
    Modify specific attributes of AST nodes while preserving the node structure.

    The Grab class provides static methods that create transformation functions to modify specific attributes of AST
    nodes. Unlike DOT which provides read-only access, Grab allows for targeted modifications of node attributes without
    replacing the entire node.

    Each method returns a function that takes a node, applies a transformation to a specific attribute of that node, and
    returns the modified node. This enables fine-grained control when transforming AST structures.
    """
)
docstrings[dictionaryIdentifiers['Grab']][dictionaryIdentifiers['Grab']] = Make.Expr(Make.Constant(ImaDocstring))
del ImaDocstring

import documentationMake  # noqa: E402
