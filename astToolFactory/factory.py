from astToolFactory import (
	astName_overload, astName_staticmethod, astName_typing_TypeAlias, getElementsBe, getElementsClassIsAndAttribute,
	getElementsDOT, getElementsGrab, getElementsMake, getElementsTypeAlias, keywordKeywordArguments4Call,
	ManufacturedPackageSettings, settingsManufacturing,
)
from astToolFactory.documentation import docstrings, docstringWarning
from astToolFactory.factory_annex import (
	astModule_theSSOT, FunctionDef_boolopJoinMethod, FunctionDef_join_boolop, FunctionDef_join_operator,
	FunctionDef_operatorJoinMethod, FunctionDefGrab_andDoAllOf, FunctionDefMake_Attribute, FunctionDefMake_Import,
	listHandmade_astTypes, listOverloads_keyword, listOverloadsTypeAlias,
)
from astToolkit import (
	astModuleToIngredientsFunction, ClassIsAndAttribute, IfThis, IngredientsFunction, IngredientsModule, LedgerOfImports,
	Make, NodeChanger, parseLogicalPath2astModule,
)
from astToolkit.transformationTools import write_astModule
from collections.abc import Callable
from isort import code as isort_code
from pathlib import PurePosixPath
from typing import Any, cast, TypedDict, TypeIs
from Z0Z_tools import writeStringToHere
import ast
import autoflake

class GuardIfThen(TypedDict):
	"""Guard for Python versions."""
	test: ast.expr
	body: list[ast.stmt]

# NOTE These are Global identifiers used by multiple functions to simplify using the `_makeGuardVersion` function.
# If the separate functions converge enough, I can combine them into one function and remove this suboptimal system.
dictionaryGuardVersion: dict[int, GuardIfThen] = {}
ast_stmt: ast.stmt | None = None
guardVersion: int = 0
versionMinorMinimum: int = 0

def writeModule(astModule: ast.Module, moduleIdentifier: str) -> None:
	ast.fix_missing_locations(astModule)
	pythonSource: str = ast.unparse(astModule)
	if 'Make' in moduleIdentifier:

		# type ignore only works on hasDOTtype_comment, right?
		# TODO update docs

		listTypeIgnore: list[ast.TypeIgnore] = []
		lineno: int = 0
		for attribute, tag in [('keyword', '[reportInconsistentOverload]'), ('MatchClass', '[reportSelfClsParameterName]'), ('TypeAlias', '[reportInconsistentOverload]')]:
			for splitlinesNumber, line in enumerate(pythonSource.splitlines()):
				if 'def ' + attribute in line:
					# get the last occurrence of the match in the source code
					lineno = splitlinesNumber + 1
			listTypeIgnore.append(ast.TypeIgnore(lineno, tag))
		astModule = ast.parse(pythonSource)
		astModule.type_ignores.extend(listTypeIgnore)
		pythonSource = ast.unparse(astModule)
		pythonSource = pythonSource.replace('# type: ignore[', '# pyright: ignore[')
	autoflake_additional_imports: list[str] = ['astToolkit']
	pythonSource = autoflake.fix_code(pythonSource, autoflake_additional_imports, expand_star_imports=True, remove_all_unused_imports=True, remove_duplicate_keys = False, remove_unused_variables = False)
	pythonSource = isort_code(code=pythonSource, **settingsManufacturing.isort_code) # pyright: ignore[reportArgumentType]
	pathFilenameModule = PurePosixPath(settingsManufacturing.pathPackage, moduleIdentifier + settingsManufacturing.fileExtension)
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

