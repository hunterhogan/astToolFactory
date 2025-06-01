"""Large blocks of 'pre-fabricated' static code added to manufactured AST tools."""
from astToolFactory import astName_overload, astName_staticmethod
from astToolFactory.docstrings import (
	FunctionDefDocstring_join_boolop, FunctionDefDocstring_join_operator,
	FunctionDefMake_AttributeDocstring,
)
from astToolkit import Make
import ast

# `Grab` =====================================================================
FunctionDefGrab_andDoAllOf: ast.stmt = Make.FunctionDef('andDoAllOf'
	, Make.arguments(list_arg=[Make.arg('listOfActions', Make.Subscript(Make.Name('list'), Make.Subscript(Make.Name('Callable'), Make.Tuple([Make.List([Make.Name('个')]), Make.Name('个')]))))])
	, body=[Make.FunctionDef('workhorse'
			, Make.arguments(list_arg=[Make.arg('node', Make.Name('个'))])
			, body=[Make.For(Make.Name('action', ast.Store()), iter=Make.Name('listOfActions')
					, body=[Make.Assign([Make.Name('node', ast.Store())], value=Make.Call(Make.Name('action'), listParameters=[Make.Name('node')]))]), Make.Return(Make.Name('node'))]
			, returns=Make.Name('个')), Make.Return(Make.Name('workhorse'))]
	, decorator_list=[astName_staticmethod]
	, returns=Make.Subscript(Make.Name('Callable'), Make.Tuple([Make.List([Make.Name('个')]), Make.Name('个')])))

# `Make` =====================================================================
def makeFunctionDef_join(identifierContainer: str, identifierCallee: str, docstring: ast.Expr) -> ast.stmt:
	return Make.FunctionDef('join'
		, Make.arguments(list_arg=[Make.arg('cls'), Make.arg('expressions', annotation=Make.Subscript(Make.Name(identifierContainer), slice=Make.Attribute(Make.Name('ast'), 'expr')))]
						, kwarg=Make.arg('keywordArguments', annotation=Make.Subscript(Make.Name('Unpack'), slice=Make.Name('ast_attributes'))))
		, body=[docstring
			, Make.Return(Make.Call(callee=Make.Attribute(Make.Name('Make'), identifierCallee), listParameters=[Make.Name('cls'), Make.Name('expressions')], list_keyword=[Make.keyword(None, value=Make.Name('keywordArguments'))]))]
		, decorator_list=[Make.Name('classmethod')]
		, returns=Make.Attribute(Make.Name('ast'), 'expr'))

identifier_operatorJoinMethod: str = '_operatorJoinMethod'
identifier_boolopJoinMethod: str = '_boolopJoinMethod'

