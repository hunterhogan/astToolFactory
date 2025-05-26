from astToolFactory import (
	astName_overload, astName_staticmethod, astName_typing_TypeAlias, Dictionary_type_ast_expr,
	DictionaryClassDef, DictionaryGrabElements, DictionaryMatchArgs, DictionaryTypeAliasAttribute,
	getElementsBe, getElementsClassIsAndAttribute, getElementsDOT, getElementsGrab, getElementsMake,
	getElementsTypeAlias, keywordArgumentsIdentifier, listPylanceErrors, pythonVersionMinorMinimum,
	settingsPackageToManufacture, toolMakeFunctionDefReturnCall_keywords,
)
from astToolFactory.docstrings import (
	ClassDefDocstring_ast_operator, ClassDefDocstringBe, ClassDefDocstringClassIsAndAttribute,
	ClassDefDocstringDOT, ClassDefDocstringGrab, ClassDefDocstringMake, docstringWarning,
)
from astToolFactory.factory_annex import (
	FunctionDef_join, FunctionDef_operatorJoinMethod, FunctionDefGrab_andDoAllOf,
	FunctionDefMake_Attribute, FunctionDefMake_Import, listHandmade_astTypes,
)
from astToolkit import (
	Add, astModuleToIngredientsFunction, BitOr, ClassIsAndAttribute, IfThis, IngredientsModule, Make,
	NodeChanger, parseLogicalPath2astModule, Then, LedgerOfImports, dump
)
from astToolkit.transformationTools import write_astModule
from collections import defaultdict
from itertools import chain
from pathlib import PurePosixPath
from typing import cast
from Z0Z_tools import writeStringToHere
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
	def append_ast_stmtTypeAlias() -> None:
		ast_stmt = None
		if len(dictionaryVersions) == 1:
			# This branch is the simplest case: one TypeAlias for the attribute for all Python versions
			for versionMinorData, listClassAs_astAttribute in dictionaryVersions.items():
				ast_stmt = Make.AnnAssign(astNameTypeAlias, astName_typing_TypeAlias, BitOr.join([eval(classAs_astAttribute) for classAs_astAttribute in listClassAs_astAttribute]))
				if versionMinorData > pythonVersionMinorMinimum:
					ast_stmt = Make.If(Make.Compare(Make.Attribute(Make.Name('sys'), 'version_info')
								, ops=[ast.GtE()]
								, comparators=[Make.Tuple([Make.Constant(3), Make.Constant(versionMinorData)])])
								, body=[ast_stmt])
		else:
			listVersionsMinor = sorted(dictionaryVersions.keys(), reverse=False)
			if len(listVersionsMinor) > 2:
				raise NotImplementedError
			ast_stmtAtPythonMinimum = Make.AnnAssign(astNameTypeAlias, astName_typing_TypeAlias, BitOr.join([eval(classAs_astAttribute) for classAs_astAttribute in dictionaryVersions[min(listVersionsMinor)]]))
			ast_stmtAbovePythonMinimum = Make.AnnAssign(astNameTypeAlias, astName_typing_TypeAlias, BitOr.join([eval(classAs_astAttribute) for classAs_astAttribute in dictionaryVersions[max(listVersionsMinor)]]))

			ast_stmt = Make.If(Make.Compare(Make.Attribute(Make.Name('sys'), 'version_info')
						, ops=[ast.GtE()]
						, comparators=[Make.Tuple([Make.Constant(3), Make.Constant(max(listVersionsMinor))])])
						, body=[ast_stmtAbovePythonMinimum]
						, orelse=[ast_stmtAtPythonMinimum])
		assert ast_stmt is not None, "Coding by brinkmanship!"
		list4ModuleBody.append(ast_stmt)

	list4ModuleBody: list[ast.stmt] = []
	ledgerOfImports = LedgerOfImports(
		Make.Module([
			Make.ImportFrom('types', [Make.alias('EllipsisType'), Make.alias('NotImplementedType')])
			, Make.ImportFrom('typing', [Make.alias('Any'), Make.alias('TypeAlias', 'typing_TypeAlias'), Make.alias('TypedDict'), Make.alias('TypeVar', 'typing_TypeVar')])
			, Make.Import('ast')
			, Make.Import('sys')
		])
	)
	dictionaryToolElements: dict[str, DictionaryTypeAliasAttribute] = getElementsTypeAlias()

	for attribute, attributeData in dictionaryToolElements.items(): # pyright: ignore[reportUnusedVariable]
		hasDOTIdentifier: str = attributeData['TypeAlias_hasDOTIdentifier']
		dictionaryTypeAliasSubcategory = attributeData['subcategories']
		hasDOTTypeAliasName_Store: ast.Name = Make.Name(hasDOTIdentifier, ast.Store())

		if len(dictionaryTypeAliasSubcategory) == 1:
			astNameTypeAlias = hasDOTTypeAliasName_Store
			for TypeAliasSubcategory, dictionaryVersions in dictionaryTypeAliasSubcategory.items():
				append_ast_stmtTypeAlias()
		else:
			# This defaultdict builds a dictionary to mimic the process I'm already using to build the TypeAlias.
			attributeDictionaryVersions: dict[int, list[str]] = defaultdict(list)
			for TypeAliasSubcategory, dictionaryVersions in dictionaryTypeAliasSubcategory.items():
				astNameTypeAlias: ast.Name = Make.Name(TypeAliasSubcategory)
				if any(dictionaryVersions.keys()) <= pythonVersionMinorMinimum:
					attributeDictionaryVersions[min(dictionaryVersions.keys())].append(dump(astNameTypeAlias))
				else:
					attributeDictionaryVersions[min(dictionaryVersions.keys())].append(dump(astNameTypeAlias))
					attributeDictionaryVersions[max(dictionaryVersions.keys())].append(dump(astNameTypeAlias))
				append_ast_stmtTypeAlias()
			astNameTypeAlias = hasDOTTypeAliasName_Store
			dictionaryVersions: dict[int, list[str]] = attributeDictionaryVersions
			append_ast_stmtTypeAlias()

	astModule = Make.Module(
		body=[docstringWarning
			, ledgerOfImports.makeList_ast()
			, *listHandmade_astTypes
			, *list4ModuleBody
			]
		)

	writeModule(astModule, '_astTypes')