def _makeGuardVersion() -> None:
	global ast_stmt, guardVersion, versionMinorMinimum
	orElse: ast.stmt | None = None
	if versionMinorMinimum >= settingsManufacturing.pythonMinimumVersionMinor:
		test: ast.Compare = Make.Compare(Make.Attribute(Make.Name('sys'), 'version_info'), ops=[ast.GtE()], comparators=[Make.Tuple([Make.Constant(3), Make.Constant(int(versionMinorMinimum))])])
		assert ast_stmt is not None, "Programming by brinkmanship!"
		body: list[ast.stmt] = [ast_stmt]
		dictionaryGuardVersion[versionMinorMinimum] = GuardIfThen(test=test, body=body)
	else:
		orElse = ast_stmt

	if guardVersion > 1:
		ast_stmt = None
	else:
		for test_body in [dictionaryGuardVersion[version] for version in sorted(dictionaryGuardVersion)]:
			orElse = Make.If(**test_body, orElse=[orElse] if orElse else [])
		assert orElse is not None, "Programming by brinkmanship!"
		ast_stmt = orElse
		dictionaryGuardVersion.clear()

def make_astTypes(**keywordArguments: Any) -> None:
	global ast_stmt, guardVersion, versionMinorMinimum
	list4ModuleBody: list[ast.stmt] = []
	ledgerOfImports = LedgerOfImports(
		Make.Module([
			Make.ImportFrom('types', [Make.alias('EllipsisType')])
			, Make.ImportFrom('typing', [Make.alias('Any'), Make.alias('TypeAlias', 'typing_TypeAlias'), Make.alias('TypedDict'), Make.alias('TypeVar', 'typing_TypeVar')])
			, Make.Import('ast')
			, Make.Import('sys')
		])
	)

	for identifierTypeAlias, list4TypeAlias_value, guardVersion, versionMinorMinimum in getElementsTypeAlias(**keywordArguments):
		astNameTypeAlias: ast.Name = Make.Name(identifierTypeAlias, ast.Store())
		TypeAlias_value: ast.expr = Make.BitOr.join(list4TypeAlias_value)
		ast_stmt = Make.AnnAssign(astNameTypeAlias, astName_typing_TypeAlias, value=TypeAlias_value)

		if guardVersion:
			_makeGuardVersion()
		if ast_stmt is not None: # pyright: ignore[reportUnnecessaryComparison]
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

def makeTool_dump() -> None:
	ingredientsFunction: IngredientsFunction = astModuleToIngredientsFunction(parseLogicalPath2astModule('ast'), 'dump')
	astConstant: ast.Constant = Make.Constant('ast.')
	findThis: Callable[[ast.AST], TypeIs[ast.MatchSingleton | ast.Constant | ast.Assign | ast.Attribute | ast.AugAssign | ast.Await | ast.DictComp | ast.Expr | ast.FormattedValue | ast.keyword | ast.MatchValue | ast.NamedExpr | ast.Starred | ast.Subscript | ast.TypeAlias | ast.YieldFrom | ast.AnnAssign | ast.Return | ast.Yield] | bool] = (
		ClassIsAndAttribute.valueIs(
		ast.Attribute, IfThis.isAttributeNamespaceIdentifier('node', '__class__'))) # pyright: ignore[reportArgumentType]
	def doThatPrepend(node: ast.Attribute) -> ast.AST:
		return Make.Add.join([astConstant, cast(ast.expr, node)])
	prepend_ast = NodeChanger(findThis, doThatPrepend)
	findThis = IfThis.isFunctionDefIdentifier('_format')
	def doThat(node: ast.FunctionDef) -> ast.AST:
		return prepend_ast.visit(node)
	NodeChanger(findThis, doThat).visit(ingredientsFunction.astFunctionDef)
	pathFilename = PurePosixPath(settingsManufacturing.pathPackage, '_dumpFunctionDef' + settingsManufacturing.fileExtension)
	write_astModule(IngredientsModule(ingredientsFunction), pathFilename, settingsManufacturing.identifierPackage)

