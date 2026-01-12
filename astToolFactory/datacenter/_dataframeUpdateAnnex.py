"""Mask-based dataframe update system for declarative bulk assignments.

(AI generated docstring)

This module defines a system for applying bulk updates to a `pandas.DataFrame` using
declarative dictionaries. The system separates *what* to update from *how* to update it,
making large-scale data transformations readable and maintainable.

System Overview
---------------
The system has three components:

1. **Mask tuples** (defined in `astToolFactory._theTypes`): `NamedTuple` classes whose
   field names are dataframe column names and whose values are cell values. These tuples
   define *which rows* to update. Examples:
   - `Column__attribute('ctx')` selects rows where the `attribute` column equals `'ctx'`.
   - `Column__ClassDefIdentifier_attribute('FunctionDef', 'args')` selects rows where
     `ClassDefIdentifier` equals `'FunctionDef'` AND `attribute` equals `'args'`.

2. **Assignment tuple** (`column__value` in `astToolFactory._theTypes`): A `NamedTuple`
   holding exactly one assignment: the `.column` field names the target column, and the
   `.value` field holds the value to assign.

3. **Executor functions** (in `astToolFactory.datacenter._dataframeUpdate`):
   - `getMaskByColumnValue`: Converts a mask tuple to a boolean `pandas.Series`.
   - `dictionary2UpdateDataframe`: Iterates a dictionary of mask→assignment pairs and
     applies each update to the dataframe.

Naming Convention
-----------------
Identifiers in this module use a punctuation-to-underscore cipher to embed semantics:

==========  ==========  ==========================================
Character   Encodes     Meaning
==========  ==========  ==========================================
`_`         `,`         Separates multiple values within a concept
`,`         `_`         Encodes a literal underscore
`__`        `=`         Represents assignment ("column = value")
`=`         `__`        Encodes a literal double underscore
==========  ==========  ==========================================

Examples
--------
- `Column__attribute` decodes to "Column = attribute", meaning "mask by the `attribute`
  column."
- `attributeRename__` decodes to "attributeRename =", meaning "this dictionary assigns
  to the `attributeRename` column."
- `Column__ClassDefIdentifier_attribute` decodes to "Column = ClassDefIdentifier,
  attribute", meaning "mask by both columns."

Usage Pattern
-------------
1. Define a dictionary with mask tuples as keys and `column__value` as values::

    attributeRename__: dict[Column__attribute, column__value] = {
        Column__attribute('ctx'): column__value('attributeRename', 'context'),
        Column__attribute('func'): column__value('attributeRename', 'callee'),
    }

2. Apply to a dataframe::

    dataframe = dictionary2UpdateDataframe(attributeRename__, dataframe)

This sets `dataframe.loc[dataframe['attribute'] == 'ctx', 'attributeRename'] = 'context'`
and `dataframe.loc[dataframe['attribute'] == 'func', 'attributeRename'] = 'callee'`.

Dictionaries in This Module
---------------------------
`attributeRename__`
    Maps attribute names to their renamed identifiers for code generation.
`attributeType__ClassDefIdentifier_attribute`
    Overrides attribute types for specific class-attribute pairs.
`defaultValue__`
    Assigns default values (as `ast` nodes) to attributes.
`dictionary_defaultValue_ast_arg_Call_keyword_orElse`
    Maps attributes to their fallback expressions for keyword arguments.
`move2keywordArguments__`
    Flags attributes that should become keyword-only arguments.

See Also
--------
`astToolFactory._theTypes` : Defines the mask and assignment tuple classes.
`astToolFactory.datacenter._dataframeUpdate.dictionary2UpdateDataframe` : Applies updates.
`astToolFactory.datacenter._dataframeUpdate.getMaskByColumnValue` : Builds boolean masks.

"""
from astToolFactory import (
	Column__attribute, Column__attributeKind, Column__attributeType_attribute, Column__ClassDefIdentifier_attribute,
	Column__ClassDefIdentifier_versionMinorPythonInterpreter, column__value)
