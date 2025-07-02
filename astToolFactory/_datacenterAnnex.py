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
]

"""
NOTE How to construct an identifier for a dictionary to update the dataframe:
Use the actual column names, case sensitive.
columnLHS__columnRHS: dict = {}
columnLHS__columnRHS_columnRHSn: dict = {}
Convert punctuation to underscores:
`_` -> `,`
`__` -> `=`
"""

class __attribute(NamedTuple):
	attribute: str

class __attributeKind(NamedTuple):
	attributeKind: str

class __ClassDefIdentifier_attribute(NamedTuple):
	ClassDefIdentifier: str
	attribute: str

class __attributeType_attribute(NamedTuple):
	attributeType: str
	attribute: str

attributeRename__attribute: dict[__attribute, column__value] = {
	__attribute('arg'): column__value('attributeRename', 'Buffalo_buffalo_Buffalo_buffalo_buffalo_buffalo_Buffalo_buffalo'),
	__attribute('asname'): column__value('attributeRename', 'asName'),
	__attribute('attr'): column__value('attributeRename', 'attribute'),
	__attribute('ctx'): column__value('attributeRename', 'context'),
	__attribute('elt'): column__value('attributeRename', 'element'),
	__attribute('elts'): column__value('attributeRename', 'listElements'),
	__attribute('func'): column__value('attributeRename', 'callee'),
	__attribute('keywords'): column__value('attributeRename', 'list_keyword'),
	__attribute('module'): column__value('attributeRename', 'dotModule'),
	__attribute('orelse'): column__value('attributeRename', 'orElse'),
}

attributeRename__ClassDefIdentifier_attribute: dict[__ClassDefIdentifier_attribute, column__value] = {
	__ClassDefIdentifier_attribute('arguments', 'args'): column__value('attributeRename', 'list_arg'),
	__ClassDefIdentifier_attribute('AsyncFunctionDef', 'args'): column__value('attributeRename', 'argumentSpecification'),
	__ClassDefIdentifier_attribute('Call', 'args'): column__value('attributeRename', 'listParameters'),
	__ClassDefIdentifier_attribute('FunctionDef', 'args'): column__value('attributeRename', 'argumentSpecification'),
	__ClassDefIdentifier_attribute('ImportFrom', 'names'): column__value('attributeRename', 'list_alias'),
	__ClassDefIdentifier_attribute('Lambda', 'args'): column__value('attributeRename', 'argumentSpecification'),
}

attributeType__ClassDefIdentifier_attribute: dict[__ClassDefIdentifier_attribute, column__value] = {
	__ClassDefIdentifier_attribute('Constant', 'value'): column__value('attributeType', "ConstantValueType"),
}

defaultValue__attribute: dict[__attribute, column__value] = {
	__attribute('asname'): column__value('defaultValue', Make.Constant(None)),
	__attribute('bound'): column__value('defaultValue', Make.Constant(None)),
	__attribute('cause'): column__value('defaultValue', Make.Constant(None)),
	__attribute('default_value'): column__value('defaultValue', Make.Constant(None)),
	__attribute('exc'): column__value('defaultValue', Make.Constant(None)),
	__attribute('format_spec'): column__value('defaultValue', Make.Constant(None)),
	__attribute('guard'): column__value('defaultValue', Make.Constant(None)),
	__attribute('is_async'): column__value('defaultValue', Make.Constant(0)),
	__attribute('kind'): column__value('defaultValue', Make.Constant(None)),
	__attribute('kwarg'): column__value('defaultValue', Make.Constant(None)),
	__attribute('level'): column__value('defaultValue', Make.Constant(0)),
	__attribute('lower'): column__value('defaultValue', Make.Constant(None)),
	__attribute('msg'): column__value('defaultValue', Make.Constant(None)),
	__attribute('optional_vars'): column__value('defaultValue', Make.Constant(None)),
	__attribute('rest'): column__value('defaultValue', Make.Constant(None)),
	__attribute('simple'): column__value('defaultValue', Make.Call(Make.Name('int'), [Make.Call(Make.Name('isinstance'), [Make.Name('target'), Make.Attribute(Make.Name('ast'), 'Name')])])),
	__attribute('step'): column__value('defaultValue', Make.Constant(None)),
	__attribute('type'): column__value('defaultValue', Make.Constant(None)),
	__attribute('type_comment'): column__value('defaultValue', Make.Constant(None)),
	__attribute('upper'): column__value('defaultValue', Make.Constant(None)),
	__attribute('vararg'): column__value('defaultValue', Make.Constant(None)),
}

defaultValue__attributeType_attribute: dict[__attributeType_attribute, column__value] = {
	__attributeType_attribute('int | None', 'end_col_offset'): column__value('defaultValue', Make.Constant(None)),
	__attributeType_attribute('int | None', 'end_lineno'): column__value('defaultValue', Make.Constant(None)),
}