def makeToolBe(identifierToolClass: str, **keywordArguments: Any) -> None:
	list4ClassDefBody: list[ast.stmt] = [docstrings[settingsManufacturing.identifiers[identifierToolClass]][settingsManufacturing.identifiers[identifierToolClass]]]

	for ClassDefIdentifier, versionMinorMinimum, classAs_astAttribute in getElementsBe(identifierToolClass, **keywordArguments):
		ast_stmt: ast.stmt = Make.FunctionDef(ClassDefIdentifier
			, argumentSpecification=Make.arguments(list_arg=[Make.arg('node', annotation=Make.Name('ast.AST'))])
			, body=[docstrings[identifierToolClass][ClassDefIdentifier], Make.Return(Make.Call(Make.Name('isinstance'), listParameters=[Make.Name('node'), classAs_astAttribute]))]
			, decorator_list=[astName_staticmethod]
			, returns=Make.Subscript(Make.Name('TypeIs'), slice=classAs_astAttribute))

		if versionMinorMinimum > settingsManufacturing.pythonMinimumVersionMinor:
			ast_stmt = Make.If(Make.Compare(Make.Attribute(Make.Name('sys'), 'version_info')
						, ops=[ast.GtE()]
						, comparators=[Make.Tuple([Make.Constant(3), Make.Constant(int(versionMinorMinimum))])])
					, body=[ast_stmt]
				)

		list4ClassDefBody.append(ast_stmt)

	list4ModuleBody: list[ast.stmt] = [
		Make.ImportFrom('typing_extensions', [Make.alias('TypeIs')])
		, Make.Import('ast')
		, Make.Import('sys')
	]

	writeClass(identifierToolClass, list4ClassDefBody, list4ModuleBody)

def makeToolClassIsAndAttribute(identifierToolClass: str, **keywordArguments: Any) -> None:
	global ast_stmt, guardVersion, versionMinorMinimum
	list4ClassDefBody: list[ast.stmt] = [docstrings[settingsManufacturing.identifiers[identifierToolClass]][settingsManufacturing.identifiers[identifierToolClass]]]

	for identifierTypeOfNode, overloadDefinition, canBeNone, attribute, list_ast_expr, guardVersion, versionMinorMinimum in getElementsClassIsAndAttribute(identifierToolClass, **keywordArguments):
		# Construct the parameters for `Make.FunctionDef`.
		astNameTypeOfNode: ast.Name = Make.Name(identifierTypeOfNode)
		decorator_list: list[ast.expr] = [astName_staticmethod]

		workhorse_returnsAnnotation: ast.expr = Make.BitOr.join([Make.Subscript(Make.Name('TypeIs'), slice=astNameTypeOfNode), Make.Name('bool')])

		if overloadDefinition:
			continue
			decorator_list.append(astName_overload)
			body: list[ast.stmt] = [Make.Expr(Make.Constant(value=...))]
		else:
			# Create the body of the function, which is a workhorse function.
			listAntecedentConditions: list[ast.expr] = [Make.Call(Make.Name('isinstance'), listParameters=[Make.Name('node'), Make.Name('astClass')])]

			if canBeNone:
				ops: list[ast.cmpop]= [ast.IsNot()]
				comparators: list[ast.expr]=[Make.Constant(None)]
				if canBeNone == 'list':
					ops: list[ast.cmpop]= [ast.NotEq()]
					comparators: list[ast.expr]=[Make.List([Make.Constant(None)])]
				listAntecedentConditions.append(Make.Compare(Make.Attribute(Make.Name('node'), attribute), ops=ops, comparators=comparators))

			listAntecedentConditions.append(Make.Call(Make.Name('attributeCondition'), listParameters=[Make.Attribute(Make.Name('node'), attribute)]))

			body = [
				Make.FunctionDef('workhorse'
					, argumentSpecification=Make.arguments(list_arg=[Make.arg('node', annotation=Make.Attribute(Make.Name('ast'), 'AST'))])
					, body=[Make.Return(Make.And.join(listAntecedentConditions))]
					, returns=workhorse_returnsAnnotation)
				, Make.Return(Make.Name('workhorse'))
			]

		returns: ast.expr = Make.Subscript(Make.Name('Callable'), slice=Make.Tuple([Make.List([Make.Attribute(Make.Name('ast'), 'AST')]), workhorse_returnsAnnotation]))

		annotation: ast.expr = (Make.Subscript(Make.Name('Callable'), Make.Tuple([Make.List([Make.BitOr.join(list_ast_expr)]), Make.Name('bool')])))

		# Create the overload or implementation of the function.
		ast_stmt = Make.FunctionDef(attribute + 'Is'
				, argumentSpecification=Make.arguments(list_arg=[
					Make.arg('astClass', annotation=Make.Subscript(Make.Name('type'), astNameTypeOfNode)),
					Make.arg('attributeCondition', annotation=annotation)
				])
				, body=body
				, decorator_list=decorator_list
				, returns=returns
			)

		if guardVersion:
			_makeGuardVersion()
		if ast_stmt is not None: # pyright: ignore[reportUnnecessaryComparison]
			list4ClassDefBody.append(ast_stmt)

	list4ModuleBody: list[ast.stmt] = [
		Make.ImportFrom('astToolkit', [Make.alias('*')])
		, Make.ImportFrom('collections.abc', [Make.alias('Callable'), Make.alias('Sequence')])
		, Make.ImportFrom('typing', [Make.alias(identifier) for identifier in ['overload']])
		, Make.ImportFrom('typing_extensions', [Make.alias(identifier) for identifier in ['TypeIs']])
		, Make.Import('ast')
		, Make.Import('sys')
		, Make.If(Make.Compare(Make.Attribute(Make.Name('sys'), 'version_info'), [Make.GtE()], [Make.Tuple([Make.Constant(3), Make.Constant(13)])]),
			[Make.ImportFrom('astToolkit', [Make.alias('hasDOTdefault_value', 'hasDOTdefault_value')])]
		)
	]

	writeClass(identifierToolClass, list4ClassDefBody, list4ModuleBody)

