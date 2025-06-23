"""API for data. The rest of the package should be ignorant of the specifics of the data source.

This module provides a set of functions to interact with the data source, allowing for easy retrieval and manipulation of data.

"""

from ast import (
	alias, arg, arguments, Attribute, boolop, cmpop, comprehension, ExceptHandler, expr, expr_context, keyword, match_case,
	Name, operator, pattern, stmt, Subscript, type_param, TypeIgnore, unaryop, withitem,
)
from astToolFactory import pathRoot_typeshed, settingsManufacturing
from astToolFactory._datacenterAnnex import (
	_columns, attributeRename__attribute, attributeRename__ClassDefIdentifier_attribute, defaultValue__attribute,
	defaultValue__ClassDefIdentifier_attribute, defaultValue__type_attribute, move2keywordArguments__attribute,
	move2keywordArguments__attributeKind, type__ClassDefIdentifier_attribute,
)
from astToolkit import (
	Be, ConstantValueType as _ConstantValue, DOT, dump, identifierDotAttribute, IfThis, Make, NodeChanger, NodeTourist,
	parsePathFilename2astModule, Then,
)
from astToolkit.transformationTools import makeDictionaryClassDef
from collections.abc import Callable, Mapping, Sequence
from typing import Any, cast, Literal, TypeIs
from Z0Z_tools import raiseIfNone
import ast
import numpy
import pandas
import typeshed_client
import typing_extensions

if typing_extensions.TYPE_CHECKING:
	from pathlib import Path

"""
- Use idiomatic pandas.
- No `lambda`, except `key=lambda`.
- No intermediate data structures.
- A dataframe is a data structure: no intermediate dataframes.
- A so-called mask is an intermediate dataframe: no "masks".
- A column is a data structure: no intermediate columns.
- No `for`, no `iterrows`, no loops, no loops hidden in comprehension.
- No `zip`.
- No new functions.
- No new classes.
- No helper dataframes, no helper functions, no helper classes.
- Use idiomatic pandas.
"""

"""
Generalized flow for get* functions:
listColumnsHARDCODED
listColumns
dataframe
elementsTarget
...
_makeColumn_guardVersion
dataframe = dataframe[elementsTarget]
return list(dataframe.to_records(index=False))
"""


def _makeColumn_guardVersion(dataframe: pandas.DataFrame, byColumn: str) -> pandas.DataFrame:
	"""No summary.

	Column 'guardVersion' = False unless:
	- A `byColumn`-'versionMinorMinimum' group is larger than 1, then 'guardVersion' is a countdown
		from the total number of versions in the group.
	- Or if the only member of a group has a python version greater than `pythonMinimumVersionMinor`.

	"""
	dataframe["guardVersion"] = numpy.where(
		(
			(versionsTotal := (seriesGroupByVersion := dataframe.groupby(byColumn)["versionMinorMinimum"]).transform("nunique"))
			== 1
		)
		& (seriesGroupByVersion.transform("max") <= settingsManufacturing.pythonMinimumVersionMinor),
		False,  # noqa: FBT003
		numpy.maximum(1, versionsTotal - seriesGroupByVersion.rank(method="first", ascending=False).astype(int) + 1),
	)
	return dataframe


def _sortCaseInsensitive(
	dataframe: pandas.DataFrame,
	sortBy: Sequence[str],
	*,
	caseInsensitive: bool | Sequence[bool] = True,
	ascending: bool | Sequence[bool] = True,
) -> pandas.DataFrame:
	dataframeCopy: pandas.DataFrame = dataframe.copy()
	maskCaseInsensitive = pandas.Series(caseInsensitive, index=list(sortBy), dtype=numpy.bool)
	dataframeCopy[maskCaseInsensitive[maskCaseInsensitive].index] = dataframe[maskCaseInsensitive[maskCaseInsensitive].index].map(  # pyright: ignore[reportArgumentType]
		str.lower
	)

	indicesSorted = dataframeCopy.sort_values(by=sortBy, ascending=ascending).index
	return dataframe.loc[indicesSorted]


def getDataframe(*indices: str, **keywordArguments: Any) -> pandas.DataFrame:
	pathFilename: Path = keywordArguments.get("pathFilename") or settingsManufacturing.pathFilenameDataframeAST
	includeDeprecated: bool = keywordArguments.get("includeDeprecated") or settingsManufacturing.includeDeprecated
	versionMinorMaximum: int | None = keywordArguments.get("versionMinorMaximum") or settingsManufacturing.versionMinorMaximum
	modifyVersionMinorMinimum: bool = keywordArguments.get("modifyVersionMinorMinimum") or True

	dataframe: pandas.DataFrame = pandas.read_pickle(pathFilename)  # noqa: S301

	if not includeDeprecated:
		dataframe = dataframe[~dataframe["deprecated"]]

	if versionMinorMaximum is not None:
		dataframe = dataframe[dataframe["versionMinorPythonInterpreter"] <= versionMinorMaximum]

	if modifyVersionMinorMinimum:
		columnsVersion: list[str] = ["versionMinorMinimumAttribute", "versionMinorMinimumClass", "versionMinorMinimum_match_args"]
		dataframe[columnsVersion] = dataframe[columnsVersion].where(  # pyright: ignore[reportArgumentType]
			dataframe[columnsVersion] > settingsManufacturing.pythonMinimumVersionMinor, -1
		)
	if indices:
		dataframe = dataframe.set_index(list(indices))

	return dataframe


