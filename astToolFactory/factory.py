"""Module for manufacturing and writing ast tools and modules."""

from astToolFactory import (
	astASTastAttribute, astName_overload, astName_staticmethod, getElementsBe, getElementsDOT, getElementsGrab,
	getElementsMake, getElementsTypeAlias, keywordKeywordArguments4Call, ManufacturedPackageSettings,
	settingsManufacturing, settingsPackage)
from astToolFactory.documentation import docstrings, docstringWarning
from astToolFactory.factoryAnnex import (
	astModule_theSSOT, FunctionDef_bodyMake_Import, FunctionDef_boolopJoinMethod, FunctionDef_join_boolop,
	FunctionDef_join_operator, FunctionDef_operatorJoinMethod, FunctionDefGrab_andDoAllOf, FunctionDefMake_Attribute,
	list_argMake_Import, listFunctionDefs_index, listHandmade_astTypes, listOverloads_keyword)
from astToolkit import (
	astModuleToIngredientsFunction, Be, extractClassDef, IfThis, IngredientsFunction, IngredientsModule, LedgerOfImports,
	Make, NodeChanger, parseLogicalPath2astModule)
from astToolkit.transformationTools import unjoinBinOP, write_astModule
from hunterMakesPy import raiseIfNone, writeStringToHere
from isort import code as isort_code
from pathlib import PurePosixPath
from typing import Any, TypedDict
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

def _makeGuardVersion() -> None:
	"""Construct version guard."""
	global ast_stmt, guardVersion, versionMinorMinimum  # noqa: PLW0602, PLW0603
	orElse: ast.stmt | None = None
	if versionMinorMinimum >= settingsManufacturing.pythonMinimumVersionMinor:
		test: ast.Compare = Make.Compare(
			Make.Attribute(Make.Name("sys"), "version_info"),
			ops=[Make.GtE()],
			comparators=[Make.Tuple([Make.Constant(3), Make.Constant(int(versionMinorMinimum))])],
		)
		assert ast_stmt is not None, "Programming by brinkmanship!"  # noqa: S101
		body: list[ast.stmt] = [ast_stmt]
		dictionaryGuardVersion[versionMinorMinimum] = GuardIfThen(test=test, body=body)
	else:
		orElse = ast_stmt

	if guardVersion > 1:
		ast_stmt = None
	else:
		for test_body in [dictionaryGuardVersion[version] for version in sorted(dictionaryGuardVersion)]:
			orElse = Make.If(**test_body, orElse=[orElse] if orElse else [])
		assert orElse is not None, "Programming by brinkmanship!"  # noqa: S101
		ast_stmt = orElse
		dictionaryGuardVersion.clear()

def writeModule(astModule: ast.Module, moduleIdentifier: str) -> None:
	"""Write an AST module to disk, handling type ignores and formatting.

	Parameters
	----------
	astModule : ast.Module
		The AST module to write.
	moduleIdentifier : str
		The stem for the module file.

	Returns
	-------
	None

	"""
	ast.fix_missing_locations(astModule)
	pythonSource: str = ast.unparse(astModule)
	if "Grab" in moduleIdentifier:
		pythonSource = "# ruff: noqa: B009, B010\n" + pythonSource
	if "Find" in moduleIdentifier:
		pythonSource = "# ruff: noqa: A001\n" + pythonSource
	if "Make" in moduleIdentifier:
		# type ignore only works on hasDOTtype_comment, right?
		# TODO update docs  # noqa: ERA001

		listTypeIgnore: list[ast.TypeIgnore] = []
		lineno: int = 0
		for astClass, tag in [
			("keyword", "[reportInconsistentOverload]"),
			("MatchClass", "[reportSelfClsParameterName]"),
			("MatchSingleton", "FBT001"),
		]:
			for splitlinesNumber, line in enumerate(pythonSource.splitlines()):
				if "def " + astClass in line:
					# get the last occurrence of the match in the source code
					lineno = splitlinesNumber + 1
			listTypeIgnore.append(Make.TypeIgnore(lineno, tag))
		astModule = ast.parse(pythonSource)
		astModule.type_ignores.extend(listTypeIgnore)
		ast.fix_missing_locations(astModule)
		pythonSource = ast.unparse(astModule)
		pythonSource = "# ruff: noqa: A002\n" + pythonSource
		pythonSource = pythonSource.replace("# type: ignore[", "# pyright: ignore[")
		pythonSource = pythonSource.replace("# type: ignore", "# noqa: ")
	autoflake_additional_imports: list[str] = [settingsManufacturing.identifierPackage]
	pythonSource = autoflake.fix_code(
		pythonSource,
		autoflake_additional_imports,
		expand_star_imports=True,
		remove_all_unused_imports=True,
		remove_duplicate_keys=False,
		remove_unused_variables=False,
	)
	pythonSource = isort_code(code=pythonSource, **settingsManufacturing.isort_code)  # pyright: ignore[reportArgumentType]
	pathFilenameModule = PurePosixPath(settingsManufacturing.pathPackage, moduleIdentifier + settingsManufacturing.fileExtension)
	pythonSource += "\n"
	writeStringToHere(pythonSource, pathFilenameModule)

