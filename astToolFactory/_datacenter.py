"""API for data. The rest of the package should be ignorant of the specifics of the data source.
This module provides a set of functions to interact with the data source, allowing for easy retrieval and manipulation of data."""
from astToolFactory import settingsManufacturing
from astToolFactory._datacenter_annex import (
	_columns, attributeRename__attribute, attributeRename__ClassDefIdentifier_attribute, defaultValue__attribute,
	defaultValue__ClassDefIdentifier_attribute, defaultValue__typeStub_attribute, move2keywordArguments__attribute,
	move2keywordArguments__attributeKind, type__ClassDefIdentifier_attribute,
)
from astToolkit import Be, DOT, Make, NodeTourist, Then
from collections.abc import Sequence
from pathlib import Path
from typing import Any, cast
from Z0Z_tools import raiseIfNone
import ast
import numpy
import pandas

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

def _makeColumn_guardVersion(dataframe: pandas.DataFrame, byColumn: str) -> pandas.DataFrame:
	"""Column 'guardVersion' = False unless:
	- A `byColumn`-'versionMinorMinimum' group is larger than 1, then 'guardVersion' is a countdown from the total number of versions in the group.
	- Or if the only member of a group has a python version greater than `pythonMinimumVersionMinor`."""
	dataframe['guardVersion'] = numpy.where(
		((versionsTotal := (seriesGroupByVersion := dataframe.groupby(byColumn)['versionMinorMinimum']).transform('nunique')) == 1)
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

def getElementsBe(identifierToolClass: str, **keywordArguments: Any) -> list[tuple[str, int, ast.expr]]:
	listColumnsHARDCODED: list[str] = ['ClassDefIdentifier', 'versionMinorMinimumClass', 'classAs_astAttribute']
	listColumns: list[str] = listColumnsHARDCODED
	del listColumnsHARDCODED
	sliceString: slice = slice(0, 1)
	sliceNonString: slice = slice(1, 2)
	slice_drop_duplicates: slice = slice(0, 2)

	dataframe: pandas.DataFrame = (getDataframe(**keywordArguments)
		[listColumns]
		.drop_duplicates(listColumns[slice_drop_duplicates], keep='last')
		.pipe(_sortCaseInsensitive, listColumns[sliceString] + listColumns[sliceNonString], listColumns[sliceNonString], [True] * len(listColumns[sliceString]) + [False] * len(listColumns[sliceNonString]))
		.reset_index(drop=True)
	)
	del listColumns

	return list(dataframe.to_records(index=False))

def getElementsClassIsAndAttribute(identifierToolClass: str, **keywordArguments: Any) -> list[tuple[str, bool, str | bool, str, list[ast.expr], int, int]]:
	listColumnsHARDCODED: list[str] = [
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

	def makeColumn_list_ast_expr(dataframeTarget: pandas.DataFrame) -> list[ast.expr]:
		if bool(dataframeTarget['overloadDefinition']):
			return [cast(ast.expr, dataframeTarget['type_ast_expr'])]
		matchingRows = dataframe.loc[
			(dataframe['attribute'] == dataframeTarget['attribute'])
			& (dataframe['type'] != "No")
			& (dataframe['versionMinorMinimum'] <= dataframeTarget['versionMinorMinimum'])
			, ['type_ast_expr', 'type']
		].drop_duplicates(subset='type').sort_values('type', key=lambda x: x.str.lower())

		return matchingRows['type_ast_expr'].tolist()

	dataframe['list_ast_expr'] = dataframe.apply(makeColumn_list_ast_expr, axis='columns')
	dataframe.drop(columns=['type_ast_expr', 'type',], inplace=True)

	byColumn: str = 'identifierTypeOfNode'
	dataframe = _makeColumn_guardVersion(dataframe, byColumn)

	dataframe = dataframe[elementsTarget]
	return list(dataframe.to_records(index=False))

def getElementsDOT(identifierToolClass: str, **keywordArguments: Any) -> list[tuple[str, bool, str | bool, str, list[ast.expr], int, int]]:
	return getElementsClassIsAndAttribute(identifierToolClass, **keywordArguments)

def getElementsGrab(identifierToolClass: str, **keywordArguments: Any) -> list[tuple[str, list[ast.expr], str, int, int]]:
	listColumnsHARDCODED: list[str] = ['attribute', 'type_astSuperClasses', 'versionMinorMinimumAttribute', 'TypeAlias_hasDOTIdentifier', 'type_astSuperClasses_ast_expr', ]
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

	def makeColumn_list_ast_expr(dataframeTarget: pandas.DataFrame) -> list[ast.expr]:
		matchingRows: pandas.DataFrame = dataframe.loc[
			(dataframe['attribute'] == dataframeTarget['attribute'])
			& (dataframe['versionMinorMinimum'] <= dataframeTarget['versionMinorMinimum']),
			['type_ast_expr', 'type']
		].sort_values('type', key=lambda x: x.str.lower())

		return matchingRows['type_ast_expr'].tolist()

	dataframe['list_ast_expr'] = dataframe.apply(makeColumn_list_ast_expr, axis='columns')

	byColumn: str = 'attribute'
	dataframe = _makeColumn_guardVersion(dataframe, byColumn)

	dataframe = dataframe[elementsTarget].drop_duplicates(subset=elementsTarget[2:None], keep='last').reset_index(drop=True)

	return list(dataframe.to_records(index=False))

def getElementsMake(identifierToolClass: str, **keywordArguments: Any) -> list[tuple[str, list[ast.arg], str, list[ast.expr], ast.expr, bool, list[ast.keyword], int, int]]:
	listColumnsHARDCODED: list[str] = [
	'ClassDefIdentifier',
	'versionMinorMinimumClass',
	'versionMinorMinimum_match_args',
	'listFunctionDef_args',
	'kwarg_annotationIdentifier',
	'listDefaults',
	'classAs_astAttribute',
	'listCall_keyword',
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

	elementsTarget: list[str] = ['ClassDefIdentifier', 'listFunctionDef_args', 'kwarg_annotationIdentifier', 'listDefaults', 'classAs_astAttribute', 'overloadDefinition', 'listCall_keyword', 'guardVersion', 'versionMinorMinimum']

	byColumn: str = 'ClassDefIdentifier'
	dataframe = _makeColumn_guardVersion(dataframe, byColumn)

	# TODO Create overloadDefinition flag - False until new logic added
	dataframe['overloadDefinition'] = False

	dataframe = dataframe[elementsTarget]
	return list(dataframe.to_records(index=False))

def getElementsTypeAlias(**keywordArguments: Any) -> list[tuple[str, list[ast.expr], int, int]]:
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

	def makeColumn_list4TypeAlias_value(dataframeTarget: pandas.DataFrame) -> tuple[list[Any], str]:
		matchingRows: pandas.DataFrame = dataframe.loc[
			(dataframe['TypeAlias_hasDOTSubcategory'] == dataframeTarget['TypeAlias_hasDOTSubcategory'])
			& (dataframe['ClassDefIdentifier'] != "No")
			& (dataframe['versionMinorMinimum'] <= dataframeTarget['versionMinorMinimum'])
			, ['classAs_astAttribute', 'ClassDefIdentifier']
		].drop_duplicates(subset='ClassDefIdentifier').sort_values('ClassDefIdentifier', key=lambda x: x.str.lower())

		return matchingRows['classAs_astAttribute'].tolist(), str(matchingRows['ClassDefIdentifier'].tolist())

	dataframe[['list4TypeAlias_value', 'hashable_list4TypeAlias_value']] = dataframe.apply(makeColumn_list4TypeAlias_value, axis='columns', result_type='expand') # pyright: ignore[reportArgumentType]
	dataframe.drop_duplicates(subset=['attribute', 'TypeAlias_hasDOTSubcategory', 'versionMinorMinimum', 'hashable_list4TypeAlias_value'], inplace=True)

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

	def MakeName4TypeAlias(subcategoryName: str):
		return Make.Name(subcategoryName)

	def updateColumn_list4TypeAlias_value(dataframeTarget: pandas.DataFrame) -> list[ast.expr]:
		matchingRows: pandas.DataFrame = dataframe.loc[
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

	byColumn: str = 'identifierTypeAlias'
	dataframe = _makeColumn_guardVersion(dataframe, byColumn)

	dataframe = dataframe[elementsTarget]
	return list(dataframe.to_records(index=False))

def updateDataframe() -> None:
	dataframe: pandas.DataFrame = getDataframe(includeDeprecated=True, versionMinorMaximum=None, modifyVersionMinorMinimum=False)

	# columns: reorder; drop columns, but they might be recreated later in the flow.
	# dataframe = dataframe[_columns]

	# Create 'attributeRename'
	dataframe['attributeRename'] = dataframe['attribute']
	dataframe['attributeRename'] = dataframe['attribute'].map(attributeRename__attribute).fillna(dataframe['attributeRename'])
	dataframe['attributeRename'] = dataframe[['ClassDefIdentifier', 'attribute']].apply(tuple, axis='columns').map(attributeRename__ClassDefIdentifier_attribute).fillna(dataframe['attributeRename'])

	dataframe['move2keywordArguments'] = False  # Default value for the column
	dataframe['move2keywordArguments'] = dataframe['attributeKind'].map(move2keywordArguments__attributeKind).fillna(dataframe['move2keywordArguments'])
	dataframe['move2keywordArguments'] = dataframe['attribute'].map(move2keywordArguments__attribute).fillna(dataframe['move2keywordArguments'])

	dataframe['defaultValue'] = "No"  # Default value for the column
	dataframe['defaultValue'] = dataframe['attribute'].map(defaultValue__attribute).fillna(dataframe['defaultValue'])
	dataframe['defaultValue'] = dataframe[['ClassDefIdentifier', 'attribute']].apply(tuple, axis='columns').map(defaultValue__ClassDefIdentifier_attribute).fillna(dataframe['defaultValue'])
	dataframe['defaultValue'] = dataframe[['typeStub', 'attribute']].apply(tuple, axis='columns').map(defaultValue__typeStub_attribute).fillna(dataframe['defaultValue'])

	def makeColumn_classAs_astAttribute(ClassDefIdentifier:str):
		return Make.Attribute(Make.Name('ast'), ClassDefIdentifier)
	dataframe['classAs_astAttribute'] = dataframe['ClassDefIdentifier'].astype(str).map(makeColumn_classAs_astAttribute)

	identifiersPattern: str = r'\b(' + '|'.join(dataframe['ClassDefIdentifier'].dropna().unique()) + r')\b'
	dataframe['type'] = (
		dataframe['typeStub']
		.where(dataframe['typeStub_typing_TypeAlias'] == 'No', dataframe['typeC'])
		.str.replace(identifiersPattern, r'ast.\1', regex=True)
		.str.replace("Literal[True, False]", "bool", regex=False)
	)

	dataframe['type'] = dataframe[['ClassDefIdentifier', 'attribute']].apply(tuple, axis='columns').map(type__ClassDefIdentifier_attribute).fillna(dataframe['type'])

	def makeColumn_canBeNone(dataframeTarget: pandas.DataFrame) -> str | bool:
		if cast(str, dataframeTarget['type']) == "No":
			return "No"
		elif ' | None' in dataframeTarget['type'] and 'list' in dataframeTarget['type']:
			return "list"
		elif ' | None' in dataframeTarget['type']:
			return True
		else:
			return False
	dataframe['canBeNone'] = dataframe.apply(makeColumn_canBeNone, axis='columns')

	def pythonCode2expr(string: str) -> Any:
		astModule: ast.Module = ast.parse(string)
		ast_expr: ast.expr = raiseIfNone(NodeTourist(Be.Expr, Then.extractIt(DOT.value)).captureLastMatch(astModule))
		return ast_expr

	# Create 'type_ast_expr' based on columns 'type' and 'list2Sequence'
	dataframe.loc[dataframe['list2Sequence'], 'type_ast_expr'] = dataframe['type'].str.replace("list", "Sequence").apply(pythonCode2expr)
	dataframe.loc[~dataframe['list2Sequence'], 'type_ast_expr'] = dataframe['type'].apply(pythonCode2expr)
	dataframe.loc[dataframe['type'] == "No", 'type_ast_expr'] = "No"

	# Create 'type_astSuperClasses' with TypeVar substitutions
	dataframe['type_astSuperClasses'] = dataframe['type'].replace({f"ast.{key}": value for key, value in settingsManufacturing.astSuperClasses.items()}, regex=True)
	# Create 'type_astSuperClasses_ast_expr'
	dataframe['type_astSuperClasses_ast_expr'] = numpy.where(dataframe['type_astSuperClasses'] == 'No', 'No', dataframe['type_astSuperClasses'].apply(pythonCode2expr))

	def makeColumn_ast_arg(dataframeTarget: pandas.DataFrame) -> Any:
		if cast(str | bool, dataframeTarget['move2keywordArguments']) != False:  # noqa: E712
			return "No"
		return Make.arg(cast(str, dataframeTarget['attributeRename']), annotation=cast(ast.expr, dataframeTarget['type_ast_expr']))
	dataframe['ast_arg'] = dataframe.apply(makeColumn_ast_arg, axis='columns')

	# Create TypeAlias_hasDOTIdentifier
	dataframe['TypeAlias_hasDOTIdentifier'] = numpy.where(dataframe['attributeKind'] == '_field', "hasDOT" + cast(str, dataframe['attribute']), "No")

	# Create TypeAlias_hasDOTSubcategory
	dataframe['TypeAlias_hasDOTSubcategory'] = numpy.where((identifier := dataframe['TypeAlias_hasDOTIdentifier']) == "No", "No",
		cast(str, identifier) + "_" + dataframe['type'].str.replace('|', 'Or', regex=False).str.replace('[', '_', regex=False).str.replace('[\\] ]', '', regex=True).str.replace('ast.', '', regex=False)
	)

	# === Group-Based Column Computation ===
	def computeVersionMinimum(list_byColumns: list[str]) -> numpy.ndarray[tuple[int, ...], numpy.dtype[numpy.int64]]:
		return numpy.where(dataframe.groupby(list_byColumns)['versionMinorData'].transform('min') == settingsManufacturing.versionMinor_astMinimumSupported,
			-1, dataframe.groupby(list_byColumns)['versionMinorData'].transform('min'))

	dataframe['versionMinorMinimum_match_args'] = computeVersionMinimum(['ClassDefIdentifier', 'match_args'])
	dataframe['versionMinorMinimumAttribute'] = computeVersionMinimum(['ClassDefIdentifier', 'attribute'])
	dataframe['versionMinorMinimumClass'] = computeVersionMinimum(['ClassDefIdentifier'])

	columnsOfLists: list[str] = ['listFunctionDef_args', 'listDefaults', 'listCall_keyword']
	def compute_listFunctionDef_args(dataframeTarget: pandas.DataFrame) -> pandas.Series: # pyright: ignore[reportMissingTypeArgument, reportUnknownParameterType]
		listFunctionDef_args: list[ast.arg] = []
		listDefaults: list[ast.expr] = []
		listCall_keyword: list[ast.keyword] = []

		if cast(str, dataframeTarget['attributeKind']) != "No":
			for attributeTarget in list(cast(tuple[str, ...], dataframeTarget['match_args'])):
				# TODO if dataframe['move2keywordArguments'] == 'Unpack':
				if attributeTarget == 'type_comment':
					continue

				matchingRows: pandas.DataFrame = dataframe[
					(dataframe['attribute'] == attributeTarget)
					& (dataframe['ClassDefIdentifier'] == cast(str, dataframeTarget['ClassDefIdentifier']))
					& (dataframe['versionMinorMinimum_match_args'] == cast(int, dataframeTarget['versionMinorMinimum_match_args']))
				]

				# "Hide" `attributeTarget` in the call to the `ast` constructor
				if matchingRows.iloc[0]['move2keywordArguments']:
					keywordValue = cast(ast.expr, matchingRows.iloc[0]['defaultValue'])
				# `attributeTarget` is a `Make` parameter
				else:
					# Append 'ast_arg' in the same order as match_args
					listFunctionDef_args.append(cast(ast.arg, matchingRows.iloc[0]['ast_arg']))

					# "argspec" or ast.arguments or Make.arguments: default values must be in the same order as their parameters
					if matchingRows.iloc[0]['defaultValue'] != "No":
						listDefaults.append(cast(ast.expr, matchingRows.iloc[0]['defaultValue']))

					keywordValue = Make.Name(cast(str, matchingRows.iloc[0]['attributeRename']))
					# If the type is `Sequence`, type checker will complain unless call `list` in the `ast` constructor
					if matchingRows.iloc[0]['list2Sequence']:
						keywordValue = Make.Call(Make.Name('list'), [keywordValue])

				listCall_keyword.append(Make.keyword(attributeTarget, keywordValue))

		return pandas.Series([listFunctionDef_args, listDefaults, listCall_keyword], index=columnsOfLists)
	dataframe[columnsOfLists] = dataframe.apply(compute_listFunctionDef_args, axis='columns') # pyright: ignore[reportUnknownArgumentType, reportArgumentType]

	dataframe.to_pickle(settingsManufacturing.pathFilenameDataframeAST)

if __name__ == "__main__":
	updateDataframe()