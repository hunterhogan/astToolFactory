"""API for data. The rest of the package should be ignorant of the specifics of the data source.
This module provides a set of functions to interact with the data source, allowing for easy retrieval and manipulation of data."""
from astToolFactory import settingsManufacturing
from astToolFactory.datacenter_annex import (
	_columns, attributeRename__attribute, attributeRename__ClassDefIdentifier_attribute, defaultValue__attribute,
	defaultValue__ClassDefIdentifier_attribute, defaultValue__typeStub_attribute, move2keywordArguments__attribute,
	move2keywordArguments__attributeKind, type__ClassDefIdentifier_attribute,
)
from astToolkit import Be, DOT, dump, Make, NodeTourist, Then
from collections.abc import Sequence
from pathlib import Path
from typing import Any, cast
from Z0Z_tools import raiseIfNone
import ast
import numpy
import pandas
import re

# Use idiomatic pandas.
# No `lambda`.
# No intermediate data structures.
# No `for`, no `iterrows`, no loops.
# No duplicate statements.
# Use idiomatic pandas.

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

def _makeColumn_guardVersion(dataframe: pandas.DataFrame, by: str) -> pandas.DataFrame:
	# Calculate guardVersion as countdown for each ClassDefIdentifier-versionMinorMinimum_match_args group
	# If only one version exists, guardVersion should be 0 (no match-case needed)
	# If multiple versions exist, countdown from total count to 1
	# And as a guard for Python versions below the minimum.
	dataframe['guardVersion'] = numpy.where(
		((versionsTotal := (seriesGroupByVersion := dataframe.groupby(by)['versionMinorMinimum']).transform('nunique')) == 1)
		& (seriesGroupByVersion.transform('max') <= settingsManufacturing.pythonMinimumVersionMinor),
		False,
		numpy.maximum(1, versionsTotal - seriesGroupByVersion.rank(method='first', ascending=False).astype(int) + 1)
	)
	return dataframe

def _sortCaseInsensitive(dataframe: pandas.DataFrame, columnsPriority: Sequence[str], columnsNonString: Sequence[str] = [], ascending: bool | Sequence[bool] = True) -> pandas.DataFrame:
	dataframeCopy: pandas.DataFrame = dataframe.copy()
	columnsString: list[str] = list(set(columnsPriority).difference(set(columnsNonString)))
	dataframeCopy[columnsString] = dataframe[columnsString].map(str.lower) # pyright: ignore[reportArgumentType]

	indicesSorted = dataframeCopy.sort_values(by=columnsPriority, ascending=ascending).index
	return dataframe.loc[indicesSorted]

def getDataframe(*indices: str, **keywordArguments: Any) -> pandas.DataFrame:
	pathFilename: Path = keywordArguments.get('pathFilename') or settingsManufacturing.pathFilenameDataframeAST
	includeDeprecated: bool = keywordArguments.get('includeDeprecated') or settingsManufacturing.includeDeprecated
	versionMinorMaximum: int | None = keywordArguments.get('versionMinorMaximum') or settingsManufacturing.versionMinorMaximum
	modifyVersionMinorMinimum: bool = keywordArguments.get('modifyVersionMinorMinimum') or True

	dataframe: pandas.DataFrame = pandas.read_pickle(pathFilename)

	if not includeDeprecated:
		dataframe = dataframe[~dataframe['deprecated']]

	if versionMinorMaximum is not None:
		dataframe = dataframe[dataframe['versionMinorData'] <= versionMinorMaximum]

	if modifyVersionMinorMinimum:
		columnsVersion: list[str] = ['versionMinorMinimumAttribute', 'versionMinorMinimumClass', 'versionMinorMinimum_match_args']
		dataframe[columnsVersion] = dataframe[columnsVersion].where(dataframe[columnsVersion] > settingsManufacturing.pythonMinimumVersionMinor, -1) # pyright: ignore[reportArgumentType]
	if indices:
		dataframe = dataframe.set_index(list(indices))

	return dataframe

