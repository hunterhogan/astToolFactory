from astToolFactory import column__value
from astToolkit import Make
from typing import NamedTuple
import ast

_columns: list[str] = [
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

	# columns computed from sources per row
	'classAs_astAttribute',
	'type_ast_expr',
	'ast_arg',
	'TypeAlias_hasDOTIdentifier',
	'TypeAlias_hasDOTSubcategory',
	'Call_keyword',

	# columns computed from sources per group
	'versionMinorMinimumClass',
	'versionMinorMinimum_match_args',
	'versionMinorMinimumAttribute',
	'listFunctionDef_args',
	'listDefaults',
	'listCall_keyword',

	# columns ought to be computed per group
	'kwarg_annotationIdentifier',

	# columns computed from other columns and a dictionary per row
	'list2Sequence',
	'type_astSuperClasses',
	'type_astSuperClasses_ast_expr',
	'listTupleAttributes',

	# columns computed from other columns and a dictionary per group
	'list4TypeAlias_value',
	'hashable_list4TypeAlias_value',
	'list4TypeAliasSubcategories',
]

"""
NOTE How to construct an identifier:
	Use the actual column names, case sensitive.
	Convert punctuation to underscores:
		`_` -> `,`
		`__` -> `=`
"""

class Column__attribute(NamedTuple):
	attribute: str

class Column__attributeKind(NamedTuple):
	attributeKind: str

class Column__attributeType_attribute(NamedTuple):
	attributeType: str
	attribute: str

class Column__ClassDefIdentifier_attribute(NamedTuple):
	ClassDefIdentifier: str
	attribute: str

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
	Column__ClassDefIdentifier_attribute('alias', 'name'): column__value('attributeRename', 'dotModule'),
	Column__ClassDefIdentifier_attribute('arguments', 'args'): column__value('attributeRename', 'list_arg'),
	Column__ClassDefIdentifier_attribute('AsyncFunctionDef', 'args'): column__value('attributeRename', 'argumentSpecification'),
	Column__ClassDefIdentifier_attribute('Call', 'args'): column__value('attributeRename', 'listParameters'),
	Column__ClassDefIdentifier_attribute('FunctionDef', 'args'): column__value('attributeRename', 'argumentSpecification'),
	Column__ClassDefIdentifier_attribute('ImportFrom', 'names'): column__value('attributeRename', 'list_alias'),
	Column__ClassDefIdentifier_attribute('Lambda', 'args'): column__value('attributeRename', 'argumentSpecification'),
}

attributeType__ClassDefIdentifier_attribute: dict[Column__ClassDefIdentifier_attribute, column__value] = {
	# HUNTER-from-the-past! Why is this commented out? An error or a style choice?
	# Column__ClassDefIdentifier_attribute('alias', 'name'): column__value('attributeType', 'identifierDotAttribute'),  # noqa: ERA001
	Column__ClassDefIdentifier_attribute('Constant', 'value'): column__value('attributeType', 'ConstantValueType'),
}

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

move2keywordArguments__: dict[Column__attribute | Column__attributeKind, column__value] = {
	Column__attribute('simple'): column__value('move2keywordArguments', True),  # noqa: FBT003
	Column__attribute('type_comment'): column__value('move2keywordArguments', 'Unpack'),
	Column__attributeKind('_attribute'): column__value('move2keywordArguments', 'No'),
	Column__attributeKind('No'): column__value('move2keywordArguments', 'No'),
}