def getElementsBe(
	identifierToolClass: str,  # noqa: ARG001
	**keywordArguments: Any,
) -> list[tuple[str, int, ast.expr, list[tuple[str, ast.expr]]]]:
	listColumnsHARDCODED: list[str] = [
		"ClassDefIdentifier",
		"versionMinorMinimumClass",
		"classAs_astAttribute",
		"listTupleAttributes",
	]
	listColumns: list[str] = listColumnsHARDCODED
	del listColumnsHARDCODED

	sortBy: list[str] = listColumns[0:2]
	caseInsensitive: list[bool] = [True, False]
	ascending: list[bool] = caseInsensitive.copy()
	drop_duplicates: list[str] = sortBy.copy()

	dataframe: pandas.DataFrame = (
		getDataframe(**keywordArguments)[listColumns]
		.drop_duplicates(drop_duplicates, keep="last")
		.pipe(_sortCaseInsensitive, sortBy, caseInsensitive=caseInsensitive, ascending=ascending)
		.reset_index(drop=True)
	)
	del listColumns

	return dataframe.to_records(index=False).tolist()


def getElementsDOT(identifierToolClass: str, **keywordArguments: Any) -> list[tuple[str, bool, str, list[ast.expr], int, int]]:  # noqa: ARG001
	listColumnsHARDCODED: list[str] = [
		"attribute",
		"TypeAlias_hasDOTSubcategory",
		"versionMinorMinimumAttribute",
		"type_ast_expr",
		"type",
		"TypeAlias_hasDOTIdentifier",
	]
	listColumns: list[str] = listColumnsHARDCODED
	del listColumnsHARDCODED

	sortBy: list[str] = listColumns[0:3]
	caseInsensitive: list[bool] = [True, True, False]
	ascending: list[bool] = caseInsensitive.copy()
	drop_duplicates: list[str] = listColumns[0:2]

	index_type_ast_expr: int = 3
	index_versionMinorMinimum: int = 2

	dataframe: pandas.DataFrame = (
		getDataframe(**keywordArguments)
		.query("attributeKind == '_field'")
		.pipe(_sortCaseInsensitive, sortBy, caseInsensitive=caseInsensitive, ascending=ascending)[listColumns]
		.drop_duplicates(drop_duplicates, keep="last")
		.reset_index(drop=True)
	)

	dataframe = dataframe.rename(
		columns={
			listColumns[index_type_ast_expr]: "type_ast_expr",
			listColumns[index_versionMinorMinimum]: "versionMinorMinimum",
		},
	)

	del listColumns

	elementsTarget: list[str] = [
		"identifierTypeOfNode",
		"overloadDefinition",
		"attribute",
		"list_ast_expr",
		"guardVersion",
		"versionMinorMinimum",
	]

	# dataframe['identifierTypeOfNode'] = dataframe['TypeAlias_hasDOTSubcategory'].where(
	# 	dataframe['attribute'].map(dataframe['attribute'].value_counts()) > 1
	# 	, dataframe['TypeAlias_hasDOTIdentifier']
	# )
	# dataframe['overloadDefinition'] = dataframe['attribute'].map(dataframe['attribute'].value_counts()) > 1
	# dataframe['list_ast_expr'] = dataframe['type_ast_expr'].apply(lambda srsly: [srsly])

	# currentColumns: list[str] = ['TypeAlias_hasDOTIdentifier', 'identifierTypeOfNode', 'overloadDefinition', 'attribute', 'list_ast_expr', 'versionMinorMinimum',]
	# dataframe = dataframe[currentColumns]

	# #idk

	# byColumn: str = 'identifierTypeOfNode'
	# dataframe = _makeColumn_guardVersion(dataframe, byColumn)

	# dataframe = dataframe[elementsTarget]
	# return dataframe.to_records(index=False).tolist()

	dataframe["overloadDefinition"] = dataframe.groupby("attribute").transform("size") > 1
	dataframeImplementationFunctionDefinitions: pandas.DataFrame = (
		dataframe[dataframe["overloadDefinition"]]
		.groupby("attribute")["versionMinorMinimum"]
		.unique()
		.explode()
		.reset_index()
		.merge(dataframe[["attribute", "TypeAlias_hasDOTIdentifier"]].drop_duplicates("attribute"), on="attribute", how="left")
		.assign(
			overloadDefinition=False,
			TypeAlias_hasDOTSubcategory="No",
			type_ast_expr="No",
			type="No",
		)[dataframe.columns]
	)
	dataframe = cast(
		"pandas.DataFrame",
		(
			pandas.concat([dataframe, dataframeImplementationFunctionDefinitions], ignore_index=True)  # pyright: ignore[reportCallIssue, reportArgumentType]
			.assign(__sequence_in_group=lambda df: df.groupby("attribute").cumcount())
			.sort_values(["attribute", "__sequence_in_group"], kind="stable")
			.drop(columns="__sequence_in_group")
		),
	)
	del dataframeImplementationFunctionDefinitions

	dataframe["identifierTypeOfNode"] = dataframe["TypeAlias_hasDOTSubcategory"].where(
		dataframe["overloadDefinition"], dataframe["TypeAlias_hasDOTIdentifier"]
	)
	dataframe = dataframe.drop(
		columns=[
			"TypeAlias_hasDOTIdentifier",
			"TypeAlias_hasDOTSubcategory",
		],
	)

	def makeColumn_list_ast_expr(dataframeTarget: pandas.DataFrame) -> list[ast.expr]:
		if bool(dataframeTarget["overloadDefinition"]):
			return [cast("ast.expr", dataframeTarget["type_ast_expr"])]
		matchingRows: pandas.DataFrame = (
			dataframe.loc[
				(dataframe["attribute"] == dataframeTarget["attribute"])
				& (dataframe["type"] != "No")
				& (dataframe["versionMinorMinimum"] <= dataframeTarget["versionMinorMinimum"]),
				["type_ast_expr", "type"],
			]
			.drop_duplicates(subset="type")
			.sort_values("type", key=lambda x: x.str.lower())
		)

		return matchingRows["type_ast_expr"].tolist()

	dataframe["list_ast_expr"] = dataframe.apply(makeColumn_list_ast_expr, axis="columns")
	dataframe = dataframe.drop(
		columns=[
			"type_ast_expr",
			"type",
		],
	)

	byColumn: str = "identifierTypeOfNode"
	dataframe = _makeColumn_guardVersion(dataframe, byColumn)

	dataframe = dataframe[elementsTarget]
	return list(dataframe.to_records(index=False))


