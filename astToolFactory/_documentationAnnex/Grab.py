# ruff: noqa
# pyright: basic
"""A warehouse for docstrings added to manufactured ast tools.

NOTE Use special indentation in this file.
    1. The generated files use spaces, not tabs, so use spaces here.
    2. As of this writing, I only know how to _manually_ align the indentation of the docstrings with the associated code. So,
        indent one or two levels as appropriate.
"""
from astToolFactory import getElementsDocstringGrab, getElementsGrab, settingsManufacturing
from astToolFactory.documentation import aDocument, diminutive2etymology, Docstring, docstrings, make1docstring
from astToolkit import Make
import ast

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

for identifierTypeOfNode, list_ast_expr, attribute, _guardVersion, _versionMinorMinimum in getElementsGrab(identifierToolClass):
	""""""
	astNameTypeOfNode: ast.Name = Make.Name(identifierTypeOfNode)
	data = Docstring(attribute
		, aDocument(f"Apply a function to the `{attribute}` attribute of a 'node' of `type` `{identifierTypeOfNode}`.", AIgenerated=False)
		, aDocument(f"The `type` of the `{attribute}` attribute is `something` for [any of] `class` `ast.IDK`.\n\nIf `type` were represented by a `TypeVar`, I would tell you what the ideogram is.\n\nIf `{attribute}` could be a second type, I would tell you it is `type` `somethingElse` for [any of] `class` `ast.FML`."
			, AIgenerated=False)
		, {"action": aDocument("A function with one parameter and a `return` of the same `type`."
			, subtitle=ast.unparse(Make.BitOr.join([Make.Subscript(Make.Name("Callable"), Make.Tuple([Make.List([ast_expr]), ast_expr])) for ast_expr in list_ast_expr]))
			, AIgenerated=False)}
		, {"workhorse": aDocument(f"A function with one parameter for a 'node' of `type` `{identifierTypeOfNode}` and a `return` of the same `type`."
			, ast.unparse(Make.Subscript(Make.Name("Callable"), Make.Tuple([Make.List([astNameTypeOfNode]), astNameTypeOfNode])))
			, AIgenerated=False)}
		, {'Type Checker Error?': aDocument("If you use `Grab` with one level of complexity, your type checker will give you accurate guidance. With two levels of complexity, such as nesting `Grab` in another `Grab`, your type checker will be angry. I recommend `typing.cast()`. The fault is mine: the 'type safety' of `Grab` is inherently limited.")}
	)

	docstrings[identifierToolClass][data.identifier] = Make.Expr(Make.Constant(make1docstring(data, firstIndent=2)))
