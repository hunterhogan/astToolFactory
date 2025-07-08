"""Large blocks of 'pre-fabricated' static code added to manufactured AST tools."""
from astToolFactory import (
	astName_overload, astName_staticmethod, astSubscriptUnpack_ast_attributes, settingsManufacturing)
from astToolFactory.documentation import docstrings
from astToolkit import Make
from typing import NotRequired, TypedDict
import ast

# `Grab` =====================================================================
FunctionDefGrab_andDoAllOf: ast.stmt = Make.FunctionDef('andDoAllOf'
	, Make.arguments(list_arg=[Make.arg('listOfActions', Make.Subscript(Make.Name('Sequence'), Make.Subscript(Make.Name('Callable'), Make.Tuple([Make.List([Make.Name('Any')]), Make.Name('Any')]))))])
	, body=[Make.FunctionDef('workhorse'
			, Make.arguments(list_arg=[Make.arg('node', Make.Name('个'))])
			, body=[Make.For(Make.Name('action', Make.Store()), iter=Make.Name('listOfActions')
					, body=[Make.Assign([Make.Name('node', Make.Store())], value=Make.Call(Make.Name('action'), listParameters=[Make.Name('node')]))]), Make.Return(Make.Name('node'))]
			, returns=Make.Name('个')), Make.Return(Make.Name('workhorse'))]
	, decorator_list=[astName_staticmethod]
	, returns=Make.Subscript(Make.Name('Callable'), Make.Tuple([Make.List([Make.Name('个')]), Make.Name('个')])))

# `Index` =====================================================================
listFunctionDefs_index: list[ast.stmt] = [
Make.FunctionDef('index'
	, Make.arguments(list_arg=[Make.arg('at', annotation=Make.Name('int'))])
	, body=[Make.FunctionDef('workhorse'
		, Make.arguments(list_arg=[Make.arg('node', annotation=Make.Subscript(Make.Name('Sequence'), slice=Make.Name('个')))])
		, body=[Make.Return(Make.Call(Make.Name('cast'), listParameters=[Make.Constant('归个'), Make.Subscript(Make.Name('node'), slice=Make.Name('at'))]))]
		, returns=Make.Name('归个')), Make.Return(Make.Name('workhorse'))]
	, returns=Make.Subscript(Make.Name('Callable'), slice=Make.Tuple([Make.List([Make.Subscript(Make.Name('Sequence'), slice=Make.Name('个'))]), Make.Name('归个')]))
	, type_params=[Make.TypeVar('个'), Make.TypeVar('归个')])
,
Make.FunctionDef('indices'
	, Make.arguments(list_arg=[Make.arg('at', annotation=Make.Name('slice'))])
	, body=[Make.FunctionDef('workhorse'
		, Make.arguments(list_arg=[Make.arg('node', annotation=Make.Subscript(Make.Name('Sequence'), slice=Make.Name('个')))])
		, body=[Make.Return(Make.Call(Make.Name('cast'), listParameters=[Make.Constant('归个'), Make.Subscript(Make.Name('node'), slice=Make.Name('at'))]))]
		, returns=Make.Name('归个')), Make.Return(Make.Name('workhorse'))]
	, returns=Make.Subscript(Make.Name('Callable'), slice=Make.Tuple([Make.List([Make.Subscript(Make.Name('Sequence'), slice=Make.Name('个'))]), Make.Name('归个')]))
	, type_params=[Make.TypeVar('个'), Make.TypeVar('归个')])
]