def getElementsBe(identifierToolClass: str, **keywordArguments: Any) -> list[tuple[str, int, str]]:
	listColumnsHARDCODED: list[str] = ['ClassDefIdentifier', 'versionMinorMinimumClass', 'classAs_astAttribute']
	listColumns: list[str] = listColumnsHARDCODED
	del listColumnsHARDCODED
	sliceString: slice = slice(0, 1)
	sliceNonString: slice = slice(1, 2)
	slice_drop_duplicates: slice = slice(0, None)

	dataframe: pandas.DataFrame = (getDataframe(**keywordArguments)
		[listColumns]
		.drop_duplicates(listColumns[slice_drop_duplicates], keep='last')
		.pipe(_sortCaseInsensitive, listColumns[sliceString] + listColumns[sliceNonString], listColumns[sliceNonString], [True] * len(listColumns[sliceString]) + [False] * len(listColumns[sliceNonString]))
		.reset_index(drop=True)
	)
	del listColumns

	return list(dataframe.to_records(index=False))

def getElementsClassIsAndAttribute(identifierToolClass: str, **keywordArguments: Any) -> list[tuple[str, bool, str | bool, str, list[str], int, int]]:
	listColumnsHARDCODED: list[str] = [
	# 	'attribute',
	# 	'TypeAlias_hasDOTSubcategory',
	# 	'versionMinorMinimumAttribute',
	# 	'typeSansNone_ast_expr',
	# 	'typeSansNone',
	# 	'TypeAlias_hasDOTIdentifier',
	# 	'canBeNone',
	# 	]

	# if identifierToolClass == dictionaryIdentifiers['DOT']:
	# 	listColumnsHARDCODED: list[str] = [
		'attribute',
		'TypeAlias_hasDOTSubcategory',
		'versionMinorMinimumAttribute',
		'type_ast_expr',
		'type',
		'TypeAlias_hasDOTIdentifier',
		'canBeNone',
		]

	listColumns: list[str] = listColumnsHARDCODED
	del listColumnsHARDCODED
	sliceString: slice = slice(0, 2)
	sliceNonString: slice = slice(2, 3)
	slice_drop_duplicates: slice = slice(0, 2)
	index_type: int = 4
	index_type_ast_expr: int = 3
	index_versionMinorMinimum: int = 2

	dataframe: pandas.DataFrame = (getDataframe(**keywordArguments)
		.query("attributeKind == '_field'")
		.pipe(_sortCaseInsensitive, listColumns[sliceString] + listColumns[sliceNonString], listColumns[sliceNonString], [True] * len(listColumns[sliceString]) + [False] * len(listColumns[sliceNonString]))
		[listColumns]
		.drop_duplicates(listColumns[slice_drop_duplicates], keep='last')
		.reset_index(drop=True)
	)

	dataframe.rename(columns = {
			listColumns[index_type]: 'type',
			listColumns[index_type_ast_expr]: 'type_ast_expr',
			listColumns[index_versionMinorMinimum]: 'versionMinorMinimum',
		}, inplace=True)

	del listColumns

	elementsTarget: list[str] = ['identifierTypeOfNode', 'overloadDefinition', 'canBeNone', 'attribute', 'list_ast_expr', 'guardVersion', 'versionMinorMinimum']

	dataframe['overloadDefinition'] = dataframe.groupby('attribute').transform('size') > 1
	dataframeImplementationFunctionDefinitions = (
		dataframe[dataframe['overloadDefinition']]
		.groupby('attribute')['versionMinorMinimum']
		.unique()
		.explode()
		.reset_index()
		.merge(
			dataframe[['attribute', 'TypeAlias_hasDOTIdentifier']].drop_duplicates('attribute'),
			on='attribute',
			how='left'
		)
		.assign(
			overloadDefinition=False,
			TypeAlias_hasDOTSubcategory="No",
			type_ast_expr="No",
			type="No",
			canBeNone="Not calculated"
		)
		[dataframe.columns]
	)
	dataframe = (
		pandas.concat([dataframe, dataframeImplementationFunctionDefinitions], ignore_index=True)
		.assign(__sequence_in_group=lambda df: df.groupby('attribute').cumcount())
		.sort_values(['attribute', '__sequence_in_group'], kind='stable')
		.drop(columns='__sequence_in_group')
	)
	del dataframeImplementationFunctionDefinitions

	dataframe['identifierTypeOfNode'] = dataframe['TypeAlias_hasDOTSubcategory'].where(
		dataframe['overloadDefinition'], dataframe['TypeAlias_hasDOTIdentifier']
	)
	dataframe.drop(columns=['TypeAlias_hasDOTIdentifier', 'TypeAlias_hasDOTSubcategory',], inplace=True)
	def makeColumn_canBeNone(dataframeTarget: pandas.DataFrame) -> str | bool:
		matchingRows = dataframe[
			(dataframe['attribute'] == dataframeTarget['attribute']) &
			(dataframe['canBeNone'] != "Not calculated") &
			(dataframe['versionMinorMinimum'] <= dataframeTarget['versionMinorMinimum'])
		]['canBeNone']

		if (matchingRows == False).all():  # noqa: E712
			return False
		elif any(matchingRows.apply(lambda x: isinstance(x, str))): # pyright: ignore[reportUnknownArgumentType, reportUnknownLambdaType]
			return cast(str, matchingRows.loc[matchingRows.apply(lambda x: isinstance(x, str))].iloc[0]) # pyright: ignore[reportUnknownArgumentType, reportUnknownLambdaType]
		elif (matchingRows == True).any():  # noqa: E712
			return True
		else:
			return "Not calculated"

	dataframe.loc[dataframe['canBeNone'] == "Not calculated", 'canBeNone'] = dataframe[dataframe['canBeNone'] == "Not calculated"].apply(makeColumn_canBeNone, axis='columns')

	def makeColumn_list_ast_expr(dataframeTarget: pandas.DataFrame) -> list[str]:
		if bool(dataframeTarget['overloadDefinition']):
			return [str(dataframeTarget['type_ast_expr'])]
		matchingRows = dataframe.loc[
			(dataframe['attribute'] == dataframeTarget['attribute']) &
			(dataframe['type'] != "No") &
			(dataframe['versionMinorMinimum'] <= dataframeTarget['versionMinorMinimum']),
			'type_ast_expr'
		].drop_duplicates()

		return sorted(matchingRows
				, key=lambda ast_expr: dataframe.loc[dataframe['type_ast_expr'] == ast_expr, 'type'].iloc[0].lower()
		)

	dataframe['list_ast_expr'] = dataframe.apply(makeColumn_list_ast_expr, axis='columns')
	dataframe.drop(columns=['type_ast_expr', 'type',], inplace=True)

	by: str = 'identifierTypeOfNode'
	dataframe = _makeColumn_guardVersion(dataframe, by)

	dataframe = dataframe[elementsTarget]
	return list(dataframe.to_records(index=False))

