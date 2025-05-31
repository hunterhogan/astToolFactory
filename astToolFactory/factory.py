from astToolFactory import (
	astName_overload, astName_staticmethod, astName_typing_TypeAlias, DictionaryClassDef,
	DictionaryMatchArgs, getElementsBe, getElementsClassIsAndAttribute, getElementsDOT,
	getElementsGrab, getElementsMake, getElementsTypeAlias, keywordArgumentsIdentifier,
	listPylanceErrors, pythonMinimumVersionMinor, settingsPackageToManufacture,
	toolMakeFunctionDefReturnCall_keywords,
)
from astToolFactory.datacenter import DictionaryToolBe
from astToolFactory.docstrings import (
	ClassDefDocstring_ast_boolop, ClassDefDocstring_ast_operator, ClassDefDocstringBe,
	ClassDefDocstringClassIsAndAttribute, ClassDefDocstringDOT, ClassDefDocstringGrab,
	ClassDefDocstringMake, docstringWarning,
)
from astToolFactory.factory_annex import (
	FunctionDef_boolopJoinMethod, FunctionDef_join_boolop, FunctionDef_join_operator,
	FunctionDef_operatorJoinMethod, FunctionDefGrab_andDoAllOf, FunctionDefMake_Attribute,
	FunctionDefMake_Import, listHandmade_astTypes,
)
from astToolkit import (
	Add, astModuleToIngredientsFunction, BitOr, ClassIsAndAttribute, IfThis, IngredientsFunction,
	IngredientsModule, LedgerOfImports, Make, NodeChanger, NodeTourist, parseLogicalPath2astModule,
	Then,
)
from astToolkit.transformationTools import write_astModule
from collections.abc import Callable, Sequence
from pathlib import PurePosixPath
from typing import cast, TypeGuard
from Z0Z_tools import raiseIfNone, writeStringToHere
import ast
import autoflake

"""
class Name(expr):
...
	ctx: expr_context  # Not present in Python < 3.13 if not passed to `__init__`

TODO protect against AttributeError (I guess) in DOT, Grab, and ClassIsAndAttribute
	add docstrings to warn of problem, including in Make

"""
def writeModule(astModule: ast.Module, moduleIdentifier: str) -> None:
	ast.fix_missing_locations(astModule)
	pythonSource: str = ast.unparse(astModule)
	if 'ClassIsAndAttribute' in moduleIdentifier or 'DOT' in moduleIdentifier or 'Grab' in moduleIdentifier:
		pythonSource = "# ruff: noqa: F403, F405\n" + pythonSource
	if 'ClassIsAndAttribute' in moduleIdentifier:
		pythonSource = "# pyright: reportArgumentType=false\n" + pythonSource
	if 'DOT' in moduleIdentifier:
		pythonSource = "# pyright: reportReturnType=false\n" + pythonSource
	if 'Grab' in moduleIdentifier:
		listTypeIgnore: list[ast.TypeIgnore] = []
		tag = '[reportArgumentType, reportAttributeAccessIssue]'
		for attribute in listPylanceErrors:
			for splitlinesNumber, line in enumerate(pythonSource.splitlines()):
				if 'node.'+attribute in line:
					listTypeIgnore.append(ast.TypeIgnore(splitlinesNumber+1, tag))
					break
		astModule = ast.parse(pythonSource)
		astModule.type_ignores.extend(listTypeIgnore)
		pythonSource = ast.unparse(astModule)
		pythonSource = "# ruff: noqa: F403, F405\n" + pythonSource
		pythonSource = pythonSource.replace('# type: ignore[', '# pyright: ignore[')
	autoflake_additional_imports: list[str] = ['astToolkit']
	pythonSource = autoflake.fix_code(pythonSource, autoflake_additional_imports, expand_star_imports=False, remove_all_unused_imports=True, remove_duplicate_keys = False, remove_unused_variables = False)
	pathFilenameModule = PurePosixPath(settingsPackageToManufacture.pathPackage, moduleIdentifier + settingsPackageToManufacture.fileExtension)
	writeStringToHere(pythonSource, pathFilenameModule)