# `Make` =====================================================================
def makeFunctionDef_join(identifierContainer: str, identifierCallee: str, docstring: ast.Expr) -> ast.stmt:
	"""Create a `FunctionDef` AST node for a join method.

	(AI generated docstring)

	Constructs a `classmethod` `FunctionDef` that accepts expressions and joins them using a specified callee method.
	The generated method signature includes type annotations for container types and supports keyword arguments.

	Parameters
	----------
	identifierContainer : str
		The type identifier for the expressions container (e.g., 'Sequence', 'Iterable').
	identifierCallee : str
		The method name to call on `Make` for joining the expressions.
	docstring : ast.Expr
		The docstring expression to include in the function body.

	Returns
	-------
	functionDef : ast.stmt
		A `FunctionDef` AST node representing the join method.

	"""
	return Make.FunctionDef('join'
		, Make.arguments(list_arg=[Make.arg('cls'), Make.arg('expressions', annotation=Make.Subscript(Make.Name(identifierContainer), slice=Make.Attribute(Make.Name('ast'), 'expr')))]
						, kwarg=Make.arg('keywordArguments', annotation=Make.Subscript(Make.Name('Unpack'), slice=Make.Name('ast_attributes'))))
		, body=[docstring
			, Make.Return(Make.Call(callee=Make.Attribute(Make.Name('Make'), identifierCallee), listParameters=[Make.Name('cls'), Make.Name('expressions')], list_keyword=[Make.keyword(None, value=Make.Name('keywordArguments'))]))]
		, decorator_list=[Make.Name('classmethod')]
		, returns=Make.Attribute(Make.Name('ast'), 'expr'))

FunctionDef_boolopJoinMethod: ast.stmt = Make.FunctionDef(settingsManufacturing.identifiers['boolopJoinMethod']
    , Make.arguments(list_arg=[Make.arg('ast_operator', annotation=Make.Subscript(Make.Name('type'), slice=Make.Attribute(Make.Name('ast'), 'boolop')))
            , Make.arg('expressions', annotation=Make.Subscript(Make.Name('Sequence'), slice=Make.Attribute(Make.Name('ast'), 'expr')))
            ]
        , kwarg=Make.arg('keywordArguments', annotation=Make.Subscript(Make.Name('Unpack'), slice=Make.Name('ast_attributes')))
    )
    , body=[docstrings[settingsManufacturing.identifiers['Make']]['_boolopJoinMethod']
		, Make.AnnAssign(Make.Name('listExpressions', Make.Store())
                        , annotation=Make.Subscript(Make.Name('list'), slice=Make.Attribute(Make.Name('ast'), 'expr'))
                        , value=Make.Call(Make.Name('list'), listParameters=[Make.Name('expressions')])
                    )
        , Make.Match(subject=Make.Call(Make.Name('len'), listParameters=[Make.Name('listExpressions')])
                    , cases=[Make.match_case(pattern=Make.MatchValue(Make.Constant(0))
                                , body=[Make.Assign([Make.Name('expressionsJoined', Make.Store())], value=Make.Call(Make.Attribute(Make.Name('Make'), 'Constant'), listParameters=[Make.Constant('')], list_keyword=[Make.keyword(None, value=Make.Name('keywordArguments'))]))])
                            , Make.match_case(pattern=Make.MatchValue(value=Make.Constant(1))
                                , body=[Make.Assign([Make.Name('expressionsJoined', Make.Store())], value=Make.Subscript(Make.Name('listExpressions'), slice=Make.Constant(0)))])
                            , Make.match_case(pattern=Make.MatchAs()
                                , body=[Make.Assign([Make.Name('expressionsJoined', Make.Store())]
                                                    , value=Make.Call(Make.Attribute(Make.Name('Make'), 'BoolOp')
                                                            , listParameters=[Make.Call(Make.Name('ast_operator')), Make.Name('listExpressions')]
                                                            , list_keyword=[Make.keyword(None, value=Make.Name('keywordArguments'))]
                                                            )
                                                )
                                    ]
                            )
                        ]
                    )
        , Make.Return(Make.Name('expressionsJoined'))]
	, decorator_list=[astName_staticmethod]
    , returns=Make.BitOr().join([Make.Attribute(Make.Name('ast'), 'expr'), Make.Attribute(Make.Name('ast'), 'BoolOp')]))

FunctionDef_join_boolop: ast.stmt = makeFunctionDef_join('Sequence', settingsManufacturing.identifiers['boolopJoinMethod'], docstrings[settingsManufacturing.identifiers['Make']]['join_boolop'])
FunctionDef_join_operator: ast.stmt = makeFunctionDef_join('Iterable', settingsManufacturing.identifiers['operatorJoinMethod'], docstrings[settingsManufacturing.identifiers['Make']]['join_operator'])

