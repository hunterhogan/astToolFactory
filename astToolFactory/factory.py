from astToolFactory import (
	astName_overload, astName_staticmethod, astName_typing_TypeAlias, dictionaryIdentifiers,
	getElementsBe, getElementsClassIsAndAttribute, getElementsDOT, getElementsGrab, getElementsMake,
	getElementsTypeAlias, keywordArgumentsIdentifier, keywordKeywordArguments4Call, listPylanceErrors,
	pythonMinimumVersionMinor, settingsPackageToManufacture,
)
from astToolFactory.datacenter import DictionaryToolBe
from astToolFactory.documentation import docstrings, docstringWarning
from astToolFactory.factory_annex import (
	astModule_theSSOT, FunctionDef_boolopJoinMethod, FunctionDef_join_boolop,
	FunctionDef_join_operator, FunctionDef_operatorJoinMethod, FunctionDefGrab_andDoAllOf,
	FunctionDefMake_Attribute, FunctionDefMake_Import, listHandmade_astTypes, listOverloads_keyword,
	listOverloadsTypeAlias,
)
from astToolkit import (
	astModuleToIngredientsFunction, ClassIsAndAttribute, IfThis, IngredientsFunction,
	IngredientsModule, LedgerOfImports, Make, NodeChanger, parseLogicalPath2astModule,
)
from astToolkit.transformationTools import write_astModule
from isort import code as isort_code
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
	if '_astTypes' in moduleIdentifier:
		pythonSource = "# pyright: reportMatchNotExhaustive=false\n" + pythonSource
	if 'ClassIsAndAttribute' in moduleIdentifier:
		pythonSource = "# pyright: reportArgumentType=false\n" + pythonSource
		pythonSource = "# pyright: reportMatchNotExhaustive=false\n" + pythonSource
	if 'DOT' in moduleIdentifier:
		pythonSource = "# pyright: reportMatchNotExhaustive=false\n" + pythonSource
		pythonSource = "# pyright: reportReturnType=false\n" + pythonSource
	if 'Grab' in moduleIdentifier:
		listTypeIgnore: list[ast.TypeIgnore] = []
		tag = '[reportArgumentType, reportAttributeAccessIssue]'
		for attribute in listPylanceErrors:
			for splitlinesNumber, line in enumerate(pythonSource.splitlines()):
				if 'node.'+attribute in line:
					listTypeIgnore.append(ast.TypeIgnore(splitlinesNumber+1, tag))
					# get the first occurrence of the match in the source code
					break
		astModule = ast.parse(pythonSource)
		astModule.type_ignores.extend(listTypeIgnore)
		pythonSource = ast.unparse(astModule)
		pythonSource = pythonSource.replace('# type: ignore[', '# pyright: ignore[')
		pythonSource = "# pyright: reportMatchNotExhaustive=false\n" + pythonSource
	if 'Make' in moduleIdentifier:
		listTypeIgnore: list[ast.TypeIgnore] = []
		lineno: int = 0
		for attribute, tag in [('keyword', '[reportInconsistentOverload]'), ('MatchClass', '[reportSelfClsParameterName]'), ('TypeAlias', '[reportInconsistentOverload]')]:
			for splitlinesNumber, line in enumerate(pythonSource.splitlines()):
				if 'def ' + attribute in line:
					# get the last occurrence of the match in the source code
					lineno = splitlinesNumber + 1
			listTypeIgnore.append(ast.TypeIgnore(lineno, tag))
		tag = '[reportRedeclaration]'
		for attribute in ['ParamSpec', 'TypeVar', 'TypeVarTuple']:
			for splitlinesNumber, line in enumerate(pythonSource.splitlines()):
				if 'def ' + attribute in line:
					listTypeIgnore.append(ast.TypeIgnore(splitlinesNumber+1, tag))
					# get the first occurrence of the match in the source code
					break
		astModule = ast.parse(pythonSource)
		astModule.type_ignores.extend(listTypeIgnore)
		pythonSource = ast.unparse(astModule)
		pythonSource = pythonSource.replace('# type: ignore[', '# pyright: ignore[')
	autoflake_additional_imports: list[str] = ['astToolkit']
	pythonSource = autoflake.fix_code(pythonSource, autoflake_additional_imports, expand_star_imports=True, remove_all_unused_imports=True, remove_duplicate_keys = False, remove_unused_variables = False)
	pythonSource = isort_code(pythonSource, **settingsPackageToManufacture.isort_codeConfiguration) # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue, reportUnknownArgumentType]
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
	for identifierTypeAlias, list4TypeAlias_value, useMatchCase, versionMinorMinimum in getElementsTypeAlias():
		astNameTypeAlias: ast.Name = Make.Name(identifierTypeAlias, ast.Store())
		TypeAlias_value: ast.expr = Make.BitOr.join([eval(classAs_astAttribute) for classAs_astAttribute in list4TypeAlias_value])
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

