"""Module for manufacturing and writing ast tools and modules."""
from __future__ import annotations

from astToolFactory import (
	astASTastAttribute, astAttribute_builtins_str, astName_overload, astName_staticmethod, GuardIfThen, keywordKeywordArguments4Call,
	ManufacturedPackageSettings, settingsManufacturing)
from astToolFactory._documentationAnnex.Be import makeDocstringBe
from astToolFactory._documentationAnnex.Grab import makeDocstringGrab
from astToolFactory.datacenter import (
	getAttributesBe, getElementsBe, getElementsDOT, getElementsGrab, getElementsMake, getElementsTypeAlias, getFieldTypesGrab)
from astToolFactory.documentation import docstrings, docstringWarning
from astToolFactory.factoryAnnex import (
	astModule_theSSOT, FunctionDef_boolopJoinMethod, FunctionDef_join_boolop, FunctionDef_join_operator, FunctionDef_operatorJoinMethod,
	FunctionDefBe_at, FunctionDefGrab_andDoAllOf, FunctionDefGrab_index, ignoreAbstractClassWarning, keywordMake_Import_names,
	list_argMake_Import, listHandmade_astTypes, listOverloads_keyword)
from astToolFactory.filesystem import writeModule
from astToolkit import Be, DOT, Grab, IfThis, Make, NodeChanger, NodeTourist, Then
from astToolkit.changeDef import extractFunctionDef
from astToolkit.filesystem import parseLogicalPath2astModule, parsePathFilename2astModule, write_astModule
from astToolkit.ohWow import unjoinBinOP
from hunterMakesPy import raiseIfNone
from typing import TYPE_CHECKING
import ast
import typeshed_client

if TYPE_CHECKING:
	from collections.abc import Sequence
	from typing import Any

# NOTE These are Global identifiers used by multiple functions to simplify using the `_makeGuardVersion` function.
# If the separate functions converge enough, I can combine them into one function and remove this suboptimal system.
dictionaryGuardVersion: dict[int, GuardIfThen] = {}
ast_stmt: ast.stmt | None = None
guardVersion: int = 0
versionMinorMinimum: int = 0
# END global identifiers
"""makeTool*
list4ClassDefBody
for customTuple in getElements*
	ast_stmt
	dictionaryGuardVersion
list4ModuleBody
writeClass

What if getElements* always returned the same dataclass with the same attributes, but not all attributes were populated?
Then, I could pass the dataclass around more easily.
"""

def _makeNestedGuardVersions() -> None:
	"""Construct version guard."""
	global ast_stmt, guardVersion, versionMinorMinimum  # ruff:ignore[global-variable-not-assigned, global-statement]
	orElse: ast.stmt | None = None
	if versionMinorMinimum >= settingsManufacturing.pythonMinimumVersionMinor:
		test: ast.Compare = Make.Compare(
			Make.Attribute(Make.Name("sys"), "version_info"),
			ops=[Make.GtE()],
			comparators=[Make.Tuple([Make.Constant(3), Make.Constant(int(versionMinorMinimum))])],
		)
		body: list[ast.stmt] = [raiseIfNone(ast_stmt)]
		dictionaryGuardVersion[versionMinorMinimum] = GuardIfThen(test=test, body=body)
	else:
		orElse = ast_stmt

	if guardVersion > 1:
		ast_stmt = None
	else:
		for test_body in [dictionaryGuardVersion[version] for version in sorted(dictionaryGuardVersion)]:
			orElse = Make.If(**test_body, orElse=[orElse] if orElse else [])
		ast_stmt = raiseIfNone(orElse)
		dictionaryGuardVersion.clear()

def _makeSimpleGuardVersion(list_ast_stmt: Sequence[ast.stmt], versionMinorMinimum: int) -> ast.stmt:
	return Make.If(Make.Compare(Make.Attribute(Make.Name("sys"), "version_info"), ops=[Make.GtE()]
			, comparators=[Make.Tuple([Make.Constant(3), Make.Constant(int(versionMinorMinimum))])])
		, body=list_ast_stmt)