from astToolkit import Make
import ast

_columns: list[str] = [
	# All column names used in the package dataframe, grouped by data source and
	# computation stage. This list serves as the single source of truth for column
	# ordering and existence.
	# read from sources
	# Interpreter
	'ClassDefIdentifier',
	'versionMajorPythonInterpreter',
	'versionMinorPythonInterpreter',
	'versionMicroPythonInterpreter',
	'base',

	# getDictionary_match_args and stdlib/ast.pyi
	'deprecated',
	'match_args',
	'attribute',
	'attributeKind',
	'attributeType',

	# Purely a human choice
	'attributeRename',
	'move2keywordArguments',
	'defaultValue', # (for now)

	# Put this here? I think it needs the information from `move2keywordArguments`.
	# columns ought to be computed per group
    # NOTE TODO FIXME Why did I write "ought to be"? I think I knew this was not automated, but that I didn't document it in a way/place I can currently find.
	'kwarg_annotationIdentifier',


	# columns computed from sources per row, with exceptions
	'classAs_astAttribute',
	'list2Sequence', # column computed from other columns and a dictionary per row
	'type_ast_expr',
	'type_astSuperClasses', # column computed from other columns and a dictionary per row
	'ast_arg',
	'type_astSuperClasses_ast_expr', # column computed from other columns and a dictionary per row
	'TypeAlias_hasDOTIdentifier',
	'TypeAlias_hasDOTSubcategory',

	# columns computed from other columns and a dictionary per group
	'list4TypeAlias_value',
	'hashable_list4TypeAlias_value',
	'list4TypeAliasSubcategories',

	# columns computed from sources per group
	'versionMinorMinimumClass',
	'versionMinorMinimum_match_args',
	'versionMinorMinimumAttribute',
	'Call_keyword', # column computed from sources per row
	'listFunctionDef_args',
	'listDefaults',
	'listCall_keyword',
	'listTupleAttributes', # column computed from other columns and a dictionary per row


]

"""NOTE How to construct an identifier:
	Use the actual column names, case sensitive.
	Convert punctuation to underscores:
		`_` -> `,`
		`,` -> `_`
		`__` -> `==`
		`==` -> `__`
"""

attributeRename__: dict[Column__attribute | Column__ClassDefIdentifier_attribute, column__value] = {
	Column__attribute('arg'): column__value('attributeRename', 'Buffalo_buffalo_Buffalo_buffalo_buffalo_buffalo_Buffalo_buffalo'),
	Column__attribute('asname'): column__value('attributeRename', 'asName'),
	Column__attribute('attr'): column__value('attributeRename', 'attribute'),
	Column__attribute('ctx'): column__value('attributeRename', 'context'),
	Column__attribute('elt'): column__value('attributeRename', 'element'),
	Column__attribute('elts'): column__value('attributeRename', 'listElements'),
	Column__attribute('func'): column__value('attributeRename', 'callee'),
	Column__attribute('keywords'): column__value('attributeRename', 'list_keyword'),
	Column__attribute('module'): column__value('attributeRename', 'dotModule'),
	Column__attribute('orelse'): column__value('attributeRename', 'orElse'),
	Column__attribute('str'): column__value('attributeRename', 'string'),
	Column__ClassDefIdentifier_attribute('alias', 'name'): column__value('attributeRename', 'dotModule'),
	Column__ClassDefIdentifier_attribute('arguments', 'args'): column__value('attributeRename', 'list_arg'),
	Column__ClassDefIdentifier_attribute('AsyncFunctionDef', 'args'): column__value('attributeRename', 'argumentSpecification'),
	Column__ClassDefIdentifier_attribute('Call', 'args'): column__value('attributeRename', 'listParameters'),
	Column__ClassDefIdentifier_attribute('FunctionDef', 'args'): column__value('attributeRename', 'argumentSpecification'),
	Column__ClassDefIdentifier_attribute('ImportFrom', 'names'): column__value('attributeRename', 'list_alias'),
	Column__ClassDefIdentifier_attribute('Lambda', 'args'): column__value('attributeRename', 'argumentSpecification'),
}
"""Mask-to-assignment dictionary for the `attributeRename` column.

Each key is a mask tuple selecting rows by `attribute` or by
(`ClassDefIdentifier`, `attribute`). Each value assigns a renamed
identifier to the `attributeRename` column for those rows.

Applied via `dictionary2UpdateDataframe`. See module docstring for the
full system description.
"""

