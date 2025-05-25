"""Large blocks of 'pre-fabricated' static code added to manufactured AST tools."""
from astToolFactory.docstrings import FunctionDefDocstring_join, FunctionDefMake_AttributeDocstring
from astToolkit import BitOr, Make
import ast

# `Grab` =====================================================================
FunctionDefGrab_andDoAllOf = Make.FunctionDef('andDoAllOf'
	, Make.arguments(args=[Make.arg('listOfActions', Make.Subscript(Make.Name('list'), Make.Subscript(Make.Name('Callable'), Make.Tuple([Make.List([Make.Name('个')]), Make.Name('个')]))))])
	, body=[Make.FunctionDef('workhorse'
			, Make.arguments(args=[Make.arg('node', Make.Name('个'))])
			, body=[Make.For(Make.Name('action', ast.Store()), iter=Make.Name('listOfActions')
					, body=[Make.Assign([Make.Name('node', ast.Store())], value=Make.Call(Make.Name('action'), args=[Make.Name('node')]))]), Make.Return(Make.Name('node'))]
			, returns=Make.Name('个')), Make.Return(Make.Name('workhorse'))]
	, decorator_list=[Make.Name('staticmethod')]
	, returns=Make.Subscript(Make.Name('Callable'), Make.Tuple([Make.List([Make.Name('个')]), Make.Name('个')])))

# `.join` classmethod =====================================================================
FunctionDef_join = 	Make.FunctionDef('join'
		, Make.arguments(args=[Make.arg('cls'), Make.arg('expressions', annotation=Make.Subscript(Make.Name('Iterable'), slice=Make.Attribute(Make.Name('ast'), 'expr')))]
						, kwarg=Make.arg('keywordArguments', annotation=Make.Subscript(Make.Name('Unpack'), slice=Make.Name('ast_attributes'))))
		, body=[FunctionDefDocstring_join
			, Make.Return(Make.Call(Make.Name('operatorJoinMethod'), args=[Make.Name('cls'), Make.Name('expressions')], list_keyword=[Make.keyword(None, value=Make.Name('keywordArguments'))]))]
		, decorator_list=[Make.Name('classmethod')]
		, returns=Make.Attribute(Make.Name('ast'), 'expr'))

FunctionDef_operatorJoinMethod = Make.FunctionDef('operatorJoinMethod'
	, Make.arguments(args=[Make.arg('ast_operator', annotation=Make.Subscript(Make.Name('type'), slice=Make.Attribute(Make.Name('ast'), 'operator')))
						, Make.arg('expressions', annotation=Make.Subscript(Make.Name('Iterable'), slice=Make.Attribute(Make.Name('ast'), 'expr')))]
					, kwarg=Make.arg('keywordArguments', annotation=Make.Subscript(Make.Name('Unpack'), slice=Make.Name('ast_attributes'))))
	, body=[Make.AnnAssign(Make.Name('listExpressions', ast.Store()), annotation=Make.Subscript(Make.Name('list'), slice=Make.Attribute(Make.Name('ast'), 'expr'))
						, value=Make.Call(Make.Name('list'), args=[Make.Name('expressions')]))
		, Make.If(Make.UnaryOp(ast.Not(), Make.Name('listExpressions'))
			, body=[Make.Expr(Make.Call(Make.Attribute(Make.Name('listExpressions'), 'append')
								, args=[Make.Call(Make.Attribute(Make.Name('Make'), 'Constant')
										, args=[Make.Constant('')], list_keyword=[Make.keyword(None, value=Make.Name('keywordArguments'))])]))])
		, Make.AnnAssign(Make.Name('expressionsJoined', ast.Store()), annotation=Make.Attribute(Make.Name('ast'), 'expr'), value=Make.Subscript(Make.Name('listExpressions'), slice=Make.Constant(0)))
		, Make.For(Make.Name('expression', ast.Store()), iter=Make.Subscript(Make.Name('listExpressions'), slice=Make.Slice(lower=Make.Constant(1)))
			, body=[Make.Assign([Make.Name('expressionsJoined', ast.Store())]
						, value=Make.Call(Make.Attribute(Make.Name('ast'), 'BinOp')
								, list_keyword=[Make.keyword('left', Make.Name('expressionsJoined'))
											, Make.keyword('op', Make.Call(Make.Name('ast_operator')))
											, Make.keyword('right', Make.Name('expression'))
											, Make.keyword(None, value=Make.Name('keywordArguments'))]))])
		, Make.Return(Make.Name('expressionsJoined'))]
	, returns=Make.Attribute(Make.Name('ast'), 'expr'))

