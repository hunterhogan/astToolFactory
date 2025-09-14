"""Large blocks of 'pre-fabricated' static code added to manufactured AST tools."""
from astToolFactory import (
	astASTastAttribute, astName_classmethod, astName_overload, astName_staticmethod, astSubscriptUnpack_ast_attributes,
	keywordKeywordArguments4Call, settingsManufacturing)
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

FunctionDefGrab_indexV2: ast.stmt = Make.FunctionDef(
	'index',
	Make.arguments(
		posonlyargs=[
			Make.arg(
				'at',
				annotation=Make.Name('int'))],
		list_arg=[
			Make.arg(
				'action',
				annotation=Make.Subscript(
					value=Make.Name('Callable'),
					slice=Make.Tuple(
						[
							Make.List(
								[
									Make.Name('Any')]),
							Make.Name('Any')])))]),
	body=[
		Make.FunctionDef(
			'workhorse',
			Make.arguments(
				list_arg=[
					Make.arg(
						'node',
						annotation=Make.Subscript(
							value=Make.Name('Sequence'),
							slice=Make.Name('个')))]),
			body=[
				Make.Assign(
					targets=[
						Make.Name('node', context=Make.Store())],
					value=Make.Call(
						Make.Name('list'),
						listParameters=[
							Make.Name('node')])),
				Make.Assign(
					targets=[
						Make.Name('consequences', context=Make.Store())],
					value=Make.Call(
						Make.Name('action'),
						listParameters=[
							Make.Subscript(
								value=Make.Name('node'),
								slice=Make.Name('at'))])),
				Make.If(
					test=Make.Compare(
						left=Make.Name('consequences'),
						ops=[
							Make.Is()],
						comparators=[
							Make.Constant(None)]),
					body=[
						Make.Delete(
							targets=[
								Make.Subscript(
									value=Make.Name('node'),
									slice=Make.Name('at'),
									context=Make.Del())])],
					orElse=[
						Make.If(
							test=Make.Call(
								Make.Name('isinstance'),
								listParameters=[
									Make.Name('consequences'),
									Make.Name('list')]),
							body=[
								Make.Assign(
									targets=[
										Make.Name('node', context=Make.Store())],
									value=Make.BinOp(
										left=Make.BinOp(
											left=Make.Subscript(
												value=Make.Name('node'),
												slice=Make.Slice(
													lower=Make.Constant(0),
													upper=Make.Name('at'))),
											op=Make.Add(),
											right=Make.Name('consequences')),
										op=Make.Add(),
										right=Make.Subscript(
											value=Make.Name('node'),
											slice=Make.Slice(
												lower=Make.BinOp(
													left=Make.Name('at'),
													op=Make.Add(),
													right=Make.Constant(1)),
												upper=Make.Constant(None)))))],
							orElse=[
								Make.Assign(
									targets=[
										Make.Subscript(
											value=Make.Name('node'),
											slice=Make.Name('at'),
											context=Make.Store())],
									value=Make.Name('consequences'))])]),
				Make.Return(
					value=Make.Name('node'))],
			returns=Make.Subscript(
				value=Make.Name('list'),
				slice=Make.Name('个'))),
		Make.Return(
			value=Make.Name('workhorse'))],
	decorator_list=[Make.Name('staticmethod')],
	returns=Make.Subscript(
		value=Make.Name('Callable'),
		slice=Make.Tuple(
			[
				Make.List(
					[
						Make.Subscript(
							value=Make.Name('Sequence'),
							slice=Make.Name('个'))]),
				Make.Subscript(
					value=Make.Name('list'),
					slice=Make.Name('个'))])))