def make_astTypes(identifierModule: str, **keywordArguments: Any) -> None:
	"""Generate and write the `ast` types module.

	Parameters
	----------
	identifierModule : str
		The logical identifier of the `ast` types module.
	**keywordArguments : Any
		Override `ManufacturedPackageSettings`.
	"""
	global ast_stmt, guardVersion, versionMinorMinimum  # ruff:ignore[global-statement]
	astModuleStub: ast.Module = parsePathFilename2astModule(raiseIfNone(typeshed_client.get_stub_file('ast'
		, search_context=typeshed_client.get_search_context(typeshed=settingsManufacturing.pathRoot_typeshed))))
	ast_expr: ast.expr = raiseIfNone(NodeTourist(
		Be.AnnAssign.targetIs(IfThis.isNameIdentifier('_ConstantValue')), DOT.value
	).captureLastMatch(astModuleStub))
	list4ModuleBody: list[ast.stmt] = []
	list4ModuleImports: list[ast.stmt] = [
		Make.ImportFrom('__future__', [Make.alias('annotations')])
		, Make.ImportFrom("types", [Make.alias("EllipsisType")])
		, Make.ImportFrom("typing", [Make.alias("Any"), Make.alias("TypeAlias", "typing_TypeAlias"), Make.alias("TypedDict"), Make.alias("TypeVar", "typing_TypeVar")])
		, Make.Import("ast")
		, Make.Import("sys")
	]

	for identifierTypeAlias, list4TypeAlias_value, guardVersion, versionMinorMinimum in getElementsTypeAlias(**keywordArguments):  # ruff:ignore[unused-loop-control-variable]
		ast_stmt = Make.TypeAlias(Make.Name(identifierTypeAlias, Make.Store()), type_params=[], value=Make.BitOr.join(list4TypeAlias_value))

		if guardVersion:
			_makeNestedGuardVersions()
		if ast_stmt is not None:  # pyright: ignore[reportUnnecessaryComparison]
			list4ModuleBody.append(ast_stmt)

	astModule: ast.Module = Make.Module([
		docstringWarning
		, *list4ModuleImports
		, Make.TypeAlias(Make.Name('ast_ConstantValue', Make.Store()), type_params=[], value=ast_expr)
		, *listHandmade_astTypes
		, *list4ModuleBody])

	writeModule(astModule, identifierModule)