def getElementsDOT(identifierToolClass: str, **keywordArguments: Any) -> list[tuple[str, bool, str | bool, str, list[str], int, int]]:
	return getElementsClassIsAndAttribute(identifierToolClass, **keywordArguments)

def getElementsGrab(identifierToolClass: str, **keywordArguments: Any) -> list[tuple[str, list[str], str, int, int]]:
	listColumnsHARDCODED: list[str] = ['attribute', 'typeGrab', 'versionMinorMinimumAttribute', 'TypeAlias_hasDOTIdentifier', 'typeGrab_ast_expr', ]
	listColumns: list[str] = listColumnsHARDCODED
	del listColumnsHARDCODED
	sliceString: slice = slice(0, 2)
	sliceNonString: slice = slice(2, 3)
	slice_drop_duplicates: slice = slice(0, 2)
	index_type: int = 1
	index_type_ast_expr: int = 4
	index_versionMinorMinimum: int = 2

	dataframe: pandas.DataFrame = (getDataframe(**keywordArguments)
		.query("attributeKind == '_field'")
		[listColumns]
		.pipe(_sortCaseInsensitive, listColumns[sliceString] + listColumns[sliceNonString], listColumns[sliceNonString], [True] * len(listColumns[sliceString]) + [False] * len(listColumns[sliceNonString]))
		.drop_duplicates(listColumns[slice_drop_duplicates], keep='last')
		.reset_index(drop=True)
	)

	dataframe.rename(columns = {listColumns[index_type]: 'type', listColumns[index_type_ast_expr]: 'type_ast_expr', listColumns[index_versionMinorMinimum]: 'versionMinorMinimum'}, inplace=True)

	del listColumns

	elementsTarget: list[str] = ['TypeAlias_hasDOTIdentifier', 'list_ast_expr', 'attribute', 'guardVersion', 'versionMinorMinimum']
	def makeColumn_list_ast_expr(dataframeTarget: pandas.DataFrame) -> list[str]:
		matchingRows = dataframe.loc[
			(dataframe['attribute'] == dataframeTarget['attribute']) &
			(dataframe['versionMinorMinimum'] <= dataframeTarget['versionMinorMinimum']),
			'type_ast_expr'
		]

		return sorted(matchingRows
				, key=lambda ast_expr: dataframe.loc[dataframe['type_ast_expr'] == ast_expr, 'type'].iloc[0].lower()
		)

	dataframe['list_ast_expr'] = dataframe.apply(makeColumn_list_ast_expr, axis='columns')

	# TODO more semantic identifier than `by`
	by: str = 'attribute'
	dataframe = _makeColumn_guardVersion(dataframe, by)

	dataframe = dataframe[elementsTarget].drop_duplicates(subset=elementsTarget[2:None], keep='last').reset_index(drop=True)

	return list(dataframe.to_records(index=False))

