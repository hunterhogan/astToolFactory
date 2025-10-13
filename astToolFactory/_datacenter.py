"""API for data. The rest of the package should be ignorant of the specifics of the data source.

This module provides a set of functions to interact with the data source, allowing for easy retrieval and manipulation of data.

"""

from astToolFactory import settingsManufacturing
from collections.abc import Sequence
from typing import Any, cast
import ast
import numpy
import pandas
import typing_extensions

if typing_extensions.TYPE_CHECKING:
	from numpy.typing import NDArray
	from pathlib import Path

"""Generalized flow for get* functions:
listColumnsHARDCODED
listColumns
dataframe
elementsTarget
...
_makeColumn_guardVersion
dataframe = dataframe[elementsTarget]
return dataframe.to_records(index=False).tolist()
"""

def _makeColumn_guardVersion(dataframe: pandas.DataFrame, byColumn: str) -> pandas.DataFrame:
	"""No summary.

	Column 'guardVersion' = False unless:
	- A `byColumn`-'versionMinorMinimum' group is larger than 1, then 'guardVersion' is a countdown
		from the total number of versions in the group.
	- Or if the only member of a group has a python version greater than `pythonMinimumVersionMinor`.

	"""
	dataframe["guardVersion"] = numpy.where(
		((versionsTotal := (seriesGroupByVersion := dataframe.groupby(byColumn)["versionMinorMinimum"]).transform("nunique")) == 1)
			& (seriesGroupByVersion.transform("max") <= settingsManufacturing.pythonMinimumVersionMinor) # pyright: ignore[reportArgumentType]
		, False # noqa: FBT003
		, numpy.maximum(1, versionsTotal - seriesGroupByVersion.rank(method="first", ascending=False).astype(int) + 1) # pyright: ignore[reportUnknownArgumentType]
	)
	return dataframe

def _sortCaseInsensitive(dataframe: pandas.DataFrame, sortBy: Sequence[str], *, caseInsensitive: bool | Sequence[bool] = True, ascending: bool | Sequence[bool] = True) -> pandas.DataFrame:
	dataframeCopy: pandas.DataFrame = dataframe.copy()
	maskCaseInsensitive = pandas.Series(caseInsensitive, index=list(sortBy), dtype=numpy.bool)
	dataframeCopy[maskCaseInsensitive[maskCaseInsensitive].index] = dataframe[maskCaseInsensitive[maskCaseInsensitive].index].map(str.lower)

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
		dataframe[columnsVersion] = dataframe[columnsVersion].where(
			dataframe[columnsVersion] > settingsManufacturing.pythonMinimumVersionMinor
			, -1
		)
	if indices:
		dataframe = dataframe.set_index(list(indices))

	return dataframe

def getElementsBe(identifierToolClass: str, **keywordArguments: Any) -> list[tuple[str, int, ast.expr, list[tuple[str, ast.expr]]]]:  # noqa: ARG001
	listColumnsHARDCODED: list[str] = ["ClassDefIdentifier", "versionMinorMinimumClass", "classAs_astAttribute", "listTupleAttributes"]
	listColumns: list[str] = listColumnsHARDCODED
	del listColumnsHARDCODED

	sortBy: list[str] = listColumns[0:2]
	caseInsensitive: list[bool] = [True, False]
	ascending: list[bool] = caseInsensitive.copy()
	drop_duplicates: list[str] = sortBy.copy()

	dataframe: pandas.DataFrame = getDataframe(**keywordArguments)[listColumns].drop_duplicates(drop_duplicates).pipe(_sortCaseInsensitive, sortBy, caseInsensitive=caseInsensitive, ascending=ascending).reset_index(drop=True)
	del listColumns

	return dataframe.to_records(index=False).tolist()