def makeTool_dump() -> None:
	ingredientsFunction: IngredientsFunction = astModuleToIngredientsFunction(parseLogicalPath2astModule('ast'), 'dump')
	astConstant: ast.Constant = Make.Constant('ast.')
	findThis = ClassIsAndAttribute.valueIs(ast.Attribute, IfThis.isAttributeNamespaceIdentifier('node', '__class__'))
	def doThatPrepend(node: ast.Attribute) -> ast.AST:
		return Make.Add.join([astConstant, cast(ast.expr, node)])
	prepend_ast = NodeChanger(findThis, doThatPrepend)
	findThis = IfThis.isFunctionDefIdentifier('_format')
	def doThat(node: ast.FunctionDef) -> ast.AST:
		return prepend_ast.visit(node)
	NodeChanger(findThis, doThat).visit(ingredientsFunction.astFunctionDef)
	pathFilename = PurePosixPath(settingsPackageToManufacture.pathPackage, '_dumpFunctionDef' + settingsPackageToManufacture.fileExtension)
	write_astModule(IngredientsModule(ingredientsFunction), pathFilename, settingsPackageToManufacture.identifierPackage)

def makeToolBe(identifierToolClass: str) -> None:
	list4ClassDefBody: list[ast.stmt] = [docstrings[dictionaryIdentifiers['Be']][dictionaryIdentifiers['Be']]]

	listDictionaryToolElements: list[DictionaryToolBe] = getElementsBe()

	for dictionaryToolElements in listDictionaryToolElements:
		ClassDefIdentifier: str = dictionaryToolElements['ClassDefIdentifier']
		classAs_astAttribute: ast.expr = eval(dictionaryToolElements['classAs_astAttribute'])
		versionMinorMinimumClass: int = dictionaryToolElements['versionMinorMinimumClass']

		ast_stmt: ast.stmt = Make.FunctionDef(ClassDefIdentifier
			, argumentSpecification=Make.arguments(list_arg=[Make.arg('node', annotation=Make.Name('ast.AST'))])
			, body=[Make.Return(Make.Call(Make.Name('isinstance'), listParameters=[Make.Name('node'), classAs_astAttribute]))]
			, decorator_list=[astName_staticmethod]
			, returns=Make.Subscript(Make.Name('TypeIs'), slice=classAs_astAttribute))

		if versionMinorMinimumClass > pythonMinimumVersionMinor:
			ast_stmt = Make.If(Make.Compare(Make.Attribute(Make.Name('sys'), 'version_info')
						, ops=[ast.GtE()]
						, comparators=[Make.Tuple([Make.Constant(3), Make.Constant(versionMinorMinimumClass)])])
					, body=[ast_stmt]
				)

		list4ClassDefBody.append(ast_stmt)

	list4ModuleBody: list[ast.stmt] = [
		Make.ImportFrom('typing_extensions', [Make.alias('TypeIs')])
		, Make.Import('ast')
		, Make.Import('sys')
	]

	writeClass(identifierToolClass, list4ClassDefBody, list4ModuleBody)

def makeToolClassIsAndAttribute(identifierToolClass: str) -> None:
	list4ClassDefBody: list[ast.stmt] = [docstrings[dictionaryIdentifiers['ClassIsAndAttribute']][dictionaryIdentifiers['ClassIsAndAttribute']]]
	list_match_case: list[ast.match_case] = []

	for identifierTypeOfNode, overloadDefinition, canBeNone, attribute, list_ast_expr, useMatchCase, versionMinorMinimum in getElementsClassIsAndAttribute():
		# Construct the parameters for `Make.FunctionDef`.
		astNameTypeOfNode: ast.Name = Make.Name(identifierTypeOfNode)
		decorator_list: list[ast.expr] = [astName_staticmethod]

		workhorse_returnsAnnotation: ast.expr = Make.BitOr.join([Make.Subscript(Make.Name('TypeIs'), slice=astNameTypeOfNode), Make.Name('bool')])

		if overloadDefinition:
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

		annotation: ast.expr = (Make.BitOr.join([Make.Subscript(Make.Name('Callable'), Make.Tuple([Make.List([eval(ast_expr)]), Make.Name('bool')])) for ast_expr in list_ast_expr]))

		# Create the overload or implementation of the function.
		ast_stmt: ast.stmt = Make.FunctionDef(attribute + 'Is'
				, argumentSpecification=Make.arguments(list_arg=[
					Make.arg('astClass', annotation=Make.Subscript(Make.Name('type'), astNameTypeOfNode)),
					Make.arg('attributeCondition', annotation=annotation)
				])
				, body=body
				, decorator_list=decorator_list
				, returns=returns
			)

		# If the function might not be available in the minimum "supported" version of Python, guard it with a match-case.
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