def makeToolBe(identifierToolClass: str, **keywordArguments: Any) -> None:
	"""Generate and write `class` `Be`."""
	list4ClassDefBody: list[ast.stmt] = [docstrings[settingsManufacturing.identifiers[identifierToolClass]][settingsManufacturing.identifiers[identifierToolClass]]
		, FunctionDefBe_at]
	lookupAttributes = getAttributesBe(**keywordArguments)

	for ClassDefIdentifier, versionMinorMinimum, classAs_astAttribute, listTupleAttributes in getElementsBe(identifierToolClass, **keywordArguments):
		astExprDocstring: ast.Expr = makeDocstringBe(ClassDefIdentifier, lookupAttributes[ClassDefIdentifier, versionMinorMinimum])
		if not listTupleAttributes:
			ast_stmt: ast.stmt = Make.FunctionDef(
				ClassDefIdentifier
				, Make.arguments(list_arg=[Make.arg("node", annotation=astASTastAttribute)])
				, body=[astExprDocstring
					, Make.Return(Make.Call(Make.Name("isinstance"), listParameters=[Make.Name("node"), classAs_astAttribute]))]
				, decorator_list=[astName_staticmethod]
				, returns=Make.Subscript(Make.Name("TypeIs"), slice=classAs_astAttribute))

			if versionMinorMinimum > settingsManufacturing.pythonMinimumVersionMinor:
				ast_stmt = _makeSimpleGuardVersion([ast_stmt], versionMinorMinimum)

			list4ClassDefBody.append(ast_stmt)
		else:
			list4subClassDefBody: list[ast.stmt] = [astExprDocstring
				, Make.FunctionDef("__call__"
				, Make.arguments(list_arg=[Make.arg("self"), Make.arg("node", annotation=astASTastAttribute)])
				, body=[Make.Return(Make.Call(Make.Name("isinstance"), listParameters=[Make.Name("node"), classAs_astAttribute]))]
				, returns=Make.Subscript(Make.Name("TypeIs"), slice=classAs_astAttribute))]

			for attribute, _type_ast_expr, versionMinorMinimumAttribute in listTupleAttributes:
				ast_stmt = Make.FunctionDef(attribute + "Is"
					, Make.arguments(list_arg=[Make.arg("attributeCondition", annotation=Make.Subscript(Make.Name("Callable"), slice=Make.Tuple([Make.List([Make.Name('Any')]), Make.Name("bool")])))])
					, body=[Make.FunctionDef("workhorse"
							, Make.arguments(list_arg=[Make.arg("node", annotation=astASTastAttribute)])
							, body=[Make.Return(Make.BoolOp(Make.And(), values=[Make.Call(Make.Name("isinstance"), listParameters=[Make.Name("node"), classAs_astAttribute]), Make.Call(Make.Name("attributeCondition"), listParameters=[Make.Attribute(Make.Name("node"), attribute)])]))]
							, returns=Make.Subscript(Make.Name("TypeIs"), slice=classAs_astAttribute))
						, Make.Return(Make.Name("workhorse"))]
					, decorator_list=[astName_staticmethod]
					, returns=Make.Subscript(Make.Name("Callable"), slice=Make.Tuple([Make.List([astASTastAttribute]), Make.Subscript(Make.Name("TypeIs"), slice=classAs_astAttribute)])))
				if versionMinorMinimumAttribute > settingsManufacturing.pythonMinimumVersionMinor:
					ast_stmt = _makeSimpleGuardVersion([ast_stmt], versionMinorMinimumAttribute)
				list4subClassDefBody.append(ast_stmt)

			list_ast_stmt: list[ast.stmt] = [
				Make.ClassDef(ClassDefIdentifier, body=list4subClassDefBody, decorator_list=[Make.Name("call")])]

			if versionMinorMinimum > settingsManufacturing.pythonMinimumVersionMinor:
				list_ast_stmt = [_makeSimpleGuardVersion(list_ast_stmt, versionMinorMinimum)]

			list4ClassDefBody.extend(list_ast_stmt)

	list4ModuleBody: list[ast.stmt] = [
		Make.ImportFrom("operator", [Make.alias("call")]),
		Make.ImportFrom('typing', [Make.alias('TYPE_CHECKING')]),
		Make.Import("ast"),
		Make.Import("sys"),
		Make.If(Make.Name('TYPE_CHECKING'), body=[
			Make.ImportFrom('collections.abc', [Make.alias('Callable'), Make.alias('Sequence')]),
			Make.ImportFrom('typing', [Make.alias('Any'), Make.alias('TypeIs')]),
		]),
	]

	writeClass(identifierToolClass, list4ClassDefBody, list4ModuleBody)

def makeToolDOT(identifierToolClass: str, **keywordArguments: Any) -> None:
	"""Generate and write the `DOT` tool class.

	Parameters
	----------
	identifierToolClass : str
		Name of the tool class to generate.
	**keywordArguments : Any
		Override `ManufacturedPackageSettings`.
	"""
	global ast_stmt, guardVersion, versionMinorMinimum  # ruff:ignore[global-statement]
	list4ClassDefBody: list[ast.stmt] = [docstrings[settingsManufacturing.identifiers[identifierToolClass]][settingsManufacturing.identifiers[identifierToolClass]]]
	list4TypeCheckingBody: list[ast.stmt] = [
		Make.ImportFrom(f"{settingsManufacturing.identifierPackage}.{settingsManufacturing.identifiers['types']}", [Make.alias('*')]),
		Make.ImportFrom('collections.abc', [Make.alias('Sequence')]),
		Make.Import('ast'),
		Make.Import('builtins'),  # https://github.com/python/cpython/issues/143661
	]

	for identifierTypeOfNode, overloadDefinition, attribute, list_ast_expr, guardVersion, versionMinorMinimum in getElementsDOT(identifierToolClass, **keywordArguments):
		if versionMinorMinimum > settingsManufacturing.pythonMinimumVersionMinor:
			list4TypeCheckingBody.append(_makeSimpleGuardVersion([
				Make.ImportFrom(f"{settingsManufacturing.identifierPackage}.{settingsManufacturing.identifiers['types']}", [Make.alias(identifierTypeOfNode)])
			], versionMinorMinimum))
		decorator_list: list[ast.expr] = [astName_staticmethod]

