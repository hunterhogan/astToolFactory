# pyright: basic
"""A warehouse for docstrings added to manufactured ast tools."""
from __future__ import annotations

from astToolFactory import settingsManufacturing
from astToolFactory.documentation import aDocument, Docstring, docstrings, make1docstring
from astToolkit import Make
from itertools import starmap
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

def _describeFieldType(attributeType: str, type_astSuperClasses: str, boxOfClasses: list[str]) -> str:
	description: str = f"The field has type `{attributeType}` on {', '.join(map('`ast.{}`'.format, boxOfClasses))}."
	if type_astSuperClasses != attributeType:
		description += f" The `action` annotation uses `{type_astSuperClasses}` for this type."
	return description

def makeDocstringGrab(attribute: str, ast_exprReturns: ast.expr, boxOfFieldTypes: list[tuple[str, str, list[str]]]) -> ast.Expr:
	data = Docstring(attribute
		, aDocument(f"Apply `action` to the `{attribute}` field of an AST node.")
		, aDocument('\n\n'.join(starmap(_describeFieldType, boxOfFieldTypes)))
		, {"action": aDocument("A function that takes the field's current value and returns a replacement of the same type."
			, subtitle='Callable')}
		, {"workhorse": aDocument(f"A function that updates the node's `{attribute}` field in place and returns the same node."
			, subtitle=ast.unparse(ast_exprReturns))}
	)
	return Make.Expr(Make.Constant(make1docstring(data, lineWidth=94)))