def getElementsGrab(identifierToolClass: str, **keywordArguments: Any) -> list[tuple[str, list[ast.expr], str, int, int]]:  # noqa: ARG001
	listColumnsHARDCODED: list[str] = [
		"attribute",
		"type_astSuperClasses",
		"versionMinorMinimumAttribute",
		"TypeAlias_hasDOTIdentifier",
		"type_astSuperClasses_ast_expr",
	]
	listColumns: list[str] = listColumnsHARDCODED
	del listColumnsHARDCODED

	sortBy: list[str] = listColumns[0:3]
	caseInsensitive: list[bool] = [True, True, False]
	ascending: list[bool] = caseInsensitive.copy()
	drop_duplicates: list[str] = listColumns[0:2]

	index_type: int = 1
	index_type_ast_expr: int = 4
	index_versionMinorMinimum: int = 2

	dataframe: pandas.DataFrame = (
		getDataframe(**keywordArguments)
		.query("attributeKind == '_field'")[listColumns]
		.pipe(_sortCaseInsensitive, sortBy, caseInsensitive=caseInsensitive, ascending=ascending)
		.drop_duplicates(drop_duplicates, keep="last")
		.reset_index(drop=True)
	)

	dataframe = dataframe.rename(
		columns={
			listColumns[index_type]: "type",
			listColumns[index_type_ast_expr]: "type_ast_expr",
			listColumns[index_versionMinorMinimum]: "versionMinorMinimum",
		},
	)

	del listColumns

	elementsTarget: list[str] = [
		"TypeAlias_hasDOTIdentifier",
		"list_ast_expr",
		"attribute",
		"guardVersion",
		"versionMinorMinimum",
	]

	def makeColumn_list_ast_expr(dataframeTarget: pandas.DataFrame) -> list[ast.expr]:
		matchingRows: pandas.DataFrame = dataframe.loc[
			(dataframe["attribute"] == dataframeTarget["attribute"])
			& (dataframe["versionMinorMinimum"] <= dataframeTarget["versionMinorMinimum"]),
			["type_ast_expr", "type"],
		].sort_values("type", key=lambda x: x.str.lower())

		return matchingRows["type_ast_expr"].tolist()

	dataframe["list_ast_expr"] = dataframe.apply(makeColumn_list_ast_expr, axis="columns")

	byColumn: str = "attribute"
	dataframe = _makeColumn_guardVersion(dataframe, byColumn)

	dataframe = dataframe[elementsTarget].drop_duplicates(subset=elementsTarget[2:None], keep="last").reset_index(drop=True)

	return list(dataframe.to_records(index=False))


def getElementsMake(
	identifierToolClass: str,  # noqa: ARG001
	**keywordArguments: Any,
) -> list[tuple[str, list[ast.arg], str, list[ast.expr], ast.expr, bool, list[ast.keyword], int, int]]:
	listColumnsHARDCODED: list[str] = [
		"ClassDefIdentifier",
		"versionMinorMinimumClass",
		"versionMinorMinimum_match_args",
		"listFunctionDef_args",
		"kwarg_annotationIdentifier",
		"listDefaults",
		"classAs_astAttribute",
		"listCall_keyword",
	]
	listColumns: list[str] = listColumnsHARDCODED
	del listColumnsHARDCODED

	sortBy: list[str] = listColumns[0:3]
	caseInsensitive: list[bool] = [True, False, False]
	ascending: list[bool] = caseInsensitive.copy()
	drop_duplicates: list[str] = sortBy.copy()

	index_versionMinorMinimum: int = 2

	dataframe: pandas.DataFrame = (
		getDataframe(**keywordArguments)[listColumns]
		.pipe(_sortCaseInsensitive, sortBy, caseInsensitive=caseInsensitive, ascending=ascending)
		.drop_duplicates(drop_duplicates)
		.reset_index(drop=True)
	)
	dataframe = dataframe.rename(columns={listColumns[index_versionMinorMinimum]: "versionMinorMinimum"})
	del listColumns

	elementsTarget: list[str] = [
		"ClassDefIdentifier",
		"listFunctionDef_args",
		"kwarg_annotationIdentifier",
		"listDefaults",
		"classAs_astAttribute",
		"overloadDefinition",
		"listCall_keyword",
		"guardVersion",
		"versionMinorMinimum",
	]

	byColumn: str = "ClassDefIdentifier"
	dataframe = _makeColumn_guardVersion(dataframe, byColumn)

	# TODO Create overloadDefinition flag - False until new logic added
	dataframe["overloadDefinition"] = False

	dataframe = dataframe[elementsTarget]
	return list(dataframe.to_records(index=False))