attributeType__ClassDefIdentifier_attribute: dict[Column__ClassDefIdentifier_attribute, column__value] = {
	# HUNTER-from-the-past! Why is this commented out? An error or a style choice?
	# Column__ClassDefIdentifier_attribute('alias', 'name'): column__value('attributeType', 'identifierDotAttribute'),  # noqa: ERA001
	Column__ClassDefIdentifier_attribute('Constant', 'value'): column__value('attributeType', 'ConstantValueType'),
}
"""Mask-to-assignment dictionary for overriding the `attributeType` column.

Keys select rows by (`ClassDefIdentifier`, `attribute`) pairs. Values
assign a custom type string to override the default type inference.

Applied via `dictionary2UpdateDataframe`. See module docstring for the
full system description.
"""

defaultValue__: dict[Column__attribute | Column__attributeType_attribute | Column__ClassDefIdentifier_attribute, column__value] = {
	Column__attribute('asname'): column__value('defaultValue', Make.Constant(None)),
	Column__attribute('bound'): column__value('defaultValue', Make.Constant(None)),
	Column__attribute('cause'): column__value('defaultValue', Make.Constant(None)),
	Column__attribute('default_value'): column__value('defaultValue', Make.Constant(None)),
	Column__attribute('exc'): column__value('defaultValue', Make.Constant(None)),
	Column__attribute('format_spec'): column__value('defaultValue', Make.Constant(None)),
	Column__attribute('guard'): column__value('defaultValue', Make.Constant(None)),
	Column__attribute('is_async'): column__value('defaultValue', Make.Constant(0)),
	Column__attribute('kind'): column__value('defaultValue', Make.Constant(None)),
	Column__attribute('kwarg'): column__value('defaultValue', Make.Constant(None)),
	Column__attribute('level'): column__value('defaultValue', Make.Constant(0)),
	Column__attribute('lower'): column__value('defaultValue', Make.Constant(None)),
	Column__attribute('msg'): column__value('defaultValue', Make.Constant(None)),
	Column__attribute('optional_vars'): column__value('defaultValue', Make.Constant(None)),
	Column__attribute('rest'): column__value('defaultValue', Make.Constant(None)),
	Column__attribute('simple'): column__value('defaultValue', Make.Call(Make.Name('int'), [Make.Call(Make.Name('isinstance'), [Make.Name('target'), Make.Attribute(Make.Name('ast'), 'Name')])])),
	Column__attribute('step'): column__value('defaultValue', Make.Constant(None)),
	Column__attribute('type_comment'): column__value('defaultValue', Make.Constant(None)),
	Column__attribute('type'): column__value('defaultValue', Make.Constant(None)),
	Column__attribute('upper'): column__value('defaultValue', Make.Constant(None)),
	Column__attribute('vararg'): column__value('defaultValue', Make.Constant(None)),
	Column__attributeType_attribute('int | None', 'end_col_offset'): column__value('defaultValue', Make.Constant(None)),
	Column__attributeType_attribute('int | None', 'end_lineno'): column__value('defaultValue', Make.Constant(None)),
	Column__ClassDefIdentifier_attribute('AnnAssign', 'value'): column__value('defaultValue', Make.Constant(None)),
	Column__ClassDefIdentifier_attribute('arg', 'annotation'): column__value('defaultValue', Make.Constant(None)),
	Column__ClassDefIdentifier_attribute('AsyncFunctionDef', 'returns'): column__value('defaultValue', Make.Constant(None)),
	Column__ClassDefIdentifier_attribute('Dict', 'keys'): column__value('defaultValue', Make.List([Make.Constant(None)])),
	Column__ClassDefIdentifier_attribute('ExceptHandler', 'name'): column__value('defaultValue', Make.Constant(None)),
	Column__ClassDefIdentifier_attribute('FunctionDef', 'returns'): column__value('defaultValue', Make.Constant(None)),
	Column__ClassDefIdentifier_attribute('MatchAs', 'name'): column__value('defaultValue', Make.Constant(None)),
	Column__ClassDefIdentifier_attribute('MatchAs', 'pattern'): column__value('defaultValue', Make.Constant(None)),
	Column__ClassDefIdentifier_attribute('MatchStar', 'name'): column__value('defaultValue', Make.Constant(None)),
	Column__ClassDefIdentifier_attribute('Return', 'value'): column__value('defaultValue', Make.Constant(None)),
	Column__ClassDefIdentifier_attribute('Yield', 'value'): column__value('defaultValue', Make.Constant(None)),
}
"""Mask-to-assignment dictionary for the `defaultValue` column.

Keys are mask tuples of varying specificity: by `attribute` alone, by
(`attributeType`, `attribute`), or by (`ClassDefIdentifier`, `attribute`).
Values are `ast` node expressions representing the default value for code
generation.

Applied via `dictionary2UpdateDataframe`. See module docstring for the
full system description.
"""