def makeToolDOT(identifierToolClass: str, **keywordArguments: Any) -> None:
	global ast_stmt, guardVersion, versionMinorMinimum
	list4ClassDefBody: list[ast.stmt] = [docstrings[settingsManufacturing.identifiers[identifierToolClass]][settingsManufacturing.identifiers[identifierToolClass]]]

	for identifierTypeOfNode, overloadDefinition, _canBeNone, attribute, list_ast_expr, guardVersion, versionMinorMinimum in getElementsDOT(identifierToolClass, **keywordArguments):
		astNameTypeOfNode: ast.Name = Make.Name(identifierTypeOfNode)

		decorator_list: list[ast.expr] = [astName_staticmethod]
		if overloadDefinition:
			decorator_list.append(astName_overload)
			body: list[ast.stmt] = [Make.Expr(Make.Constant(value=...))]
		else:
			body = [Make.Return(Make.Attribute(Make.Name('node'), attribute))]

		returns: ast.expr = Make.BitOr.join(list_ast_expr)

		ast_stmt = Make.FunctionDef(attribute
			, argumentSpecification=Make.arguments(list_arg=[Make.arg('node', annotation=astNameTypeOfNode)])
			, body=body
			, decorator_list=decorator_list
			, returns=returns
		)

		if guardVersion:
			_makeGuardVersion()
		if ast_stmt is not None: # pyright: ignore[reportUnnecessaryComparison]
			list4ClassDefBody.append(ast_stmt)

	list4ModuleBody: list[ast.stmt] = [
		Make.ImportFrom('astToolkit', [Make.alias('*')])
		, Make.ImportFrom('collections.abc', [Make.alias('Sequence')])
		, Make.ImportFrom('typing', [Make.alias('overload')])
		, Make.Import('ast')
		, Make.Import('sys')
		, Make.If(Make.Compare(Make.Attribute(Make.Name('sys'), 'version_info'), [Make.GtE()], [Make.Tuple([Make.Constant(3), Make.Constant(13)])]),
			[Make.ImportFrom('astToolkit', [Make.alias('hasDOTdefault_value', 'hasDOTdefault_value')])]
		)
	]

	writeClass(identifierToolClass, list4ClassDefBody, list4ModuleBody)