# `Make` =====================================================================
FunctionDefMake_Attribute: ast.FunctionDef = Make.FunctionDef('Attribute'
	, args=Make.arguments(args=[Make.arg('value', annotation=Make.Attribute(Make.Name('ast'), 'expr'))]
						, vararg=Make.arg('attribute', annotation=Make.Name('str'))
						, kwonlyargs=[Make.arg('context', annotation=Make.Attribute(Make.Name('ast'), 'expr_context'))]
						, kw_defaults=[Make.Call(Make.Attribute(Make.Name('ast'), 'Load'))]
						, kwarg=Make.arg('keywordArguments', annotation=Make.Name('int')))
	, body=[FunctionDefMake_AttributeDocstring
		, Make.FunctionDef('addDOTattribute'
			, args=Make.arguments(args=[Make.arg('chain', annotation=Make.Attribute(Make.Name('ast'), 'expr'))
										, Make.arg('identifier', annotation=Make.Name('str'))
										, Make.arg('context', annotation=Make.Attribute(Make.Name('ast'), 'expr_context'))]
								, kwarg=Make.arg('keywordArguments', annotation=Make.Name('int')))
			, body=[Make.Return(Make.Call(Make.Attribute(Make.Name('ast'), 'Attribute')
										, list_keyword=[Make.keyword('value', Make.Name('chain')), Make.keyword('attr', Make.Name('identifier'))
													, Make.keyword('ctx', Make.Name('context')), Make.keyword(None, value=Make.Name('keywordArguments'))]))]
			, returns=Make.Attribute(Make.Name('ast'), 'Attribute'))
		, Make.Assign([Make.Name('buffaloBuffalo', ast.Store())], value=Make.Call(Make.Name('addDOTattribute')
																				, args=[Make.Name('value'), Make.Subscript(Make.Name('attribute'), slice=Make.Constant(0)), Make.Name('context')]
																				, list_keyword=[Make.keyword(None, value=Make.Name('keywordArguments'))]))
		, Make.For(Make.Name('identifier', ast.Store()), iter=Make.Subscript(Make.Name('attribute'), slice=Make.Slice(lower=Make.Constant(1), upper=Make.Constant(None)))
			, body=[Make.Assign([Make.Name('buffaloBuffalo', ast.Store())], value=Make.Call(Make.Name('addDOTattribute')
																				, args=[Make.Name('buffaloBuffalo'), Make.Name('identifier'), Make.Name('context')]
																				, list_keyword=[Make.keyword(None, value=Make.Name('keywordArguments'))]))])
		, Make.Return(Make.Name('buffaloBuffalo'))]
	, decorator_list=[Make.Name('staticmethod')]
	, returns=Make.Attribute(Make.Name('ast'), 'Attribute'))

FunctionDefMake_Import: ast.FunctionDef = Make.FunctionDef('Import'
	, args=Make.arguments(args=[Make.arg('moduleWithLogicalPath', annotation=Make.Name('str_nameDOTname'))
							, Make.arg('asName', annotation=BitOr().join([Make.Name('str'), Make.Constant(None)]))]
					, kwarg=Make.arg('keywordArguments', annotation=Make.Name('int'))
					, defaults=[Make.Constant(None)])
	, body=[Make.Return(Make.Call(Make.Attribute(Make.Name('ast'), 'Import')
							, list_keyword=[Make.keyword('names', Make.List([Make.Call(Make.Attribute(Make.Name('Make'), 'alias'), args=[Make.Name('moduleWithLogicalPath'), Make.Name('asName')])]))
										, Make.keyword(None, value=Make.Name('keywordArguments'))]))]
	, decorator_list=[Make.Name('staticmethod')]
	, returns=Make.Attribute(Make.Name('ast'), 'Import'))