FunctionDef_boolopJoinMethod: ast.stmt = Make.FunctionDef(identifier_boolopJoinMethod
    , argumentSpecification=Make.arguments(list_arg=[Make.arg('ast_operator', annotation=Make.Subscript(Make.Name('type'), slice=Make.Attribute(Make.Name('ast'), 'boolop')))
            , Make.arg('expressions', annotation=Make.Subscript(Make.Name('Sequence'), slice=Make.Attribute(Make.Name('ast'), 'expr')))
            ]
        , kwarg=Make.arg('keywordArguments', annotation=Make.Subscript(Make.Name('Unpack'), slice=Make.Name('ast_attributes')))
    )
    , body=[Make.AnnAssign(Make.Name('listExpressions', ast.Store())
                        , annotation=Make.Subscript(Make.Name('list'), slice=Make.Attribute(Make.Name('ast'), 'expr'))
                        , value=Make.Call(Make.Name('list'), listParameters=[Make.Name('expressions')])
                    )
        , Make.Match(subject=Make.Call(Make.Name('len'), listParameters=[Make.Name('listExpressions')])
                    , cases=[Make.match_case(pattern=Make.MatchValue(Make.Constant(0))
                                , body=[Make.Assign([Make.Name('expressionsJoined', ast.Store())], value=Make.Call(Make.Attribute(Make.Name('Make'), 'Constant'), listParameters=[Make.Constant('')], list_keyword=[Make.keyword(None, value=Make.Name('keywordArguments'))]))])
                            , Make.match_case(pattern=Make.MatchValue(value=Make.Constant(1))
                                , body=[Make.Assign([Make.Name('expressionsJoined', ast.Store())], value=Make.Subscript(Make.Name('listExpressions'), slice=Make.Constant(0)))])
                            , Make.match_case(pattern=Make.MatchAs()
                                , body=[Make.Assign([Make.Name('expressionsJoined', ast.Store())]
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

FunctionDef_join_boolop: ast.stmt = makeFunctionDef_join('Sequence', identifier_boolopJoinMethod, FunctionDefDocstring_join_boolop)
FunctionDef_join_operator: ast.stmt = makeFunctionDef_join('Iterable', identifier_operatorJoinMethod, FunctionDefDocstring_join_operator)

FunctionDef_operatorJoinMethod: ast.stmt = Make.FunctionDef(identifier_operatorJoinMethod
	, Make.arguments(list_arg=[Make.arg('ast_operator', annotation=Make.Subscript(Make.Name('type'), slice=Make.Attribute(Make.Name('ast'), 'operator')))
						, Make.arg('expressions', annotation=Make.Subscript(Make.Name('Iterable'), slice=Make.Attribute(Make.Name('ast'), 'expr')))]
					, kwarg=Make.arg('keywordArguments', annotation=Make.Subscript(Make.Name('Unpack'), slice=Make.Name('ast_attributes'))))
	, body=[Make.AnnAssign(Make.Name('listExpressions', ast.Store()), annotation=Make.Subscript(Make.Name('list'), slice=Make.Attribute(Make.Name('ast'), 'expr'))
						, value=Make.Call(Make.Name('list'), listParameters=[Make.Name('expressions')]))
		, Make.If(Make.UnaryOp(ast.Not(), Make.Name('listExpressions'))
			, body=[Make.Expr(Make.Call(Make.Attribute(Make.Name('listExpressions'), 'append')
								, listParameters=[Make.Call(Make.Attribute(Make.Name('Make'), 'Constant')
										, listParameters=[Make.Constant('')], list_keyword=[Make.keyword(None, value=Make.Name('keywordArguments'))])]))])
		, Make.AnnAssign(Make.Name('expressionsJoined', ast.Store()), annotation=Make.Attribute(Make.Name('ast'), 'expr'), value=Make.Subscript(Make.Name('listExpressions'), slice=Make.Constant(0)))
		, Make.For(Make.Name('expression', ast.Store()), iter=Make.Subscript(Make.Name('listExpressions'), slice=Make.Slice(lower=Make.Constant(1)))
			, body=[Make.Assign([Make.Name('expressionsJoined', ast.Store())]
						, value=Make.Call(Make.Attribute(Make.Name('ast'), 'BinOp')
								, list_keyword=[Make.keyword('left', Make.Name('expressionsJoined'))
											, Make.keyword('op', Make.Call(Make.Name('ast_operator')))
											, Make.keyword('right', Make.Name('expression'))
											, Make.keyword(None, value=Make.Name('keywordArguments'))]))])
		, Make.Return(Make.Name('expressionsJoined'))]
	, decorator_list=[astName_staticmethod]
	, returns=Make.Attribute(Make.Name('ast'), 'expr'))

FunctionDefMake_Attribute: ast.stmt = Make.FunctionDef('Attribute'
	, argumentSpecification=Make.arguments(list_arg=[Make.arg('value', annotation=Make.Attribute(Make.Name('ast'), 'expr'))]
						, vararg=Make.arg('attribute', annotation=Make.Name('str'))
						, kwonlyargs=[Make.arg('context', annotation=Make.Attribute(Make.Name('ast'), 'expr_context'))]
						, kw_defaults=[Make.Call(Make.Attribute(Make.Name('ast'), 'Load'))]
						, kwarg=Make.arg('keywordArguments', annotation=Make.Subscript(Make.Name('Unpack'), slice=Make.Name('ast_attributes'))))
	, body=[FunctionDefMake_AttributeDocstring
		, Make.FunctionDef('addDOTattribute'
			, argumentSpecification=Make.arguments(list_arg=[Make.arg('chain', annotation=Make.Attribute(Make.Name('ast'), 'expr'))
										, Make.arg('identifier', annotation=Make.Name('str'))
										, Make.arg('context', annotation=Make.Attribute(Make.Name('ast'), 'expr_context'))]
								, kwarg=Make.arg('keywordArguments', annotation=Make.Subscript(Make.Name('Unpack'), slice=Make.Name('ast_attributes'))))
			, body=[Make.Return(Make.Call(Make.Attribute(Make.Name('ast'), 'Attribute')
										, list_keyword=[Make.keyword('value', Make.Name('chain')), Make.keyword('attr', Make.Name('identifier'))
													, Make.keyword('ctx', Make.Name('context')), Make.keyword(None, value=Make.Name('keywordArguments'))]))]
			, returns=Make.Attribute(Make.Name('ast'), 'Attribute'))
		, Make.Assign([Make.Name('buffaloBuffalo', ast.Store())], value=Make.Call(Make.Name('addDOTattribute')
																				, listParameters=[Make.Name('value'), Make.Subscript(Make.Name('attribute'), slice=Make.Constant(0)), Make.Name('context')]
																				, list_keyword=[Make.keyword(None, value=Make.Name('keywordArguments'))]))
		, Make.For(Make.Name('identifier', ast.Store()), iter=Make.Subscript(Make.Name('attribute'), slice=Make.Slice(lower=Make.Constant(1), upper=Make.Constant(None)))
			, body=[Make.Assign([Make.Name('buffaloBuffalo', ast.Store())], value=Make.Call(Make.Name('addDOTattribute')
																				, listParameters=[Make.Name('buffaloBuffalo'), Make.Name('identifier'), Make.Name('context')]
																				, list_keyword=[Make.keyword(None, value=Make.Name('keywordArguments'))]))])
		, Make.Return(Make.Name('buffaloBuffalo'))]
	, decorator_list=[astName_staticmethod]
	, returns=Make.Attribute(Make.Name('ast'), 'Attribute'))

# This relatively simple can probably be removed from the annex after I tweak a few things in the dataframe.
# Minimum changes in the dataframe data for this 'ClassDefIdentifier': 'attributeRename', override 'type'.
# Oh, wait. I don't plan to add anything that would _add_ `Make.arg('asName')` to 'match_args'.
FunctionDefMake_Import: ast.stmt = Make.FunctionDef('Import'
	, argumentSpecification=Make.arguments(list_arg=[Make.arg('dotModule', annotation=Make.Name('identifierDotAttribute'))
							, Make.arg('asName', annotation=Make.BitOr().join([Make.Name('str'), Make.Constant(None)]))]
					, kwarg=Make.arg('keywordArguments', annotation=Make.Subscript(Make.Name('Unpack'), slice=Make.Name('ast_attributes')))
					, defaults=[Make.Constant(None)])
	, body=[Make.Return(Make.Call(Make.Attribute(Make.Name('ast'), 'Import')
							, list_keyword=[Make.keyword('names', Make.List([Make.Call(Make.Attribute(Make.Name('Make'), 'alias'), listParameters=[Make.Name('dotModule'), Make.Name('asName')])]))
										, Make.keyword(None, value=Make.Name('keywordArguments'))]))]
	, decorator_list=[astName_staticmethod]
	, returns=Make.Attribute(Make.Name('ast'), 'Import'))

listOverloads_keyword: list[ast.stmt] = [
	Make.FunctionDef('keyword'
		, argumentSpecification=Make.arguments(list_arg=[Make.arg('Buffalo_buffalo_Buffalo_buffalo_buffalo_buffalo_Buffalo_buffalo', annotation=Make.BitOr.join([Make.Name('str'), Make.Constant(None)]))
							, Make.arg('value', annotation=Make.Attribute(Make.Name('ast'), 'expr'))
							]
						, kwarg=Make.arg('keywordArguments', annotation=Make.Subscript(Make.Name('Unpack'), slice=Make.Name('ast_attributes'))))
		, body=[Make.Expr(value=Make.Constant(...))]
		, decorator_list=[Make.Name('staticmethod'), Make.Name('overload')]
		, returns=Make.Attribute(Make.Name('ast'), 'keyword'))
	, Make.FunctionDef('keyword'
		, argumentSpecification=Make.arguments(list_arg=[Make.arg('Buffalo_buffalo_Buffalo_buffalo_buffalo_buffalo_Buffalo_buffalo', annotation=Make.BitOr.join([Make.Name('str'), Make.Constant(None)]))]
						, kwonlyargs=[Make.arg('value', annotation=Make.Attribute(Make.Name('ast'), 'expr'))]
						, kw_defaults=[None]
						, kwarg=Make.arg('keywordArguments', annotation=Make.Subscript(Make.Name('Unpack'), slice=Make.Name('ast_attributes')))
						, defaults=[Make.Constant(None)])
		, body=[Make.Expr(value=Make.Constant(...))]
		, decorator_list=[Make.Name('staticmethod'), Make.Name('overload')]
		, returns=Make.Attribute(Make.Name('ast'), 'keyword'))]

listOverloadsTypeAlias: list[ast.stmt] = [
	Make.FunctionDef('TypeAlias'
		, argumentSpecification=Make.arguments(list_arg=[Make.arg('name', annotation=Make.Attribute(Make.Name('ast'), 'Name'))
				, Make.arg('type_params', annotation=Make.Subscript(Make.Name('Sequence'), slice=Make.Attribute(Make.Name('ast'), 'type_param')))
			]
			, kwonlyargs=[Make.arg('value', annotation=Make.Attribute(Make.Name('ast'), 'expr'))]
			, kw_defaults=[None]
			, kwarg=Make.arg('keywordArguments', annotation=Make.Subscript(Make.Name('Unpack'), slice=Make.Name('ast_attributes')))
			, defaults=[Make.List()]
		)
		, body=[Make.Expr(Make.Constant(...))]
		, decorator_list=[astName_staticmethod, astName_overload]
		, returns=Make.Attribute(Make.Name('ast'), 'TypeAlias'))
	, Make.FunctionDef('TypeAlias'
		, argumentSpecification=Make.arguments(list_arg=[Make.arg('name', annotation=Make.Attribute(Make.Name('ast'), 'Name'))
				, Make.arg('type_params', annotation=Make.Subscript(Make.Name('Sequence'), slice=Make.Attribute(Make.Name('ast'), 'type_param')))
				, Make.arg('value', annotation=Make.Attribute(Make.Name('ast'), 'expr'))
			]
			, kwarg=Make.arg('keywordArguments', annotation=Make.Subscript(Make.Name('Unpack'), slice=Make.Name('ast_attributes'))))
		, body=[Make.Expr(Make.Constant(...))]
		, decorator_list=[astName_staticmethod, astName_overload]
		, returns=Make.Attribute(Make.Name('ast'), 'TypeAlias'))
]

# `theSSOT` =====================================================================
astModule_theSSOT = Make.Module([
    Make.ImportFrom('importlib', list_alias=[Make.alias('import_module', asName='importlib_import_module')])
	, Make.ImportFrom('inspect', list_alias=[Make.alias('getfile', asName='inspect_getfile')])
	, Make.ImportFrom('pathlib', list_alias=[Make.alias('Path')])
	, Make.ImportFrom('tomli', list_alias=[Make.alias('load', asName='tomli_load')])
	, Make.Import(dotModule='dataclasses')
	, Make.Assign([Make.Name('identifierPackage', Make.Store())], value=Make.Constant('astToolkit'))
	, Make.FunctionDef('getPathPackageINSTALLING'
		, argumentSpecification=Make.arguments()
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
    # _ConstantValue: typing_extensions.TypeAlias = str | bytes | bool | int | float | complex | None | EllipsisType
    # If I automate the creation of ConstantValueType from ast.pyi `_ConstantValue`, their definition doesn't include `bytes` or `range`.
    # And, I would change the identifier to `ast_ConstantValue`.
	Make.AnnAssign(Make.Name('ConstantValueType', ast.Store()), annotation=Make.Name('typing_TypeAlias')
		, value=Make.BitOr().join(Make.Name(identifier)
				for identifier in ['bool', 'bytes', 'complex', 'EllipsisType', 'float', 'int', 'None', 'range', 'str']
			)
	),
	Make.AnnAssign(Make.Name('identifierDotAttribute', ast.Store()), annotation=Make.Name('typing_TypeAlias'), value=Make.Name('str')),
	Make.Assign([Make.Name('木', ast.Store())], value=Make.Call(Make.Name('typing_TypeVar'), listParameters=[Make.Constant('木')], list_keyword=[Make.keyword('bound', value=Make.Attribute(Make.Name('ast'), 'AST')), Make.keyword('covariant', value=Make.Constant(True))])),
	Make.Assign([Make.Name('个', ast.Store())], value=Make.Call(Make.Name('typing_TypeVar'), listParameters=[Make.Constant('个')], list_keyword=[Make.keyword('covariant', value=Make.Constant(True))])),
	Make.Assign([Make.Name('个return', ast.Store())], value=Make.Call(Make.Name('typing_TypeVar'), listParameters=[Make.Constant('个return')], list_keyword=[Make.keyword('covariant', value=Make.Constant(True))])),
	# TODO, a non-trivial automatic transformation from ast.pyi `TypedDict._Attributes` and `TypeVar._EndPositionT` to the following:
	Make.ClassDef('_attributes', bases=[Make.Name('TypedDict')], list_keyword=[Make.keyword('total', value=Make.Constant(False))]
		, body=[Make.AnnAssign(Make.Name('lineno', ast.Store()), annotation=Make.Name('int'))
			, Make.AnnAssign(Make.Name('col_offset', ast.Store()), annotation=Make.Name('int'))
		]
	),
	Make.ClassDef('ast_attributes', bases=[Make.Name('_attributes')], list_keyword=[Make.keyword('total', value=Make.Constant(False))]
		, body=[Make.AnnAssign(Make.Name('end_lineno', ast.Store()), annotation=Make.BitOr().join([Make.Name('int'), Make.Constant(None)]))
			, Make.AnnAssign(Make.Name('end_col_offset', ast.Store()), annotation=Make.BitOr().join([Make.Name('int'), Make.Constant(None)]))
		]
	),
	Make.ClassDef('ast_attributes_int', bases=[Make.Name('_attributes')], list_keyword=[Make.keyword('total', value=Make.Constant(False))]
		, body=[Make.AnnAssign(Make.Name('end_lineno', ast.Store()), annotation=Make.Name('int'))
			, Make.AnnAssign(Make.Name('end_col_offset', ast.Store()), annotation=Make.Name('int'))
		]
	),
	Make.ClassDef('ast_attributes_type_comment', bases=[Make.Name('ast_attributes')], list_keyword=[Make.keyword('total', value=Make.Constant(False))]
		, body=[Make.AnnAssign(Make.Name('type_comment', ast.Store()), annotation=Make.BitOr().join([Make.Name('str'), Make.Constant(None)]))]
	),
]