def getElementsTypeAlias(**keywordArguments: Any) -> list[tuple[str, list[ast.expr], int, int]]:
	listColumnsHARDCODED: list[str] = [
		"attribute",
		"TypeAlias_hasDOTSubcategory",
		"ClassDefIdentifier",
		"versionMinorMinimumAttribute",
		"classAs_astAttribute",
		"TypeAlias_hasDOTIdentifier",
	]
	listColumns: list[str] = listColumnsHARDCODED
	del listColumnsHARDCODED

	sortBy: list[str] = listColumns[0:4]
	caseInsensitive: list[bool] = [True, True, True, False]
	ascending: list[bool] = caseInsensitive.copy()
	drop_duplicates: list[str] = sortBy.copy()

	index_versionMinorMinimum: int = 3

	dataframe: pandas.DataFrame = (
		getDataframe(**keywordArguments)
		.query("attributeKind == '_field'")[listColumns]
		.pipe(_sortCaseInsensitive, sortBy, caseInsensitive=caseInsensitive, ascending=ascending)
		.drop_duplicates(drop_duplicates, keep="last")
		.reset_index(drop=True)
	)
	dataframe = dataframe.rename(columns={listColumns[index_versionMinorMinimum]: "versionMinorMinimum"})
	del listColumns

	elementsTarget: list[str] = ["identifierTypeAlias", "list4TypeAlias_value", "guardVersion", "versionMinorMinimum"]

	def makeColumn_list4TypeAlias_value(dataframeTarget: pandas.DataFrame) -> tuple[list[Any], str]:
		matchingRows: pandas.DataFrame = (
			dataframe.loc[
				(dataframe["TypeAlias_hasDOTSubcategory"] == dataframeTarget["TypeAlias_hasDOTSubcategory"])
				& (dataframe["ClassDefIdentifier"] != "No")
				& (dataframe["versionMinorMinimum"] <= dataframeTarget["versionMinorMinimum"]),
				["classAs_astAttribute", "ClassDefIdentifier"],
			]
			.drop_duplicates(subset="ClassDefIdentifier")
			.sort_values("ClassDefIdentifier", key=lambda x: x.str.lower())
		)

		return matchingRows["classAs_astAttribute"].tolist(), str(matchingRows["ClassDefIdentifier"].tolist())

	dataframe[["list4TypeAlias_value", "hashable_list4TypeAlias_value"]] = dataframe.apply(  # pyright: ignore[reportArgumentType]
		makeColumn_list4TypeAlias_value, axis="columns", result_type="expand"
	)
	dataframe = dataframe.drop_duplicates(
		subset=["attribute", "TypeAlias_hasDOTSubcategory", "versionMinorMinimum", "hashable_list4TypeAlias_value"]
	)

	dataframe = (
		dataframe.sort_values("versionMinorMinimum", ascending=False)
		.groupby("attribute")[dataframe.columns]
		.apply(
			lambda group: group
			if group["TypeAlias_hasDOTSubcategory"].nunique() == 1
			else pandas.concat(
				[
					group,
					group.drop_duplicates(subset="TypeAlias_hasDOTSubcategory", keep="last")[["versionMinorMinimum"]]
					.drop_duplicates()
					.assign(
						attribute=group["attribute"].iloc[0],
						TypeAlias_hasDOTSubcategory="No",
						TypeAlias_hasDOTIdentifier=group["TypeAlias_hasDOTIdentifier"].iloc[0],
						list4TypeAlias_value="No",
					),
				]
			)  # pyright: ignore[reportCallIssue, reportArgumentType]
		)
		.reset_index(drop=True)
	)

	def MakeName4TypeAlias(subcategoryName: str) -> ast.Name:
		return Make.Name(subcategoryName)

	def updateColumn_list4TypeAlias_value(dataframeTarget: pandas.DataFrame) -> list[ast.expr]:
		matchingRows: pandas.DataFrame = dataframe.loc[
			(dataframe["attribute"] == dataframeTarget["attribute"])
			& (dataframe["TypeAlias_hasDOTSubcategory"] != "No")
			& (dataframe["versionMinorMinimum"] <= dataframeTarget["versionMinorMinimum"]),
			["TypeAlias_hasDOTSubcategory"],
		].drop_duplicates()

		return [MakeName4TypeAlias(subcategory) for subcategory in matchingRows["TypeAlias_hasDOTSubcategory"]]

	mask = dataframe["list4TypeAlias_value"] == "No"
	dataframe.loc[mask, "list4TypeAlias_value"] = dataframe.loc[mask].apply(updateColumn_list4TypeAlias_value, axis="columns")

	dataframe["identifierTypeAlias"] = dataframe["TypeAlias_hasDOTIdentifier"].where(
		dataframe.groupby("attribute")["TypeAlias_hasDOTSubcategory"].transform("nunique") == 1,
		dataframe["TypeAlias_hasDOTSubcategory"].where(
			dataframe["TypeAlias_hasDOTSubcategory"] != "No", dataframe["TypeAlias_hasDOTIdentifier"]
		),
	)

	byColumn: str = "identifierTypeAlias"
	dataframe = _makeColumn_guardVersion(dataframe, byColumn)

	dataframe = dataframe[elementsTarget]
	return list(dataframe.to_records(index=False))