def writeClass(classIdentifier: str, list4ClassDefBody: list[ast.stmt], list4ModuleBody: list[ast.stmt], moduleIdentifierPrefix: str | None = '_tool') -> None:
	if moduleIdentifierPrefix:
		moduleIdentifier = moduleIdentifierPrefix + classIdentifier
	else:
		moduleIdentifier = classIdentifier
	return writeModule(Make.Module(
			body=[docstringWarning
				, *list4ModuleBody
				, Make.ClassDef(classIdentifier, body=list4ClassDefBody)
				]
			)
		, moduleIdentifier)

def make_astTypes() -> None:
	list4ModuleBody: list[ast.stmt] = []
	ledgerOfImports = LedgerOfImports(
		Make.Module([
			Make.ImportFrom('types', [Make.alias('EllipsisType'), Make.alias('NotImplementedType')])
			, Make.ImportFrom('typing', [Make.alias('Any'), Make.alias('TypeAlias', 'typing_TypeAlias'), Make.alias('TypedDict'), Make.alias('TypeVar', 'typing_TypeVar')])
			, Make.Import('ast')
			, Make.Import('sys')
		])
	)

	list_match_case: list[ast.match_case] = []
	for TypeAlias_hasDOTIdentifier, list4TypeAlias_value, useMatchCase, versionMinorMinimum in getElementsTypeAlias():
		astNameTypeAlias: ast.Name = Make.Name(TypeAlias_hasDOTIdentifier, ast.Store())
		TypeAlias_value: ast.expr = BitOr.join([eval(classAs_astAttribute) for classAs_astAttribute in list4TypeAlias_value])
		ast_stmt: ast.stmt = Make.AnnAssign(astNameTypeAlias, astName_typing_TypeAlias, value=TypeAlias_value)

		if useMatchCase:
			if versionMinorMinimum >= pythonMinimumVersionMinor:
				pattern: ast.MatchAs = Make.MatchAs(name = 'version')
				guard: ast.Compare | None = Make.Compare(Make.Name('version'), ops=[ast.GtE()], comparators=[Make.Tuple([Make.Constant(3), Make.Constant(int(versionMinorMinimum))])])
			else:
				pattern = Make.MatchAs()
				guard = None
			list_match_case.append(Make.match_case(pattern, guard, body = [ast_stmt]))

			if useMatchCase > 1:
				continue
			else:
				ast_stmt = Make.Match(Make.Attribute(Make.Name('sys'), 'version_info'), cases=list_match_case)
				list_match_case.clear()

		list4ModuleBody.append(ast_stmt)

	astModule: ast.Module = Make.Module(
		body=[
			docstringWarning
			, *ledgerOfImports.makeList_ast()
			, *listHandmade_astTypes
			, *list4ModuleBody
			]
		)

	writeModule(astModule, '_astTypes')

def makeJoinClassmethod() -> None:
	list_aliasIdentifier: list[str] = ['ast_attributes', 'Make']
	list4ModuleBody: list[ast.stmt] = [
		FunctionDef_boolopJoinMethod
		, FunctionDef_operatorJoinMethod
		]

	listBoolOpIdentifiers: list[str] = sorted([subclass.__name__ for subclass in ast.boolop.__subclasses__()])
	listOperatorIdentifiers: list[str] = sorted([subclass.__name__ for subclass in ast.operator.__subclasses__()])

	for identifier in listBoolOpIdentifiers:
		list4ModuleBody.append(Make.ClassDef(identifier
			, bases=[Make.Attribute(Make.Name('ast'), identifier)]
			, body=[ClassDefDocstring_ast_boolop, FunctionDef_join_boolop]
		))

	for identifier in listOperatorIdentifiers:
		list4ModuleBody.append(Make.ClassDef(identifier
			, bases=[Make.Attribute(Make.Name('ast'), identifier)]
			, body=[ClassDefDocstring_ast_operator, FunctionDef_join_operator]
		))

	astModule: ast.Module = Make.Module([docstringWarning
		, Make.ImportFrom('astToolkit', [Make.alias(identifier) for identifier in list_aliasIdentifier])
		, Make.ImportFrom('collections.abc', [Make.alias('Iterable'), Make.alias('Sequence')])
		, Make.ImportFrom('typing', [Make.alias('TypedDict'), Make.alias('Unpack')])
		, Make.Import('ast')
		, Make.Import('sys')
		, *list4ModuleBody
	])

	writeModule(astModule, '_joinClassmethod')

