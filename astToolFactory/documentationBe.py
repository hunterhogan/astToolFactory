"""A warehouse for docstrings added to manufactured ast tools.
NOTE Use special indentation in this file.
    1. The generated files use spaces, not tabs, so use spaces here.
    2. As of this writing, I only know how to _manually_ align the indentation of the docstrings with the associated code. So, indent one or two levels as appropriate."""
from astToolFactory import settingsManufacturing
from astToolFactory.documentation import docstrings
from astToolkit import Make
import ast

identifierToolClass: str = 'Be'

docstrings[settingsManufacturing.identifiers[identifierToolClass]][settingsManufacturing.identifiers[identifierToolClass]] = Make.Expr(Make.Constant(
    """A comprehensive suite of functions for AST class identification and type narrowing.

    `class` `Be` has a method for each `ast.AST` subclass, also called "node type", to perform type
    checking while enabling compile-time type narrowing through `TypeIs` annotations. This tool
    forms the foundation of type-safe AST analysis and transformation throughout astToolkit.

    Each method takes an `ast.AST` node and returns a `TypeIs` that confirms both runtime type
    safety and enables static type checkers to narrow the node type in conditional contexts. This
    eliminates the need for unsafe casting while providing comprehensive coverage of Python's AST
    node hierarchy.

    Methods correspond directly to Python AST node types, following the naming convention of the AST
    classes themselves. Coverage includes expression nodes (`Add`, `Call`, `Name`), statement nodes
    (`Assign`, `FunctionDef`, `Return`), operator nodes (`And`, `Or`, `Not`), and structural nodes
    (`Module`, `arguments`, `keyword`).

    The `class` is the primary type-checker in the antecedent-action pattern, where
    predicates identify target nodes and actions, uh... act on nodes and their attributes. Type guards from this class are
    commonly used as building blocks in `IfThis` predicates and directly as `findThis` parameters in
    visitor classes.

    Parameters:

        node: AST node to test for specific type membership

    Returns:

        typeIs: `TypeIs` enabling both runtime validation and static type narrowing

    Examples:

        Type-safe node processing with automatic type narrowing:

        ```python
            if Be.FunctionDef(node):
                functionName = node.name  # Type-safe access to name attribute parameterCount =
                len(node.args.args)
        ```

        Using type guards in visitor patterns:

        ```python
            NodeTourist(Be.Return, Then.extractIt(DOT.value)).visit(functionNode)
        ```

        Type-safe access to attributes of specific node types:

        ```python
            if Be.Call(node) and Be.Name(node.func):
                callableName = node.func.id  # Type-safe access to function name
        ```
    """
))