# python/cpython#143661
		listOfNonIssues: list[ast.expr] = list_ast_expr.copy()
		list_ast_expr.clear()
		for shadowingIsNotAnIssue in listOfNonIssues:
			NodeChanger(
				IfThis.isNameIdentifier('str')
				, doThat=Then.replaceWith(astAttribute_builtins_str)
			).visit(shadowingIsNotAnIssue)
# TODO Investigate if `NodeChanger` will NOT replace a node if the "match" is the _entire_ node.
			if ast.unparse(shadowingIsNotAnIssue) == 'str':
				shadowingIsNotAnIssue: ast.expr = astAttribute_builtins_str

			list_ast_expr.append(shadowingIsNotAnIssue)
		del listOfNonIssues

		if overloadDefinition:
			decorator_list.append(astName_overload)
			body: list[ast.stmt] = [Make.Expr(Make.Constant(value=...))]
		else:
			body = [Make.Return(Make.Attribute(Make.Name("node"), attribute))]
			workbench: list[ast.expr] = list_ast_expr.copy()
			list_ast_expr.clear()
			caseInsensitiveSort: list[str] = []
			while workbench:
				ast_expr: ast.expr = workbench.pop()
				if isinstance(ast_expr, ast.BinOp):
					workbench.extend(unjoinBinOP(ast_expr, ast.BitOr))
				else:
					checkMe: str = str(ast.unparse(ast_expr)).lower()
					if checkMe not in caseInsensitiveSort:
						index: int = len([item for item in caseInsensitiveSort if item <= checkMe])
						caseInsensitiveSort.insert(index, checkMe)
						list_ast_expr.insert(index, ast_expr)

		ast_stmt = Make.FunctionDef(attribute
				, Make.arguments(list_arg=[Make.arg("node", annotation=Make.Name(identifierTypeOfNode))])
				, body=body
				, decorator_list=decorator_list
				, returns=Make.BitOr.join(list_ast_expr)
		)

		if guardVersion:
			_makeNestedGuardVersions()
		if ast_stmt is not None:  # pyright: ignore[reportUnnecessaryComparison]
			list4ClassDefBody.append(ast_stmt)

	list4ModuleBody: list[ast.stmt] = [
		Make.ImportFrom('typing', [Make.alias('overload'), Make.alias('TYPE_CHECKING')]),
		Make.Import('sys'),
		Make.If(Make.Name('TYPE_CHECKING'), body=list4TypeCheckingBody),
	]

	writeClass(identifierToolClass, list4ClassDefBody, list4ModuleBody)

def makeToolDump(identifierModule: str = '_tool_dump') -> None:
	"""Transform ast.dump to print full attribute names, all empty items, and not default context."""
	astModule: ast.Module = parseLogicalPath2astModule('ast')
	astFunctionDef: ast.FunctionDef = raiseIfNone(extractFunctionDef(astModule, 'dump'))
	astModuleStub: ast.Module = parsePathFilename2astModule(raiseIfNone(typeshed_client.get_stub_file('ast'
		, search_context=typeshed_client.get_search_context(typeshed=settingsManufacturing.pathRoot_typeshed))))
	dictionaryArguments: dict[str, ast.arg] = {}
	NodeTourist(IfThis.isFunctionDefIdentifier('dump')
		, NodeTourist(Be.arg, Then.updateKeyValueIn(DOT.arg, Then.extractIt, dictionaryArguments)).visit).visit(astModuleStub)
	NodeChanger(Be.arguments, Grab.andDoAllOf([
		Grab.argsAttribute(Then.replaceWith(list(map(dictionaryArguments.__getitem__
			, map(DOT.arg, astFunctionDef.args.args)))))
		, Grab.kwonlyargsAttribute(Then.replaceWith(list(map(dictionaryArguments.__getitem__
			, map(DOT.arg, astFunctionDef.args.kwonlyargs)))))
	])).visit(astFunctionDef.args)
	NodeChanger(IfThis.isFunctionDefIdentifier('dump')
		, Grab.returnsAttribute(Then.replaceWith(raiseIfNone(extractFunctionDef(astModuleStub, 'dump')).returns))
	).visit(astFunctionDef)

	NodeChanger(IfThis.isNameIdentifier('AST')
		, Then.replaceWith(Make.Attribute(Make.Name('ast'), 'AST'))).visit(astFunctionDef)
	NodeChanger(IfThis.isAssignAndTargets0Is(IfThis.isNameIdentifier('cls_name'))
		, Grab.valueAttribute(Then.replaceWith(Make.JoinedStr([
			Make.FormattedValue(Make.Attribute(Make.Name('t'), 'node'), -1)
			, Make.Constant('ast.')
			, Make.FormattedValue(Make.Attribute(Make.Name('cls'), '__name__'), -1)
			, Make.FormattedValue(Make.Attribute(Make.Name('t'), 'reset'), -1)
		])))).visit(astFunctionDef)

	NodeChanger(Be.For.iterIs(IfThis.astIs(Make.Attribute(Make.Name('node'), '_fields')))
		, NodeChanger(Be.If.testIs(Be.BoolOp.opIs(Be.And))
			, NodeChanger(Be.BoolOp, Grab.valuesAttribute([
				Make.UnaryOp(Make.Not(), Make.Name('show_empty'))].__add__)).visit).visit
	).visit(astFunctionDef)
	NodeChanger(Be.If.testIs(IfThis.astIs(Make.Call(Make.Name('isinstance'), [Make.Name('value'), Make.Name('Load')])))
		, Then.removeIt).visit(astFunctionDef)

	astModule.body = [Make.ImportFrom('__future__', [Make.alias('annotations')]), Make.Import('ast'), astFunctionDef]
	write_astModule(astModule, settingsManufacturing.pathPackage / (identifierModule + settingsManufacturing.fileExtension))