def getElementsMake(identifierToolClass: str, **keywordArguments: Any) -> list[tuple[str, list[str], str, list[str], str, bool, list[tuple[str, str]], int, int]]:
	listColumnsHARDCODED: list[str] = [
	'ClassDefIdentifier',
	'versionMinorMinimumClass',
	'versionMinorMinimum_match_args',
	'listStr4FunctionDef_args',
	'kwarg_annotationIdentifier',
	'listDefaults',
	'classAs_astAttribute',
	'listTupleCall_keywords',
	]
	listColumns: list[str] = listColumnsHARDCODED
	del listColumnsHARDCODED
	sliceString: slice = slice(0, 1)
	sliceNonString: slice = slice(1, 3)
	slice_drop_duplicates: slice = slice(0, 3)
	index_versionMinorMinimum: int = 2

	dataframe: pandas.DataFrame = (getDataframe(**keywordArguments)
		[listColumns]
		.pipe(_sortCaseInsensitive, listColumns[sliceString] + listColumns[sliceNonString], listColumns[sliceNonString], [True] * len(listColumns[sliceString]) + [False] * len(listColumns[sliceNonString]))
		.drop_duplicates(listColumns[slice_drop_duplicates], keep='last')
		.reset_index(drop=True)
	)
	dataframe.rename(columns = {listColumns[index_versionMinorMinimum]: 'versionMinorMinimum'}, inplace=True)
	del listColumns

	elementsTarget: list[str] = ['ClassDefIdentifier', 'listStr4FunctionDef_args', 'kwarg_annotationIdentifier', 'listDefaults', 'classAs_astAttribute', 'overloadDefinition', 'listTupleCall_keywords', 'guardVersion', 'versionMinorMinimum']

	by: str = 'ClassDefIdentifier'
	dataframe = _makeColumn_guardVersion(dataframe, by)

	# TODO Create overloadDefinition flag - False until new logic added
	dataframe['overloadDefinition'] = False

	dataframe = dataframe[elementsTarget]
	return list(dataframe.to_records(index=False))