def getElementsDOT(identifierToolClass: str, **keywordArguments: Any) -> list[tuple[str, bool, str, list[ast.expr], int, int]]:  # noqa: ARG001
	listColumnsHARDCODED: list[str] = ["attribute", "TypeAlias_hasDOTSubcategory", "versionMinorMinimumAttribute", "type_ast_expr", "attributeType", "TypeAlias_hasDOTIdentifier"]
	listColumns: list[str] = listColumnsHARDCODED
	del listColumnsHARDCODED

	sortBy: list[str] = listColumns[0:3]
	caseInsensitive: list[bool] = [True, True, False]
	ascending: list[bool] = caseInsensitive.copy()
	drop_duplicates: list[str] = listColumns[0:2]

	index_type_ast_expr: int = 3
	index_versionMinorMinimum: int = 2

	dataframe: pandas.DataFrame = (getDataframe(**keywordArguments)
			.query("attributeKind == '_field'")
			.pipe(_sortCaseInsensitive, sortBy, caseInsensitive=caseInsensitive, ascending=ascending)[listColumns]
			.drop_duplicates(drop_duplicates, keep="last")
			.reset_index(drop=True))

	dataframe = dataframe.rename(columns={
			listColumns[index_type_ast_expr]: "type_ast_expr"
			, listColumns[index_versionMinorMinimum]: "versionMinorMinimum"})

	del listColumns

	elementsTarget: list[str] = ["identifierTypeOfNode", "overloadDefinition", "attribute", "list_ast_expr", "guardVersion", "versionMinorMinimum"]

	dataframe["overloadDefinition"] = dataframe.groupby("attribute").transform("size") > 1
	dataframe = pandas.concat([
		dataframe
		, (dataframe[dataframe["overloadDefinition"]]
			.groupby("attribute")["versionMinorMinimum"]
			.unique()
			.explode()
			.reset_index()
			.merge(dataframe[["attribute", "TypeAlias_hasDOTIdentifier"]].drop_duplicates("attribute"), on="attribute", how="left")
			.assign(
				overloadDefinition=False,
				TypeAlias_hasDOTSubcategory="No",
				type_ast_expr="No",
				attributeType="No",
			)[dataframe.columns]
		)
	], ignore_index=True).sort_values("attribute", kind="stable")

	dataframe["identifierTypeOfNode"] = dataframe["TypeAlias_hasDOTSubcategory"].where(dataframe["overloadDefinition"], dataframe["TypeAlias_hasDOTIdentifier"])
	dataframe = dataframe.drop(columns=["TypeAlias_hasDOTIdentifier", "TypeAlias_hasDOTSubcategory"])

	def makeColumn_list_ast_expr(dataframeTarget: pandas.DataFrame) -> list[ast.expr]:
		if bool(dataframeTarget["overloadDefinition"]):
			return [cast(ast.expr, dataframeTarget["type_ast_expr"])]
		matchingRows: pandas.DataFrame = (
			dataframe.loc[
				(dataframe["attribute"] == dataframeTarget["attribute"])
				& (dataframe["attributeType"] != "No")
				& (dataframe["versionMinorMinimum"] <= dataframeTarget["versionMinorMinimum"]),
				["type_ast_expr", "attributeType"],
			]
			.drop_duplicates(subset="attributeType")
			.sort_values("attributeType", key=lambda x: x.str.lower())
		)

		return matchingRows["type_ast_expr"].tolist()

	dataframe["list_ast_expr"] = dataframe.apply(makeColumn_list_ast_expr, axis="columns")
	dataframe = dataframe.drop(columns=["type_ast_expr", "attributeType"])

	byColumn: str = "identifierTypeOfNode"
	dataframe = _makeColumn_guardVersion(dataframe, byColumn)

	dataframe = dataframe[elementsTarget]
	return dataframe.to_records(index=False).tolist()

def getElementsDocstringGrab(identifierToolClass: str, **keywordArguments: Any) -> dict[str, dict]:  # noqa: ARG001
	"""Get docstring elements for Grab."""
	return {}