def makeToolGrab(identifierToolClass: str, **keywordArguments: Any) -> None:
	"""Generate and write `class` `Grab`.

	Parameters
	----------
	identifierToolClass : str
		Name of the tool class to generate.
	**keywordArguments : Any
		Override `ManufacturedPackageSettings`.
	"""
	global ast_stmt, guardVersion, versionMinorMinimum  # ruff:ignore[global-statement]
	list4ClassDefBody: list[ast.stmt] = [
		docstrings[settingsManufacturing.identifiers[identifierToolClass]][settingsManufacturing.identifiers[identifierToolClass]]
		, FunctionDefGrab_andDoAllOf
		, FunctionDefGrab_index
		]
	list4TypeCheckingBody: list[ast.stmt] = [
		Make.ImportFrom(f"{settingsManufacturing.identifierPackage}.{settingsManufacturing.identifiers['types']}", [Make.alias('*')]),
		Make.ImportFrom('collections.abc', [Make.alias('Callable'), Make.alias('Sequence')]),
		Make.ImportFrom('typing', [Make.alias('Any')]),
		Make.Import('ast'),
	]
	lookupFieldTypes = getFieldTypesGrab(**keywordArguments)

	for identifierTypeOfNode, list_ast_expr, attribute, guardVersion, versionMinorMinimum in getElementsGrab(
		identifierToolClass, **keywordArguments
	):
		if versionMinorMinimum > settingsManufacturing.pythonMinimumVersionMinor:
			list4TypeCheckingBody.append(_makeSimpleGuardVersion([
				Make.ImportFrom(f"{settingsManufacturing.identifierPackage}.{settingsManufacturing.identifiers['types']}", [Make.alias(identifierTypeOfNode)])
			], versionMinorMinimum))
		astNameTypeOfNode: ast.Name = Make.Name(identifierTypeOfNode)
		ast_exprReturns: ast.expr = Make.Subscript(Make.Name("Callable"), Make.Tuple([Make.List([astNameTypeOfNode]), astNameTypeOfNode]))

		type_params: list[ast.type_param] | None = None