def makeTool_dump() -> None:
	ingredientsFunction: IngredientsFunction = astModuleToIngredientsFunction(parseLogicalPath2astModule('ast'), 'dump')
	astConstant: ast.Constant = Make.Constant('ast.')
	findThis = ClassIsAndAttribute.valueIs(ast.Attribute, IfThis.isAttributeNamespaceIdentifier('node', '__class__'))
	def doThatPrepend(node: ast.Attribute) -> ast.AST:
		return Add.join([astConstant, cast(ast.expr, node)])
	prepend_ast = NodeChanger(findThis, doThatPrepend)
	findThis = IfThis.isFunctionDefIdentifier('_format')
	def doThat(node: ast.FunctionDef) -> ast.AST:
		return prepend_ast.visit(node)
	NodeChanger(findThis, doThat).visit(ingredientsFunction.astFunctionDef)
	pathFilename = PurePosixPath(settingsPackageToManufacture.pathPackage, '_dumpFunctionDef' + settingsPackageToManufacture.fileExtension)
	write_astModule(IngredientsModule(ingredientsFunction), pathFilename, settingsPackageToManufacture.identifierPackage)

def makeToolBe() -> None:
	list4ClassDefBody: list[ast.stmt] = [ClassDefDocstringBe]

	listDictionaryToolElements: list[DictionaryToolBe] = getElementsBe()

	for dictionaryToolElements in listDictionaryToolElements:
		ClassDefIdentifier: str = dictionaryToolElements['ClassDefIdentifier']
		classAs_astAttribute: ast.expr = eval(dictionaryToolElements['classAs_astAttribute'])
		versionMinorMinimumClass: int = dictionaryToolElements['versionMinorMinimumClass']

		ast_stmt: ast.stmt = Make.FunctionDef(ClassDefIdentifier
			, args=Make.arguments(args=[Make.arg('node', annotation=Make.Name('ast.AST'))])
			, body=[Make.Return(Make.Call(Make.Name('isinstance'), args=[Make.Name('node'), classAs_astAttribute]))]
			, decorator_list=[astName_staticmethod]
			, returns=Make.Subscript(Make.Name('TypeGuard'), slice=classAs_astAttribute))

		if versionMinorMinimumClass > pythonMinimumVersionMinor:
			ast_stmt = Make.If(Make.Compare(Make.Attribute(Make.Name('sys'), 'version_info')
						, ops=[ast.GtE()]
						, comparators=[Make.Tuple([Make.Constant(3), Make.Constant(versionMinorMinimumClass)])])
					, body=[ast_stmt]
				)

		list4ClassDefBody.append(ast_stmt)

	list4ModuleBody: list[ast.stmt] = [
		Make.ImportFrom('typing', [Make.alias('TypeGuard')])
		, Make.Import('ast')
		, Make.Import('sys')
	]

	writeClass('Be', list4ClassDefBody, list4ModuleBody)