def getElementsTypeAlias(**keywordArguments: Any) -> list[tuple[str, list[str], int, int]]:
	listColumnsHARDCODED: list[str] = ['attribute', 'TypeAlias_hasDOTSubcategory', 'ClassDefIdentifier', 'versionMinorMinimumAttribute', 'classAs_astAttribute', 'TypeAlias_hasDOTIdentifier',]
	listColumns: list[str] = listColumnsHARDCODED
	del listColumnsHARDCODED
	sliceString: slice = slice(0, 3)
	sliceNonString: slice = slice(3, 4)
	slice_drop_duplicates: slice = slice(0, None)
	index_versionMinorMinimum: int = 3
	dataframe: pandas.DataFrame = (getDataframe(**keywordArguments)
		.query("attributeKind == '_field'")
		[listColumns]
		.pipe(_sortCaseInsensitive, listColumns[sliceString] + listColumns[sliceNonString], listColumns[sliceNonString], [True] * len(listColumns[sliceString]) + [False] * len(listColumns[sliceNonString]))
		.drop_duplicates(listColumns[slice_drop_duplicates], keep='last')
		.reset_index(drop=True)
	)
	dataframe.rename(columns = {listColumns[index_versionMinorMinimum]: 'versionMinorMinimum'}, inplace=True)
	del listColumns

	elementsTarget: list[str] = ['identifierTypeAlias', 'list4TypeAlias_value', 'guardVersion', 'versionMinorMinimum']

	def makeColumn_list4TypeAlias_value(dataframeTarget: pandas.DataFrame):
		matchingRows = dataframe.loc[
			(dataframe['TypeAlias_hasDOTSubcategory'] == dataframeTarget['TypeAlias_hasDOTSubcategory']) &
			(dataframe['ClassDefIdentifier'] != "No") &
			(dataframe['versionMinorMinimum'] <= dataframeTarget['versionMinorMinimum']),
			['classAs_astAttribute', 'ClassDefIdentifier']
		].drop_duplicates().sort_values('ClassDefIdentifier', key=lambda x: x.str.lower())

		return matchingRows['classAs_astAttribute'].tolist(), str(matchingRows['ClassDefIdentifier'].tolist())

	dataframe[['list4TypeAlias_value', 'hashable_list4TypeAlias_value']] = dataframe.apply(makeColumn_list4TypeAlias_value, axis='columns', result_type='expand') # pyright: ignore[reportArgumentType]
	dataframe.drop_duplicates(subset=['attribute', 'TypeAlias_hasDOTSubcategory', 'versionMinorMinimum', 'hashable_list4TypeAlias_value'], inplace=True)
	dataframe.drop(columns=['classAs_astAttribute', 'ClassDefIdentifier', 'hashable_list4TypeAlias_value'], inplace=True)

	dataframe = dataframe.sort_values('versionMinorMinimum', ascending=False).groupby('attribute')[dataframe.columns].apply(
		lambda group: group if group['TypeAlias_hasDOTSubcategory'].nunique() == 1 else pandas.concat([
			group,
			group.drop_duplicates(subset='TypeAlias_hasDOTSubcategory', keep='last')[['versionMinorMinimum']].drop_duplicates().assign(
				attribute=group['attribute'].iloc[0],
				TypeAlias_hasDOTSubcategory="No",
				TypeAlias_hasDOTIdentifier=group['TypeAlias_hasDOTIdentifier'].iloc[0],
				list4TypeAlias_value="No"
			)
		])
	).reset_index(drop=True)

	def MakeName4TypeAlias(subcategoryName: str) -> str:
		return dump(Make.Name(subcategoryName))

	def updateColumn_list4TypeAlias_value(dataframeTarget: pandas.DataFrame):
		matchingRows = dataframe.loc[
			(dataframe['attribute'] == dataframeTarget['attribute']) &
			(dataframe['TypeAlias_hasDOTSubcategory'] != "No") &
			(dataframe['versionMinorMinimum'] <= dataframeTarget['versionMinorMinimum']),
			['TypeAlias_hasDOTSubcategory']
		].drop_duplicates()

		return [MakeName4TypeAlias(subcategory) for subcategory in matchingRows['TypeAlias_hasDOTSubcategory']]

	mask = dataframe['list4TypeAlias_value'] == "No"
	dataframe.loc[mask, 'list4TypeAlias_value'] = dataframe.loc[mask].apply(updateColumn_list4TypeAlias_value, axis='columns')

	dataframe['identifierTypeAlias'] = dataframe['TypeAlias_hasDOTIdentifier'].where(
		dataframe.groupby('attribute')['TypeAlias_hasDOTSubcategory'].transform('nunique') == 1,
		dataframe['TypeAlias_hasDOTSubcategory'].where(
			dataframe['TypeAlias_hasDOTSubcategory'] != "No",
			dataframe['TypeAlias_hasDOTIdentifier']
		)
	)
	dataframe.drop(columns=['attribute', 'TypeAlias_hasDOTSubcategory', 'TypeAlias_hasDOTIdentifier'], inplace=True)

	by: str = 'identifierTypeAlias'
	dataframe = _makeColumn_guardVersion(dataframe, by)

	dataframe = dataframe[elementsTarget]
	return list(dataframe.to_records(index=False))