FunctionDef_operatorJoinMethod: ast.stmt = Make.FunctionDef(settingsManufacturing.identifiers['operatorJoinMethod']
	, Make.arguments(list_arg=[Make.arg('ast_operator', annotation=Make.Subscript(Make.Name('type'), slice=Make.Attribute(Make.Name('ast'), 'operator')))
						, Make.arg('expressions', annotation=Make.Subscript(Make.Name('Iterable'), slice=Make.Attribute(Make.Name('ast'), 'expr')))]
					, kwarg=Make.arg('keywordArguments', annotation=Make.Subscript(Make.Name('Unpack'), slice=Make.Name('ast_attributes'))))
	, body=[docstrings[settingsManufacturing.identifiers['Make']]['_operatorJoinMethod']
		, Make.AnnAssign(Make.Name('listExpressions', Make.Store()), annotation=Make.Subscript(Make.Name('list'), slice=Make.Attribute(Make.Name('ast'), 'expr'))
						, value=Make.Call(Make.Name('list'), listParameters=[Make.Name('expressions')]))
		, Make.If(Make.UnaryOp(Make.Not(), Make.Name('listExpressions'))
			, body=[Make.Expr(Make.Call(Make.Attribute(Make.Name('listExpressions'), 'append')
								, listParameters=[Make.Call(Make.Attribute(Make.Name('Make'), 'Constant')
										, listParameters=[Make.Constant('')], list_keyword=[Make.keyword(None, value=Make.Name('keywordArguments'))])]))])
		, Make.AnnAssign(Make.Name('expressionsJoined', Make.Store()), annotation=Make.Attribute(Make.Name('ast'), 'expr'), value=Make.Subscript(Make.Name('listExpressions'), slice=Make.Constant(0)))
		, Make.For(Make.Name('expression', Make.Store()), iter=Make.Subscript(Make.Name('listExpressions'), slice=Make.Slice(lower=Make.Constant(1)))
			, body=[Make.Assign([Make.Name('expressionsJoined', Make.Store())]
						, value=Make.Call(Make.Attribute(Make.Name('ast'), 'BinOp')
								, list_keyword=[Make.keyword('left', Make.Name('expressionsJoined'))
											, Make.keyword('op', Make.Call(Make.Name('ast_operator')))
											, Make.keyword('right', Make.Name('expression'))
											, Make.keyword(None, value=Make.Name('keywordArguments'))]))])
		, Make.Return(Make.Name('expressionsJoined'))]
	, decorator_list=[astName_staticmethod]
	, returns=Make.Attribute(Make.Name('ast'), 'expr'))

FunctionDefMake_Attribute: ast.stmt = Make.FunctionDef('Attribute'
	, Make.arguments(list_arg=[Make.arg('value', annotation=Make.Attribute(Make.Name('ast'), 'expr'))]
		, vararg=Make.arg('attribute', annotation=Make.Name('str'))
		, kwonlyargs=[Make.arg('context', annotation=Make.BitOr.join([Make.Attribute(Make.Name('ast'), 'expr_context'), Make.Constant(None)]))]
		, kw_defaults=[Make.Constant(None)]
		, kwarg=Make.arg('keywordArguments', annotation=Make.Subscript(Make.Name('Unpack'), slice=Make.Name('ast_attributes'))))
	, body=[docstrings[settingsManufacturing.identifiers['Make']]['Attribute']
		, Make.Assign([Make.Name('ctx', Make.Store())], value=Make.Or.join([Make.Name('context'), Make.Call(Make.Attribute(Make.Name('ast'), 'Load'))]))
		, Make.FunctionDef('addDOTattribute'
			, Make.arguments(list_arg=[Make.arg('chain', annotation=Make.Attribute(Make.Name('ast'), 'expr'))
					, Make.arg('identifier', annotation=Make.Name('str'))
					, Make.arg('ctx', annotation=Make.Attribute(Make.Name('ast'), 'expr_context'))]
				, kwarg=Make.arg('keywordArguments', annotation=Make.Subscript(Make.Name('Unpack'), slice=Make.Name('ast_attributes'))))
			, body=[Make.Return(Make.Call(Make.Attribute(Make.Name('ast'), 'Attribute')
					, list_keyword=[Make.keyword('value', Make.Name('chain')), Make.keyword('attr', Make.Name('identifier'))
						, Make.keyword('ctx', Make.Name('ctx')), Make.keyword(None, value=Make.Name('keywordArguments'))]))]
			, returns=Make.Attribute(Make.Name('ast'), 'Attribute'))
		, Make.Assign([Make.Name('buffaloBuffalo', Make.Store())], value=Make.Call(Make.Name('addDOTattribute')
					, listParameters=[Make.Name('value'), Make.Subscript(Make.Name('attribute'), slice=Make.Constant(0)), Make.Name('ctx')]
					, list_keyword=[Make.keyword(None, value=Make.Name('keywordArguments'))]))
		, Make.For(Make.Name('identifier', Make.Store()), iter=Make.Subscript(Make.Name('attribute'), slice=Make.Slice(lower=Make.Constant(1), upper=Make.Constant(None)))
			, body=[Make.Assign([Make.Name('buffaloBuffalo', Make.Store())], value=Make.Call(Make.Name('addDOTattribute')
					, listParameters=[Make.Name('buffaloBuffalo'), Make.Name('identifier'), Make.Name('ctx')]
					, list_keyword=[Make.keyword(None, value=Make.Name('keywordArguments'))]))])
		, Make.Return(Make.Name('buffaloBuffalo'))]
	, decorator_list=[astName_staticmethod]
	, returns=Make.Attribute(Make.Name('ast'), 'Attribute'))

