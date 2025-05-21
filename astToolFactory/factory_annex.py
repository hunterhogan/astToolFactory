from astToolFactory.docstrings import (
    FunctionDefDocstring_join, FunctionDefMake_AttributeDocstring,
)
from astToolkit import Be, BitOr, Grab, Make, NodeChanger, Then
from copy import deepcopy

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
list_keyword=[Make.keyword('default', BitOr.join([Make.Name('int'), Make.Constant(None)]))]
astAssign_EndPositionT = Make.Assign([Make.Name('_EndPositionT', ast.Store())], value=Make.Call(Make.Name('typing_TypeVar'), [Make.Constant('_EndPositionT'), Make.Name('int'), BitOr.join([Make.Name('int'), Make.Constant(None)])], list_keyword), lineno=1)
orElse = deepcopy(astAssign_EndPositionT)
NodeChanger(Be.Call, Grab.keywordsAttribute(Then.replaceWith([]))).visit(orElse)
astIf_EndPositionT = Make.If(Make.Compare(Make.Attribute(Make.Name('sys'), 'version_info'), [ast.GtE()], [Make.Tuple([Make.Constant(3), Make.Constant(13)])])
							, body=[astAssign_EndPositionT]
							, orElse=[orElse])

astClassDefTypedDict_Attributes = Make.ClassDef('_Attributes'
	, bases=[Make.Name('TypedDict'), Make.Subscript(Make.Name('Generic'), slice=Make.Name('_EndPositionT'))]
    , list_keyword=[Make.keyword('total', Make.Constant(False))]
    , body=[Make.AnnAssign(Make.Name('lineno', ast.Store()), annotation=Make.Name('int'))
            , Make.AnnAssign(Make.Name('col_offset', ast.Store()), annotation=Make.Name('int'))
            , Make.AnnAssign(Make.Name('end_lineno', ast.Store()), annotation=Make.Name('_EndPositionT'))
            , Make.AnnAssign(Make.Name('end_col_offset', ast.Store()), annotation=Make.Name('_EndPositionT'))
		]
	)

FunctionDef_join = 	Make.FunctionDef('join'
		, Make.arguments(args=[Make.arg('cls'), Make.arg('expressions', annotation=Make.Subscript(Make.Name('Iterable'), slice=Make.Attribute(Make.Name('ast'), 'expr')))]
						, kwarg=Make.arg('keywordArguments', annotation=Make.Subscript(Make.Name('Unpack'), slice=Make.Name('_Attributes'))))
		, body=[FunctionDefDocstring_join
            , Make.Return(Make.Call(Make.Name('operatorJoinMethod'), args=[Make.Name('cls'), Make.Name('expressions')], list_keyword=[Make.keyword(None, value=Make.Name('keywordArguments'))]))]
		, decorator_list=[Make.Name('classmethod')]
		, returns=Make.Attribute(Make.Name('ast'), 'expr'))