def writeClass(classIdentifier: str, list4ClassDefBody: list[ast.stmt], list4ModuleBody: list[ast.stmt], moduleIdentifierPrefix: str | None = "_tool") -> None:
	"""Write a class definition and its module to disk.

	(AI generated docstring)

	Parameters
	----------
	classIdentifier : str
			Name of the class to write.
	list4ClassDefBody : list[ast.stmt]
			Statements for the class body.
	list4ModuleBody : list[ast.stmt]
			Statements for the module body.
	moduleIdentifierPrefix : str | None = '_tool'
			Prefix for the module identifier.

	Returns
	-------
	None

	"""
	moduleIdentifier: str = (moduleIdentifierPrefix or "") + classIdentifier
	return writeModule(
		Make.Module([docstringWarning, *list4ModuleBody, Make.ClassDef(classIdentifier, body=list4ClassDefBody)]),
		moduleIdentifier,
	)

def make_astTypes(**keywordArguments: Any) -> None:
	"""Generate and write the AST types module.

	Parameters
	----------
	**keywordArguments : Any
		Override `ManufacturedPackageSettings`.

	Returns
	-------
	None

	"""
	global ast_stmt, guardVersion, versionMinorMinimum  # noqa: PLW0603
	list4ModuleBody: list[ast.stmt] = []
	ledgerOfImports = LedgerOfImports(Make.Module([
		Make.ImportFrom("types", [Make.alias("EllipsisType")])
		, Make.ImportFrom("typing", [Make.alias("Any"), Make.alias("TypeAlias", "typing_TypeAlias"), Make.alias("TypedDict"), Make.alias("TypeVar", "typing_TypeVar")])
		, Make.Import("ast")
		, Make.Import("sys")]))

	for identifierTypeAlias, list4TypeAlias_value, guardVersion, versionMinorMinimum in getElementsTypeAlias(**keywordArguments):  # noqa: B007
		ast_stmt = Make.TypeAlias(Make.Name(identifierTypeAlias, Make.Store()), type_params=[], value=Make.BitOr.join(list4TypeAlias_value))

		if guardVersion:
			_makeGuardVersion()
		if ast_stmt is not None:  # pyright: ignore[reportUnnecessaryComparison]
			list4ModuleBody.append(ast_stmt)

	astModule: ast.Module = Make.Module([
		docstringWarning
		, *ledgerOfImports.makeList_ast()
		, *listHandmade_astTypes
		, *list4ModuleBody])

	writeModule(astModule, "_astTypes")

def makeTool_dump() -> None:
	"""Generate and write `dump`."""
	ingredientsFunction: IngredientsFunction = astModuleToIngredientsFunction(parseLogicalPath2astModule("ast"), "dump")

	def doThat(node: ast.FunctionDef) -> ast.expr | Any:
		return NodeChanger[ast.Attribute, ast.expr](
			Be.Attribute.valueIs(IfThis.isAttributeNamespaceIdentifier("node", "__class__")),
			lambda node: Make.Add.join([Make.Constant("ast."), node]),
		).visit(node)

	# Nested NodeChanger, find the correct function, then find the statements to replace.
	NodeChanger(IfThis.isFunctionDefIdentifier("_format"), doThat).visit(ingredientsFunction.astFunctionDef)

	pathFilename = PurePosixPath(settingsManufacturing.pathPackage, "_dumpFunctionDef" + settingsManufacturing.fileExtension)

	write_astModule(IngredientsModule(ingredientsFunction), pathFilename, settingsManufacturing.identifierPackage)