def getElementsGrab(identifierToolClass: str, **keywordArguments: Any) -> list[tuple[str, list[ast.expr], str, int, int]]:  # noqa: ARG001
	listColumnsHARDCODED: list[str] = ["attribute", "type_astSuperClasses", "versionMinorMinimumAttribute", "TypeAlias_hasDOTIdentifier", "type_astSuperClasses_ast_expr"]
	listColumns: list[str] = listColumnsHARDCODED
	del listColumnsHARDCODED

	sortBy: list[str] = listColumns[0:3]
	caseInsensitive: list[bool] = [True, True, False]
	ascending: list[bool] = caseInsensitive.copy()
	drop_duplicates: list[str] = listColumns[0:2]

	index_attributeType: int = 1
	index_type_ast_expr: int = 4
	index_versionMinorMinimum: int = 2

	dataframe: pandas.DataFrame = getDataframe(**keywordArguments).query("attributeKind == '_field'")[listColumns].pipe(_sortCaseInsensitive, sortBy, caseInsensitive=caseInsensitive, ascending=ascending).drop_duplicates(drop_duplicates, keep="last").reset_index(drop=True)

	dataframe = dataframe.rename(columns={
		listColumns[index_attributeType]: "attributeType",
		listColumns[index_type_ast_expr]: "type_ast_expr",
		listColumns[index_versionMinorMinimum]: "versionMinorMinimum",
	})

	del listColumns

	elementsTarget: list[str] = ["TypeAlias_hasDOTIdentifier", "list_ast_expr", "attribute", "guardVersion", "versionMinorMinimum"]

	def makeColumn_list_ast_expr(dataframeTarget: pandas.DataFrame) -> list[ast.expr]:
		matchingRows: pandas.DataFrame = dataframe.loc[
			(dataframe["attribute"] == dataframeTarget["attribute"])
			& (dataframe["versionMinorMinimum"] <= dataframeTarget["versionMinorMinimum"])
			, ["type_ast_expr", "attributeType"]
		].sort_values("attributeType", key=lambda x: x.str.lower())

		return matchingRows["type_ast_expr"].tolist()

	dataframe["list_ast_expr"] = dataframe.apply(makeColumn_list_ast_expr, axis="columns")

	byColumn: str = "attribute"
	dataframe = _makeColumn_guardVersion(dataframe, byColumn)

	dataframe = dataframe[elementsTarget].drop_duplicates(subset=elementsTarget[2:None], keep="last").reset_index(drop=True)

	return dataframe.to_records(index=False).tolist()

def getElementsMake(identifierToolClass: str, **keywordArguments: Any) -> list[tuple[str, list[ast.arg], str, list[ast.expr], ast.expr, bool, list[ast.keyword], int, int]]:  # noqa: ARG001
	listColumnsHARDCODED: list[str] = ["ClassDefIdentifier", "versionMinorMinimumClass", "versionMinorMinimum_match_args", "listFunctionDef_args", "kwarg_annotationIdentifier", "listDefaults", "classAs_astAttribute", "listCall_keyword"]
	listColumns: list[str] = listColumnsHARDCODED
	del listColumnsHARDCODED

	sortBy: list[str] = listColumns[0:3]
	caseInsensitive: list[bool] = [True, False, False]
	ascending: list[bool] = caseInsensitive.copy()
	drop_duplicates: list[str] = sortBy.copy()

	index_versionMinorMinimum: int = 2

	dataframe: pandas.DataFrame = (getDataframe(**keywordArguments)[listColumns]
					.pipe(_sortCaseInsensitive, sortBy, caseInsensitive=caseInsensitive, ascending=ascending)
					.drop_duplicates(drop_duplicates).reset_index(drop=True))
	dataframe = dataframe.rename(columns={listColumns[index_versionMinorMinimum]: "versionMinorMinimum"})
	del listColumns

	elementsTarget: list[str] = ["ClassDefIdentifier", "listFunctionDef_args", "kwarg_annotationIdentifier", "listDefaults", "classAs_astAttribute", "overloadDefinition", "listCall_keyword", "guardVersion", "versionMinorMinimum"]

	byColumn: str = "ClassDefIdentifier"
	dataframe = _makeColumn_guardVersion(dataframe, byColumn)

	# TODO Create overloadDefinition flag - False until new logic added
	dataframe["overloadDefinition"] = False

	dataframe = dataframe[elementsTarget]
	return dataframe.to_records(index=False).tolist()