def makeToolDOT(identifierToolClass: str) -> None:
	list4ClassDefBody: list[ast.stmt] = [docstrings[dictionaryIdentifiers['DOT']][dictionaryIdentifiers['DOT']]]
	list_match_case: list[ast.match_case] = []

	for identifierTypeOfNode, overloadDefinition, _canBeNone, attribute, list_ast_expr, useMatchCase, versionMinorMinimum in getElementsDOT():
		astNameTypeOfNode: ast.Name = Make.Name(identifierTypeOfNode)

		decorator_list: list[ast.expr] = [astName_staticmethod]
		if overloadDefinition:
			decorator_list.append(astName_overload)
			body: list[ast.stmt] = [Make.Expr(Make.Constant(value=...))]
		else:
			body = [Make.Return(Make.Attribute(Make.Name('node'), attribute))]

		returns: ast.expr = Make.BitOr.join([eval(ast_expr) for ast_expr in list_ast_expr])

		ast_stmt: ast.stmt = Make.FunctionDef(attribute
			, argumentSpecification=Make.arguments(list_arg=[Make.arg('node', annotation=astNameTypeOfNode)])
			, body=body
			, decorator_list=decorator_list
			, returns=returns
		)

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

def makeToolGrab(identifierToolClass: str) -> None:
	list4ClassDefBody: list[ast.stmt] = [docstrings[dictionaryIdentifiers['Grab']][dictionaryIdentifiers['Grab']], FunctionDefGrab_andDoAllOf]
	list_match_case: list[ast.match_case] = []

	for identifierTypeOfNode, list_ast_expr, attribute, useMatchCase, versionMinorMinimum in getElementsGrab():
		astNameTypeOfNode: ast.Name = Make.Name(identifierTypeOfNode)

		annotation: ast.expr = (Make.BitOr.join([Make.Subscript(Make.Name('Callable'), Make.Tuple([Make.List([eval(ast_expr)]), eval(ast_expr)])) for ast_expr in list_ast_expr]))

		ast_stmt: ast.stmt = Make.FunctionDef(attribute + 'Attribute'
			, argumentSpecification=Make.arguments(list_arg=[Make.arg('action', annotation=annotation)])
			, body=[Make.FunctionDef('workhorse'
						, argumentSpecification=Make.arguments(list_arg=[Make.arg('node', annotation=astNameTypeOfNode)])
						, body=[Make.Assign([Make.Attribute(Make.Name('node'), attribute, context=ast.Store())], value=Make.Call(Make.Name('action'), [Make.Attribute(Make.Name('node'), attribute)]))
								, Make.Return(Make.Name('node'))
						]
						, returns=astNameTypeOfNode)
					, Make.Return(Make.Name('workhorse'))
				]
			, decorator_list=[astName_staticmethod]
			, returns=Make.Subscript(Make.Name('Callable'), Make.Tuple([Make.List([astNameTypeOfNode]), astNameTypeOfNode])))

		if useMatchCase:
			# Create a guard or a catch-all match-case and append to list_match_case.
			if versionMinorMinimum >= pythonMinimumVersionMinor:
				pattern: ast.MatchAs = Make.MatchAs(name = 'version')
				guard: ast.Compare | None = Make.Compare(Make.Name('version'), ops=[ast.GtE()], comparators=[Make.Tuple([Make.Constant(3), Make.Constant(int(versionMinorMinimum))])])
			else:
				pattern = Make.MatchAs()
				guard = None
			list_match_case.append(Make.match_case(pattern, guard, body = [ast_stmt]))

			# If there are more match-case in the queue, then wait to create ast.Match.
			if useMatchCase > 1:
				continue
			else:
				ast_stmt = Make.Match(Make.Attribute(Make.Name('sys'), 'version_info'), cases=list_match_case)
				list_match_case.clear()

		list4ClassDefBody.append(ast_stmt)

	list4ModuleBody: list[ast.stmt] = [
		Make.ImportFrom('astToolkit', [Make.alias('*')])
		, Make.ImportFrom('collections.abc', [Make.alias('Callable'), Make.alias('Sequence')])
		, Make.ImportFrom('typing', [Make.alias('Any'), Make.alias('Literal')])
		, Make.Import('ast')
		, Make.Import('sys')
		, Make.If(Make.Compare(Make.Attribute(Make.Name('sys'), 'version_info'), [Make.GtE()], [Make.Tuple([Make.Constant(3), Make.Constant(13)])]),
			[Make.ImportFrom('astToolkit', [Make.alias('hasDOTdefault_value', 'hasDOTdefault_value')])]
		)
	]

	writeClass(identifierToolClass, list4ClassDefBody, list4ModuleBody)