def makeToolBe(identifierToolClass: str, **keywordArguments: Any) -> None:
	"""Generate and write `class` `Be`."""
	list4ClassDefBody: list[ast.stmt] = [docstrings[settingsManufacturing.identifiers[identifierToolClass]][settingsManufacturing.identifiers[identifierToolClass]]]

	for ClassDefIdentifier, versionMinorMinimum, classAs_astAttribute, listTupleAttributes in getElementsBe(identifierToolClass, **keywordArguments):
		if not listTupleAttributes:
			ast_stmt: ast.stmt = Make.FunctionDef(
				ClassDefIdentifier
				, Make.arguments(list_arg=[Make.arg("node", annotation=astASTastAttribute)])
				, body=[docstrings[identifierToolClass][ClassDefIdentifier]
					, Make.Return(Make.Call(Make.Name("isinstance"), listParameters=[Make.Name("node"), classAs_astAttribute]))]
				, decorator_list=[astName_staticmethod]
				, returns=Make.Subscript(Make.Name("TypeIs"), slice=classAs_astAttribute))

			if versionMinorMinimum > settingsManufacturing.pythonMinimumVersionMinor:
				ast_stmt = Make.If(Make.Compare(
						Make.Attribute(Make.Name("sys"), "version_info")
						, ops=[Make.GtE()]
						, comparators=[Make.Tuple([Make.Constant(3), Make.Constant(int(versionMinorMinimum))])])
					, body=[ast_stmt])

			list4ClassDefBody.append(ast_stmt)
		else:
			list4subClassDefBody: list[ast.stmt] = [Make.FunctionDef("__call__"
				, Make.arguments(list_arg=[Make.arg("self"), Make.arg("node", annotation=astASTastAttribute)])
				, body=[Make.Return(Make.Call(Make.Name("isinstance"), listParameters=[Make.Name("node"), classAs_astAttribute]))]
				, returns=Make.Subscript(Make.Name("TypeIs"), slice=classAs_astAttribute))]

			for attribute, _type_ast_expr in listTupleAttributes:
				list4subClassDefBody.append(Make.FunctionDef(attribute + "Is"
					, Make.arguments(list_arg=[Make.arg("attributeCondition", annotation=Make.Subscript(Make.Name("Callable"), slice=Make.Tuple([Make.List([Make.Name('Any')]), Make.Name("bool")])))])
					, body=[Make.FunctionDef("workhorse"
							, Make.arguments(list_arg=[Make.arg("node", annotation=astASTastAttribute)])
							, body=[Make.Return(Make.BoolOp(Make.And(), values=[Make.Call(Make.Name("isinstance"), listParameters=[Make.Name("node"), classAs_astAttribute]), Make.Call(Make.Name("attributeCondition"), listParameters=[Make.Attribute(Make.Name("node"), attribute)])]))]
							, returns=Make.Subscript(Make.Name("TypeIs"), slice=classAs_astAttribute))
						, Make.Return(Make.Name("workhorse"))]
					, decorator_list=[astName_staticmethod]
					, returns=Make.Subscript(Make.Name("Callable"), slice=Make.Tuple([Make.List([astASTastAttribute]), Make.Subscript(Make.Name("TypeIs"), slice=classAs_astAttribute)]))))

			list_ast_stmt: list[ast.stmt] = [
				Make.ClassDef(f"_{ClassDefIdentifier}", body=list4subClassDefBody)
				, Make.Assign([Make.Name(ClassDefIdentifier, context=Make.Store())], value=Make.Call(Make.Name(f"_{ClassDefIdentifier}")))
				, docstrings[identifierToolClass][ClassDefIdentifier]]

			if versionMinorMinimum > settingsManufacturing.pythonMinimumVersionMinor:
				list_ast_stmt = [
					Make.If(Make.Compare(
							Make.Attribute(Make.Name("sys"), "version_info")
							, ops=[Make.GtE()]
							, comparators=[Make.Tuple([Make.Constant(3), Make.Constant(int(versionMinorMinimum))])])
						, body=list_ast_stmt)]

			list4ClassDefBody.extend(list_ast_stmt)

	list4ModuleBody: list[ast.stmt] = [
		Make.ImportFrom("typing_extensions", [Make.alias("TypeIs")]),
		Make.ImportFrom("typing", [Make.alias("Any")]),
		Make.ImportFrom("collections.abc", [Make.alias("Callable"), Make.alias("Sequence")]),
		Make.ImportFrom(settingsManufacturing.identifierPackage, [Make.alias("ConstantValueType")]),
		Make.Import("ast"),
		Make.Import("sys"),
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

	Returns
	-------
	None

	"""
	global ast_stmt, guardVersion, versionMinorMinimum  # noqa: PLW0603
	list4ClassDefBody: list[ast.stmt] = [docstrings[settingsManufacturing.identifiers[identifierToolClass]][settingsManufacturing.identifiers[identifierToolClass]]]

	for identifierTypeOfNode, overloadDefinition, attribute, list_ast_expr, guardVersion, versionMinorMinimum in getElementsDOT(identifierToolClass, **keywordArguments):  # noqa: B007
		decorator_list: list[ast.expr] = [astName_staticmethod]
		if overloadDefinition:
			decorator_list.append(astName_overload)
			body: list[ast.stmt] = [Make.Expr(Make.Constant(value=...))]
		else:
			body = [Make.Return(Make.Attribute(Make.Name("node"), attribute))]
			workbench = list_ast_expr.copy()
			list_ast_expr.clear()
			caseInsensitiveSort: list[str] = []
			while workbench:
				ast_expr: ast.expr = workbench.pop()
				if isinstance(ast_expr, ast.BinOp):
					workbench.extend(unjoinBinOP(ast_expr, ast.BitOr))
				else:
					checkMe = str(ast.unparse(ast_expr)).lower()
					if checkMe not in caseInsensitiveSort:
						index = len([item for item in caseInsensitiveSort if item <= checkMe])
						caseInsensitiveSort.insert(index, checkMe)
						list_ast_expr.insert(index, ast_expr)

		ast_stmt = Make.FunctionDef(attribute
				, Make.arguments(list_arg=[Make.arg("node", annotation=Make.Name(identifierTypeOfNode))])
				, body=body
				, decorator_list=decorator_list
				, returns=Make.BitOr.join(list_ast_expr)
		)

		if guardVersion:
			_makeGuardVersion()
		if ast_stmt is not None:  # pyright: ignore[reportUnnecessaryComparison]
			list4ClassDefBody.append(ast_stmt)

	list4ModuleBody: list[ast.stmt] = [
		Make.ImportFrom(settingsManufacturing.identifierPackage, [Make.alias("*")])
		, Make.ImportFrom("collections.abc", [Make.alias("Sequence")])
		, Make.ImportFrom("typing", [Make.alias("overload")])
		, Make.Import("ast")
		, Make.Import("sys")
		, Make.If(
			Make.Compare(Make.Attribute(Make.Name("sys"), "version_info")
				, [Make.GtE()]
				, [Make.Tuple([Make.Constant(3), Make.Constant(13)])]
			)
			, body=[Make.ImportFrom(settingsManufacturing.identifierPackage, [Make.alias("hasDOTdefault_value")])]
		)
	]

	writeClass(identifierToolClass, list4ClassDefBody, list4ModuleBody)

def makeToolFind(identifierToolClass: str, **keywordArguments: Any) -> None:
	"""Find."""
	list4ClassDefBody: list[ast.stmt] = []

	for ClassDefIdentifier, versionMinorMinimum, classAs_astAttribute, listTupleAttributes in getElementsBe(identifierToolClass, **keywordArguments):
		"""With workhorse
		ast_stmt: ast.stmt = Make.FunctionDef(ClassDefIdentifier
			, Make.arguments(list_arg=[Make.arg("self")])
			, body=[
				# docstrings[identifierToolClass][ClassDefIdentifier]
				# ,
				Make.FunctionDef("workhorse"
					, Make.arguments(list_arg=[Make.arg("node", annotation=astASTastAttribute)])
					, body=[Make.Return(ast.Tuple([Make.Call(Make.Name("isinstance"), listParameters=[Make.Name("node"), classAs_astAttribute]), Make.Name("node")]))]
					, returns=Make.Subscript(Make.Name("tuple"), slice=Make.Tuple([Make.Subscript(Make.Name("TypeIs"), slice=classAs_astAttribute), astASTastAttribute]))
				)
				, Make.Assign([Make.Name("dontMutateMyQueue", Make.Store())]
					, value=Make.List([Make.Starred(Make.Attribute(Make.Name("self"), "queueOfTruth")), Make.Name("workhorse")])
				)
				, Make.Return(Make.Call(Make.Name("Find"), listParameters=[Make.Name("dontMutateMyQueue")]))
			]
			, returns=Make.Constant("Find")
		)
		"""

		"""Separate subclass and attributes
		"""
		ast_stmt: ast.stmt = Make.FunctionDef(
			ClassDefIdentifier
			, Make.arguments(list_arg=[Make.arg("node", annotation=astASTastAttribute)])
			, body=[Make.Return(Make.Call(Make.Name("isinstance"), listParameters=[Make.Name("node"), classAs_astAttribute]))]
			, decorator_list=[astName_staticmethod]
			, returns=Make.Subscript(Make.Name("TypeIs"), slice=classAs_astAttribute)
		)

		if versionMinorMinimum > settingsManufacturing.pythonMinimumVersionMinor:
			ast_stmt = Make.If(
				Make.Compare(Make.Attribute(Make.Name("sys"), 'version_info')
					, ops=[Make.GtE()]
					, comparators=[Make.Tuple([Make.Constant(3), Make.Constant(int(versionMinorMinimum))])])
				, body=[ast_stmt])

		list4ClassDefBody.append(ast_stmt)

		if listTupleAttributes:
			list4subClassDefBody: list[ast.stmt] = []

			for attribute, type_ast_expr in listTupleAttributes:
				list4subClassDefBody.append(Make.FunctionDef(ClassDefIdentifier + '_' + attribute
					, argumentSpecification=Make.arguments(list_arg=[Make.arg("node", annotation=classAs_astAttribute)])
					, returns=type_ast_expr
					, decorator_list=[astName_staticmethod]
					, body=[Make.Return(Make.Attribute(Make.Name('node'), attribute))]
					))

			list_ast_stmt: list[ast.stmt] = list4subClassDefBody

			if versionMinorMinimum > settingsManufacturing.pythonMinimumVersionMinor:
				list_ast_stmt = [
					Make.If(Make.Compare(
							Make.Attribute(Make.Name("sys"), "version_info")
							, ops=[Make.GtE()]
							, comparators=[Make.Tuple([Make.Constant(3), Make.Constant(int(versionMinorMinimum))])])
						, body=list_ast_stmt)]

			list4ClassDefBody.extend(list_ast_stmt)

		"""Classes within classes
		list4subClassDefBody: list[ast.stmt] = [
			Make.FunctionDef(
			'__call__'
			, Make.arguments(list_arg=[Make.arg("cls"), Make.arg("node", annotation=astASTastAttribute)])
			, body=[Make.Return(Make.Call(Make.Name("isinstance"), listParameters=[Make.Name("node"), classAs_astAttribute]))]
			, decorator_list=[astName_classmethod]
			, returns=Make.Subscript(Make.Name("TypeIs"), slice=classAs_astAttribute)
			)
		]

		for attribute, type_ast_expr in listTupleAttributes:
			list4subClassDefBody.append(
				Make.ClassDef(
					attribute
					, body=[Make.FunctionDef(
						'__call__'
						, Make.arguments(list_arg=[Make.arg("cls"), Make.arg("node", annotation=classAs_astAttribute)])
						, body=[Make.Return(Make.Attribute(Make.Name("node"), attribute))]
						, decorator_list=[astName_classmethod]
						, returns=type_ast_expr
					)])
			)

		list_ast_stmt: list[ast.stmt] = [Make.ClassDef(ClassDefIdentifier, body=list4subClassDefBody)]

		if versionMinorMinimum > settingsManufacturing.pythonMinimumVersionMinor:
			list_ast_stmt = [
				Make.If(Make.Compare(
						Make.Attribute(Make.Name("sys"), "version_info")
						, ops=[Make.GtE()]
						, comparators=[Make.Tuple([Make.Constant(3), Make.Constant(int(versionMinorMinimum))])])
					, body=list_ast_stmt)]

		list4ClassDefBody.extend(list_ast_stmt)
	"""
	# NOTE A temporary system during prototype development.
	identifierToolClassOVERRIDE: str = "Find"
	identifierToolClass = identifierToolClassOVERRIDE
	moduleIdentifier = "_prototype" + identifierToolClass

	astModule: ast.Module = parseLogicalPath2astModule(f"{settingsPackage.identifierPackage}.{moduleIdentifier}")
	astClassDef: ast.ClassDef = raiseIfNone(extractClassDef(astModule, identifierToolClass))
	ledgerOfImports = LedgerOfImports(astModule)
	del astModule
	ledgerOfImports.walkThis(ast.parse("""from astToolkit import ConstantValueType, 木
from collections.abc import Callable, Sequence
from typing_extensions import TypeIs
import ast"""))

	astClassDef.body.extend(list4ClassDefBody)

	astModule = Make.Module([*ledgerOfImports.makeList_ast(), astClassDef])

	writeModule(astModule, moduleIdentifier)

def makeToolGrab(identifierToolClass: str, **keywordArguments: Any) -> None:
	"""Generate and write the `Grab` tool class.

	Parameters
	----------
	identifierToolClass : str
		Name of the tool class to generate.
	**keywordArguments : Any
		Override `ManufacturedPackageSettings`.

	Returns
	-------
	None

	"""
	global ast_stmt, guardVersion, versionMinorMinimum  # noqa: PLW0603
	list4ClassDefBody: list[ast.stmt] = [
		docstrings[settingsManufacturing.identifiers[identifierToolClass]][settingsManufacturing.identifiers[identifierToolClass]]
		, FunctionDefGrab_andDoAllOf]

	for identifierTypeOfNode, list_ast_expr, attribute, guardVersion, versionMinorMinimum in getElementsGrab(# noqa: B007
		identifierToolClass, **keywordArguments
	):
		astNameTypeOfNode: ast.Name = Make.Name(identifierTypeOfNode)

		ast_stmt = Make.FunctionDef(attribute + "Attribute"
			, Make.arguments(list_arg=[Make.arg("action", annotation=Make.BitOr.join([Make.Subscript(Make.Name("Callable"), Make.Tuple([Make.List([ast_expr]), ast_expr])) for ast_expr in list_ast_expr]))])
			, body=[Make.FunctionDef("workhorse"
				, Make.arguments(list_arg=[Make.arg("node", annotation=astNameTypeOfNode)])
				, body=[Make.Expr(Make.Call(Make.Name("setattr"), listParameters=[Make.Name("node"), Make.Constant(f"{attribute}")
									, Make.Call(Make.Name("action"), listParameters=[
										Make.Call(Make.Name("getattr"), listParameters=[Make.Name("node"), Make.Constant(f"{attribute}")])])]))
					, Make.Return(Make.Name("node"))]
				, returns=astNameTypeOfNode), Make.Return(Make.Name("workhorse"))]
			, decorator_list=[astName_staticmethod]
			, returns=Make.Subscript(Make.Name("Callable"), Make.Tuple([Make.List([astNameTypeOfNode]), astNameTypeOfNode])))

		if guardVersion:
			_makeGuardVersion()
		if ast_stmt is not None:  # pyright: ignore[reportUnnecessaryComparison]
			list4ClassDefBody.append(ast_stmt)

	list4ModuleBody: list[ast.stmt] = [
		Make.ImportFrom(settingsManufacturing.identifierPackage, [Make.alias("*")])
		, Make.ImportFrom("collections.abc", [Make.alias("Callable"), Make.alias("Sequence")])
		, Make.ImportFrom("typing", [Make.alias("Any"), Make.alias("cast")])
		, Make.Import("ast")
		, Make.Import("sys")
		, Make.If(Make.Compare(Make.Attribute(Make.Name("sys"), "version_info"), [Make.GtE()], [Make.Tuple([Make.Constant(3), Make.Constant(13)])]), [Make.ImportFrom(settingsManufacturing.identifierPackage, [Make.alias("hasDOTdefault_value")])])
		, *listFunctionDefs_index
	]

	writeClass(identifierToolClass, list4ClassDefBody, list4ModuleBody)

def makeToolMake(identifierToolClass: str, **keywordArguments: Any) -> None:  # noqa: C901
	"""Generate and write `class` `Make`.

	Parameters
	----------
	identifierToolClass : str
		Name of the tool class to generate.
	**keywordArguments : Any
		Override `ManufacturedPackageSettings`.

	Returns
	-------
	None

	"""
	global ast_stmt, guardVersion, versionMinorMinimum  # noqa: PLW0603
	ledgerOfImports: LedgerOfImports = LedgerOfImports(Make.Module([
		Make.ImportFrom("collections.abc", [Make.alias("Iterable"), Make.alias("Sequence")])
		, Make.ImportFrom("typing", [Make.alias("Any")])
		, Make.Import("ast")]))
	ledgerOfImports.addImportFrom_asStr(settingsManufacturing.identifierPackage, "ConstantValueType")
	ledgerOfImports.addImportFrom_asStr(settingsManufacturing.identifierPackage, "identifierDotAttribute")
	ledgerOfImports.addImportFrom_asStr(settingsManufacturing.identifierPackage, "ast_attributes")

	list4ClassDefBody: list[ast.stmt] = [
		docstrings[identifierToolClass][identifierToolClass]
		, FunctionDef_boolopJoinMethod
		, FunctionDef_operatorJoinMethod]

	for (ClassDefIdentifier, listFunctionDef_args, kwarg_annotationIdentifier, defaults, classAs_astAttribute, overloadDefinition,
		listCall_keyword, guardVersion, versionMinorMinimum) in getElementsMake(identifierToolClass, **keywordArguments):  # noqa: B007
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
		elif ClassDefIdentifier == "Attribute":
			list4ClassDefBody.append(FunctionDefMake_Attribute)
			continue
		elif ClassDefIdentifier == "keyword":
			list4ClassDefBody.extend(listOverloads_keyword)
			ledgerOfImports.addImportFrom_asStr("typing", "overload")

		if kwarg_annotationIdentifier != "No":
			listCall_keyword.append(keywordKeywordArguments4Call)
			ledgerOfImports.addImportFrom_asStr(settingsManufacturing.identifierPackage, kwarg_annotationIdentifier)
			ledgerOfImports.addImportFrom_asStr("typing", 'Unpack')
			kwarg: ast.arg | None = Make.arg(settingsManufacturing.keywordArgumentsIdentifier
				, annotation=Make.Subscript(Make.Name("Unpack"), slice=Make.Name(kwarg_annotationIdentifier)))
		else:
			kwarg = None
		decorator_list: list[ast.expr] = [astName_staticmethod]

		# For now, all `overloadDefinition` are `False` because overload is handled above.
		if overloadDefinition:
			decorator_list.append(astName_overload)
			body: list[ast.stmt] = [Make.Expr(Make.Constant(value=...))]
		elif ClassDefIdentifier == "Import":
			listFunctionDef_args: list[ast.arg] = list_argMake_Import  # noqa: PLW2901
			body = FunctionDef_bodyMake_Import
		else:
			body = [docstrings[identifierToolClass][ClassDefIdentifier]
				, Make.Return(Make.Call(classAs_astAttribute, list_keyword=listCall_keyword))]

		ast_stmt = Make.FunctionDef(ClassDefIdentifier
			, Make.arguments(list_arg=listFunctionDef_args, kwarg=kwarg, defaults=defaults)
			, body=body
			, decorator_list=decorator_list
			, returns=classAs_astAttribute)

		if guardVersion:
			_makeGuardVersion()
			ledgerOfImports.addImport_asStr("sys")
		if ast_stmt is not None:  # pyright: ignore[reportUnnecessaryComparison]
			list4ClassDefBody.append(ast_stmt)

	list4ModuleBody: list[ast.stmt] = [*ledgerOfImports.makeList_ast()]
	writeClass(identifierToolClass, list4ClassDefBody, list4ModuleBody)

def write_theSSOT() -> None:
	"""Write the SSOT module to disk.

	(AI generated docstring)

	Returns
	-------
	None

	"""
	writeModule(astModule_theSSOT, "_theSSOT")

def manufactureTools(settingsManufacturing: ManufacturedPackageSettings) -> None:
	"""Manufacture all tools and write generated modules.

	(AI generated docstring)

	Parameters
	----------
	settingsManufacturing : ManufacturedPackageSettings
			Settings object containing identifiers for tool generation.

	Returns
	-------
	None

	"""
	make_astTypes()
	makeToolBe(settingsManufacturing.identifiers["Be"])
	makeToolDOT(settingsManufacturing.identifiers["DOT"])
	makeToolFind(settingsManufacturing.identifiers["Be"])
	makeToolGrab(settingsManufacturing.identifiers["Grab"])
	makeToolMake(settingsManufacturing.identifiers["Make"])
	makeTool_dump()
	write_theSSOT()

if __name__ == "__main__":
	manufactureTools(settingsManufacturing)