def makeJoinClassmethod() -> None:
	list_aliasIdentifier: list[str] = ['ast_attributes', 'Make']
	list4ModuleBody: list[ast.stmt] = [
		FunctionDef_operatorJoinMethod
		]

	listOperatorIdentifiers: list[str] = ['Add', 'BitAnd', 'BitOr', 'BitXor', 'Div', 'FloorDiv', 'LShift', 'MatMult', 'Mod', 'Mult', 'Pow', 'RShift', 'Sub',]

	for identifier in listOperatorIdentifiers:
		list4ModuleBody.append(Make.ClassDef(identifier
			, bases=[Make.Attribute(Make.Name('ast'), identifier)]
			, body=[ClassDefDocstring_ast_operator, FunctionDef_join]
		))

	astModule = Make.Module([docstringWarning
		, Make.ImportFrom('astToolkit', [Make.alias(identifier) for identifier in list_aliasIdentifier])
		, Make.ImportFrom('collections.abc', [Make.alias('Iterable')])
		, Make.ImportFrom('typing', [Make.alias('TypedDict'), Make.alias('Unpack')])
		, Make.Import('ast')
		, Make.Import('sys')
		, *list4ModuleBody
	])

	writeModule(astModule, '_joinClassmethod')

def makeTool_dump() -> None:
	ingredientsFunction = astModuleToIngredientsFunction(parseLogicalPath2astModule('ast'), 'dump')
	astConstant = Make.Constant('ast.')
	findThis = ClassIsAndAttribute.valueIs(ast.Attribute, IfThis.isAttributeNamespaceIdentifier('node', '__class__'))
	doThat = lambda node: Add.join([astConstant, cast(ast.expr, node)]) # pyright: ignore[reportUnknownLambdaType, reportUnknownVariableType]
	prepend_ast = NodeChanger(findThis, doThat) # pyright: ignore[reportUnknownArgumentType]
	findThis = IfThis.isFunctionDefIdentifier('_format')
	doThat = lambda node: prepend_ast.visit(node) # pyright: ignore[reportUnknownArgumentType, reportUnknownLambdaType, reportUnknownVariableType]
	NodeChanger(findThis, doThat).visit(ingredientsFunction.astFunctionDef) # pyright: ignore[reportUnknownArgumentType]
	pathFilename = PurePosixPath(settingsPackageToManufacture.pathPackage, '_dumpFunctionDef' + settingsPackageToManufacture.fileExtension)
	write_astModule(IngredientsModule(ingredientsFunction), pathFilename, settingsPackageToManufacture.identifierPackage)

