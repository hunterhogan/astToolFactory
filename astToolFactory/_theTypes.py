from typing import Any, NamedTuple, NotRequired, TypedDict, TypeVar
import ast

class column__value(NamedTuple):
	"""A column name and its value."""

	column: str
	value: Any

class dataTypeVariables(TypedDict):
	"""Data to manufacture a `TypeVar`.

	Attributes
	----------
	constraints : NotRequired[list[ast.expr]]
		List of constraint expressions that limit the type variable to specific types.
	bound : NotRequired[ast.expr]
		Upper bound expression that constrains the type variable to subtypes.
	tuple_keyword : NotRequired[list[tuple[str, bool]]]
		Keyword arguments as tuples of parameter name and boolean value.
	default_value : NotRequired[ast.expr]
		Default value expression for the type variable.

	"""

	constraints: NotRequired[list[ast.expr]]
	bound: NotRequired[ast.expr]
	tuple_keyword: NotRequired[list[tuple[str, bool]]]
	default_value: NotRequired[ast.expr]

MaskTuple = TypeVar('MaskTuple', bound=NamedTuple, covariant=True)

