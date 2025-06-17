from astToolkit import Make
import ast

_columns: list[str] = [
	# read from sources
    # Interpreter
	'ClassDefIdentifier',
	'versionMajorPythonInterpreter',
	'versionMinorPythonInterpreter',
	'versionMicroPythonInterpreter',
	'base',

    # stdlib/ast.pyi
	'deprecated',
	'match_args',
	'attribute',
	'attributeKind',
	'type',

	# Purely a human choice
	'attributeRename',
	'move2keywordArguments',
	'defaultValue', # (for now)

	# columns computed from sources per row
	'classAs_astAttribute',
	'canBeNone',
	'type_ast_expr',
	'ast_arg',
	'TypeAlias_hasDOTIdentifier',
	'TypeAlias_hasDOTSubcategory',

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
]

"""
NOTE How to construct an identifier for a dictionary to update the dataframe:
Use the actual column names, case sensitive.
columnLHS__columnRHS: dict[str, str] = {}
columnLHS__columnRHS_columnRHSn: dict[tuple[str, bool], str] = {}
Convert punctuation to underscores:
`_` -> `,`
`__` -> `=`
The dictionaries are used in statement like these:
dataframe['columnLHS'] = dataframe['columnRHS'].map(columnLHS__columnRHS).fillna(dataframe['columnLHS'])
dataframe['columnLHS'] = dataframe[['columnRHS', 'columnRHSn']].apply(tuple, axis='columns').map(columnLHS__columnRHS_columnRHSn).fillna(dataframe['columnLHS'])
"""

"""
dataframe = dataframe[dataframe['deprecated'].apply(str).str.contains("False", regex=False, na=False, case=False)]
"""

attributeRename__attribute: dict[str, str] = {
    'arg': 'Buffalo_buffalo_Buffalo_buffalo_buffalo_buffalo_Buffalo_buffalo',
    'asname': 'asName',
    'attr': 'attribute',
    'ctx': 'context',
    'elt': 'element',
    'elts': 'listElements',
    'func': 'callee',
    'keywords': 'list_keyword',
    'module': 'dotModule',
    'orelse': 'orElse',
}

attributeRename__ClassDefIdentifier_attribute: dict[tuple[str, str], str] = {
    ('arguments', 'args'): 'list_arg',
    ('AsyncFunctionDef', 'args'): 'argumentSpecification',
    ('Call', 'args'): 'listParameters',
    ('FunctionDef', 'args'): 'argumentSpecification',
    ('ImportFrom', 'names'): 'list_alias',
    ('Lambda', 'args'): 'argumentSpecification',
}

defaultValue__attribute: dict[str, ast.expr] = {
    'asname': Make.Constant(None),
    'bases': Make.List(),
    'bound': Make.Constant(None),
    'cases': Make.List(),
    'cause': Make.Constant(None),
    'ctx': Make.Call(Make.Attribute(Make.Name('ast'), 'Load')),
    'decorator_list': Make.List(),
    'default_value': Make.Constant(None),
    'defaults': Make.List(),
    'elts': Make.List(),
    'exc': Make.Constant(None),
    'finalbody': Make.List(),
    'format_spec': Make.Constant(None),
    'guard': Make.Constant(None),
    'keywords': Make.List(),
    'kind': Make.Constant(None),
    'kw_defaults': Make.List([Make.Constant(None)]),
    'kwarg': Make.Constant(None),
    'kwd_attrs': Make.List(),
    'kwd_patterns': Make.List(),
    'kwonlyargs': Make.List(),
    'level': Make.Constant(0),
    'lower': Make.Constant(None),
    'msg': Make.Constant(None),
    'optional_vars': Make.Constant(None),
    'patterns': Make.List(),
    'posonlyargs': Make.List(),
    'rest': Make.Constant(None),
    'simple': Make.Call(Make.Name('int'), [Make.Call(Make.Name('isinstance'), [Make.Name('target'), Make.Attribute(Make.Name('ast'), 'Name')])]),
    'step': Make.Constant(None),
    'type': Make.Constant(None),
    'type_comment': Make.Constant(None),
    'type_ignores': Make.List(),
    'upper': Make.Constant(None),
    'vararg': Make.Constant(None),
}

defaultValue__ClassDefIdentifier_attribute: dict[tuple[str, str], ast.expr] = {
    ('AnnAssign', 'value'): Make.Constant(None),
    ('arg', 'annotation'): Make.Constant(None),
    ('arguments', 'args'): Make.List(),
    ('AsyncFor', 'orelse'): Make.List(),
    ('AsyncFunctionDef', 'args'): Make.Call(Make.Attribute(Make.Name('ast'), 'arguments')),
    ('AsyncFunctionDef', 'body'): Make.List(),
    ('AsyncFunctionDef', 'returns'): Make.Constant(None),
    ('AsyncFunctionDef', 'type_params'): Make.List(),
    ('Call', 'args'): Make.List(),
    ('ClassDef', 'body'): Make.List(),
    ('ClassDef', 'type_params'): Make.List(),
    ('Dict', 'keys'): Make.List([Make.Constant(None)]),
    ('Dict', 'values'): Make.List(),
    ('ExceptHandler', 'body'): Make.List(),
    ('ExceptHandler', 'name'): Make.Constant(None),
    ('For', 'orelse'): Make.List(),
    ('FunctionDef', 'args'): Make.Call(Make.Attribute(Make.Name('ast'), 'arguments')),
    ('FunctionDef', 'body'): Make.List(),
    ('FunctionDef', 'returns'): Make.Constant(None),
    ('FunctionDef', 'type_params'): Make.List(),
    ('If', 'orelse'): Make.List(),
    ('match_case', 'body'): Make.List(),
    ('MatchAs', 'name'): Make.Constant(None),
    ('MatchAs', 'pattern'): Make.Constant(None),
    ('MatchMapping', 'keys'): Make.List(),
    ('Return', 'value'): Make.Constant(None),
    ('Try', 'orelse'): Make.List(),
    ('TryStar', 'orelse'): Make.List(),
    ('While', 'orelse'): Make.List(),
    ('Yield', 'value'): Make.Constant(None),
}

defaultValue__type_attribute: dict[tuple[str, str], ast.expr] = {
	('int | None', 'end_col_offset'): Make.Constant(None),
	('int | None', 'end_lineno'): Make.Constant(None),
}

move2keywordArguments__attributeKind: dict[str, str] = {
    "No": "No",
    "_attribute": "No",
}

move2keywordArguments__attribute: dict[str, str] = {
    "type_comment": "Unpack",
    "simple": "True",
}

type__ClassDefIdentifier_attribute: dict[tuple[str, str], str] = {
    ('Constant', 'value'): "ConstantValueType",
}