def makeToolBe() -> None:
	list4ClassDefBody: list[ast.stmt] = [ClassDefDocstringBe]

	listDictionaryToolElements = getElementsBe()

	for dictionaryToolElements in listDictionaryToolElements:
		ClassDefIdentifier = dictionaryToolElements['ClassDefIdentifier']
		classAs_astAttribute = eval(dictionaryToolElements['classAs_astAttribute'])
		versionMinorMinimumClass = dictionaryToolElements['versionMinorMinimumClass']

		ast_stmt = Make.FunctionDef(ClassDefIdentifier
			, Make.arguments(args=[Make.arg('node', annotation=Make.Name('ast.AST'))])
			, body=[Make.Return(Make.Call(Make.Name('isinstance'), args=[Make.Name('node'), classAs_astAttribute]))]
			, decorator_list=[astName_staticmethod]
			, returns=Make.Subscript(Make.Name('TypeGuard'), slice=classAs_astAttribute))

		if versionMinorMinimumClass > pythonVersionMinorMinimum:
			ast_stmt = ast.If(ast.Compare(ast.Attribute(ast.Name('sys'), 'version_info')
						, ops=[ast.GtE()]
						, comparators=[ast.Tuple([ast.Constant(3)
												, ast.Constant(versionMinorMinimumClass)])])
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
	def create_ast_stmt() -> ast.If | ast.FunctionDef:
		ast_stmt = Make.FunctionDef(attribute + 'Is'
				, args=Make.arguments(args=[Make.arg('astClass', annotation=Make.Subscript(Make.Name('type'), astNameTypeAlias))
						, Make.arg('attributeCondition', annotation=annotation)
					])
					, body=body
					, decorator_list=decorator_list
					, returns=returns
		)

		if versionMinorMinimumAttribute > pythonVersionMinorMinimum:
			ast_stmt = ast.If(ast.Compare(left=ast.Attribute(ast.Name('sys'), 'version_info')
								, ops=[ast.GtE()]
								, comparators=[ast.Tuple([ast.Constant(3), ast.Constant(versionMinorMinimumAttribute)])])
							, body=[ast_stmt]
							, orelse=orelse
			)

		return ast_stmt

	list4ClassDefBody: list[ast.stmt] = [ClassDefDocstringClassIsAndAttribute]

	dictionaryToolElements: dict[str, dict[str, Dictionary_type_ast_expr]] = getElementsClassIsAndAttribute()
	# Process each attribute group to generate overloaded methods and implementations
	for attribute, dictionaryTypeAliasSubcategory in dictionaryToolElements.items():
		# Get the pre-computed hasDOTIdentifier from the first entry
		hasDOTIdentifier: str = next(iter(dictionaryTypeAliasSubcategory.values()))['TypeAlias_hasDOTIdentifier']
		hasDOTTypeAliasName_Load: ast.Name = ast.Name(hasDOTIdentifier)
		orelse: list[ast.stmt] = []

		list_type_ast_expr: list[ast.expr] = []
		dictionaryVersionsTypeAliasSubcategory: dict[int, list[ast.expr]] = defaultdict(list)

		if len(dictionaryTypeAliasSubcategory) > 1:
			for TypeAliasSubcategory, dictionary_type_ast_expr in dictionaryTypeAliasSubcategory.items():
				versionMinorMinimumAttribute: int = dictionary_type_ast_expr['versionMinorMinimumAttribute']
				astNameTypeAlias: ast.Name = ast.Name(TypeAliasSubcategory)
				body: list[ast.stmt] = [ast.Expr(ast.Constant(value=...))]
				decorator_list=[astName_staticmethod, astName_overload]
				returns=ast.Subscript(ast.Name('Callable'), ast.Tuple([ast.List([ast.Attribute(ast.Name('ast'), attr='AST')]), BitOr.join([Make.Subscript(Make.Name('TypeGuard'), slice=astNameTypeAlias), Make.Name('bool')])]))

				typeSansNone_ast_expr = eval(dictionary_type_ast_expr['typeSansNone_ast_expr'])
				annotation = ast.Subscript(ast.Name('Callable'), ast.Tuple([ast.List([typeSansNone_ast_expr]), ast.Name('bool')]))

				list_type_ast_expr.append(annotation)
				dictionaryVersionsTypeAliasSubcategory[dictionary_type_ast_expr['versionMinorMinimumAttribute']].append(annotation)

				list4ClassDefBody.append(create_ast_stmt())

		astNameTypeAlias = hasDOTTypeAliasName_Load
		if len(dictionaryVersionsTypeAliasSubcategory) > 1:
			versionMinorMinimumAttribute: int = min(dictionaryVersionsTypeAliasSubcategory.keys())
			decorator_list: list[ast.expr] = [astName_staticmethod]

			annotation = BitOr.join(dictionaryVersionsTypeAliasSubcategory[versionMinorMinimumAttribute])
			workhorseReturnValue: ast.BoolOp = ast.BoolOp(op=ast.And(), values=[ast.Call(ast.Name('isinstance'), args=[ast.Name('node'), ast.Name('astClass')], keywords=[])])
			for node in ast.walk(annotation):
				if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name) and node.value.id == 'Sequence' and isinstance(node.slice, ast.BinOp) and isinstance(node.slice.right, ast.Constant) and node.slice.right.value is None:
					workhorseReturnValue.values.append(ast.Compare(ast.Attribute(ast.Name('node'), attribute)
													, ops=[ast.NotEq()]
													, comparators=[ast.List([ast.Constant(None)])]))
					break
				if isinstance(node, ast.Constant) and node.value is None:
					workhorseReturnValue.values.append(ast.Compare(ast.Attribute(ast.Name('node'), attribute)
													, ops=[ast.IsNot()]
													, comparators=[ast.Constant(None)]))
					break

			workhorseReturnValue.values.append(ast.Call(ast.Name('attributeCondition'), args=[ast.Attribute(ast.Name('node'), attribute)]))

			buffaloBuffalo_workhorse_returnsAnnotation = BitOr.join([ast.Subscript(ast.Name('TypeGuard'), slice=astNameTypeAlias), ast.Name('bool')])
			body: list[ast.stmt] = [Make.FunctionDef('workhorse',
						args=Make.arguments(args=[Make.arg('node', annotation=Make.Attribute(Make.Name('ast'), 'AST'))])
						, body=[Make.Return(workhorseReturnValue)]
						, returns=buffaloBuffalo_workhorse_returnsAnnotation)
					, Make.Return(Make.Name('workhorse'))]
			returns=Make.Subscript(Make.Name('Callable'), slice=Make.Tuple([Make.List([Make.Attribute(Make.Name('ast'), 'AST')]), buffaloBuffalo_workhorse_returnsAnnotation]))

			del dictionaryVersionsTypeAliasSubcategory[versionMinorMinimumAttribute]
			orelse = [create_ast_stmt()]

		for TypeAliasSubcategory, dictionary_type_ast_expr in dictionaryTypeAliasSubcategory.items():
			versionMinorMinimumAttribute: int = dictionary_type_ast_expr['versionMinorMinimumAttribute']
			decorator_list=[astName_staticmethod]
			if list_type_ast_expr:
				annotation = BitOr.join(list_type_ast_expr)
			else:
				typeSansNone_ast_expr = eval(dictionary_type_ast_expr['typeSansNone_ast_expr'])
				annotation = ast.Subscript(ast.Name('Callable'), ast.Tuple([ast.List([typeSansNone_ast_expr]), ast.Name('bool')]))

			workhorseReturnValue: ast.BoolOp = ast.BoolOp(op=ast.And(), values=[ast.Call(ast.Name('isinstance'), args=[ast.Name('node'), ast.Name('astClass')], keywords=[])])
			for node in ast.walk(annotation):
				if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name) and node.value.id == 'list' and isinstance(node.slice, ast.BinOp) and isinstance(node.slice.right, ast.Constant) and node.slice.right.value is None:
					workhorseReturnValue.values.append(ast.Compare(ast.Attribute(ast.Name('node'), attribute)
													, ops=[ast.NotEq()]
													, comparators=[ast.List([ast.Constant(None)])]))
					break
				if isinstance(node, ast.Constant) and node.value is None:
					workhorseReturnValue.values.append(ast.Compare(ast.Attribute(ast.Name('node'), attribute)
													, ops=[ast.IsNot()]
													, comparators=[ast.Constant(None)]))
					break

			workhorseReturnValue.values.append(ast.Call(ast.Name('attributeCondition'), args=[ast.Attribute(ast.Name('node'), attribute)]))
			buffaloBuffalo_workhorse_returnsAnnotation = BitOr.join([ast.Subscript(ast.Name('TypeGuard'), slice=astNameTypeAlias), ast.Name('bool')])
			body: list[ast.stmt] = [Make.FunctionDef('workhorse',
						args=Make.arguments(args=[Make.arg('node', annotation=Make.Attribute(Make.Name('ast'), 'AST'))])
						, body=[Make.Return(workhorseReturnValue)]
						, returns=buffaloBuffalo_workhorse_returnsAnnotation)
					, Make.Return(Make.Name('workhorse'))]
			returns=Make.Subscript(Make.Name('Callable'), Make.Tuple([Make.List([Make.Attribute(Make.Name('ast'), 'AST')]), buffaloBuffalo_workhorse_returnsAnnotation]))

			list4ClassDefBody.append(create_ast_stmt())
			break

	list4ModuleBody: list[ast.stmt] = [
			Make.ImportFrom('astToolkit._astTypes', [Make.alias('*')])
			, Make.ImportFrom('collections.abc', [Make.alias('Callable'), Make.alias('Sequence')])
			, Make.ImportFrom('typing', [Make.alias(identifier) for identifier in ['Any', 'Literal', 'overload', 'TypeGuard']])
			, Make.Import('ast')
	]

	writeClass('ClassIsAndAttribute', list4ClassDefBody, list4ModuleBody)