def makeToolGrab(identifierToolClass: str, **keywordArguments: Any) -> None:
	global ast_stmt, guardVersion, versionMinorMinimum
	list4ClassDefBody: list[ast.stmt] = [docstrings[settingsManufacturing.identifiers[identifierToolClass]][settingsManufacturing.identifiers[identifierToolClass]], FunctionDefGrab_andDoAllOf]

	for identifierTypeOfNode, list_ast_expr, attribute, guardVersion, versionMinorMinimum in getElementsGrab(identifierToolClass, **keywordArguments):
		astNameTypeOfNode: ast.Name = Make.Name(identifierTypeOfNode)

		annotation: ast.expr = (Make.BitOr.join([Make.Subscript(Make.Name('Callable'), Make.Tuple([Make.List([ast_expr]), ast_expr])) for ast_expr in list_ast_expr]))

		ast_stmt = Make.FunctionDef(attribute + 'Attribute'
			, argumentSpecification=Make.arguments(list_arg=[Make.arg('action', annotation=annotation)])
			, body=[Make.FunctionDef('workhorse'
						, argumentSpecification=Make.arguments(list_arg=[Make.arg('node', annotation=astNameTypeOfNode)])
						, body=[Make.Expr(
								Make.Call(Make.Name('setattr'), listParameters=[Make.Name('node'), Make.Constant(f"{attribute}")
									, Make.Call(Make.Name('action')
										, listParameters=[Make.Call(Make.Name('getattr'), listParameters=[Make.Name('node'), Make.Constant(f"{attribute}")])])
										]
									)
								)
							, Make.Return(Make.Name('node'))
						]
						, returns=astNameTypeOfNode)
					, Make.Return(Make.Name('workhorse'))
				]
			, decorator_list=[astName_staticmethod]
			, returns=Make.Subscript(Make.Name('Callable'), Make.Tuple([Make.List([astNameTypeOfNode]), astNameTypeOfNode])))

		if guardVersion:
			_makeGuardVersion()
		if ast_stmt is not None: # pyright: ignore[reportUnnecessaryComparison]
			list4ClassDefBody.append(ast_stmt)

	list4ModuleBody: list[ast.stmt] = [
		Make.ImportFrom('astToolkit', [Make.alias('*')])
		, Make.ImportFrom('collections.abc', [Make.alias('Callable'), Make.alias('Sequence')])
		, Make.ImportFrom('typing', [Make.alias('Any')])
		, Make.Import('ast')
		, Make.Import('sys')
		, Make.If(Make.Compare(Make.Attribute(Make.Name('sys'), 'version_info'), [Make.GtE()], [Make.Tuple([Make.Constant(3), Make.Constant(13)])]),
			[Make.ImportFrom('astToolkit', [Make.alias('hasDOTdefault_value', 'hasDOTdefault_value')])]
		)
	]

	writeClass(identifierToolClass, list4ClassDefBody, list4ModuleBody)