# `TypeAlias` =====================================================================
listHandmade_astTypes: list[ast.stmt] = [
	Make.AnnAssign(Make.Name('intORstr', ast.Store()), annotation=Make.Name('typing_TypeAlias'), value=Make.Name('Any')),
	Make.AnnAssign(Make.Name('intORstrORtype_params', ast.Store()), annotation=Make.Name('typing_TypeAlias'), value=Make.Name('Any')),
	Make.AnnAssign(Make.Name('intORtype_params', ast.Store()), annotation=Make.Name('typing_TypeAlias'), value=Make.Name('Any')),
	Make.AnnAssign(Make.Name('_Scalar', ast.Store())
				, annotation=Make.Name('typing_TypeAlias')
				, value=BitOr().join(Make.Name(identifier) 
									for identifier in ['bool', 'bytes', 'complex', 'EllipsisType', 'float'
													, 'int', 'None', 'NotImplementedType', 'range', 'str'
													]
								)
	),
	Make.AnnAssign(Make.Name('ScalarOrContainerOfScalar', ast.Store()), annotation=Make.Name('typing_TypeAlias')
					, value=BitOr().join([Make.Name('_Scalar')
										, Make.Subscript(Make.Name('frozenset'), Make.Constant('ScalarOrContainerOfScalar'))
										, Make.Subscript(Make.Name('tuple'), Make.Tuple([Make.Constant('ScalarOrContainerOfScalar'), Make.Constant(...)]))
									]
								)
	),
	Make.Assign([Make.Name('木', ast.Store())], value=Make.Call(Make.Name('typing_TypeVar'), args=[Make.Constant('木')], list_keyword=[Make.keyword('bound', value=Make.Attribute(Make.Name('ast'), 'AST')), Make.keyword('covariant', value=Make.Constant(True))])),
	Make.Assign([Make.Name('个', ast.Store())], value=Make.Call(Make.Name('typing_TypeVar'), args=[Make.Constant('个')], list_keyword=[Make.keyword('covariant', value=Make.Constant(True))])),
	Make.Assign([Make.Name('个return', ast.Store())], value=Make.Call(Make.Name('typing_TypeVar'), args=[Make.Constant('个return')], list_keyword=[Make.keyword('covariant', value=Make.Constant(True))])),
	Make.ClassDef('_attributes', bases=[Make.Name('TypedDict')], list_keyword=[Make.keyword('total', value=Make.Constant(False))]
		, body=[Make.AnnAssign(Make.Name('lineno', ast.Store()), annotation=Make.Name('int'))
			, Make.AnnAssign(Make.Name('col_offset', ast.Store()), annotation=Make.Name('int'))
		]
	),
	Make.ClassDef('ast_attributes', bases=[Make.Name('_attributes')], list_keyword=[Make.keyword('total', value=Make.Constant(False))]
		, body=[Make.AnnAssign(Make.Name('end_lineno', ast.Store()), annotation=BitOr().join([Make.Name('int'), Make.Constant(None)]))
			, Make.AnnAssign(Make.Name('end_col_offset', ast.Store()), annotation=BitOr().join([Make.Name('int'), Make.Constant(None)]))
		]
	),
	Make.ClassDef('ast_attributes_int', bases=[Make.Name('_attributes')], list_keyword=[Make.keyword('total', value=Make.Constant(False))]
		, body=[Make.AnnAssign(Make.Name('end_lineno', ast.Store()), annotation=Make.Name('int'))
			, Make.AnnAssign(Make.Name('end_col_offset', ast.Store()), annotation=Make.Name('int'))
		]
	),
	Make.ClassDef('ast_attributes_type_comment', bases=[Make.Name('ast_attributes')], list_keyword=[Make.keyword('total', value=Make.Constant(False))]
		, body=[Make.AnnAssign(Make.Name('type_comment', ast.Store()), annotation=BitOr().join([Make.Name('str'), Make.Constant(None)]))]
	),
]