# DEVELOPMENT Make.TypeVar, name = type_astSuperClasses?, bound = type_astSuperClasses_ast_expr?. But, only for some functions. Maybe crossref with dictionary_astSuperClasses.

		ast_stmt = Make.FunctionDef(attribute + "Attribute"
			, Make.arguments(list_arg=[Make.arg("action", annotation=Make.BitOr.join([Make.Subscript(Make.Name("Callable"), Make.Tuple([Make.List([ast_expr]), ast_expr])) for ast_expr in list_ast_expr]))])
			, body=[makeDocstringGrab(attribute, ast_exprReturns, lookupFieldTypes[attribute, versionMinorMinimum])
				, Make.FunctionDef("workhorse"
				, Make.arguments(list_arg=[Make.arg("node", annotation=astNameTypeOfNode)])
				, body=[Make.Expr(Make.Call(Make.Name("setattr"), listParameters=[Make.Name("node"), Make.Constant(f"{attribute}")
									, Make.Call(Make.Name("action"), listParameters=[
										Make.Call(Make.Name("getattr"), listParameters=[Make.Name("node"), Make.Constant(f"{attribute}")])])]))
					, Make.Return(Make.Name("node"))]
				, returns=astNameTypeOfNode)
				, Make.Return(Make.Name("workhorse"))]
			, decorator_list=[astName_staticmethod]
			, returns=ast_exprReturns
			, type_params=type_params)

		if guardVersion:
			_makeNestedGuardVersions()
		if ast_stmt is not None:  # pyright: ignore[reportUnnecessaryComparison]
			list4ClassDefBody.append(ast_stmt)

	list4ModuleBody: list[ast.stmt] = [
		Make.ImportFrom('typing', [Make.alias('TYPE_CHECKING')]),
		Make.Import('sys'),
		Make.If(Make.Name('TYPE_CHECKING'), body=list4TypeCheckingBody),
	]

	writeClass(identifierToolClass, list4ClassDefBody, list4ModuleBody)

def makeToolMake(identifierToolClass: str, **keywordArguments: Any) -> None:
	"""Generate and write `class` `Make`.

	Parameters
	----------
	identifierToolClass : str
		Name of the tool class to generate.
	**keywordArguments : Any
		Override `ManufacturedPackageSettings`.
	"""
	global ast_stmt, guardVersion, versionMinorMinimum  # ruff:ignore[global-statement]
	list4ModuleBody: list[ast.stmt] = [
		Make.ImportFrom('typing', [Make.alias('TYPE_CHECKING')])
		, Make.Import("ast")
		, Make.Import("warnings")
	]
	list4TypeCheckingBody: list[ast.stmt] = [
		Make.ImportFrom('collections.abc', [Make.alias('Iterable'), Make.alias('Sequence')])
		, Make.ImportFrom('hunterMakesPy', [Make.alias('identifierDotAttribute')])
		, Make.ImportFrom('typing', [Make.alias('Any'), Make.alias('Unpack')])
		, Make.Import("builtins")  # https://github.com/python/cpython/issues/143661
		, Make.ImportFrom(f"{settingsManufacturing.identifierPackage}.{settingsManufacturing.identifiers['types']}", [Make.alias('ast_ConstantValue'), Make.alias('ast_attributes')])
	]

	list4ClassDefBody: list[ast.stmt] = [
		docstrings[identifierToolClass][identifierToolClass]
		, FunctionDef_boolopJoinMethod
		, FunctionDef_operatorJoinMethod]

	for (ClassDefIdentifier, listFunctionDef_args, kwarg_annotationIdentifier, defaults, classAs_astAttribute, overloadDefinition,
		listCall_keyword, guardVersion, versionMinorMinimum) in getElementsMake(identifierToolClass, **keywordArguments):  # ruff:ignore[unused-loop-control-variable]
		# Bypass the manufacture of the tool by using a prefabricated tool from the annex.
		if ClassDefIdentifier in [subclass.__name__ for subclass in ast.boolop.__subclasses__()]:
			list4ClassDefBody.append(
				Make.ClassDef(ClassDefIdentifier
					, bases=[Make.Attribute(Make.Name("ast"), ClassDefIdentifier)]
					, body=[docstrings[identifierToolClass][ClassDefIdentifier], FunctionDef_join_boolop]))
			continue
		elif ClassDefIdentifier in [subclass.__name__ for subclass in ast.operator.__subclasses__()]:
			list4ClassDefBody.append(
				Make.ClassDef(ClassDefIdentifier
					, bases=[Make.Attribute(Make.Name("ast"), ClassDefIdentifier)]
					, body=[docstrings[identifierToolClass][ClassDefIdentifier], FunctionDef_join_operator]))
			continue
		elif ClassDefIdentifier == "keyword":
			list4ClassDefBody.extend(listOverloads_keyword)
			list4ModuleBody.append(Make.ImportFrom("typing", [Make.alias("overload")]))

		if kwarg_annotationIdentifier != "No":
			listCall_keyword.append(keywordKeywordArguments4Call)
			list4TypeCheckingBody.append(Make.ImportFrom(f"{settingsManufacturing.identifierPackage}.{settingsManufacturing.identifiers['types']}", [Make.alias(kwarg_annotationIdentifier)]))
			kwarg: ast.arg | None = Make.arg(settingsManufacturing.keywordArgumentsIdentifier
				, annotation=Make.Subscript(Make.Name("Unpack"), slice=Make.Name(kwarg_annotationIdentifier)))
		else:
			kwarg = None
		decorator_list: list[ast.expr] = [astName_staticmethod]

		# For now, all `overloadDefinition` are `False` because overload is handled above.
		if overloadDefinition:
			decorator_list.append(astName_overload)
			body: list[ast.stmt] = [Make.Expr(Make.Constant(value=...))]
		else:
			if ClassDefIdentifier == "Import":
				# Replace the manufactured `names` parameter with the prefabricated `dotModule` and `asName`; keep the other manufactured parameters.
				listFunctionDef_args = [*list_argMake_Import, *listFunctionDef_args[1:None]]
				defaults = [Make.Constant(None), *defaults[1:None]]
				listCall_keyword = [keywordMake_Import_names, *listCall_keyword[1:None]]
			body = [docstrings[settingsManufacturing.identifiers[identifierToolClass]][ClassDefIdentifier]
				, Make.Return(Make.Call(classAs_astAttribute, list_keyword=listCall_keyword))]

		ast_stmt = Make.FunctionDef(ClassDefIdentifier
			, Make.arguments(list_arg=listFunctionDef_args, kwarg=kwarg, defaults=defaults)
			, body=body
			, decorator_list=decorator_list
			, returns=classAs_astAttribute)

		if guardVersion:
			_makeNestedGuardVersions()
			list4ModuleBody.append(Make.Import("sys"))
		if ast_stmt is not None:  # pyright: ignore[reportUnnecessaryComparison]
			list4ClassDefBody.append(ast_stmt)

	writeClass(identifierToolClass, list4ClassDefBody, [
		*list4ModuleBody,
		Make.If(Make.Name('TYPE_CHECKING'), body=list4TypeCheckingBody),
		ignoreAbstractClassWarning,
	])