# This relatively simple FunctionDef can probably be removed from the annex after I tweak a few things in the dataframe.
# Minimum changes in the dataframe data for this 'ClassDefIdentifier': 'attributeRename', override 'type'.
# Oh, wait. I don't plan to add anything that would _add_ `Make.arg('asName')` to 'match_args'.
ClassDefIdentifier: str = 'Import' # `ClassDefIdentifier` and not `FunctionDefIdentifier` to be consistent with `makeToolMake` in "factory.py".
FunctionDefMake_Import: ast.stmt = Make.FunctionDef(ClassDefIdentifier
	, Make.arguments(list_arg=[Make.arg('dotModule', annotation=Make.Name('identifierDotAttribute'))
			, Make.arg('asName', annotation=Make.BitOr().join([Make.Name('str'), Make.Constant(None)]))]
		, kwarg=Make.arg('keywordArguments', annotation=Make.Subscript(Make.Name('Unpack'), slice=Make.Name('ast_attributes')))
		, defaults=[Make.Constant(None)])
	, body=[docstrings[settingsManufacturing.identifiers['Make']][ClassDefIdentifier]
		, Make.Return(Make.Call(Make.Attribute(Make.Name('ast'), ClassDefIdentifier)
			, list_keyword=[Make.keyword('names', Make.List([Make.Call(Make.Attribute(Make.Name('Make'), 'alias')
				, listParameters=[Make.Name('dotModule'), Make.Name('asName')])])), Make.keyword(None, value=Make.Name('keywordArguments'))]))]
	, decorator_list=[astName_staticmethod]
	, returns=Make.Attribute(Make.Name('ast'), ClassDefIdentifier))
del ClassDefIdentifier

ClassDefIdentifier: str = 'keyword' # `ClassDefIdentifier` and not `FunctionDefIdentifier` to be consistent with `makeToolMake` in "factory.py".
listOverloads_keyword: list[ast.stmt] = [
	Make.FunctionDef(ClassDefIdentifier
		, Make.arguments(list_arg=[Make.arg('Buffalo_buffalo_Buffalo_buffalo_buffalo_buffalo_Buffalo_buffalo'
					, annotation=Make.BitOr.join([Make.Name('str'), Make.Constant(None)]))
				, Make.arg('value', annotation=Make.Attribute(Make.Name('ast'), 'expr'))]
			, kwarg=Make.arg('keywordArguments', annotation=astSubscriptUnpack_ast_attributes))
		, body=[Make.Expr(value=Make.Constant(...))]
		, decorator_list=[astName_staticmethod, astName_overload]
		, returns=Make.Attribute(Make.Name('ast'), ClassDefIdentifier))
	, Make.FunctionDef(ClassDefIdentifier
		, Make.arguments(list_arg=[Make.arg('Buffalo_buffalo_Buffalo_buffalo_buffalo_buffalo_Buffalo_buffalo'
				, annotation=Make.BitOr.join([Make.Name('str'), Make.Constant(None)]))]
			, kwonlyargs=[Make.arg('value', annotation=Make.Attribute(Make.Name('ast'), 'expr'))]
			, kw_defaults=[None]
			, kwarg=Make.arg('keywordArguments', annotation=Make.Subscript(Make.Name('Unpack'), slice=Make.Name('ast_attributes')))
			, defaults=[Make.Constant(None)])
		, body=[Make.Expr(value=Make.Constant(...))]
		, decorator_list=[astName_staticmethod, astName_overload]
		, returns=Make.Attribute(Make.Name('ast'), ClassDefIdentifier))]