def makeToolDOT() -> None:
	def create_ast_stmt() -> ast.If | ast.FunctionDef:
		ast_stmt = Make.FunctionDef(attribute
				, args=Make.arguments(args=[Make.arg('node', annotation=astNameTypeAlias)])
					, body=body
					, decorator_list=decorator_list
					, returns=returns
		)

		if versionMinorMinimumAttribute > pythonVersionMinorMinimum:
			ast_stmt = ast.If(ast.Compare(left=ast.Attribute(ast.Name('sys'), 'version_info')
								, ops=[ast.GtE()]
								, comparators=[ast.Tuple([ast.Constant(3), ast.Constant(versionMinorMinimumAttribute)])])
							, body=[ast_stmt]
							, orelse=orelse
			)

		return ast_stmt

	list4ClassDefBody: list[ast.stmt] = [ClassDefDocstringDOT]

	dictionaryToolElements: dict[str, dict[str, Dictionary_type_ast_expr]] = getElementsDOT()
	# Process each attribute group to generate overloaded methods and implementations
	for attribute, dictionaryTypeAliasSubcategory in dictionaryToolElements.items():
		# Get the pre-computed hasDOTIdentifier from the first entry
		hasDOTIdentifier: str = next(iter(dictionaryTypeAliasSubcategory.values()))['TypeAlias_hasDOTIdentifier']
		hasDOTTypeAliasName_Load: ast.Name = ast.Name(hasDOTIdentifier)
		orelse: list[ast.stmt] = []

		list_type_ast_expr: list[ast.expr] = []
		dictionaryVersionsTypeAliasSubcategory: dict[int, list[ast.expr]] = defaultdict(list)
		if len(dictionaryTypeAliasSubcategory) > 1:
			for TypeAliasSubcategory, dictionary_type_ast_expr in dictionaryTypeAliasSubcategory.items():
				versionMinorMinimumAttribute: int = dictionary_type_ast_expr['versionMinorMinimumAttribute']
				astNameTypeAlias: ast.Name = ast.Name(TypeAliasSubcategory)
				body: list[ast.stmt] = [ast.Expr(ast.Constant(value=...))]
				decorator_list=[astName_staticmethod, astName_overload]
				returns = cast(ast.Attribute, eval(dictionary_type_ast_expr['typeSansNone_ast_expr']))
				list_type_ast_expr.append(returns)
				dictionaryVersionsTypeAliasSubcategory[dictionary_type_ast_expr['versionMinorMinimumAttribute']].append(returns)
				list4ClassDefBody.append(create_ast_stmt())

		astNameTypeAlias = hasDOTTypeAliasName_Load
		if len(dictionaryVersionsTypeAliasSubcategory) > 1:
			body: list[ast.stmt] = [ast.Return(ast.Attribute(ast.Name('node'), attribute))]
			decorator_list: list[ast.expr] = [astName_staticmethod]
			versionMinorMinimumAttribute: int = min(dictionaryVersionsTypeAliasSubcategory.keys())
			returns = BitOr.join(dictionaryVersionsTypeAliasSubcategory[versionMinorMinimumAttribute])
			del dictionaryVersionsTypeAliasSubcategory[versionMinorMinimumAttribute]
			orelse = [create_ast_stmt()]

		for TypeAliasSubcategory, dictionary_type_ast_expr in dictionaryTypeAliasSubcategory.items():
			versionMinorMinimumAttribute: int = dictionary_type_ast_expr['versionMinorMinimumAttribute']
			body: list[ast.stmt] = [ast.Return(ast.Attribute(ast.Name('node'), attribute))]
			decorator_list=[astName_staticmethod]
			if list_type_ast_expr:
				returns = BitOr.join(list_type_ast_expr)
			else:
				returns = cast(ast.Attribute, eval(dictionary_type_ast_expr['typeSansNone_ast_expr']))
			list4ClassDefBody.append(create_ast_stmt())
			break

	list4ModuleBody: list[ast.stmt] = [
			Make.ImportFrom('astToolkit._astTypes', [Make.alias('*')])
			, Make.ImportFrom('collections.abc', [Make.alias('Sequence')])
			, Make.ImportFrom('typing', [Make.alias('Any'), Make.alias('Literal'), Make.alias('overload')])
			, Make.Import('ast')
			, Make.Import('sys')
			]

	writeClass('DOT', list4ClassDefBody, list4ModuleBody)