def makeToolMake(identifierToolClass: str, **keywordArguments: Any) -> None:
	global ast_stmt, guardVersion, versionMinorMinimum
	ledgerOfImports: LedgerOfImports = LedgerOfImports()
	ledgerOfImports.addImportFrom_asStr('astToolkit', 'ConstantValueType')
	list4ClassDefBody: list[ast.stmt] = [docstrings[identifierToolClass][identifierToolClass]]

	ledgerOfImports.addImportFrom_asStr('astToolkit', 'ast_attributes')
	list4ClassDefBody.extend([
		FunctionDef_boolopJoinMethod
		, FunctionDef_operatorJoinMethod
		])

	listBoolOpIdentifiers: list[str] = sorted([subclass.__name__ for subclass in ast.boolop.__subclasses__()])
	listOperatorIdentifiers: list[str] = sorted([subclass.__name__ for subclass in ast.operator.__subclasses__()])

	# The order of the tuple elements is the order in which they are used in the flow of the code.
	for ClassDefIdentifier, listFunctionDef_args, kwarg_annotationIdentifier, defaults, classAs_astAttribute, overloadDefinition, listCall_keyword, guardVersion, versionMinorMinimum in getElementsMake(identifierToolClass, **keywordArguments):
		# Bypass the manufacture of the tool by using a prefabricated tool from the annex.
		if ClassDefIdentifier in listBoolOpIdentifiers:
			list4ClassDefBody.append(Make.ClassDef(ClassDefIdentifier
				, bases=[Make.Attribute(Make.Name('ast'), ClassDefIdentifier)]
				, body=[docstrings[identifierToolClass][ClassDefIdentifier], FunctionDef_join_boolop]
			))
			continue
		elif ClassDefIdentifier in listOperatorIdentifiers:
			list4ClassDefBody.append(Make.ClassDef(ClassDefIdentifier
				, bases=[Make.Attribute(Make.Name('ast'), ClassDefIdentifier)]
				, body=[docstrings[identifierToolClass][ClassDefIdentifier], FunctionDef_join_operator]
			))
			continue
		elif ClassDefIdentifier == 'Attribute':
			list4ClassDefBody.append(FunctionDefMake_Attribute)
			continue
		elif ClassDefIdentifier == 'Import':
			list4ClassDefBody.append(FunctionDefMake_Import)
			ledgerOfImports.addImportFrom_asStr('astToolkit', 'identifierDotAttribute')
			continue
		# Add prefabricated overloads for a method.
		elif ClassDefIdentifier == 'TypeAlias':
			list4ClassDefBody.extend(listOverloadsTypeAlias)
			ledgerOfImports.addImportFrom_asStr('typing', 'overload')
		elif ClassDefIdentifier == 'keyword':
			list4ClassDefBody.extend(listOverloads_keyword)
			ledgerOfImports.addImportFrom_asStr('typing', 'overload')

		kwarg: ast.arg | None = None
		if kwarg_annotationIdentifier != 'No':
			ledgerOfImports.addImportFrom_asStr('astToolkit', kwarg_annotationIdentifier)
			kwarg = Make.arg(settingsManufacturing.keywordArgumentsIdentifier, annotation=Make.Subscript(Make.Name('Unpack'), slice=Make.Name(kwarg_annotationIdentifier)))
		decorator_list: list[ast.expr] = [astName_staticmethod]

		# For the first refactoring, _all_ `overloadDefinition` are `False` because overload is handled above.
		if overloadDefinition:
			decorator_list.append(astName_overload)
			body: list[ast.stmt] = [Make.Expr(Make.Constant(value=...))]
		else:
			if kwarg is not None:
				listCall_keyword.append(keywordKeywordArguments4Call)

			body = [docstrings[identifierToolClass][ClassDefIdentifier]
					, Make.Return(Make.Call(classAs_astAttribute, list_keyword=listCall_keyword))
				]

		ast_stmt = Make.FunctionDef(
			ClassDefIdentifier
			, argumentSpecification=Make.arguments(list_arg=listFunctionDef_args, kwarg=kwarg, defaults=defaults)
			, body=body
			, decorator_list=decorator_list
			, returns=classAs_astAttribute)

		if guardVersion:
			_makeGuardVersion()
		if ast_stmt is not None: # pyright: ignore[reportUnnecessaryComparison]
			list4ClassDefBody.append(ast_stmt)

	# Module-level operations ===============
	ledgerOfImports.walkThis(Make.Module([
		Make.ImportFrom('collections.abc', [Make.alias('Iterable'), Make.alias('Sequence')])
		, Make.ImportFrom('typing', [Make.alias('Any')])
		, Make.ImportFrom('typing_extensions', [Make.alias('Unpack')])
		, Make.Import('ast')
		, Make.Import('sys')
		]
	))
	list4ModuleBody: list[ast.stmt] = [*ledgerOfImports.makeList_ast()]
	writeClass(identifierToolClass, list4ClassDefBody, list4ModuleBody)

def write_theSSOT():
	writeModule(astModule_theSSOT, '_theSSOT')

def manufactureTools(settingsManufacturing: ManufacturedPackageSettings):
	"""Reminder: `_makeGuardVersion` relies on global identifiers, so don't use concurrency."""
	make_astTypes()
	makeToolBe(settingsManufacturing.identifiers['Be'])
	makeToolClassIsAndAttribute(settingsManufacturing.identifiers['ClassIsAndAttribute'])
	makeToolDOT(settingsManufacturing.identifiers['DOT'])
	makeToolGrab(settingsManufacturing.identifiers['Grab'])
	makeToolMake(settingsManufacturing.identifiers['Make'])
	makeTool_dump()
	write_theSSOT()

if __name__ == "__main__":
	manufactureTools(settingsManufacturing)