def write_theSSOT(identifierModule: str) -> None:
	"""Write the SSOT module to disk.

	Parameters
	----------
	identifierModule : str
		The logical identifier of the SSOT module.
	"""
	writeModule(astModule_theSSOT, identifierModule)

def writeClass(identifierClass: str, list4ClassDefBody: list[ast.stmt], list4ModuleBody: list[ast.stmt], identifierModulePrefix: str | None = '_tool') -> None:
	"""Write a class definition and its module to disk.

	Parameters
	----------
	identifierClass : str
			Name of the class to write.
	list4ClassDefBody : list[ast.stmt]
			Statements for the class body.
	list4ModuleBody : list[ast.stmt]
			Statements for the module body.
	identifierModulePrefix : str | None = '_tool'
			Prefix for the module identifier.
	"""
	identifierModule: str = (identifierModulePrefix or "") + identifierClass
	return writeModule(
		Make.Module([
			docstringWarning,
			Make.ImportFrom('__future__', [Make.alias('annotations')]),
			*list4ModuleBody,
			Make.ClassDef(identifierClass, body=list4ClassDefBody),
		])
		, identifierModule
	)

def manufactureTools(settingsManufacturing: ManufacturedPackageSettings) -> None:
	"""Manufacture all tools and write generated modules.

	Parameters
	----------
	settingsManufacturing : ManufacturedPackageSettings
			Settings `object` containing identifiers for tool generation.
	"""
	makeToolBe(settingsManufacturing.identifiers['Be'])
	makeToolDOT(settingsManufacturing.identifiers['DOT'])
	makeToolDump()
	makeToolGrab(settingsManufacturing.identifiers['Grab'])
	makeToolMake(settingsManufacturing.identifiers['Make'])
	write_theSSOT(settingsManufacturing.identifiers['SSOT'])
	make_astTypes(settingsManufacturing.identifiers['types'])

if __name__ == "__main__":
	manufactureTools(settingsManufacturing)