def updateDataframe() -> None:
	# === Base Source Columns: Read-Only ===
	dataframe: pandas.DataFrame = getDataframe(includeDeprecated=True, versionMinorMaximum=None, modifyVersionMinorMinimum=False)

	# Change the order of columns
	# dataframe = dataframe[_columns]

	# === Human Overrides (Purely Choice-Based) ===

	dataframe['attributeRename'] = dataframe['attribute'].map(attributeRename__attribute).fillna(dataframe['attributeRename'])
	dataframe['attributeRename'] = dataframe[['ClassDefIdentifier', 'attribute']].apply(tuple, axis='columns').map(attributeRename__ClassDefIdentifier_attribute).fillna(dataframe['attributeRename'])

	dataframe['move2keywordArguments'] = False  # Default value for the column
	dataframe['move2keywordArguments'] = dataframe['attributeKind'].map(move2keywordArguments__attributeKind).fillna(dataframe['move2keywordArguments'])
	dataframe['move2keywordArguments'] = dataframe['attribute'].map(move2keywordArguments__attribute).fillna(dataframe['move2keywordArguments'])

	dataframe['defaultValue'] = "No"  # Default value for the column
	dataframe['defaultValue'] = dataframe['attribute'].map(defaultValue__attribute).fillna(dataframe['defaultValue'])
	dataframe['defaultValue'] = dataframe[['ClassDefIdentifier', 'attribute']].apply(tuple, axis='columns').map(defaultValue__ClassDefIdentifier_attribute).fillna(dataframe['defaultValue'])
	dataframe['defaultValue'] = dataframe[['typeStub', 'attribute']].apply(tuple, axis='columns').map(defaultValue__typeStub_attribute).fillna(dataframe['defaultValue'])

	# === Row-Based Column Computation ===

	# Update 'classAs_astAttribute' column with formatted value
	def _makeClassAs_astAttribute(ClassDefIdentifier:str):
		return dump(Make.Attribute(Make.Name('ast'), ClassDefIdentifier))
	dataframe['classAs_astAttribute'] = dataframe['ClassDefIdentifier'].astype(str).map(_makeClassAs_astAttribute)	# Update 'type' column with standardized formatting and accurate information

	identifiersPattern: str = r'\b(' + '|'.join(dataframe['ClassDefIdentifier'].dropna().unique()) + r')\b'
	dataframe['type'] = (
		dataframe['typeStub']
		.where(dataframe['typeStub_typing_TypeAlias'] == 'No', dataframe['typeC'])
		.str.replace(identifiersPattern, r'ast.\1', regex=True)
		.str.replace("Literal[True, False]", "bool", regex=False)
	)

	# dataframe['type'] = dataframe['type'].map(type__type).fillna(dataframe['type'])
	dataframe['type'] = dataframe[['ClassDefIdentifier', 'attribute']].apply(tuple, axis='columns').map(type__ClassDefIdentifier_attribute).fillna(dataframe['type'])

	dataframe['canBeNone'] = False  # Default value for the column

	def update_canBeNone(dataframeTarget: pandas.DataFrame) -> str | bool:
		if dataframeTarget['type'] in ["No"]:
			return "No"
		elif ' | None' in dataframeTarget['type'] and 'list' in dataframeTarget['type']:
			return "list"
		elif ' | None' in dataframeTarget['type']:
			return True
		else:
			return False
	dataframe['canBeNone'] = dataframe.apply(update_canBeNone, axis='columns')

	def pythonCode2expr(string: str) -> str:
		astModule: ast.Module = ast.parse(string)
		ast_expr: ast.expr = raiseIfNone(NodeTourist(Be.Expr, Then.extractIt(DOT.value)).captureLastMatch(astModule))
		return dump(ast_expr)

	# Update 'type_ast_expr' based on 'type' column
	dataframe['type_ast_expr'] = numpy.where(dataframe['type'] == 'No', 'No', dataframe['type'].apply(pythonCode2expr))
	# Update 'type_ast_expr' based on 'list2Sequence' column
	dataframe.loc[dataframe['list2Sequence'] == True, 'type_ast_expr'] = dataframe['type_ast_expr'].str.replace("'list'", "'Sequence'")  # noqa: E712

	dataframe['typeSansNone'] = dataframe['type'].replace(' \\| None', '', regex=True)
	# Update 'typeSansNone_ast_expr' based on 'type' column
	dataframe['typeSansNone_ast_expr'] = numpy.where(dataframe['typeSansNone'] == 'No', 'No', dataframe['typeSansNone'].apply(pythonCode2expr))
	# Update 'typeSansNone_ast_expr' based on 'list2Sequence' column
	dataframe.loc[dataframe['list2Sequence'] == True, 'typeSansNone_ast_expr'] = dataframe['typeSansNone_ast_expr'].str.replace("'list'", "'Sequence'")  # noqa: E712

	# Create 'typeGrab' with TypeVar substitutions
	dataframe['typeGrab'] = dataframe['type'].replace({f"ast.{key}": value for key, value in settingsManufacturing.astSuperClasses.items()}, regex=True)
	dataframe['typeGrab_ast_expr'] = numpy.where(dataframe['typeGrab'] == 'No', 'No', dataframe['typeGrab'].apply(pythonCode2expr))

	def make_ast_arg(dataframeTarget: pandas.DataFrame) -> str:
		if cast(str | bool, dataframeTarget['move2keywordArguments']) != False:  # noqa: E712
			return "No"
		identifier: str = cast(str, dataframeTarget['attributeRename']) if cast(str, dataframeTarget['attributeRename']) != "No" else cast(str, dataframeTarget['attribute'])
		return dump(Make.arg(identifier, annotation=eval(cast(str, dataframeTarget['type_ast_expr']))))

	# Update 'ast_arg' column based on conditions
	dataframe['ast_arg'] = dataframe.apply(make_ast_arg, axis='columns')

	# Add TypeAlias_hasDOTIdentifier
	dataframe['TypeAlias_hasDOTIdentifier'] = numpy.where(
		dataframe['attributeKind'] == '_field',
		"hasDOT" + cast(str, dataframe['attribute']),
		"No"
	)

	# Add TypeAlias_hasDOTSubcategory
	processedTypeString: pandas.Series[str] = (
		dataframe['type']
		.str.replace('|', 'Or', regex=False)
		.str.replace('[', '_', regex=False)
		.str.replace('ast.', '', regex=False)
		.str.replace(']', '', regex=False)
		.str.replace(' ', '', regex=False)
	)
	dataframe['TypeAlias_hasDOTSubcategory'] = numpy.where(
		dataframe['TypeAlias_hasDOTIdentifier'] == "No",
		"No",
		cast(str, dataframe['TypeAlias_hasDOTIdentifier']) + "_" + processedTypeString
	)

	# === Group-Based Column Computation ===
	def computeVersionMinimum(columns: list[str]) -> numpy.ndarray[tuple[int, ...], numpy.dtype[numpy.int64]]:
		return numpy.where(dataframe.groupby(columns)['versionMinorData'].transform('min') == settingsManufacturing.versionMinor_astMinimumSupported,
			-1, dataframe.groupby(columns)['versionMinorData'].transform('min'))

	dataframe['versionMinorMinimum_match_args'] = computeVersionMinimum(['ClassDefIdentifier', 'match_args'])
	dataframe['versionMinorMinimumAttribute'] = computeVersionMinimum(['ClassDefIdentifier', 'attribute'])
	dataframe['versionMinorMinimumClass'] = computeVersionMinimum(['ClassDefIdentifier'])

	def compute_listFunctionDef_args(dataframeTarget: pandas.DataFrame) -> pandas.Series: # pyright: ignore[reportMissingTypeArgument, reportUnknownParameterType]
		if cast(str, dataframeTarget['attributeKind']) == "No":
			return pandas.Series([[], [], []], index=[
				'listStr4FunctionDef_args',
				'listDefaults',
				'listTupleCall_keywords'
			])
		listAttributes: list[str] = list(cast(tuple[str, ...], dataframeTarget['match_args']))
		className = cast(str, dataframeTarget['ClassDefIdentifier'])
		version = cast(int, dataframeTarget['versionMinorMinimum_match_args'])
		listStr4FunctionDef_args: list[str] = []
		listDefaults: list[str] = []
		listTupleCall_keywords: list[tuple[str, str]] = []
		for attributeTarget in listAttributes:
			# if dataframe['move2keywordArguments'] == 'Unpack':
			if attributeTarget == 'type_comment':
				continue
			argIdentifier: str = attributeTarget
			keywordValue: str = attributeTarget
			matching_row: pandas.DataFrame = dataframe[
				(dataframe['attribute'] == attributeTarget) &
				(dataframe['ClassDefIdentifier'] == className) &
				(dataframe['versionMinorMinimum_match_args'] == version)
			]

			if matching_row.iloc[0]['move2keywordArguments']:
				keywordValue = cast(str, matching_row.iloc[0]['defaultValue'])
			else:
				ast_arg: str = cast(str, matching_row.iloc[0]['ast_arg'])
				if matching_row.iloc[0]['attributeRename'] != "No":
					keywordValue = cast(str, matching_row.iloc[0]['attributeRename'])
				keywordValue = dump(Make.Name(keywordValue))
				if matching_row.iloc[0]['list2Sequence']:
					# keywordValue = dump(Make.Call(Make.Name('list'), [keywordValue]))
					keywordValue = f"ast.Call(ast.Name('list'), args=[{keywordValue}])"
				if matching_row.iloc[0]['defaultValue'] != "No":
					listDefaults.append(cast(str, matching_row.iloc[0]['defaultValue']))
				listStr4FunctionDef_args.append(ast_arg)
			listTupleCall_keywords.append((argIdentifier, keywordValue))
		return pandas.Series([listStr4FunctionDef_args, listDefaults, listTupleCall_keywords], index=[
			'listStr4FunctionDef_args',
			'listDefaults',
			'listTupleCall_keywords'
		])
	dataframe[['listStr4FunctionDef_args', 'listDefaults', 'listTupleCall_keywords']] = dataframe.apply(compute_listFunctionDef_args, axis='columns') # pyright: ignore[reportUnknownArgumentType, reportArgumentType]

	# === Row-Based: Hashable Variants ===
	dataframe['hashableListStr4FunctionDef_args'] = dataframe['listStr4FunctionDef_args'].astype(str)
	dataframe['hashableListDefaults'] = dataframe['listDefaults'].astype(str)
	dataframe['hashableListTupleCall_keywords'] = dataframe['listTupleCall_keywords'].astype(str)

	# === Save Final Result ===
	dataframe.to_pickle(settingsManufacturing.pathFilenameDataframeAST)

# if __name__ == "__main__":
# 	updateDataframe()