dictionary_defaultValue_ast_arg_Call_keyword_orElse: dict[Column__attribute | Column__ClassDefIdentifier_attribute, ast.expr] = {
	Column__attribute('bases'): Make.List(),
	Column__attribute('cases'): Make.List(),
	Column__attribute('ctx'): Make.Call(Make.Attribute(Make.Name('ast'), 'Load')),
	Column__attribute('decorator_list'): Make.List(),
	Column__attribute('defaults'): Make.List(),
	Column__attribute('elts'): Make.List(),
	Column__attribute('finalbody'): Make.List(),
	Column__attribute('keywords'): Make.List(),
	Column__attribute('kw_defaults'): Make.List(),
	Column__attribute('kwd_attrs'): Make.List(),
	Column__attribute('kwd_patterns'): Make.List(),
	Column__attribute('kwonlyargs'): Make.List(),
	Column__attribute('patterns'): Make.List(),
	Column__attribute('posonlyargs'): Make.List(),
	Column__attribute('type_ignores'): Make.List(),
	Column__ClassDefIdentifier_attribute('arguments', 'args'): Make.List(),
	Column__ClassDefIdentifier_attribute('AsyncFor', 'orelse'): Make.List(),
	Column__ClassDefIdentifier_attribute('AsyncFunctionDef', 'args'): Make.Call(Make.Attribute(Make.Name('ast'), 'arguments')),
	Column__ClassDefIdentifier_attribute('AsyncFunctionDef', 'body'): Make.List(),
	Column__ClassDefIdentifier_attribute('AsyncFunctionDef', 'type_params'): Make.List(),
	Column__ClassDefIdentifier_attribute('Call', 'args'): Make.List(),
	Column__ClassDefIdentifier_attribute('ClassDef', 'body'): Make.List(),
	Column__ClassDefIdentifier_attribute('ClassDef', 'type_params'): Make.List(),
	Column__ClassDefIdentifier_attribute('Dict', 'keys'): Make.List(),
	Column__ClassDefIdentifier_attribute('Dict', 'values'): Make.List(),
	Column__ClassDefIdentifier_attribute('ExceptHandler', 'body'): Make.List(),
	Column__ClassDefIdentifier_attribute('For', 'orelse'): Make.List(),
	Column__ClassDefIdentifier_attribute('FunctionDef', 'args'): Make.Call(Make.Attribute(Make.Name('ast'), 'arguments')),
	Column__ClassDefIdentifier_attribute('FunctionDef', 'body'): Make.List(),
	Column__ClassDefIdentifier_attribute('FunctionDef', 'type_params'): Make.List(),
	Column__ClassDefIdentifier_attribute('If', 'orelse'): Make.List(),
	Column__ClassDefIdentifier_attribute('Import', 'names'): Make.List(),
	Column__ClassDefIdentifier_attribute('match_case', 'body'): Make.List(),
	Column__ClassDefIdentifier_attribute('MatchMapping', 'keys'): Make.List(),
	Column__ClassDefIdentifier_attribute('Try', 'orelse'): Make.List(),
	Column__ClassDefIdentifier_attribute('TryStar', 'orelse'): Make.List(),
	Column__ClassDefIdentifier_attribute('While', 'orelse'): Make.List(),
}
"""Maps mask tuples to fallback `ast.expr` nodes for mutable default handling.

When an attribute has a mutable default (like an empty list), the generated
code must use a sentinel pattern: accept `None` and replace with the mutable
value at runtime. This dictionary provides the `orElse` expression used in
that pattern.

Unlike other dictionaries here, this one is NOT applied via
`dictionary2UpdateDataframe`. Instead, `_moveMutable_defaultValue` uses it
directly. See module docstring for the full system description.
"""