def makeToolClassIsAndAttribute() -> None:
	def create_ast_stmt(list_ast_expr: list[str], attributeIsNotNone: bool | str) -> ast.stmt:
		workhorseReturnValue: ast.BoolOp = Make.BoolOp(ast.And(), values=[Make.Call(Make.Name('isinstance'), args=[Make.Name('node'), Make.Name('astClass')])])
		if attributeIsNotNone:
			ops: list[ast.cmpop]= [ast.IsNot()]
			comparators: list[ast.expr]=[Make.Constant(None)]
			if attributeIsNotNone == 'Sequence':
				ops: list[ast.cmpop]= [ast.NotEq()]
				comparators: list[ast.expr]=[Make.List([Make.Constant(None)])]
			workhorseReturnValue.values.append(Make.Compare(Make.Attribute(Make.Name('node'), attribute), ops=ops, comparators=comparators))
		workhorseReturnValue.values.append(Make.Call(Make.Name('attributeCondition'), args=[Make.Attribute(Make.Name('node'), attribute)]))

		buffaloBuffalo_workhorse_returnsAnnotation: ast.expr = BitOr.join([Make.Subscript(Make.Name('TypeGuard'), slice=astNameTypeAlias), Make.Name('bool')])

		if overloadDefinition:
			decorator_list.append(astName_overload)
			body: list[ast.stmt] = [Make.Expr(Make.Constant(value=...))]
		else:
			body = [
				Make.FunctionDef('workhorse',
					args=Make.arguments(args=[Make.arg('node', annotation=Make.Attribute(Make.Name('ast'), 'AST'))])
					, body=[Make.Return(workhorseReturnValue)]
					, returns=buffaloBuffalo_workhorse_returnsAnnotation)
				, Make.Return(Make.Name('workhorse'))
			]

		returns: ast.expr = Make.Subscript(Make.Name('Callable'), slice=Make.Tuple([Make.List([Make.Attribute(Make.Name('ast'), 'AST')]), buffaloBuffalo_workhorse_returnsAnnotation]))

		annotation: ast.expr = (BitOr.join([Make.Subscript(Make.Name('Callable'), Make.Tuple([Make.List([eval(ast_expr)]), Make.Name('bool')]))
									for ast_expr in list_ast_expr]))

		return Make.FunctionDef(attribute + 'Is'
				, args=Make.arguments(args=[
					Make.arg('astClass', annotation=Make.Subscript(Make.Name('type'), astNameTypeAlias)),
					Make.arg('attributeCondition', annotation=annotation)
				])
				, body=body
				, decorator_list=decorator_list
				, returns=returns
			)

	list4ClassDefBody: list[ast.stmt] = [ClassDefDocstringClassIsAndAttribute]

	for versionMinorMinimumAttribute, attribute, TypeAlias_hasDOTIdentifier, overloadDefinition, list_ast_expr, attributeIsNotNone, orElseList_ast_expr, orElseAttributeIsNotNone in getElementsClassIsAndAttribute():
		astNameTypeAlias: ast.Name = Make.Name(TypeAlias_hasDOTIdentifier)
		decorator_list: list[ast.expr] = [astName_staticmethod]

		ast_stmt: ast.stmt = create_ast_stmt(list_ast_expr, attributeIsNotNone)

		if versionMinorMinimumAttribute > pythonMinimumVersionMinor:
			orElse: list[ast.stmt] = []
			if orElseList_ast_expr:
				orElse = [create_ast_stmt(orElseList_ast_expr, orElseAttributeIsNotNone)]
			ast_stmt = Make.If(Make.Compare(Make.Attribute(Make.Name('sys'), 'version_info'), ops=[ast.GtE()]
							, comparators=[Make.Tuple([Make.Constant(3), Make.Constant(versionMinorMinimumAttribute)])])
						, body=[ast_stmt]
						, orElse=orElse
						)

		list4ClassDefBody.append(ast_stmt)

	list4ModuleBody: list[ast.stmt] = [
		Make.ImportFrom('astToolkit._astTypes', [Make.alias('*')])
		, Make.ImportFrom('collections.abc', [Make.alias('Callable'), Make.alias('Sequence')])
		, Make.ImportFrom('typing', [Make.alias(identifier) for identifier in ['Any', 'Literal', 'overload', 'TypeGuard']])
		, Make.Import('ast')
		, Make.Import('sys')
	]

	writeClass('ClassIsAndAttribute', list4ClassDefBody, list4ModuleBody)

def makeToolDOT() -> None:
	def create_ast_stmt(list_ast_expr: list[str]) -> ast.stmt:
		decorator_list: list[ast.expr] = [astName_staticmethod]
		if isOverload:
			decorator_list.append(astName_overload)
			body: list[ast.stmt] = [Make.Expr(Make.Constant(value=...))]
		else:
			body = [Make.Return(Make.Attribute(Make.Name('node'), attribute))]

		returns: ast.expr = BitOr.join([eval(ast_expr) for ast_expr in list_ast_expr])

		return Make.FunctionDef(attribute
			, args=Make.arguments(args=[Make.arg('node', annotation=astNameTypeAlias)])
			, body=body
			, decorator_list=decorator_list
			, returns=returns
		)

	list4ClassDefBody: list[ast.stmt] = [ClassDefDocstringDOT]

	for versionMinorMinimumAttribute, attribute, TypeAlias_hasDOTIdentifier, isOverload, list_ast_expr, _attributeIsNotNone, orElseList_ast_expr, _orElseAttributeIsNotNone in getElementsDOT():
		astNameTypeAlias: ast.Name = Make.Name(TypeAlias_hasDOTIdentifier)

		ast_stmt: ast.stmt = create_ast_stmt(list_ast_expr)

		if versionMinorMinimumAttribute > pythonMinimumVersionMinor:
			orElse: list[ast.stmt] = []
			if orElseList_ast_expr:
				orElse = [create_ast_stmt(orElseList_ast_expr)]
			ast_stmt = Make.If(Make.Compare(Make.Attribute(Make.Name('sys'), 'version_info'), ops=[ast.GtE()]
							, comparators=[Make.Tuple([Make.Constant(3), Make.Constant(versionMinorMinimumAttribute)])])
						, body=[ast_stmt]
						, orElse=orElse
						)

		list4ClassDefBody.append(ast_stmt)

	list4ModuleBody: list[ast.stmt] = [
			Make.ImportFrom('astToolkit._astTypes', [Make.alias('*')])
			, Make.ImportFrom('collections.abc', [Make.alias('Sequence')])
			, Make.ImportFrom('typing', [Make.alias('Any'), Make.alias('Literal'), Make.alias('overload')])
			, Make.Import('ast')
			, Make.Import('sys')
			]

	writeClass('DOT', list4ClassDefBody, list4ModuleBody)