del ClassDefIdentifier

# `theSSOT` =====================================================================
astModule_theSSOT = Make.Module([
    Make.ImportFrom('importlib', list_alias=[Make.alias('import_module', asName='importlib_import_module')])
	, Make.ImportFrom('inspect', list_alias=[Make.alias('getfile', asName='inspect_getfile')])
	, Make.ImportFrom('pathlib', list_alias=[Make.alias('Path')])
	, Make.ImportFrom('tomli', list_alias=[Make.alias('load', asName='tomli_load')])
	, Make.Import(dotModule='dataclasses')
	, Make.Assign([Make.Name('identifierPackage', Make.Store())], value=Make.Constant('astToolkit'))
	, Make.FunctionDef('getPathPackageINSTALLING'
		, Make.arguments()
        , body=[Make.AnnAssign(Make.Name('pathPackage', Make.Store()), annotation=Make.Name('Path')
				, value=Make.Call(Make.Name('Path')
					, listParameters=[Make.Call(Make.Name('inspect_getfile')
						, listParameters=[Make.Call(Make.Name('importlib_import_module')
							, listParameters=[Make.Name('identifierPackage')])])]))
			, Make.If(test=Make.Call(Make.Attribute(Make.Name('pathPackage'), 'is_file'))
				, body=[Make.Assign([Make.Name('pathPackage', Make.Store())], value=Make.Attribute(Make.Name('pathPackage'), 'parent'))])
			, Make.Return(value=Make.Name('pathPackage'))
		]
        , returns=Make.Name('Path')
	)
	, Make.ClassDef('PackageSettings'
		, body=[
            Make.AnnAssign(Make.Name('fileExtension', Make.Store())
				, annotation=Make.Name('str')
                , value=Make.Call(Make.Attribute(Make.Name('dataclasses'), 'field'), list_keyword=[Make.keyword('default', value=Make.Constant('.py'))]))
			, Make.Expr(value=Make.Constant('Default file extension for generated code files.'))
			, Make.AnnAssign(Make.Name('packageName', Make.Store())
				, annotation=Make.Name('str')
                , value=Make.Call(Make.Attribute(Make.Name('dataclasses'), 'field'), list_keyword=[Make.keyword('default', value=Make.Name('identifierPackage'))]))
			, Make.Expr(Make.Constant('Name of this package, used for import paths and configuration.'))
			, Make.AnnAssign(Make.Name('pathPackage', Make.Store())
				, annotation=Make.Name('Path')
                , value=Make.Call(Make.Attribute(Make.Name('dataclasses'), 'field'), list_keyword=[Make.keyword('default_factory', value=Make.Name('getPathPackageINSTALLING'))
												, Make.keyword('metadata', value=Make.Dict(keys=[Make.Constant('evaluateWhen')], values=[Make.Constant('installing')]))
                                                ]))
			, Make.Expr(Make.Constant('Absolute path to the installed package directory.'))
		]
    , decorator_list=[Make.Attribute(Make.Name('dataclasses'), 'dataclass')]
    )
	, Make.Assign([Make.Name('packageSettings', Make.Store())], value=Make.Call(Make.Name('PackageSettings')))])

# `TypeAlias` =====================================================================
listHandmade_astTypes: list[ast.stmt] = [
    # If I were to automate the creation of ConstantValueType from ast.pyi `_ConstantValue`, their definition doesn't include `bytes` or `range`.
    # And, I would change the identifier to `ast_ConstantValue`.
	Make.TypeAlias(Make.Name('ConstantValueType', Make.Store()), type_params=[]
		, value=Make.BitOr().join(Make.Name(identifier)
			for identifier in ['bool', 'bytes', 'complex', 'EllipsisType', 'float', 'int', 'None', 'range', 'str']))
	, Make.TypeAlias(Make.Name('identifierDotAttribute', Make.Store()), type_params=[], value=Make.Name('str'))
]

