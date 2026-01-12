from typing import Any, NamedTuple, NotRequired, TypedDict, TypeVar
import ast

class column__value(NamedTuple):
	"""Assignment tuple representing exactly one `column = value` operation.

	(AI generated docstring)

	This tuple is the "right-hand side" of the mask-based dataframe update system.
	When paired with a mask tuple (such as `Column__attribute`) in a dictionary,
	it specifies which column to update and what value to assign to the selected
	rows.

	The identifier `column__value` decodes per the naming convention to
	"column = value", reflecting its role as an assignment specification.

	Attributes
	----------
	column : str
		Name of the dataframe column to update.
	value : Any
		Value to assign to the selected rows in that column.

	See Also
	--------
	`astToolFactory.datacenter._dataframeUpdateAnnex` : Module docstring explains
		the complete mask-based dataframe update system.

	"""

	column: str
	value: Any

"""NOTE How to construct an identifier:
	Use the actual column names, case sensitive.
	Convert punctuation to underscores:
		`_` -> `,`
		`,` -> `_`
		`__` -> `=`
		`=` -> `__`
"""

class Column__attribute(NamedTuple):
	"""Mask tuple selecting rows where the `attribute` column matches a value.

	(AI generated docstring)

	Used as a dictionary key in the mask-based dataframe update system. The field
	name `attribute` corresponds to the dataframe column name, and the field value
	specifies which rows to select.

	The identifier `Column__attribute` decodes to "Column = attribute", meaning
	"mask by the `attribute` column."

	Attributes
	----------
	attribute : str
		Value to match in the `attribute` column.

	See Also
	--------
	`astToolFactory.datacenter._dataframeUpdateAnnex` : Module docstring explains
		the complete mask-based dataframe update system.

	"""

	attribute: str

class Column__attributeKind(NamedTuple):
	"""Mask tuple selecting rows where the `attributeKind` column matches a value.

	(AI generated docstring)

	Used as a dictionary key in the mask-based dataframe update system. The field
	name `attributeKind` corresponds to the dataframe column name, and the field
	value specifies which rows to select.

	The identifier `Column__attributeKind` decodes to "Column = attributeKind".

	Attributes
	----------
	attributeKind : str
		Value to match in the `attributeKind` column (e.g., `'_field'`, `'_attribute'`).

	See Also
	--------
	`astToolFactory.datacenter._dataframeUpdateAnnex` : Module docstring explains
		the complete mask-based dataframe update system.

	"""

	attributeKind: str

class Column__attributeType_attribute(NamedTuple):
	"""Mask tuple selecting rows by both `attributeType` and `attribute` columns.

	(AI generated docstring)

	Used as a dictionary key in the mask-based dataframe update system. Both
	conditions must match for a row to be selected (logical AND).

	The identifier `Column__attributeType_attribute` decodes to
	"Column = attributeType, attribute", meaning "mask by both columns."

	Attributes
	----------
	attributeType : str
		Value to match in the `attributeType` column.
	attribute : str
		Value to match in the `attribute` column.

	See Also
	--------
	`astToolFactory.datacenter._dataframeUpdateAnnex` : Module docstring explains
		the complete mask-based dataframe update system.

	"""

	attributeType: str
	attribute: str

class Column__ClassDefIdentifier_attribute(NamedTuple):
	"""Mask tuple selecting rows by both `ClassDefIdentifier` and `attribute` columns.

	(AI generated docstring)

	Used as a dictionary key in the mask-based dataframe update system. Both
	conditions must match for a row to be selected (logical AND). This is the most
	specific mask tuple, selecting rows for a particular attribute of a particular
	AST class.

	The identifier `Column__ClassDefIdentifier_attribute` decodes to
	"Column = ClassDefIdentifier, attribute".

	Attributes
	----------
	ClassDefIdentifier : str
		Value to match in the `ClassDefIdentifier` column (e.g., `'FunctionDef'`).
	attribute : str
		Value to match in the `attribute` column (e.g., `'args'`).

	See Also
	--------
	`astToolFactory.datacenter._dataframeUpdateAnnex` : Module docstring explains
		the complete mask-based dataframe update system.

	"""

	ClassDefIdentifier: str
	attribute: str

class Column__ClassDefIdentifier_versionMinorPythonInterpreter(NamedTuple):
	"""Mask tuple selecting rows by both `ClassDefIdentifier` and `versionMinorPythonInterpreter` columns.

	(AI generated docstring)

	Used as a dictionary key in the mask-based dataframe update system. Both
	conditions must match for a row to be selected (logical AND). This is the most
	specific mask tuple, selecting rows for a particular attribute of a particular
	AST class.

	The identifier `Column__ClassDefIdentifier_versionMinorPythonInterpreter` decodes to
	"Column = ClassDefIdentifier, versionMinorPythonInterpreter".

	Attributes
	----------
	ClassDefIdentifier : str
		Value to match in the `ClassDefIdentifier` column (e.g., `'FunctionDef'`).
	versionMinorPythonInterpreter : int
		Value to match in the `versionMinorPythonInterpreter` column (e.g., `13`).

	See Also
	--------
	`astToolFactory.datacenter._dataframeUpdateAnnex` : Module docstring explains
		the complete mask-based dataframe update system.

	"""

	ClassDefIdentifier: str
	versionMinorPythonInterpreter: int

MaskTuple = TypeVar('MaskTuple', bound=NamedTuple, covariant=True)
"""Type variable representing any mask tuple in the dataframe update system.

Bound to `NamedTuple` so that `getMaskByColumnValue` can iterate over the tuple's
field names and values via `._asdict()`. Covariant because mask tuples are used
only as dictionary keys (read-only position).

See Also
--------
`astToolFactory.datacenter._dataframeUpdateAnnex` : Module docstring explains
	the complete mask-based dataframe update system.

"""

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