def getElementsTypeAlias(**keywordArguments: Any) -> list[tuple[str, list[ast.expr], int, int]]:
	listColumnsHARDCODED: list[str] = ["attribute", "TypeAlias_hasDOTSubcategory", "ClassDefIdentifier", "versionMinorMinimumAttribute", "classAs_astAttribute", "TypeAlias_hasDOTIdentifier", "list4TypeAlias_value", "hashable_list4TypeAlias_value", "list4TypeAliasSubcategories"]
	listColumns: list[str] = listColumnsHARDCODED
	del listColumnsHARDCODED

	sortBy: list[str] = listColumns[0:4]
	caseInsensitive: list[bool] = [True, True, True, False]
	ascending: list[bool] = caseInsensitive.copy()
	drop_duplicates: list[str] = sortBy.copy()

	index_versionMinorMinimum: int = 3

	dataframe: pandas.DataFrame = (getDataframe(**keywordArguments).query("attributeKind == '_field'")[listColumns]
				.pipe(_sortCaseInsensitive, sortBy, caseInsensitive=caseInsensitive, ascending=ascending)
				.drop_duplicates(drop_duplicates, keep="last").reset_index(drop=True))
	dataframe = dataframe.rename(columns={listColumns[index_versionMinorMinimum]: "versionMinorMinimum"})
	del listColumns

	elementsTarget: list[str] = ["identifierTypeAlias", "list4TypeAlias_value", "guardVersion", "versionMinorMinimum"]

	dataframe = dataframe.drop_duplicates(subset=["attribute", "TypeAlias_hasDOTSubcategory", "versionMinorMinimum", "hashable_list4TypeAlias_value"])

	def addRows_hasDOTIdentifier4Subcategories(groupBy: pandas.DataFrame) -> pandas.DataFrame:
		arrayGroupBy: NDArray[numpy.str_] = groupBy["TypeAlias_hasDOTSubcategory"].to_numpy()
		if (arrayGroupBy[0] == arrayGroupBy).all():
			return groupBy

		rows_hasDOTIdentifier: pandas.DataFrame = (groupBy.drop_duplicates(subset="TypeAlias_hasDOTSubcategory", keep="last")[["versionMinorMinimum"]].drop_duplicates()
			.assign(attribute=groupBy["attribute"].iloc[0], TypeAlias_hasDOTSubcategory="No"
				, TypeAlias_hasDOTIdentifier=groupBy["TypeAlias_hasDOTIdentifier"].iloc[0]
				, list4TypeAlias_value=[groupBy["list4TypeAliasSubcategories"].iloc[0]])
		)
		return pandas.concat([groupBy, rows_hasDOTIdentifier])

	dataframe = dataframe.groupby("attribute")[dataframe.columns].apply(addRows_hasDOTIdentifier4Subcategories).reset_index(drop=True)

	dataframe["identifierTypeAlias"] = dataframe["TypeAlias_hasDOTIdentifier"].where(
		dataframe.groupby("attribute")["TypeAlias_hasDOTSubcategory"].transform("nunique") == 1
		, dataframe["TypeAlias_hasDOTSubcategory"].where(dataframe["TypeAlias_hasDOTSubcategory"] != "No"
														, dataframe["TypeAlias_hasDOTIdentifier"])
	)

	byColumn: str = "identifierTypeAlias"
	dataframe = _makeColumn_guardVersion(dataframe, byColumn)

	dataframe = dataframe[elementsTarget]
	return dataframe.to_records(index=False).tolist()