def makeToolGrab() -> None:
	def create_ast_stmt(list_ast_expr: list[str], attributeIsNotNone: bool) -> ast.stmt:
		list_ast_expr4annotation: list[ast.expr] = []
		for type_ast_exprAsStr in list_ast_expr:
			type_ast_expr = eval(type_ast_exprAsStr)
			list_ast_expr4annotation.append(Make.Subscript(Make.Name('Callable'), slice=Make.Tuple([Make.List([type_ast_expr]), type_ast_expr])))

		ast_expr4annotation = BitOr.join(list_ast_expr4annotation)

		return Make.FunctionDef(attribute + 'Attribute'
			, args=Make.arguments(args=[Make.arg('action', annotation=ast_expr4annotation)])
			, body=[Make.FunctionDef('workhorse'
						, args=Make.arguments(args=[Make.arg('node', annotation=hasDOTTypeAliasName_Load)])
						, body=[Make.Assign([Make.Attribute(Make.Name('node'), attribute, context=ast.Store())], value=Make.Call(Make.Name('action'), [Make.Attribute(Make.Name('node'), attribute)]))
								, Make.Return(Make.Name('node'))
						]
						, returns=hasDOTTypeAliasName_Load)
					, Make.Return(Make.Name('workhorse'))
				]
			, decorator_list=[astName_staticmethod]
			, returns=Make.Subscript(Make.Name('Callable'), Make.Tuple([Make.List([hasDOTTypeAliasName_Load]), hasDOTTypeAliasName_Load])))

	list4ClassDefBody: list[ast.stmt] = [ClassDefDocstringGrab, FunctionDefGrab_andDoAllOf]
	for versionMinorMinimumAttribute, attribute, TypeAlias_hasDOTIdentifier, list_ast_expr, attributeIsNotNone, orElseList_ast_expr, orElseAttributeIsNotNone in getElementsGrab():
		hasDOTTypeAliasName_Load: ast.Name = Make.Name(TypeAlias_hasDOTIdentifier)

		ast_stmt: ast.stmt = create_ast_stmt(list_ast_expr, attributeIsNotNone)

		if versionMinorMinimumAttribute > pythonMinimumVersionMinor:
			orElse: list[ast.stmt] = []
			if orElseList_ast_expr:
				orElse = [create_ast_stmt(orElseList_ast_expr, orElseAttributeIsNotNone)]
			ast_stmt = Make.If(Make.Compare(Make.Attribute(Make.Name('sys'), 'version_info'), ops=[ast.GtE()]
							, comparators=[Make.Tuple([Make.Constant(3), Make.Constant(versionMinorMinimumAttribute)])])
						, body=[ast_stmt]
						, orElse=orElse
						)

		list4ClassDefBody.append(ast_stmt)

	list4ModuleBody: list[ast.stmt] = [
			Make.ImportFrom('astToolkit', [Make.alias(identifier) for identifier in ['个']])
			, Make.ImportFrom('astToolkit._astTypes', [Make.alias('*')])
			, Make.ImportFrom('collections.abc', [Make.alias('Callable'), Make.alias('Sequence')])
			, Make.ImportFrom('typing', [Make.alias('Any'), Make.alias('Literal')])
			, Make.Import('ast')
			, Make.Import('sys')
			]

	writeClass('Grab', list4ClassDefBody, list4ModuleBody)

# TODO add docstrings for each staticmethod and each ClassDef: idea: `Make.GtE.__doc__ = ast.GtE.__doc__` <-- hahahahaaaaaaaaaa!
# But, maybe include the ast docstring to contrast the lack of documentation in ast.
# For real, `dictionaryDocstringMake`, keynames = `ClassDefIdentifier`, values = docstrings created in a dedicated module,
# currently `astToolFactory/docstrings.py`. I am sure there are many packages designed to help with this.