move2keywordArguments__: dict[Column__attribute | Column__attributeKind, column__value] = {
	Column__attribute('simple'): column__value('move2keywordArguments', 'True'),
	Column__attribute('type_comment'): column__value('move2keywordArguments', 'Unpack'),
	Column__attributeKind('_attribute'): column__value('move2keywordArguments', 'No'),
	Column__attributeKind('No'): column__value('move2keywordArguments', 'No'),
}
"""Mask-to-assignment dictionary for the `move2keywordArguments` column.

Keys select rows by `attribute` or `attributeKind`. Values indicate whether
the attribute should become a keyword-only argument in generated function
signatures: `True` for keyword-only, `'No'` for positional, `'Unpack'` for
special handling.

Applied via `dictionary2UpdateDataframe`. See module docstring for the
full system description.
"""

kwarg_annotationIdentifier__: dict[Column__ClassDefIdentifier_versionMinorPythonInterpreter, column__value] = {
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('alias', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('AnnAssign', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('arg', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes_type_comment'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('Assert', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('Assign', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes_type_comment'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('AsyncFor', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes_type_comment'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('AsyncFunctionDef', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes_type_comment'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('AsyncWith', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes_type_comment'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('Attribute', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('AugAssign', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('Await', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('BinOp', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('BoolOp', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('Break', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('Bytes', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('Call', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('ClassDef', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('Compare', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('Constant', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('Continue', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('Delete', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('Dict', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('DictComp', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('Ellipsis', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('ExceptHandler', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('excepthandler', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('expr', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('Expr', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('For', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes_type_comment'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('FormattedValue', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('FunctionDef', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes_type_comment'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('GeneratorExp', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('Global', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('If', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('IfExp', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('Import', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('ImportFrom', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('Interpolation', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('JoinedStr', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('keyword', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('Lambda', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('List', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('ListComp', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('Match', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('MatchAs', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes_int'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('MatchClass', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes_int'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('MatchMapping', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes_int'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('MatchOr', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes_int'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('MatchSequence', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes_int'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('MatchSingleton', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes_int'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('MatchStar', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes_int'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('MatchValue', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes_int'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('Name', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('NameConstant', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('NamedExpr', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('Nonlocal', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('Num', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('ParamSpec', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes_int'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('Pass', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('pattern', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes_int'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('Raise', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('Return', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('Set', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('SetComp', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('Slice', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('Starred', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('stmt', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('Str', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('Subscript', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('TemplateStr', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('Try', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('TryStar', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('Tuple', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('type_param', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes_int'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('TypeAlias', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes_int'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('TypeVar', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes_int'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('TypeVarTuple', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes_int'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('UnaryOp', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('While', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('With', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes_type_comment'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('Yield', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
	Column__ClassDefIdentifier_versionMinorPythonInterpreter('YieldFrom', 14): column__value('kwarg_annotationIdentifier', 'ast_attributes'),
}
"""I couldn't get `_makeColumn_kwarg_annotationIdentifier` to work, so I gave up and made this dictionary by hand."""