class dataTypeVariables(TypedDict):
	"""Type specification for `TypeVar` configuration data.

	(AI generated docstring)

	Defines the structure for configuration parameters used when creating `TypeVar` instances.
	All fields are optional and provide different aspects of type variable behavior.

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

typeVariables: dict[str, dataTypeVariables] = {
	'个': {'tuple_keyword': [('covariant', True)]},
	'归个': {'tuple_keyword': [('covariant', True)]},
	'文件': {'tuple_keyword': [('covariant', True)]},
	'文义': {'tuple_keyword': [('covariant', True)]}
}
for astSuperClass, identifierTypeVariable in settingsManufacturing.astSuperClasses.items():
	typeVariables[identifierTypeVariable] = {
		'bound': Make.Attribute(Make.Name('ast'), astSuperClass),
		'tuple_keyword': [('covariant', True)],
	}

for identifierTypeVariable, data in typeVariables.items():
	listParameters: list[ast.expr] = [Make.Constant(identifierTypeVariable)]
	if 'constraints' in data:
		listParameters.extend(data['constraints'])

	list_keyword: list[ast.keyword] = []
	if 'bound' in data:
		list_keyword.append(Make.keyword('bound', value=data['bound']))
	if 'tuple_keyword' in data:
		for Buffalo_buffalo_Buffalo_buffalo_buffalo_buffalo_Buffalo_buffalo, value in data['tuple_keyword']:
			list_keyword.append(Make.keyword(Buffalo_buffalo_Buffalo_buffalo_buffalo_buffalo_Buffalo_buffalo, value=Make.Constant(value)))
	if 'default_value' in data:
		list_keyword.append(Make.keyword('default_value', value=data['default_value']))

	# Create the TypeVar assignment
	listHandmade_astTypes.append(Make.Assign([Make.Name(identifierTypeVariable, Make.Store())] , value=Make.Call(Make.Name('typing_TypeVar')
		, listParameters=listParameters
		, list_keyword=list_keyword)))

listHandmade_astTypes.extend([
# ruff: noqa: FBT003
	# TODO, a non-trivial automatic transformation from ast.pyi `TypedDict._Attributes` and `TypeVar._EndPositionT` to the following
	Make.ClassDef('_attributes', bases=[Make.Name('TypedDict')], list_keyword=[Make.keyword('total', value=Make.Constant(False))]
		, body=[Make.AnnAssign(Make.Name('lineno', Make.Store()), annotation=Make.Name('int'))
			, Make.AnnAssign(Make.Name('col_offset', Make.Store()), annotation=Make.Name('int'))
		]
	),
	Make.ClassDef('ast_attributes', bases=[Make.Name('_attributes')], list_keyword=[Make.keyword('total', value=Make.Constant(False))]
		, body=[Make.AnnAssign(Make.Name('end_lineno', Make.Store()), annotation=Make.BitOr().join([Make.Name('int'), Make.Constant(None)]))
			, Make.AnnAssign(Make.Name('end_col_offset', Make.Store()), annotation=Make.BitOr().join([Make.Name('int'), Make.Constant(None)]))
		]
	),
	Make.ClassDef('ast_attributes_int', bases=[Make.Name('_attributes')], list_keyword=[Make.keyword('total', value=Make.Constant(False))]
		, body=[Make.AnnAssign(Make.Name('end_lineno', Make.Store()), annotation=Make.Name('int'))
			, Make.AnnAssign(Make.Name('end_col_offset', Make.Store()), annotation=Make.Name('int'))
		]
	),
	Make.ClassDef('ast_attributes_type_comment', bases=[Make.Name('ast_attributes')], list_keyword=[Make.keyword('total', value=Make.Constant(False))]
		, body=[Make.AnnAssign(Make.Name('type_comment', Make.Store()), annotation=Make.BitOr().join([Make.Name('str'), Make.Constant(None)]))]
	),
])
