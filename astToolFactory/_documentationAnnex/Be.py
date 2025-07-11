"""A warehouse for docstrings added to manufactured ast tools.

NOTE Use special indentation in this file.
    1. The generated files use spaces, not tabs, so use spaces here.
    2. As of this writing, I only know how to _manually_ align the indentation of the docstrings with the associated code. So,
        indent one or two levels as appropriate.
"""
from ast import AST, Constant
from astToolFactory import settingsManufacturing
from astToolFactory.documentation import (
	diminutive2etymology, docstrings, map2PythonDelimiters, map2PythonKeywords, map2PythonOperators)
from astToolkit import identifierDotAttribute, Make
from itertools import chain
import ast

ImaIndent4aMethod: str = ' ' * 8
identifierToolClass: str = 'Be'
identifierClass = identifierMethod = settingsManufacturing.identifiers[identifierToolClass]

docstrings[identifierClass][identifierMethod] = Make.Expr(Make.Constant(
    f"""A comprehensive suite of functions for AST class identification and type narrowing.

    `class` `{identifierToolClass}` has a method for each `ast.AST` subclass, also called "node type", to perform type
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

    The `class` is the primary type-checker in the antecedent-action pattern, where predicates
    identify target nodes and actions, uh... act on nodes and their attributes. Type guards from
    this class are commonly used as building blocks in `IfThis` predicates and directly as
    `findThis` parameters in visitor classes.

    Parameters
    ----------
    node: ast.AST
        AST node to test for specific type membership

    Returns
    -------
    typeIs: TypeIs
        `TypeIs` enabling both runtime validation and static type narrowing

    Examples
    --------
    Type-safe node processing with automatic type narrowing:

    ```python
        if {identifierToolClass}.FunctionDef(node):
            functionName = node.name  # Type-safe access to name attribute parameterCount =
            len(node.args.args)
    ```

    Using type guards in visitor patterns:

    ```python
        NodeTourist({identifierToolClass}.Return, Then.extractIt(DOT.value)).visit(functionNode)
    ```

    Type-safe access to attributes of specific node types:

    ```python
        if {identifierToolClass}.Call(node) and {identifierToolClass}.Name(node.func):
            callableName = node.func.id  # Type-safe access to function name
    ```

    """
))

"""
    ClassDefIdentifier: str = 'For'
"""
for astClass in [C for C in [AST,*chain(*(c.__subclasses__() for c in [AST,Constant,*AST.__subclasses__()]))] if issubclass(C,AST)]:

    ClassDefIdentifier: str = astClass.__name__
    astClassDefIdentifier: identifierDotAttribute = 'ast.' + ClassDefIdentifier

    ImaDocstring: str = f"`{identifierToolClass}.{ClassDefIdentifier}`"
    if (etymology := diminutive2etymology.get(ClassDefIdentifier, None)):
        ImaDocstring += f", {etymology},"

    ImaDocstring += " matches"

    matchesClasses: list[identifierDotAttribute] = list(dict.fromkeys([f"`{astClassDefIdentifier}`", *sorted([f"`ast.{c.__name__}`" for c in astClass.__subclasses__() if issubclass(c, ast.AST)], key=lambda s: s.lower())]))

    if len(matchesClasses) > 1:
        ImaDocstring += " any of"

    ImaDocstring += f" `class` {' | '.join(matchesClasses)}.\n"

    indexConjunction: int = (
        bool(associatedDelimiters := map2PythonDelimiters.get(ClassDefIdentifier, None))
        + bool(associatedKeywords := map2PythonKeywords.get(ClassDefIdentifier, None))
        + bool(associatedOperators := map2PythonOperators.get(ClassDefIdentifier, None))
    )

    two = 2
    if indexConjunction:
        ImaDocstring += f"\n{ImaIndent4aMethod}This `class` is associated with"
        if associatedKeywords:
            ImaDocstring += f" Python keywords {associatedKeywords}"
            if indexConjunction > two:
                ImaDocstring += ","
            elif indexConjunction == two:
                ImaDocstring += " and"
                indexConjunction -= 1
        if associatedDelimiters:
            ImaDocstring += f" Python delimiters '{associatedDelimiters}'"
            if indexConjunction > two:
                ImaDocstring += ", and"
            elif indexConjunction == two:
                ImaDocstring += " and"
        if associatedOperators:
            ImaDocstring += f" Python operators '{associatedOperators}'"
        ImaDocstring += "."

    parentClass: identifierDotAttribute = f"`ast.{astClass.__base__.__name__}`" # pyright: ignore[reportOptionalMemberAccess]

    ImaDocstring += f"\n{ImaIndent4aMethod}It is a subclass of {parentClass}.\n{ImaIndent4aMethod}"

    """Not to be confused with"""

    docstrings[identifierClass][ClassDefIdentifier] = Make.Expr(Make.Constant(ImaDocstring))