FunctionDefGrab_index: ast.stmt = Make.FunctionDef('index'
	, Make.arguments(posonlyargs=[Make.arg('at', Make.Name('int'))]
			, list_arg=[Make.arg('action', Make.Subscript(Make.Name('Callable'), Make.Tuple([Make.List([Make.Name('Any')]), Make.Name('Any')])))])
	, body=[Make.FunctionDef('workhorse'
			, Make.arguments(list_arg=[Make.arg('node', Make.Subscript(Make.Name('Sequence'), Make.Name('个')))])
			, body=[
				Make.Assign([Make.Name('node', context=Make.Store())], Make.Call(Make.Name('list'), [Make.Name('node')]))
				, Make.Assign([Make.Name('consequences', context=Make.Store())], Make.Call(Make.Name('action'), [Make.Subscript(Make.Name('node'), Make.Name('at'))]))
				, Make.If(Make.Compare(Make.Name('consequences'), [Make.Is()], [Make.Constant(None)])
					, body=[Make.Delete([Make.Subscript(Make.Name('node'), Make.Name('at'), context=Make.Del())])]
					, orElse=[Make.If(Make.Call(Make.Name('isinstance'), [Make.Name('consequences'), Make.Name('list')])
						, body=[Make.Assign([Make.Name('node', context=Make.Store())]
								, value=Make.Add().join([Make.Subscript(Make.Name('node'), Make.Slice(Make.Constant(0), Make.Name('at')))
									, Make.Name('consequences')
									, Make.Subscript(Make.Name('node'), Make.Slice(Make.Add().join([Make.Name('at'), Make.Constant(1)]), Make.Constant(None)))])
						)]
						, orElse=[Make.Assign([Make.Subscript(Make.Name('node'), Make.Name('at'), context=Make.Store())], Make.Name('consequences'))])]
				)
				, Make.Return(Make.Name('node'))]
			, returns=Make.Subscript(Make.Name('list'), Make.Name('个'))), Make.Return(Make.Name('workhorse'))]
		, decorator_list=[astName_staticmethod]
		, returns=Make.Subscript(Make.Name('Callable')
			, Make.Tuple([Make.List([Make.Subscript(Make.Name('Sequence'), Make.Name('个'))]), Make.Subscript(Make.Name('list'), Make.Name('个'))])))

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
	"""Make the `ast.FunctionDef` `.join` `@classmethod` for the `Make` classes that correspond to the `ast.boolop` and `ast.operator` subclasses.

	Parameters
	----------
	identifierContainer : str
		The type of container that will hold the `ast.expr` to be joined by the `@classmethod` (*i.e.*, 'Sequence', 'Iterable').
	identifierCallee : str
		The `Make` `class` of which the `.join` `@classmethod` will be a member.
	docstring : ast.Expr
		The docstring for the `.join` `@classmethod`.

	Returns
	-------
	astFunctionDef : ast.stmt
		The `ast.FunctionDef` `.join` `@classmethod`.

	"""
	return Make.FunctionDef('join'
		, Make.arguments(list_arg=[Make.arg('cls'), Make.arg('expressions', annotation=Make.Subscript(Make.Name(identifierContainer), slice=Make.Attribute(Make.Name('ast'), 'expr')))]
						, kwarg=Make.arg(settingsManufacturing.keywordArgumentsIdentifier, annotation=Make.Subscript(Make.Name('Unpack'), slice=Make.Name('ast_attributes'))))
		, body=[docstring
			, Make.Return(Make.Call(callee=Make.Attribute(Make.Name('Make'), identifierCallee), listParameters=[Make.Name('cls'), Make.Name('expressions')], list_keyword=[keywordKeywordArguments4Call]))]
		, decorator_list=[astName_classmethod]
		, returns=Make.Attribute(Make.Name('ast'), 'expr'))