FunctionDef_operatorJoinMethod = Make.FunctionDef('operatorJoinMethod'
	, Make.arguments(args=[Make.arg('ast_operator', annotation=Make.Subscript(Make.Name('type'), slice=Make.Attribute(Make.Name('ast'), 'operator')))
						, Make.arg('expressions', annotation=Make.Subscript(Make.Name('Iterable'), slice=Make.Attribute(Make.Name('ast'), 'expr')))]
					, kwarg=Make.arg('keywordArguments', annotation=Make.Subscript(Make.Name('Unpack'), slice=Make.Name('_Attributes'))))
	, body=[Make.AnnAssign(Make.Name('listExpressions', ast.Store()), annotation=Make.Subscript(Make.Name('list'), slice=Make.Attribute(Make.Name('ast'), 'expr'))
						, value=Make.Call(Make.Name('list'), args=[Make.Name('expressions')]))
		, Make.If(Make.UnaryOp(ast.Not(), Make.Name('listExpressions'))
			, body=[Make.Expr(Make.Call(Make.Attribute(Make.Name('listExpressions'), 'append')
								, args=[Make.Call(Make.Attribute(Make.Name('Make'), 'Constant')
										, args=[Make.Constant(value='')], list_keyword=[Make.keyword(None, value=Make.Name('keywordArguments'))])]))])
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
FunctionDefMake_Attribute: ast.FunctionDef = ast.FunctionDef('Attribute'
	, args=ast.arguments(args=[ast.arg('value', annotation=ast.Attribute(ast.Name('ast'), 'expr'))]
						, vararg=ast.arg('attribute', annotation=ast.Name('str'))
						, kwonlyargs=[ast.arg('context', annotation=ast.Attribute(ast.Name('ast'), 'expr_context'))]
						, kw_defaults=[ast.Call(ast.Attribute(ast.Name('ast'), 'Load'))]
						, kwarg=ast.arg('keywordArguments', annotation=ast.Name('int')))
	, body=[FunctionDefMake_AttributeDocstring
		, ast.FunctionDef('addDOTattribute'
			, args=ast.arguments(args=[ast.arg('chain', annotation=ast.Attribute(ast.Name('ast'), 'expr'))
										, ast.arg('identifier', annotation=ast.Name('str'))
										, ast.arg('context', annotation=ast.Attribute(ast.Name('ast'), 'expr_context'))]
								, kwarg=ast.arg('keywordArguments', annotation=ast.Name('int')))
			, body=[ast.Return(ast.Call(ast.Attribute(ast.Name('ast'), 'Attribute')
										, keywords=[ast.keyword('value', ast.Name('chain')), ast.keyword('attr', ast.Name('identifier'))
													, ast.keyword('ctx', ast.Name('context')), ast.keyword(value=ast.Name('keywordArguments'))]))]
			, returns=ast.Attribute(ast.Name('ast'), 'Attribute'))
		, ast.Assign([ast.Name('buffaloBuffalo', ast.Store())], value=ast.Call(ast.Name('addDOTattribute')
																				, args=[ast.Name('value'), ast.Subscript(ast.Name('attribute'), slice=ast.Constant(0)), ast.Name('context')]
																				, keywords=[ast.keyword(value=ast.Name('keywordArguments'))]))
		, ast.For(target=ast.Name('identifier', ast.Store()), iter=ast.Subscript(ast.Name('attribute'), slice=ast.Slice(lower=ast.Constant(1), upper=ast.Constant(None)))
			, body=[ast.Assign([ast.Name('buffaloBuffalo', ast.Store())], value=ast.Call(ast.Name('addDOTattribute')
																				, args=[ast.Name('buffaloBuffalo'), ast.Name('identifier'), ast.Name('context')]
																				, keywords=[ast.keyword(value=ast.Name('keywordArguments'))]))])
		, ast.Return(ast.Name('buffaloBuffalo'))]
	, decorator_list=[ast.Name('staticmethod')]
	, returns=ast.Attribute(ast.Name('ast'), 'Attribute'))

FunctionDefMake_Import: ast.FunctionDef = ast.FunctionDef('Import'
	, args=ast.arguments(args=[ast.arg('moduleWithLogicalPath', annotation=ast.Name('str_nameDOTname'))
							, ast.arg('asName', annotation=ast.BinOp(left=ast.Name('str'), op=ast.BitOr(), right=ast.Constant(None)))]
					, kwarg=ast.arg('keywordArguments', annotation=ast.Name('int'))
					, defaults=[ast.Constant(None)])
	, body=[ast.Return(ast.Call(ast.Attribute(ast.Name('ast'), 'Import')
							, keywords=[ast.keyword('names', ast.List([ast.Call(ast.Attribute(ast.Name('Make'), 'alias'), args=[ast.Name('moduleWithLogicalPath'), ast.Name('asName')])]))
										, ast.keyword(value=ast.Name('keywordArguments'))]))]
	, decorator_list=[ast.Name('staticmethod')]
	, returns=ast.Attribute(ast.Name('ast'), 'Import'))

# `TypeAlias` =====================================================================
listHandmade_astTypes: list[ast.stmt] = [
	Make.AnnAssign(ast.Name('intORstr', ast.Store()), annotation=ast.Name('typing_TypeAlias'), value=ast.Name('Any')),
	Make.AnnAssign(ast.Name('intORstrORtype_params', ast.Store()), annotation=ast.Name('typing_TypeAlias'), value=ast.Name('Any')),
	Make.AnnAssign(ast.Name('intORtype_params', ast.Store()), annotation=ast.Name('typing_TypeAlias'), value=ast.Name('Any')),
	ast.Assign([ast.Name('木', ast.Store())], value=ast.Call(ast.Name('typing_TypeVar'), args=[ast.Constant('木')], keywords=[ast.keyword('bound', value=ast.Attribute(ast.Name('ast'), attr='AST')), ast.keyword('covariant', value=ast.Constant(True))])),
	ast.Assign([ast.Name('个', ast.Store())], value=ast.Call(ast.Name('typing_TypeVar'), args=[ast.Constant('个')], keywords=[ast.keyword('covariant', value=ast.Constant(True))])),
	ast.Assign([ast.Name('个return', ast.Store())], value=ast.Call(ast.Name('typing_TypeVar'), args=[ast.Constant('个return')], keywords=[ast.keyword('covariant', value=ast.Constant(True))])),
]