def makeToolMake(identifierToolClass: str) -> None:
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

	list_match_case: list[ast.match_case] = []
	# The order of the tuple elements is the order in which they are used in the flow of the code.
	for ClassDefIdentifier, listStr4FunctionDef_args, kwarg_annotationIdentifier, listDefaults, classAs_astAttributeAsStr, overloadDefinition, listTupleCall_keywords, useMatchCase, versionMinorMinimum in getElementsMake():
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

		listFunctionDef_args: list[ast.arg] = [cast(ast.arg, eval(ast_argAsStr)) for ast_argAsStr in listStr4FunctionDef_args]
		kwarg: ast.arg | None = None
		if kwarg_annotationIdentifier != 'No':
			ledgerOfImports.addImportFrom_asStr('astToolkit', kwarg_annotationIdentifier)
			kwarg = Make.arg(keywordArgumentsIdentifier, annotation=Make.Subscript(Make.Name('Unpack'), slice=Make.Name(kwarg_annotationIdentifier)))
		defaults: list[ast.expr] = [cast(ast.expr, eval(defaultAsStr)) for defaultAsStr in listDefaults]
		decorator_list: list[ast.expr] = [astName_staticmethod]
		classAs_astAttribute: ast.expr = eval(classAs_astAttributeAsStr)

		# For the first refactoring, _all_ `overloadDefinition` are `False` because overload is handled above.
		if overloadDefinition:
			decorator_list.append(astName_overload)
			body: list[ast.stmt] = [Make.Expr(Make.Constant(value=...))]
		else:
			listCall_keyword: list[ast.keyword] = []
			for tupleCall_keywords in listTupleCall_keywords:
				argIdentifier, keywordValue = tupleCall_keywords
				# If there are not call keywords
				if keywordValue == 'No':
					break
				listCall_keyword.append(Make.keyword(argIdentifier, value=eval(keywordValue)))
			if kwarg is not None:
				listCall_keyword.append(keywordKeywordArguments4Call)

			body = [docstrings[identifierToolClass][ClassDefIdentifier],
				Make.Return(Make.Call(classAs_astAttribute, list_keyword=listCall_keyword))
				]

		ast_stmt = Make.FunctionDef(
			ClassDefIdentifier
			, argumentSpecification=Make.arguments(list_arg=listFunctionDef_args, kwarg=kwarg, defaults=defaults)
			, body=body
			, decorator_list=decorator_list
			, returns=classAs_astAttribute)

		# If there are multiple versions, create a match-case for this version.
		if useMatchCase:
			# Create a guard or a catch-all match-case and append to list_match_case.
			if versionMinorMinimum >= pythonMinimumVersionMinor:
				pattern: ast.MatchAs = Make.MatchAs(name = 'version')
				guard: ast.Compare | None = Make.Compare(Make.Name('version'), ops=[ast.GtE()], comparators=[Make.Tuple([Make.Constant(3), Make.Constant(int(versionMinorMinimum))])])
			else:
				pattern = Make.MatchAs()
				guard = None
			list_match_case.append(Make.match_case(pattern, guard, body = [ast_stmt]))

			# If there are more match-case in the queue, then wait to create ast.Match.
			if useMatchCase > 1:
				continue
			else:
				ast_stmt = Make.Match(Make.Attribute(Make.Name('sys'), 'version_info'), cases=list_match_case)
				list_match_case.clear()

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

if __name__ == "__main__":
	make_astTypes()
	makeToolBe(dictionaryIdentifiers['Be'])
	makeToolClassIsAndAttribute(dictionaryIdentifiers['ClassIsAndAttribute'])
	makeToolDOT(dictionaryIdentifiers['DOT'])
	makeToolGrab(dictionaryIdentifiers['Grab'])
	makeToolMake(dictionaryIdentifiers['Make'])
	# makeTool_dump()
	write_theSSOT()