FunctionDef_boolopJoinMethod: ast.stmt = Make.FunctionDef(settingsManufacturing.identifiers['boolopJoinMethod']
    , Make.arguments(list_arg=[Make.arg('ast_operator', annotation=Make.Subscript(Make.Name('type'), slice=Make.Attribute(Make.Name('ast'), 'boolop')))
            , Make.arg('expressions', annotation=Make.Subscript(Make.Name('Sequence'), slice=Make.Attribute(Make.Name('ast'), 'expr')))
            ]
        , kwarg=Make.arg(settingsManufacturing.keywordArgumentsIdentifier, annotation=Make.Subscript(Make.Name('Unpack'), slice=Make.Name('ast_attributes')))
    )
    , body=[docstrings[settingsManufacturing.identifiers['Make']]['_boolopJoinMethod']
		, Make.AnnAssign(Make.Name('listExpressions', Make.Store())
                        , annotation=Make.Subscript(Make.Name('list'), slice=Make.Attribute(Make.Name('ast'), 'expr'))
                        , value=Make.Call(Make.Name('list'), listParameters=[Make.Name('expressions')])
                    )
        , Make.Match(subject=Make.Call(Make.Name('len'), listParameters=[Make.Name('listExpressions')])
                    , cases=[Make.match_case(pattern=Make.MatchValue(Make.Constant(0))
                                , body=[Make.Assign([Make.Name('expressionsJoined', Make.Store())], value=Make.Call(Make.Attribute(Make.Name('Make'), 'Constant'), listParameters=[Make.Constant('')], list_keyword=[keywordKeywordArguments4Call]))])
                            , Make.match_case(pattern=Make.MatchValue(value=Make.Constant(1))
                                , body=[Make.Assign([Make.Name('expressionsJoined', Make.Store())], value=Make.Subscript(Make.Name('listExpressions'), slice=Make.Constant(0)))])
                            , Make.match_case(pattern=Make.MatchAs()
                                , body=[Make.Assign([Make.Name('expressionsJoined', Make.Store())]
                                                    , value=Make.Call(Make.Attribute(Make.Name('Make'), 'BoolOp')
                                                            , listParameters=[Make.Call(Make.Name('ast_operator')), Make.Name('listExpressions')]
                                                            , list_keyword=[keywordKeywordArguments4Call]
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
					, kwarg=Make.arg(settingsManufacturing.keywordArgumentsIdentifier, annotation=Make.Subscript(Make.Name('Unpack'), slice=Make.Name('ast_attributes'))))
	, body=[docstrings[settingsManufacturing.identifiers['Make']]['_operatorJoinMethod']
		, Make.AnnAssign(Make.Name('listExpressions', Make.Store()), annotation=Make.Subscript(Make.Name('list'), slice=Make.Attribute(Make.Name('ast'), 'expr'))
						, value=Make.Call(Make.Name('list'), listParameters=[Make.Name('expressions')]))
		, Make.If(Make.UnaryOp(Make.Not(), Make.Name('listExpressions'))
			, body=[Make.Expr(Make.Call(Make.Attribute(Make.Name('listExpressions'), 'append')
								, listParameters=[Make.Call(Make.Attribute(Make.Name('Make'), 'Constant')
										, listParameters=[Make.Constant('')], list_keyword=[keywordKeywordArguments4Call])]))])
		, Make.AnnAssign(Make.Name('expressionsJoined', Make.Store()), annotation=Make.Attribute(Make.Name('ast'), 'expr'), value=Make.Subscript(Make.Name('listExpressions'), slice=Make.Constant(0)))
		, Make.For(Make.Name('expression', Make.Store()), iter=Make.Subscript(Make.Name('listExpressions'), slice=Make.Slice(lower=Make.Constant(1)))
			, body=[Make.Assign([Make.Name('expressionsJoined', Make.Store())]
						, value=Make.Call(Make.Attribute(Make.Name('ast'), 'BinOp')
								, list_keyword=[Make.keyword('left', Make.Name('expressionsJoined'))
											, Make.keyword('op', Make.Call(Make.Name('ast_operator')))
											, Make.keyword('right', Make.Name('expression'))
											, keywordKeywordArguments4Call]))])
		, Make.Return(Make.Name('expressionsJoined'))]
	, decorator_list=[astName_staticmethod]
	, returns=Make.Attribute(Make.Name('ast'), 'expr'))

ClassDefIdentifier: str = 'Attribute' # `ClassDefIdentifier` and not `FunctionDefIdentifier` to be consistent with `makeToolMake` in "factory.py".
FunctionDefMake_Attribute: ast.stmt = Make.FunctionDef(ClassDefIdentifier
	, Make.arguments(list_arg=[Make.arg('value', annotation=Make.Attribute(Make.Name('ast'), 'expr'))]
		, vararg=Make.arg('attribute', annotation=Make.Name('str'))
		, kwonlyargs=[Make.arg('context', annotation=Make.BitOr.join([Make.Attribute(Make.Name('ast'), 'expr_context'), Make.Constant(None)]))]
		, kw_defaults=[Make.Constant(None)]
		, kwarg=Make.arg(settingsManufacturing.keywordArgumentsIdentifier, annotation=Make.Subscript(Make.Name('Unpack'), slice=Make.Name('ast_attributes'))))
	, body=[docstrings[settingsManufacturing.identifiers['Make']][ClassDefIdentifier]
		, Make.Assign([Make.Name('ctx', Make.Store())], value=Make.Or.join([Make.Name('context'), Make.Call(Make.Attribute(Make.Name('ast'), 'Load'))]))
		, Make.FunctionDef('addDOTattribute'
			, Make.arguments(list_arg=[Make.arg('chain', annotation=Make.Attribute(Make.Name('ast'), 'expr'))
					, Make.arg('identifier', annotation=Make.Name('str'))
					, Make.arg('ctx', annotation=Make.Attribute(Make.Name('ast'), 'expr_context'))]
				, kwarg=Make.arg(settingsManufacturing.keywordArgumentsIdentifier, annotation=Make.Subscript(Make.Name('Unpack'), slice=Make.Name('ast_attributes'))))
			, body=[Make.Return(Make.Call(Make.Attribute(Make.Name('ast'), ClassDefIdentifier)
					, list_keyword=[Make.keyword('value', Make.Name('chain')), Make.keyword('attr', Make.Name('identifier'))
						, Make.keyword('ctx', Make.Name('ctx')), keywordKeywordArguments4Call]))]
			, returns=Make.Attribute(Make.Name('ast'), ClassDefIdentifier))
		, Make.Assign([Make.Name('buffaloBuffalo', Make.Store())], value=Make.Call(Make.Name('addDOTattribute')
					, listParameters=[Make.Name('value'), Make.Subscript(Make.Name('attribute'), slice=Make.Constant(0)), Make.Name('ctx')]
					, list_keyword=[keywordKeywordArguments4Call]))
		, Make.For(Make.Name('identifier', Make.Store()), iter=Make.Subscript(Make.Name('attribute'), slice=Make.Slice(lower=Make.Constant(1), upper=Make.Constant(None)))
			, body=[Make.Assign([Make.Name('buffaloBuffalo', Make.Store())], value=Make.Call(Make.Name('addDOTattribute')
					, listParameters=[Make.Name('buffaloBuffalo'), Make.Name('identifier'), Make.Name('ctx')]
					, list_keyword=[keywordKeywordArguments4Call]))])
		, Make.Return(Make.Name('buffaloBuffalo'))]
	, decorator_list=[astName_staticmethod]
	, returns=Make.Attribute(Make.Name('ast'), ClassDefIdentifier))
del ClassDefIdentifier

ClassDefIdentifier: str = 'Import' # `ClassDefIdentifier` and not `FunctionDefIdentifier` to be consistent with `makeToolMake` in "factory.py".
list_argMake_Import: list[ast.arg]=[Make.arg('dotModule', annotation=Make.Name('identifierDotAttribute'))
		, Make.arg('asName', annotation=Make.BitOr().join([Make.Name('str'), Make.Constant(None)]))]
FunctionDef_bodyMake_Import: list[ast.stmt] = [docstrings[settingsManufacturing.identifiers['Make']][ClassDefIdentifier]
	, Make.Return(Make.Call(Make.Attribute(Make.Name('ast'), ClassDefIdentifier)
		, list_keyword=[Make.keyword('names', Make.List([Make.Call(Make.Attribute(Make.Name('Make'), 'alias')
			, listParameters=[Make.Name('dotModule'), Make.Name('asName')])])), keywordKeywordArguments4Call]))]
del ClassDefIdentifier

ClassDefIdentifier: str = 'keyword' # `ClassDefIdentifier` and not `FunctionDefIdentifier` to be consistent with `makeToolMake` in "factory.py".
listOverloads_keyword: list[ast.stmt] = [
	Make.FunctionDef(ClassDefIdentifier
		, Make.arguments(list_arg=[Make.arg('Buffalo_buffalo_Buffalo_buffalo_buffalo_buffalo_Buffalo_buffalo'
					, annotation=Make.BitOr.join([Make.Name('str'), Make.Constant(None)]))
				, Make.arg('value', annotation=Make.Attribute(Make.Name('ast'), 'expr'))]
			, kwarg=Make.arg(settingsManufacturing.keywordArgumentsIdentifier, annotation=astSubscriptUnpack_ast_attributes))
		, body=[Make.Expr(value=Make.Constant(...))]
		, decorator_list=[astName_staticmethod, astName_overload]
		, returns=Make.Attribute(Make.Name('ast'), ClassDefIdentifier))
	, Make.FunctionDef(ClassDefIdentifier
		, Make.arguments(list_arg=[Make.arg('Buffalo_buffalo_Buffalo_buffalo_buffalo_buffalo_Buffalo_buffalo'
				, annotation=Make.BitOr.join([Make.Name('str'), Make.Constant(None)]))]
			, kwonlyargs=[Make.arg('value', annotation=Make.Attribute(Make.Name('ast'), 'expr'))]
			, kw_defaults=[None]
			, kwarg=Make.arg(settingsManufacturing.keywordArgumentsIdentifier, annotation=Make.Subscript(Make.Name('Unpack'), slice=Make.Name('ast_attributes')))
			, defaults=[Make.Constant(None)])
		, body=[Make.Expr(value=Make.Constant(...))]
		, decorator_list=[astName_staticmethod, astName_overload]
		, returns=Make.Attribute(Make.Name('ast'), ClassDefIdentifier))]
del ClassDefIdentifier

# `theSSOT` =====================================================================
astModule_theSSOT = Make.Module([
    Make.ImportFrom('hunterMakesPy', list_alias=[Make.alias('PackageSettings')])
	, Make.Assign([Make.Name('identifierPackage', Make.Store())], value=Make.Constant('astToolkit'))
	, Make.Assign([Make.Name('packageSettings', Make.Store())]
		, value=Make.Call(Make.Name('PackageSettings')
			, list_keyword=[ast.keyword('identifierPackageFALLBACK', Make.Name('identifierPackage'))]))])

# `TypeAlias` =====================================================================
listHandmade_astTypes: list[ast.stmt] = [
    # If I were to automate the creation of ConstantValueType from ast.pyi `_ConstantValue`, their definition doesn't include `bytes` or `range`.
    # And, I would change the identifier to `ast_ConstantValue`.
	Make.TypeAlias(Make.Name('ConstantValueType', Make.Store()), type_params=[]
		, value=Make.BitOr().join(Make.Name(identifier)
			for identifier in ['bool', 'bytes', 'complex', 'EllipsisType', 'float', 'int', 'None', 'range', 'str']))
	, Make.TypeAlias(Make.Name('astASTattributes', Make.Store()), type_params=[]
		, value=Make.BitOr().join([astASTastAttribute, Make.Name('ConstantValueType'), Make.Subscript(Make.Name('list'), astASTastAttribute), Make.Subscript(Make.Name('list'), Make.BitOr.join([astASTastAttribute, Make.Constant(None)])), Make.Subscript(Make.Name('list'), Make.Name('str'))]))
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