defaultValue__ClassDefIdentifier_attribute: dict[__ClassDefIdentifier_attribute, column__value] = {
	__ClassDefIdentifier_attribute('AnnAssign', 'value'): column__value('defaultValue', Make.Constant(None)),
	__ClassDefIdentifier_attribute('arg', 'annotation'): column__value('defaultValue', Make.Constant(None)),
	__ClassDefIdentifier_attribute('AsyncFunctionDef', 'returns'): column__value('defaultValue', Make.Constant(None)),
	__ClassDefIdentifier_attribute('Dict', 'keys'): column__value('defaultValue', Make.List([Make.Constant(None)])),
	__ClassDefIdentifier_attribute('ExceptHandler', 'name'): column__value('defaultValue', Make.Constant(None)),
	__ClassDefIdentifier_attribute('FunctionDef', 'returns'): column__value('defaultValue', Make.Constant(None)),
	__ClassDefIdentifier_attribute('MatchAs', 'name'): column__value('defaultValue', Make.Constant(None)),
	__ClassDefIdentifier_attribute('MatchAs', 'pattern'): column__value('defaultValue', Make.Constant(None)),
	__ClassDefIdentifier_attribute('MatchStar', 'name'): column__value('defaultValue', Make.Constant(None)),
	__ClassDefIdentifier_attribute('Return', 'value'): column__value('defaultValue', Make.Constant(None)),
	__ClassDefIdentifier_attribute('Yield', 'value'): column__value('defaultValue', Make.Constant(None)),
}

move2keywordArguments__attribute: dict[__attribute, column__value] = {
	__attribute("type_comment"): column__value('move2keywordArguments', "Unpack"),
	__attribute("simple"): column__value('move2keywordArguments', True),  # noqa: FBT003
}

move2keywordArguments__attributeKind: dict[__attributeKind, column__value] = {
	__attributeKind("No"): column__value('move2keywordArguments', "No"),
	__attributeKind("_attribute"): column__value('move2keywordArguments', "No"),
}

dictionary_defaultValue_ast_arg_Call_keyword_orElse: dict[__attribute | __ClassDefIdentifier_attribute, ast.expr] = {
	__attribute('bases'): Make.List(),
	__attribute('cases'): Make.List(),
	__attribute('ctx'): Make.Call(Make.Attribute(Make.Name('ast'), 'Load')),
	__attribute('decorator_list'): Make.List(),
	__attribute('defaults'): Make.List(),
	__attribute('elts'): Make.List(),
	__attribute('finalbody'): Make.List(),
	__attribute('keywords'): Make.List(),
	__attribute('kw_defaults'): Make.List(),
	__attribute('kwd_attrs'): Make.List(),
	__attribute('kwd_patterns'): Make.List(),
	__attribute('kwonlyargs'): Make.List(),
	__attribute('patterns'): Make.List(),
	__attribute('posonlyargs'): Make.List(),
	__attribute('type_ignores'): Make.List(),
	__ClassDefIdentifier_attribute('arguments', 'args'): Make.List(),
	__ClassDefIdentifier_attribute('AsyncFor', 'orelse'): Make.List(),
	__ClassDefIdentifier_attribute('AsyncFunctionDef', 'args'): Make.Call(Make.Attribute(Make.Name('ast'), 'arguments')),
	__ClassDefIdentifier_attribute('AsyncFunctionDef', 'body'): Make.List(),
	__ClassDefIdentifier_attribute('AsyncFunctionDef', 'type_params'): Make.List(),
	__ClassDefIdentifier_attribute('Call', 'args'): Make.List(),
	__ClassDefIdentifier_attribute('ClassDef', 'body'): Make.List(),
	__ClassDefIdentifier_attribute('ClassDef', 'type_params'): Make.List(),
	__ClassDefIdentifier_attribute('Dict', 'keys'): Make.List(),
	__ClassDefIdentifier_attribute('Dict', 'values'): Make.List(),
	__ClassDefIdentifier_attribute('ExceptHandler', 'body'): Make.List(),
	__ClassDefIdentifier_attribute('For', 'orelse'): Make.List(),
	__ClassDefIdentifier_attribute('FunctionDef', 'args'): Make.Call(Make.Attribute(Make.Name('ast'), 'arguments')),
	__ClassDefIdentifier_attribute('FunctionDef', 'body'): Make.List(),
	__ClassDefIdentifier_attribute('FunctionDef', 'type_params'): Make.List(),
	__ClassDefIdentifier_attribute('If', 'orelse'): Make.List(),
	__ClassDefIdentifier_attribute('match_case', 'body'): Make.List(),
	__ClassDefIdentifier_attribute('MatchMapping', 'keys'): Make.List(),
	__ClassDefIdentifier_attribute('Try', 'orelse'): Make.List(),
	__ClassDefIdentifier_attribute('TryStar', 'orelse'): Make.List(),
	__ClassDefIdentifier_attribute('While', 'orelse'): Make.List(),
}