def makeToolGrab() -> None:
	def create_ast_stmt() -> ast.If | ast.FunctionDef:
		ast_stmt = None
		for versionMinorMinimumAttribute, list_type_ast_expr in listTypesByVersion:
			list_ast_expr4annotation: list[ast.expr] = []
			for type_ast_exprAsStr in list_type_ast_expr:
				type_ast_expr = eval(type_ast_exprAsStr)
				list_ast_expr4annotation.append(ast.Subscript(ast.Name('Callable'), slice=ast.Tuple([ast.List([type_ast_expr]), type_ast_expr])))

			ast_expr4annotation = BitOr.join(list_ast_expr4annotation)

			ast_stmt = Make.FunctionDef(attribute + 'Attribute'
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

			if versionMinorMinimumAttribute > pythonVersionMinorMinimum:
				ast_stmt = ast.If(test=ast.Compare(
					left=ast.Attribute(ast.Name('sys'), 'version_info'),
					ops=[ast.GtE()],
					comparators=[ast.Tuple(
						elts=[ast.Constant(3), ast.Constant(versionMinorMinimumAttribute)],
						ctx=ast.Load()
					)]
				),
				body=[ast_stmt],
				orelse=ast_stmtAtPythonMinimum
				)
		assert ast_stmt is not None, "Coding by brinkmanship!"
		return ast_stmt
	list4ClassDefBody: list[ast.stmt] = [ClassDefDocstringGrab, FunctionDefGrab_andDoAllOf]
	dictionaryToolElements = getElementsGrab()

	for attribute, grabElements in dictionaryToolElements.items():
		hasDOTIdentifier: str = grabElements['TypeAlias_hasDOTIdentifier']
		listTypesByVersion = grabElements['listTypesByVersion']
		hasDOTTypeAliasName_Load: ast.Name = ast.Name(hasDOTIdentifier)
		ast_stmtAtPythonMinimum: list[ast.stmt] = []

		if len(listTypesByVersion) > 1:
			abovePythonMinimum = [((versionMax := max([typesForVersion[0] for typesForVersion in listTypesByVersion])),  sorted(chain(*[typesForVersion[1] for typesForVersion in listTypesByVersion]), key=str.lower))]
			for typesForVersion in listTypesByVersion:
				if typesForVersion[0] == versionMax:
					listTypesByVersion.remove(typesForVersion)
					break
			ast_stmtAtPythonMinimum = [create_ast_stmt()]
			listTypesByVersion = abovePythonMinimum

		list4ClassDefBody.append(create_ast_stmt())

	list4ModuleBody: list[ast.stmt] = [
			Make.ImportFrom('astToolkit', [Make.alias(identifier) for identifier in ['个']])
			, Make.ImportFrom('astToolkit._astTypes', [Make.alias('*')])
			, Make.ImportFrom('collections.abc', [Make.alias('Callable'), Make.alias('Sequence')])
			, Make.ImportFrom('typing', [Make.alias('Any'), Make.alias('Literal')])
			, Make.Import('ast')
			, Make.Import('sys')
			]

	writeClass('Grab', list4ClassDefBody, list4ModuleBody)

def makeToolMake() -> None:
	# TODO add `ClassDef` for ast subclasses that do not have __init__ parameters. At the very least, it prevents an error if the user uses `Make.GtE()` instead of `ast.GtE()`.
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

	# TODO remaking **keywordArguments
	""" 
if column 'keywordArguments' is True, 
	build a subclassed dictionary and put it in the `Make` module
	make sure to not add 14 identical subclassed dictionaries
	allow for the subclassed dictionary to have more than one new key
	analytically, this is not much different than how I construct a TypeAlias such as `intORstrORtype_params`
	But, the code complexity is higher in this case and the benefit is better.

class ast_attributes_kind(ast_attributes, total=False):
	kind: str | None

	def Break(**keywordArguments: Unpack[ast_attributes]) -> ast.Break:
		return ast.Break(**keywordArguments)

	def Constant(value: Any, **keywordArguments: ast_attributes_kind) -> ast.Constant:
		return ast.Constant(value=value, kind=None, **keywordArguments)

	def Dict(keys: Sequence[ast.expr | None]=[None], values: Sequence[ast.expr]=[], **keywordArguments: ast_attributes) -> ast.Dict:
		return ast.Dict(keys=list(keys), values=list(values), **keywordArguments)

	def pattern(**keywordArguments: Unpack[ast_attributes_int]) -> ast.pattern:
		return ast.pattern(**keywordArguments)
	
	"""
	def create_ast_stmt(dictionaryMethodElements: DictionaryMatchArgs) -> ast.FunctionDef:
		listFunctionDef_args: list[ast.arg] = [cast(ast.arg, eval(ast_argAsStr)) for ast_argAsStr in dictionaryMethodElements['listStr4FunctionDef_args']]
		kwarg: ast.arg | None = None
		if str(dictionaryMethodElements['kwarg']) != 'No':
			setKeywordArgumentsAnnotationTypeAlias.add(dictionaryMethodElements['kwarg'])
			kwarg = ast.arg(keywordArgumentsIdentifier, annotation=ast.Name(str(dictionaryMethodElements['kwarg'])))

		defaults: list[ast.expr] = [cast(ast.expr, eval(defaultAsStr)) for defaultAsStr in dictionaryMethodElements['listDefaults']]

		listCall_keyword: list[ast.keyword] = []
		for tupleCall_keywords in dictionaryMethodElements['listTupleCall_keywords']:
			argIdentifier, keywordValue = tupleCall_keywords
			listCall_keyword.append(ast.keyword(argIdentifier, value=eval(keywordValue)))
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
					orelse = []
					ast_stmt = ast.If(ast.Compare(ast.Attribute(ast.Name('sys'), 'version_info')
								, ops=[ast.GtE()]
								, comparators=[ast.Tuple([ast.Constant(3)
														, ast.Constant(versionMinorData)])])
							, body=body
							, orelse=orelse
						)
		else:
			body: list[ast.stmt] = []
			orelse: list[ast.stmt] = []
			versionMinorData: int = -999999999999999999
			for versionMinorMinimum_match_args, dictionaryMethodElements in dictionaryAllMatch_argsVersions.items():
				# Do some variations of the method need to be conditional on the Python version?
				# if versionMinorMinimum_match_args == versionMinorMinimumClass, then access to versionMinorMinimum_match_args is already conditional on the python version because it is checked at the class level.
				if versionMinorMinimum_match_args > versionMinorMinimumClass:
					body = [create_ast_stmt(dictionaryMethodElements)]
					versionMinorData = versionMinorMinimum_match_args
				else:
					orelse = [create_ast_stmt(dictionaryMethodElements)]
			ast_stmt = ast.If(ast.Compare(ast.Attribute(ast.Name('sys'), 'version_info')
						, ops=[ast.GtE()]
						, comparators=[ast.Tuple([ast.Constant(3)
												, ast.Constant(versionMinorData)])])
					, body=body
					, orelse=orelse
				)
		assert ast_stmt is not None, "Coding by brinkmanship!"
		return ast_stmt

	list_aliasIdentifier: list[str] = ['ScalarOrContainerOfScalar']
	list4ClassDefBody: list[ast.stmt] = [ClassDefDocstringMake]
	setKeywordArgumentsAnnotationTypeAlias: set[str] = set()

	dictionaryToolElements: dict[str, DictionaryClassDef] = getElementsMake()

	for ClassDefIdentifier, dictionaryClassDef in dictionaryToolElements.items():
		ast_stmt = None
		if ClassDefIdentifier == 'Attribute':
			ast_stmt = FunctionDefMake_Attribute
			list4ClassDefBody.append(ast_stmt)
			continue
		if ClassDefIdentifier == 'Import':
			ast_stmt = FunctionDefMake_Import
			list4ClassDefBody.append(ast_stmt)
			list_aliasIdentifier.append('str_nameDOTname')
			continue
		classAs_astAttribute = cast(ast.expr, eval(dictionaryClassDef['classAs_astAttribute']))
		dictionaryAllClassVersions: dict[int, dict[int, DictionaryMatchArgs]] = dictionaryClassDef['versionMinorMinimumClass']

		if len(dictionaryAllClassVersions) == 1:
			for versionMinorMinimumClass, dictionaryAllMatch_argsVersions in dictionaryAllClassVersions.items():
				ast_stmt = unpackDictionaryAllMatch_argsVersions()
				if versionMinorMinimumClass > pythonVersionMinorMinimum:
					versionMinorData: int = versionMinorMinimumClass
					body = [ast_stmt]
					orelse = []
					ast_stmt = ast.If(ast.Compare(ast.Attribute(ast.Name('sys'), 'version_info')
								, ops=[ast.GtE()]
								, comparators=[ast.Tuple([ast.Constant(3)
														, ast.Constant(versionMinorData)])])
							, body=body
							, orelse=orelse
						)

		else:
			# Does _every_ variation of the method need to be conditional on the Python version?
			body: list[ast.stmt] = []
			orelse: list[ast.stmt] = []
			versionMinorData: int = -999999999999999999
			for versionMinorMinimumClass, dictionaryAllMatch_argsVersions in dictionaryAllClassVersions.items():
				if versionMinorMinimumClass > pythonVersionMinorMinimum:
					body = [unpackDictionaryAllMatch_argsVersions()]
					versionMinorData = versionMinorMinimumClass
				else:
					orelse = [unpackDictionaryAllMatch_argsVersions()]
			ast_stmt = ast.If(ast.Compare(ast.Attribute(ast.Name('sys'), 'version_info')
						, ops=[ast.GtE()]
						, comparators=[ast.Tuple([ast.Constant(3)
												, ast.Constant(versionMinorData)])])
					, body=body
					, orelse=orelse
				)

		assert ast_stmt is not None, "Coding by brinkmanship!"
		list4ClassDefBody.append(ast_stmt)

	# Module-level operations ===============
	setKeywordArgumentsAnnotationTypeAlias.discard('int')
	list_aliasIdentifier = sorted(set([*setKeywordArgumentsAnnotationTypeAlias, *list_aliasIdentifier]), key=str.lower)
	list4ModuleBody: list[ast.stmt] = [
		Make.ImportFrom('astToolkit', [Make.alias(identifier) for identifier in list_aliasIdentifier])
		, Make.ImportFrom('collections.abc', [Make.alias('Sequence')])
		, Make.ImportFrom('typing', [Make.alias('Any')])
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
	makeTool_dump()

