"""A warehouse for docstrings added to manufactured ast tools.
NOTE Use special indentation in this file.
    1. The generated files use spaces, not tabs, so use spaces here.
    2. As of this writing, I only know how to _manually_ align the indentation of the docstrings with the associated code. So, indent one or two levels as appropriate."""
from ast import AST, Constant
from astToolFactory import settingsManufacturing
from astToolFactory.documentation import (
	diminutive2etymology, docstrings, map2PythonDelimiters, map2PythonKeywords, map2PythonOperators,
)
from astToolkit import identifierDotAttribute, Make
from itertools import chain
import ast

identifierToolClass: str = 'Be'
ImaIndentMethod: str = ' ' * 8

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

    The `class` is the primary type-checker in the antecedent-action pattern, where predicates
    identify target nodes and actions, uh... act on nodes and their attributes. Type guards from
    this class are commonly used as building blocks in `IfThis` predicates and directly as
    `findThis` parameters in visitor classes.

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

"""
    ClassDefIdentifier: str = 'For'
"""
for astClass in [C for C in [AST,*chain(*map(lambda c:c.__subclasses__(), [AST,Constant,*AST.__subclasses__()]))] if issubclass(C,AST)]:

    ClassDefIdentifier: str = astClass.__name__
    astClassDefIdentifier: identifierDotAttribute = 'ast.' + ClassDefIdentifier

    ImaDocstring: str = f"`{identifierToolClass}.{ClassDefIdentifier}`"
    if (etymology := diminutive2etymology.get(ClassDefIdentifier, None)):
        ImaDocstring += f", {etymology},"

    ImaDocstring += " matches"

    matchesClass: list[identifierDotAttribute] = [f"`class` `{astClassDefIdentifier}`"] + sorted([f"`ast.{subclass.__name__}`" for subclass in astClass.__subclasses__() if issubclass(subclass, ast.AST)], key=lambda element: element.lower())

    if len(matchesClass) > 1:
        ImaDocstring += " any of"

    ImaDocstring += f" {' | '.join(matchesClass)}."

    if (hasAttributes := astClass._fields):
        ImaDocstring += f"\n{ImaIndentMethod}It has attributes {', '.join([f'`{attribute}`' for attribute in hasAttributes])}."
        # ImaDocstring += f"\n{ImaIndentMethod}`class` `{astClassDefIdentifier}` has attributes {', '.join([f'`{attribute}`' for attribute in hasAttributes])}."

    indexConjunction: int = (
        bool(associatedDelimiters := map2PythonDelimiters.get(ClassDefIdentifier, None))
        + bool(associatedKeywords := map2PythonKeywords.get(ClassDefIdentifier, None))
        + bool(associatedOperators := map2PythonOperators.get(ClassDefIdentifier, None))
    )

    if indexConjunction:
        ImaDocstring += f"\n{ImaIndentMethod}This `class` is associated with"
        if associatedKeywords:
            ImaDocstring += f" Python keywords {associatedKeywords}"
            if indexConjunction > 2:
                ImaDocstring += ","
            elif indexConjunction == 2:
                ImaDocstring += " and"
                indexConjunction -= 1
        if associatedDelimiters:
            ImaDocstring += f" Python delimiters '{associatedDelimiters}'"
            if indexConjunction > 2:
                ImaDocstring += ", and"
            elif indexConjunction == 2:
                ImaDocstring += " and"
        if associatedOperators:
            ImaDocstring += f" Python operators '{associatedOperators}'"
        ImaDocstring += "."

    parentClass: identifierDotAttribute = f"`ast.{astClass.__base__.__name__}`" # pyright: ignore[reportOptionalMemberAccess]

    ImaDocstring += f"\n{ImaIndentMethod}It is a subclass of {parentClass}."

    """Not to be confused with"""

    docstrings[settingsManufacturing.identifiers[identifierToolClass]][ClassDefIdentifier] = Make.Expr(Make.Constant(ImaDocstring))



# if __name__ == '__main__':
#     print(ImaDocstring)