# TODO overload for Make.keyword:
"""
@staticmethod
@overload
def keyword(arg: str | None, value: ast.expr, **keywordArguments: int) -> ast.keyword:...
@staticmethod
@overload
def keyword(arg: str | None = None, *, value: ast.expr, **keywordArguments: int) -> ast.keyword:...
"""

# TODO overload for Make.TypeAlias:
"""
@staticmethod
@overload
def TypeAlias(name: ast.Name, type_params: Sequence[ast.type_param] = [], *, value: ast.expr, **keywordArguments: int) -> ast.TypeAlias:...
@staticmethod
@overload
def TypeAlias(name: ast.Name, type_params: Sequence[ast.type_param], value: ast.expr, **keywordArguments: int) -> ast.TypeAlias:...
"""

# TODO add `ClassDef` for ast subclasses that do not have __init__ parameters. At the very least, it prevents an error if the user uses `Make.GtE()` instead of `ast.GtE()`.
def makeToolMake() -> None:
	list_aliasIdentifier: list[str] = ['ConstantValueType']
	list4ClassDefBody: list[ast.stmt] = [ClassDefDocstringMake]
	setKeywordArgumentsAnnotationTypeAlias: set[str] = set()

	# list_match_case: list[ast.match_case] = []
	# # The order of the tuple elements is the order in which they are used in the flow of the code.
	# for ClassDefIdentifier, listStr4FunctionDef_args, kwarg_annotationIdentifier, listDefaults, classAs_astAttributeAsStr, overloadDefinition, listTupleCall_keywords, useMatchCase, versionMinorMinimum in getElementsMake():
	# 	# Bypass the manufacture of the tool by using a prefabricated tool from the annex.
	# 	if ClassDefIdentifier == 'Attribute':
	# 		ast_stmt = FunctionDefMake_Attribute
	# 		list4ClassDefBody.append(ast_stmt)
	# 		continue
	# 	elif ClassDefIdentifier == 'Import':
	# 		ast_stmt = FunctionDefMake_Import
	# 		list4ClassDefBody.append(ast_stmt)
	# 		list_aliasIdentifier.append('identifierDotAttribute')
	# 		continue
	# 	else:
	# 		listFunctionDef_args: list[ast.arg] = [cast(ast.arg, eval(ast_argAsStr)) for ast_argAsStr in listStr4FunctionDef_args]
	# 		kwarg: ast.arg | None = None
	# 		if kwarg_annotationIdentifier != 'No':
	# 			setKeywordArgumentsAnnotationTypeAlias.add(kwarg_annotationIdentifier)
	# 			kwarg = Make.arg(keywordArgumentsIdentifier, annotation=Make.Subscript(Make.Name('Unpack'), slice=Make.Name(kwarg_annotationIdentifier)))
	# 		defaults: list[ast.expr] = [cast(ast.expr, eval(defaultAsStr)) for defaultAsStr in listDefaults]
	# 		decorator_list: list[ast.expr] = [astName_staticmethod]
	# 		classAs_astAttribute: ast.expr = eval(classAs_astAttributeAsStr)

	# 		if overloadDefinition:
	# 			decorator_list.append(astName_overload)
	# 			body: list[ast.stmt] = [Make.Expr(Make.Constant(value=...))]
	# 		else:
	# 			listCall_keyword: list[ast.keyword] = []
	# 			for tupleCall_keywords in listTupleCall_keywords:
	# 				argIdentifier, keywordValue = tupleCall_keywords
	# 				# If there are not call keywords
	# 				if keywordValue == 'No':
	# 					break
	# 				listCall_keyword.append(Make.keyword(argIdentifier, value=eval(keywordValue)))
	# 			if kwarg is not None:
	# 				listCall_keyword.append(toolMakeFunctionDefReturnCall_keywords)
	# 			body = [Make.Return(Make.Call(classAs_astAttribute, list_keyword=listCall_keyword))]

	# 		ast_stmt = Make.FunctionDef(
	# 			ClassDefIdentifier
	# 			, args=Make.arguments(args=listFunctionDef_args, kwarg=kwarg, defaults=defaults)
	# 			, body=body
	# 			, decorator_list=decorator_list
	# 			, returns=classAs_astAttribute)


	# 	# If there are multiple versions, create a match-case for this version.
	# 	if useMatchCase:
	# 		# Create a guard or a catch-all match-case and append to list_match_case.
	# 		if versionMinorMinimum >= pythonMinimumVersionMinor:
	# 			pattern: ast.MatchAs = Make.MatchAs(name = 'version')
	# 			guard: ast.Compare | None = Make.Compare(Make.Name('version'), ops=[ast.GtE()], comparators=[Make.Tuple([Make.Constant(3), Make.Constant(int(versionMinorMinimum))])])
	# 		else:
	# 			pattern = Make.MatchAs()
	# 			guard = None
	# 		list_match_case.append(Make.match_case(pattern, guard, body = [ast_stmt]))

	# 		# If there are more match-case in the queue, then wait to create ast.Match.
	# 		if useMatchCase > 1:
	# 			continue
	# 		else:
	# 			ast_stmt = Make.Match(Make.Attribute(Make.Name('sys'), 'version_info'), cases=list_match_case)
	# 			list_match_case.clear()

	# 	list4ClassDefBody.append(ast_stmt)

	# OLD code
	def create_ast_stmt(dictionaryMethodElements: DictionaryMatchArgs) -> ast.FunctionDef:
		listFunctionDef_args: list[ast.arg] = [cast(ast.arg, eval(ast_argAsStr)) for ast_argAsStr in dictionaryMethodElements['listStr4FunctionDef_args']]
		kwarg: ast.arg | None = None
		if str(dictionaryMethodElements['kwarg_annotationIdentifier']) != 'No':
			setKeywordArgumentsAnnotationTypeAlias.add(dictionaryMethodElements['kwarg_annotationIdentifier'])
			kwarg = Make.arg(keywordArgumentsIdentifier, annotation=Make.Subscript(Make.Name('Unpack'), slice=Make.Name(dictionaryMethodElements['kwarg_annotationIdentifier'])))

		defaults: list[ast.expr] = [cast(ast.expr, eval(defaultAsStr)) for defaultAsStr in dictionaryMethodElements['listDefaults']]

		listCall_keyword: list[ast.keyword] = []
		for tupleCall_keywords in dictionaryMethodElements['listTupleCall_keywords']:
			argIdentifier, keywordValue = tupleCall_keywords
			# If there are not call keywords
			if keywordValue == 'No':
				break
			listCall_keyword.append(Make.keyword(argIdentifier, value=eval(keywordValue)))
		if kwarg is not None:
			listCall_keyword.append(toolMakeFunctionDefReturnCall_keywords)

		ast_stmt = Make.FunctionDef(ClassDefIdentifier
			, args=Make.arguments(args=listFunctionDef_args, kwarg=kwarg, defaults=defaults)
			, body=[Make.Return(Make.Call(classAs_astAttribute, list_keyword=listCall_keyword))]
			, decorator_list=[astName_staticmethod]
			, returns=classAs_astAttribute)
		return ast_stmt

	def unpackDictionaryAllMatch_argsVersions() -> ast.stmt:
		ast_stmt = None
		if len(dictionaryAllMatch_argsVersions) == 1:
			for versionMinorMinimum_match_args, dictionaryMethodElements in dictionaryAllMatch_argsVersions.items():
				ast_stmt = create_ast_stmt(dictionaryMethodElements)
				if versionMinorMinimum_match_args > versionMinorMinimumClass:
					versionMinorData: int = versionMinorMinimum_match_args
					body = [ast_stmt]
					orElse = []
					ast_stmt = Make.If(Make.Compare(Make.Attribute(Make.Name('sys'), 'version_info')
								, ops=[ast.GtE()]
								, comparators=[Make.Tuple([Make.Constant(3), Make.Constant(versionMinorData)])])
							, body=body
							, orElse=orElse
						)
		else:
			body: list[ast.stmt] = []
			orElse: list[ast.stmt] = []
			versionMinorData: int = -999999999999999999
			for versionMinorMinimum_match_args, dictionaryMethodElements in dictionaryAllMatch_argsVersions.items():
				# Do some variations of the method need to be conditional on the Python version?
				# if versionMinorMinimum_match_args == versionMinorMinimumClass, then access to versionMinorMinimum_match_args is already conditional on the python version because it is checked at the class level.
				if versionMinorMinimum_match_args > versionMinorMinimumClass:
					body = [create_ast_stmt(dictionaryMethodElements)]
					versionMinorData = versionMinorMinimum_match_args
				else:
					orElse = [create_ast_stmt(dictionaryMethodElements)]
			ast_stmt = Make.If(Make.Compare(Make.Attribute(Make.Name('sys'), 'version_info')
						, ops=[ast.GtE()]
						, comparators=[Make.Tuple([Make.Constant(3), Make.Constant(versionMinorData)])])
					, body=body
					, orElse=orElse
				)
		assert ast_stmt is not None, "Coding by brinkmanship!"
		return ast_stmt

	dictionaryToolElements: dict[str, DictionaryClassDef] = getElementsMake()
	for ClassDefIdentifier, dictionaryClassDef in dictionaryToolElements.items():
		# Bypass the manufacture of the tool by using a prefabricated tool from the annex.
		if ClassDefIdentifier == 'Attribute':
			ast_stmt = FunctionDefMake_Attribute
			list4ClassDefBody.append(ast_stmt)
			continue
		elif ClassDefIdentifier == 'Import':
			ast_stmt = FunctionDefMake_Import
			list4ClassDefBody.append(ast_stmt)
			list_aliasIdentifier.append('identifierDotAttribute')
			continue
		else:
			ast_stmt = None

		classAs_astAttribute: ast.expr = eval(dictionaryClassDef['classAs_astAttribute'])
		dictionaryAllClassVersions: dict[int, dict[int, DictionaryMatchArgs]] = dictionaryClassDef['versionMinorMinimumClass']

		if len(dictionaryAllClassVersions) == 1:
			for versionMinorMinimumClass, dictionaryAllMatch_argsVersions in dictionaryAllClassVersions.items():
				ast_stmt = unpackDictionaryAllMatch_argsVersions()
				if versionMinorMinimumClass > pythonMinimumVersionMinor:
					versionMinorData: int = versionMinorMinimumClass
					body = [ast_stmt]
					orElse = []
					ast_stmt = Make.If(Make.Compare(Make.Attribute(Make.Name('sys'), 'version_info')
								, ops=[ast.GtE()]
								, comparators=[Make.Tuple([Make.Constant(3), Make.Constant(versionMinorData)])])
							, body=body
							, orElse=orElse
						)

		else:
			# Does _every_ variation of the method need to be conditional on the Python version?
			body: list[ast.stmt] = []
			orElse: list[ast.stmt] = []
			versionMinorData: int = -999999999999999999
			for versionMinorMinimumClass, dictionaryAllMatch_argsVersions in dictionaryAllClassVersions.items():
				if versionMinorMinimumClass > pythonMinimumVersionMinor:
					body = [unpackDictionaryAllMatch_argsVersions()]
					versionMinorData = versionMinorMinimumClass
				else:
					orElse = [unpackDictionaryAllMatch_argsVersions()]
			ast_stmt = Make.If(Make.Compare(Make.Attribute(Make.Name('sys'), 'version_info')
						, ops=[ast.GtE()]
						, comparators=[Make.Tuple([Make.Constant(3), Make.Constant(versionMinorData)])])
					, body=body
					, orElse=orElse
				)

		assert ast_stmt is not None, "Coding by brinkmanship!"
		list4ClassDefBody.append(ast_stmt)
	# END OLD code

	# Module-level operations ===============
	setKeywordArgumentsAnnotationTypeAlias.discard('int')
	list_aliasIdentifier = sorted(set([*setKeywordArgumentsAnnotationTypeAlias, *list_aliasIdentifier]), key=str.lower)
	list4ModuleBody: list[ast.stmt] = [
		Make.ImportFrom('astToolkit', [Make.alias(identifier) for identifier in list_aliasIdentifier])
		, Make.ImportFrom('collections.abc', [Make.alias('Sequence')])
		, Make.ImportFrom('typing', [Make.alias('Any')])
		, Make.ImportFrom('typing_extensions', [Make.alias('Unpack')])
		, Make.Import('ast')
		, Make.Import('sys')
		]

	writeClass('Make', list4ClassDefBody, list4ModuleBody)

if __name__ == "__main__":
	make_astTypes()
	makeJoinClassmethod()
	makeToolBe()
	makeToolClassIsAndAttribute()
	makeToolDOT()
	makeToolGrab()
	makeToolMake()
	# makeTool_dump()