def updateDataframe() -> None:  # noqa: C901, PLR0915
	dataframe: pandas.DataFrame = getDataframe(
		includeDeprecated=True, versionMinorMaximum=settingsManufacturing.versionMinorMaximum, modifyVersionMinorMinimum=False
	)

	# columns: reorder; drop columns, but they might be recreated later in the flow.
	# dataframe = dataframe[_columns]

	# Set dtypes for existing columns
	dataframe = dataframe.astype(
		{
			"ClassDefIdentifier": "string",
			"versionMajorPythonInterpreter": "int64",
			"versionMinorPythonInterpreter": "int64",
			"versionMicroPythonInterpreter": "int64",
			"base": "string",
		}
	)
	# Initialize hashable columns metadata
	dataframe.attrs["hashable"] = [
		"ClassDefIdentifier",
		"versionMajorPythonInterpreter",
		"versionMinorPythonInterpreter",
		"versionMicroPythonInterpreter",
		"base",
	]
	dataframe.attrs["drop_duplicates"] = [
		"ClassDefIdentifier",
		"versionMinorPythonInterpreter",
	]

	# TODO Columns to create using the Python Interpreter,
	# from version 3.settingsManufacturing.versionMinor_astMinimumSupported
	# to version 3.settingsManufacturing.versionMinorMaximum, inclusive.
	# 'ClassDefIdentifier',
	# 'versionMajorPythonInterpreter',
	# 'versionMinorPythonInterpreter',
	# 'versionMicroPythonInterpreter',
	# 'base',

	ImaSearchContext: typeshed_client.SearchContext = typeshed_client.get_search_context(typeshed=pathRoot_typeshed)
	astModule_astStub: ast.Module = parsePathFilename2astModule(
		raiseIfNone(typeshed_client.get_stub_file("ast", search_context=ImaSearchContext))
	)

	dictionaryClassDef: dict[str, ast.ClassDef] = makeDictionaryClassDef(astModule_astStub)
	list_astIf_sys_version_info: list[ast.If] = []
	NodeTourist(
		Be.If.testIs(Be.Compare.leftIs(IfThis.isAttributeNamespaceIdentifier("sys", "version_info"))),
		doThat=Then.appendTo(list_astIf_sys_version_info),
	).visit(astModule_astStub)

	dictionaryIdentifier2astIf: dict[str, ast.If] = {}
	for astIf in list_astIf_sys_version_info:
		NodeTourist(Be.ClassDef, Then.updateKeyValueIn(DOT.name, lambda _node: astIf, dictionaryIdentifier2astIf)).visit(astIf)  # noqa: B023

	def get_match_argsByVersionGuard(dataframeTarget: pandas.DataFrame) -> pandas.Series:
		def filterByVersion(node: ast.AST, *, orelse: bool = False) -> bool:
			thisNode: bool = False
			if Be.If(node) and Be.Compare(node.test):  # noqa: SIM102
				if (
					IfThis.isAttributeNamespaceIdentifier("sys", "version_info")(node.test.left)
					and Be.Tuple(node.test.comparators[0])
					and IfThis.isConstant_value(dataframeTarget["versionMinorPythonInterpreter"] + orelse)(
						node.test.comparators[0].elts[1]
					)
				):
					thisNode = True
			return thisNode

		def findThis_body(node: ast.AST) -> bool:
			thisNode: bool = False
			if filterByVersion(node, orelse=False):  # noqa: SIM102
				if IfThis.isAssignAndTargets0Is(IfThis.isNameIdentifier("__match_args__"))(cast("ast.If", node).body[0]):
					thisNode = True
			return thisNode

		def findThis_orelse(node: ast.AST) -> bool:
			thisNode: bool = False
			if filterByVersion(node, orelse=True) and cast("ast.If", node).orelse:  # noqa: SIM102
				if IfThis.isAssignAndTargets0Is(IfThis.isNameIdentifier("__match_args__"))(cast("ast.If", node).orelse[0]):
					thisNode = True
			return thisNode

		def getNaked_match_args() -> list[ast.stmt] | None:
			body: list[ast.stmt] | None = None
			if nodeIf := dictionaryIdentifier2astIf.get(cast("str", dataframeTarget["ClassDefIdentifier"])):  # noqa: SIM102
				# `node` is an `ast.If` node. dataframeTarget['ClassDefIdentifier'] is in `ast.If.body`.
				if filterByVersion(nodeIf, orelse=False):
					# And, version == dataframeTarget['versionMinorPythonInterpreter']
					def findThis_match_args(node: ast.AST) -> bool:
						thisNode: bool = False
						# look for dataframeTarget['ClassDefIdentifier'] and return match_args or None
						if IfThis.isClassDefIdentifier(cast("str", dataframeTarget["ClassDefIdentifier"]))(node):  # noqa: SIM102
							if IfThis.isAssignAndTargets0Is(IfThis.isNameIdentifier("__match_args__"))(
								cast("ast.ClassDef", node).body[0]
							):
								thisNode = True
						return thisNode

					body = NodeTourist(
						findThis_match_args, Then.extractIt(cast("Callable[[ast.ClassDef], list[ast.stmt]]", DOT.body))
					).captureLastMatch(nodeIf)
			return body

		dataframeTarget["match_args"] = None  # Default value for the column

		body: list[ast.stmt] | None = NodeTourist(
			findThis_body, Then.extractIt(cast("Callable[[ast.If], list[ast.stmt]]", DOT.body))
		).captureLastMatch(dictionaryClassDef[cast("str", dataframeTarget["ClassDefIdentifier"])])
		if body:
			dataframeTarget["match_args"] = ast.literal_eval(cast("ast.Assign", body[0]).value)
		else:
			orelse: list[ast.stmt] | None = NodeTourist(
				findThis_orelse, Then.extractIt(cast("Callable[[ast.If], list[ast.stmt]]", DOT.orelse))
			).captureLastMatch(dictionaryClassDef[cast("str", dataframeTarget["ClassDefIdentifier"])])
			if orelse:
				dataframeTarget["match_args"] = ast.literal_eval(cast("ast.Assign", orelse[0]).value)
			else:
				naked_match_args: list[ast.stmt] | None = getNaked_match_args()
				if naked_match_args:
					dataframeTarget["match_args"] = ast.literal_eval(cast("ast.Assign", naked_match_args[0]).value)
		return dataframeTarget["match_args"]

	dataframe["match_args"] = dataframe[["ClassDefIdentifier", "versionMinorPythonInterpreter"]].apply(
		get_match_argsByVersionGuard, axis="columns"
	)
	dataframe.attrs["hashable"].extend(["match_args"])
	dataframe.attrs["drop_duplicates"].extend(["match_args"])

	dataframe.pipe(
		_sortCaseInsensitive,
		["ClassDefIdentifier", "versionMinorPythonInterpreter"],
		caseInsensitive=[True, False],
		ascending=[True, False],
	)
	# Assign 'match_args' from 'versionMinorPythonInterpreter' < your version.
	dataframe["match_args"] = dataframe.groupby("ClassDefIdentifier")["match_args"].bfill()
	# Because Python 3.9 does not have `__match_args__`, Assign 'match_args' from 'versionMinorPythonInterpreter' > your version.
	dataframe["match_args"] = dataframe.groupby("ClassDefIdentifier")["match_args"].ffill()

	# Fill missing 'match_args' values with empty tuple
	dataframe["match_args"] = dataframe["match_args"].apply(lambda x: () if pandas.isna(x) else x)

	def amIDeprecated(ClassDefIdentifier: str) -> bool:
		return bool(
			NodeTourist(IfThis.isCallIdentifier("deprecated"), doThat=Then.extractIt).captureLastMatch(
				Make.Module(cast("list[ast.stmt]", dictionaryClassDef[ClassDefIdentifier].decorator_list))
			)
		)

	dataframe["deprecated"] = pandas.Series(data=False, index=dataframe.index, dtype=bool, name="deprecated")
	dataframe.attrs["hashable"].extend(["deprecated"])
	dataframe["deprecated"] = dataframe["ClassDefIdentifier"].apply(amIDeprecated)

	def newRowsFrom_match_args(dataframeTarget: pandas.DataFrame) -> pandas.DataFrame:
		dataframeTarget = dataframeTarget[dataframeTarget["match_args"] != ()]

		# Explode match_args tuples into separate rows
		dataframeTarget = (
			dataframeTarget.assign(attribute=dataframeTarget["match_args"]).explode("attribute").reset_index(drop=True)
		)
		# Add required columns
		dataframeTarget["attributeKind"] = "_field"

		def get_type_ast_expr(dddataframeee: pandas.DataFrame) -> tuple[pandas.Series, pandas.Series]:
			getAnnotation = NodeTourist[ast.AnnAssign, ast.expr](
				Be.AnnAssign.targetIs(IfThis.isNameIdentifier(cast("str", dddataframeee["attribute"]))),
				Then.extractIt(DOT.annotation),
			)
			type_ast_expr: ast.expr = raiseIfNone(
				getAnnotation.captureLastMatch(dictionaryClassDef[cast("str", dddataframeee["ClassDefIdentifier"])])
			)

			type_ast_expr = NodeChanger(
				Be.Subscript.valueIs(IfThis.isNameIdentifier("Literal")), Then.replaceWith(Make.Name("bool"))
			).visit(type_ast_expr)

			dddataframeee["type_ast_expr"] = NodeChanger[ast.Name, ast.expr](
				(
					lambda node: Be.Name(node)
					and isinstance(ast.literal_eval(node.id), type)
					and issubclass(ast.literal_eval(node.id), ast.AST)
				),
				lambda node: Make.Attribute(Make.Name("ast"), ast.literal_eval(node.id).__name__),
			).visit(type_ast_expr)
			dddataframeee["type"] = ast.unparse(cast("ast.AST", dddataframeee["type_ast_expr"]))

			return dddataframeee["type_ast_expr"], dddataframeee["type"]

		dataframeTarget[["type_ast_expr", "type"]] = dataframeTarget.apply(
			get_type_ast_expr, axis="columns", result_type="expand"
		)

		return dataframeTarget

	dataframe = cast(
		"pandas.DataFrame",
		pandas.concat([dataframe, newRowsFrom_match_args(dataframe)], ignore_index=True, axis="rows"),  # pyright: ignore[reportCallIssue, reportArgumentType]
	)
	# `(function) extend: Any` because concat sucks
	dataframe.attrs["hashable"].extend(["attribute", "attributeKind", "type"])
	dataframe.attrs["drop_duplicates"].extend(["attribute"])
	dataframe["type"] = (
		dataframe[["ClassDefIdentifier", "attribute"]]
		.apply(tuple, axis="columns")
		.map(type__ClassDefIdentifier_attribute)
		.fillna(dataframe["type"])
	)
	dataframe = dataframe.drop_duplicates(subset=dataframe.attrs["drop_duplicates"], keep="last")

	def pythonCode2expr(string: str) -> Any:
		astModule: ast.Module = ast.parse(string)
		ast_expr: ast.expr = raiseIfNone(NodeTourist(Be.Expr, Then.extractIt(DOT.value)).captureLastMatch(astModule))
		return ast_expr

	def newRows_attributes(dataframeTarget: pandas.DataFrame) -> pandas.DataFrame:
		_attribute_ast_expr = NodeTourist(
			Be.Subscript.valueIs(IfThis.isNameIdentifier("Unpack")),
			Then.extractIt(DOT.slice),
		).captureLastMatch(dictionaryClassDef[cast("str", dataframeTarget["ClassDefIdentifier"])])
		if _attribute_ast_expr:
			if Be.Name(_attribute_ast_expr):
				_attributes = int | None
			elif Be.Subscript(_attribute_ast_expr):
				_attributes = int
		else:
			_attributes = None

		dataframeTarget["attributeKind"] = "_attribute"
		# TODO get class _Attributes, and get the key names and annotations
		dictionary_Attributes: dict[str, ast.expr] = {}
		NodeTourist[ast.AnnAssign, Mapping[str, ast.expr]](
			findThis=Be.AnnAssign.targetIs(Be.Name),
			doThat=Then.updateKeyValueIn(DOT.target(DOT.id), DOT.annotation, dictionary_Attributes),  # pyright: ignore[reportCallIssue, reportArgumentType]
		).visit(dictionaryClassDef[cast("str", dataframeTarget["ClassDefIdentifier"])])

		Make.ClassDef(
			name="_Attributes",
			bases=[ast.Name("TypedDict"), ast.Subscript(value=ast.Name("Generic"), slice=ast.Name("_EndPositionT"))],
			body=[
				Make.AnnAssign(target=ast.Name("lineno", ast.Store()), annotation=ast.Name("int")),
				Make.AnnAssign(target=ast.Name("col_offset", ast.Store()), annotation=ast.Name("int")),
				Make.AnnAssign(target=ast.Name("end_lineno", ast.Store()), annotation=ast.Name("_EndPositionT")),
				Make.AnnAssign(target=ast.Name("end_col_offset", ast.Store()), annotation=ast.Name("_EndPositionT")),
			],
		)
		return dataframeTarget

	# dataframe = cast(pandas.DataFrame, pandas.concat([dataframe, newRows_attributes(dataframe)], ignore_index=True, axis='rows'))
	# dataframe.drop_duplicates(subset=dataframe.attrs['hashable'], inplace=True)

	# Create 'attributeRename'
	dataframe["attributeRename"] = pandas.Series(
		data=dataframe["attribute"], index=dataframe.index, dtype=str, name="attributeRename", copy=True
	)
	dataframe["attributeRename"] = dataframe["attribute"].map(attributeRename__attribute).fillna(dataframe["attributeRename"])
	dataframe["attributeRename"] = (
		dataframe[["ClassDefIdentifier", "attribute"]]
		.apply(tuple, axis="columns")
		.map(attributeRename__ClassDefIdentifier_attribute)
		.fillna(dataframe["attributeRename"])
	)

	dataframe["move2keywordArguments"] = False  # Default value for the column
	dataframe["move2keywordArguments"] = (
		dataframe["attributeKind"].map(move2keywordArguments__attributeKind).fillna(dataframe["move2keywordArguments"])
	)
	dataframe["move2keywordArguments"] = (
		dataframe["attribute"].map(move2keywordArguments__attribute).fillna(dataframe["move2keywordArguments"])
	)

	dataframe["defaultValue"] = "No"  # Default value for the column
	dataframe["defaultValue"] = dataframe["attribute"].map(defaultValue__attribute).fillna(dataframe["defaultValue"])
	dataframe["defaultValue"] = (
		dataframe[["ClassDefIdentifier", "attribute"]]
		.apply(tuple, axis="columns")
		.map(defaultValue__ClassDefIdentifier_attribute)
		.fillna(dataframe["defaultValue"])
	)
	dataframe["defaultValue"] = (
		dataframe[["type", "attribute"]]
		.apply(tuple, axis="columns")
		.map(defaultValue__type_attribute)
		.fillna(dataframe["defaultValue"])
	)

	def makeColumn_classAs_astAttribute(ClassDefIdentifier: str) -> ast.expr:
		return Make.Attribute(Make.Name("ast"), ClassDefIdentifier)

	dataframe["classAs_astAttribute"] = dataframe["ClassDefIdentifier"].astype(str).map(makeColumn_classAs_astAttribute)

	# Create 'list2Sequence' based on 'type' and 'astSuperClasses'
	dataframe["list2Sequence"] = pandas.Series(data=False, index=dataframe.index, dtype=bool, name="list2Sequence")
	containsListSuperClass = pandas.Series(data=False, index=dataframe.index, dtype=bool)
	for ClassDefIdentifier in settingsManufacturing.astSuperClasses:
		containsListSuperClass |= dataframe["type"].str.contains("list", regex=False, na=False) & dataframe["type"].str.contains(
			ClassDefIdentifier, regex=False, na=False
		)
	dataframe.loc[containsListSuperClass, "list2Sequence"] = True
	del containsListSuperClass

	# Create 'type_ast_expr' based on columns 'type' and 'list2Sequence'
	dataframe.loc[dataframe["list2Sequence"], "type_ast_expr"] = (
		dataframe["type"].str.replace("list", "Sequence").apply(pythonCode2expr)
	)
	dataframe.loc[~dataframe["list2Sequence"], "type_ast_expr"] = dataframe["type"].apply(pythonCode2expr)
	dataframe.loc[dataframe["type"] == "No", "type_ast_expr"] = "No"

	# Create 'type_astSuperClasses' with TypeVar substitutions
	dataframe["type_astSuperClasses"] = dataframe["type"].replace(
		{
			f"ast.{ClassDefIdentifier}": identifierTypeVar
			for ClassDefIdentifier, identifierTypeVar in settingsManufacturing.astSuperClasses.items()
		},
		regex=True,
	)
	# Create 'type_astSuperClasses_ast_expr'
	dataframe["type_astSuperClasses_ast_expr"] = numpy.where(
		dataframe["type_astSuperClasses"] == "No", "No", dataframe["type_astSuperClasses"].apply(pythonCode2expr)
	)

	def makeColumn_ast_arg(dataframeTarget: pandas.DataFrame) -> Any:
		if cast("str | bool", dataframeTarget["move2keywordArguments"]) != False:  # noqa: E712
			return "No"
		return Make.arg(
			cast("str", dataframeTarget["attributeRename"]), annotation=cast("ast.expr", dataframeTarget["type_ast_expr"])
		)

	dataframe["ast_arg"] = dataframe.apply(makeColumn_ast_arg, axis="columns")

	# Create TypeAlias_hasDOTIdentifier
	dataframe["TypeAlias_hasDOTIdentifier"] = numpy.where(
		dataframe["attributeKind"] == "_field", "hasDOT" + cast("str", dataframe["attribute"]), "No"
	)

	# Create TypeAlias_hasDOTSubcategory
	dataframe["TypeAlias_hasDOTSubcategory"] = numpy.where(
		(attribute := dataframe["TypeAlias_hasDOTIdentifier"]) == "No",
		"No",
		cast("str", attribute)
		+ "_"
		+ dataframe["type"]
		.str.replace("|", "Or", regex=False)
		.str.replace("[", "_", regex=False)
		.str.replace("[\\] ]", "", regex=True)
		.str.replace("ast.", "", regex=False),
	)

	# === Group-Based Column Computation ===
	def computeVersionMinimum(list_byColumns: list[str]) -> numpy.ndarray[tuple[int, ...], numpy.dtype[numpy.int64]]:
		return numpy.where(
			dataframe.groupby(list_byColumns)["versionMinorPythonInterpreter"].transform("min")
			== settingsManufacturing.versionMinor_astMinimumSupported,
			-1,
			dataframe.groupby(list_byColumns)["versionMinorPythonInterpreter"].transform("min"),
		)

	dataframe["versionMinorMinimum_match_args"] = computeVersionMinimum(["ClassDefIdentifier", "match_args"])
	dataframe["versionMinorMinimumAttribute"] = computeVersionMinimum(["ClassDefIdentifier", "attribute"])
	dataframe["versionMinorMinimumClass"] = computeVersionMinimum(["ClassDefIdentifier"])

	def make3Columns4ClassMake(
		dataframeTarget: pandas.DataFrame,
	) -> tuple[pandas.Series, pandas.Series, pandas.Series, pandas.Series]:
		matchingRows: pandas.DataFrame = dataframe[
			(dataframe["ClassDefIdentifier"] == cast("str", dataframeTarget["ClassDefIdentifier"]))
			& (dataframe["versionMinorMinimum_match_args"] == cast("int", dataframeTarget["versionMinorMinimum_match_args"]))
		]

		matchingRows_listTupleAttributes = matchingRows[matchingRows["attributeKind"] == "_field"].copy()
		dataframeTarget["listTupleAttributes"] = (
			matchingRows_listTupleAttributes.drop_duplicates(subset="attribute")[["attribute", "type_ast_expr"]]
			.apply(tuple, axis="columns")
			.tolist()
		)

		matchingRows["attribute"] = pandas.Categorical(
			matchingRows["attribute"], categories=matchingRows["match_args"].iloc[0], ordered=True
		)

		matchingRows_listCall_keyword: pandas.DataFrame = matchingRows[matchingRows["move2keywordArguments"] != "No"].copy(
			deep=True
		)
		matchingRows = matchingRows[matchingRows["move2keywordArguments"] == False].sort_values("attribute")  # noqa: E712
		matchingRows_listDefaults = matchingRows[matchingRows["defaultValue"] != "No"].copy(deep=True)

		dataframeTarget["listFunctionDef_args"] = matchingRows.drop_duplicates(subset="attribute")["ast_arg"].tolist()
		dataframeTarget["listDefaults"] = matchingRows_listDefaults.drop_duplicates(subset="attribute")["defaultValue"].tolist()

		matchingRows_listCall_keyword = (
			matchingRows_listCall_keyword[matchingRows_listCall_keyword["move2keywordArguments"] != "Unpack"]
			.drop_duplicates(subset="attribute")
			.sort_values("attribute")
		)

		def make_keyword(thisIsNotA_row: pandas.DataFrame) -> Any:
			if cast("bool", thisIsNotA_row["move2keywordArguments"]):
				keywordValue: ast.expr = cast("ast.expr", thisIsNotA_row["defaultValue"])
			else:
				keywordValue = Make.Name(cast("str", thisIsNotA_row["attributeRename"]))
				if thisIsNotA_row["list2Sequence"] is True:
					keywordValue = Make.Call(Make.Name("list"), [keywordValue])
			return Make.keyword(cast("str", thisIsNotA_row["attribute"]), keywordValue)

		matchingRows_listCall_keyword["Call_keyword"] = matchingRows_listCall_keyword.apply(make_keyword, axis="columns")
		dataframeTarget["listCall_keyword"] = matchingRows_listCall_keyword["Call_keyword"].tolist()

		return (
			dataframeTarget["listFunctionDef_args"],
			dataframeTarget["listDefaults"],
			dataframeTarget["listCall_keyword"],
			dataframeTarget["listTupleAttributes"],
		)

	dataframe[["listFunctionDef_args", "listDefaults", "listCall_keyword", "listTupleAttributes"]] = dataframe.apply(
		make3Columns4ClassMake, axis="columns", result_type="expand"
	)

	dataframe.to_pickle(settingsManufacturing.pathFilenameDataframeAST)


if __name__ == "__main__":
	updateDataframe()
