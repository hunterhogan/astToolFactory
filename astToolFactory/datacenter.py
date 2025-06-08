"""API for data. The rest of the package should be ignorant of the specifics of the data source.
This module provides a set of functions to interact with the data source, allowing for easy retrieval and manipulation of data."""
from astToolFactory import (
	dictionary_astSuperClasses, dictionaryIdentifiers, pathFilenameDataframeAST,
	pythonMinimumVersionMinor, versionMinor_astMinimumSupported,
)
from astToolkit import Be, DOT, dump, Make, NodeTourist, Then
from collections.abc import Sequence
from typing import cast
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
dataframe = dataframe[elementsTarget]
return list(dataframe.to_records(index=False))
"""

def _sortCaseInsensitive(dataframe: pandas.DataFrame, columnsPriority: Sequence[str], columnsNonString: Sequence[str] = [], ascending: bool | Sequence[bool] = True) -> pandas.DataFrame:
	dataframeCopy: pandas.DataFrame = dataframe.copy()
	columnsString: list[str] = list(set(columnsPriority).difference(set(columnsNonString)))
	dataframeCopy[columnsString] = dataframe[columnsString].map(str.lower) # pyright: ignore[reportArgumentType]

	indicesSorted = dataframeCopy.sort_values(by=columnsPriority, ascending=ascending).index
	return dataframe.loc[indicesSorted]

def getDataframe(includeDeprecated: bool, versionMinorMaximum: int | None, modifyVersionMinorMinimum: bool = True, *indices: str) -> pandas.DataFrame:
	dataframe: pandas.DataFrame = pandas.read_pickle(pathFilenameDataframeAST)

	if not includeDeprecated:
		dataframe = dataframe[~dataframe['deprecated']]

	if versionMinorMaximum is not None:
		dataframe = dataframe[dataframe['versionMinorData'] <= versionMinorMaximum]

	if modifyVersionMinorMinimum:
		columnsVersion: list[str] = ['versionMinorMinimumAttribute', 'versionMinorMinimumClass', 'versionMinorMinimum_match_args']
		dataframe[columnsVersion] = dataframe[columnsVersion].where(dataframe[columnsVersion] > pythonMinimumVersionMinor, -1) # pyright: ignore[reportArgumentType]
	if indices:
		dataframe = dataframe.set_index(list(indices))

	return dataframe

def getElementsBe(identifierToolClass: str, includeDeprecated: bool = False, versionMinorMaximum: int | None = None) -> list[tuple[str, int, str]]:
	listColumnsHARDCODED: list[str] = ['ClassDefIdentifier', 'versionMinorMinimumClass', 'classAs_astAttribute']
	listColumns: list[str] = listColumnsHARDCODED
	del listColumnsHARDCODED
	sliceString: slice = slice(0, 1)
	sliceNonString: slice = slice(1, 2)
	slice_drop_duplicates: slice = slice(0, None)

	dataframe: pandas.DataFrame = (getDataframe(includeDeprecated, versionMinorMaximum)
		[listColumns]
		.drop_duplicates(listColumns[slice_drop_duplicates], keep='last')
		.pipe(_sortCaseInsensitive, listColumns[sliceString] + listColumns[sliceNonString], listColumns[sliceNonString], [True] * len(listColumns[sliceString]) + [False] * len(listColumns[sliceNonString]))
		.reset_index(drop=True)
	)
	del listColumns

	return list(dataframe.to_records(index=False))

def getElementsClassIsAndAttribute(identifierToolClass: str, includeDeprecated: bool = False, versionMinorMaximum: int | None = None) -> list[tuple[str, bool, str | bool, str, list[str], int, int]]:
	listColumnsHARDCODED: list[str] = [
		'attribute',
		'TypeAlias_hasDOTSubcategory',
		'versionMinorMinimumAttribute',
		'typeSansNone_ast_expr',
		'typeSansNone',
		'TypeAlias_hasDOTIdentifier',
		'canBeNone',
		]

	if identifierToolClass == dictionaryIdentifiers['DOT']:
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

	dataframe: pandas.DataFrame = (getDataframe(includeDeprecated, versionMinorMaximum)
		.query("attributeKind == '_field'")
		.pipe(_sortCaseInsensitive, listColumns[sliceString] + listColumns[sliceNonString], listColumns[sliceNonString], [True] * len(listColumns[sliceString]) + [False] * len(listColumns[sliceNonString]))
		[listColumns]
		.drop_duplicates(listColumns[slice_drop_duplicates], keep='last')
		.reset_index(drop=True)
	)

	dataframe.rename(columns = {listColumns[index_type]: 'type', listColumns[index_type_ast_expr]: 'type_ast_expr'}, inplace=True)

	del listColumns

	elementsTarget = ['identifierTypeOfNode', 'overloadDefinition', 'canBeNone', 'attribute', 'list_ast_expr', 'useMatchCase', 'versionMinorMinimumAttribute']

	dataframe['overloadDefinition'] = dataframe.groupby('attribute').transform('size') > 1
	dataframeImplementationFunctionDefinitions = (
		dataframe[dataframe['overloadDefinition']]
		.groupby('attribute')['versionMinorMinimumAttribute']
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
			(dataframe['versionMinorMinimumAttribute'] <= dataframeTarget['versionMinorMinimumAttribute'])
		]['canBeNone']

		if (matchingRows == False).all():  # noqa: E712
			return False
		elif any(matchingRows.apply(lambda x: isinstance(x, str))): # pyright: ignore[reportUnknownArgumentType, reportUnknownLambdaType]
			return cast(str, matchingRows.loc[matchingRows.apply(lambda x: isinstance(x, str))].iloc[0]) # pyright: ignore[reportUnknownArgumentType, reportUnknownLambdaType]
		elif (matchingRows == True).any():  # noqa: E712
			return True
		else:
			return "Not calculated"

	dataframe.loc[dataframe['canBeNone'] == "Not calculated", 'canBeNone'] = dataframe[dataframe['canBeNone'] == "Not calculated"].apply(makeColumn_canBeNone, axis=1)

	def makeColumn_list_ast_expr(dataframeTarget: pandas.DataFrame) -> list[str]:
		if bool(dataframeTarget['overloadDefinition']):
			return [str(dataframeTarget['type_ast_expr'])]
		matchingRows = dataframe.loc[
			(dataframe['attribute'] == dataframeTarget['attribute']) &
			(dataframe['type'] != "No") &
			(dataframe['versionMinorMinimumAttribute'] <= dataframeTarget['versionMinorMinimumAttribute']),
			'type_ast_expr'
		].drop_duplicates()

		return sorted(matchingRows
				, key=lambda ast_expr: dataframe.loc[dataframe['type_ast_expr'] == ast_expr, 'type'].iloc[0].lower()
		)

	dataframe['list_ast_expr'] = dataframe.apply(makeColumn_list_ast_expr, axis=1)
	dataframe.drop(columns=['type_ast_expr', 'type',], inplace=True)
	dataframe['useMatchCase'] = numpy.where(
		((versionsTotal := dataframe.groupby('identifierTypeOfNode')['versionMinorMinimumAttribute'].transform('nunique')) == 1)
		& (dataframe.groupby('identifierTypeOfNode')['versionMinorMinimumAttribute'].transform('max') <= pythonMinimumVersionMinor),
		0,
		numpy.maximum(1, versionsTotal - dataframe.groupby('identifierTypeOfNode')['versionMinorMinimumAttribute'].rank(method='first', ascending=False).astype(int) + 1)
	)

	dataframe = dataframe[elementsTarget]
	return list(dataframe.to_records(index=False))

def getElementsDOT(identifierToolClass: str, includeDeprecated: bool = False, versionMinorMaximum: int | None = None) -> list[tuple[str, bool, str | bool, str, list[str], int, int]]:
	return getElementsClassIsAndAttribute(identifierToolClass, includeDeprecated, versionMinorMaximum)

def getElementsGrab(identifierToolClass: str, includeDeprecated: bool = False, versionMinorMaximum: int | None = None) -> list[tuple[str, list[str], str, int, int]]:
	listColumnsHARDCODED: list[str] = ['attribute', 'typeGrab', 'versionMinorMinimumAttribute', 'TypeAlias_hasDOTIdentifier', 'typeGrab_ast_expr', ]
	listColumns: list[str] = listColumnsHARDCODED
	del listColumnsHARDCODED
	sliceString: slice = slice(0, 2)
	sliceNonString: slice = slice(2, 3)
	slice_drop_duplicates: slice = slice(0, 2)
	index_type: int = 1
	index_type_ast_expr: int = 4

	dataframe: pandas.DataFrame = (getDataframe(includeDeprecated, versionMinorMaximum)
		.query("attributeKind == '_field'")
		[listColumns]
		.pipe(_sortCaseInsensitive, listColumns[sliceString] + listColumns[sliceNonString], listColumns[sliceNonString], [True] * len(listColumns[sliceString]) + [False] * len(listColumns[sliceNonString]))
		.drop_duplicates(listColumns[slice_drop_duplicates], keep='last')
		.reset_index(drop=True)
	)

	dataframe.rename(columns = {listColumns[index_type]: 'type', listColumns[index_type_ast_expr]: 'type_ast_expr'}, inplace=True)

	del listColumns

	elementsTarget: list[str] = ['TypeAlias_hasDOTIdentifier', 'list_ast_expr', 'attribute', 'useMatchCase', 'versionMinorMinimumAttribute']
	def makeColumn_list_ast_expr(dataframeTarget: pandas.DataFrame) -> list[str]:
		matchingRows = dataframe.loc[
			(dataframe['attribute'] == dataframeTarget['attribute']) &
			(dataframe['versionMinorMinimumAttribute'] <= dataframeTarget['versionMinorMinimumAttribute']),
			'type_ast_expr'
		]

		return sorted(matchingRows
				, key=lambda ast_expr: dataframe.loc[dataframe['type_ast_expr'] == ast_expr, 'type'].iloc[0].lower()
		)

	dataframe['list_ast_expr'] = dataframe.apply(makeColumn_list_ast_expr, axis=1)
	dataframe['useMatchCase'] = numpy.where(
		((versionsTotal := dataframe.groupby('attribute')['versionMinorMinimumAttribute'].transform('nunique')) == 1)
		& (dataframe.groupby('attribute')['versionMinorMinimumAttribute'].transform('max') <= pythonMinimumVersionMinor),
		0,
		numpy.maximum(1, versionsTotal - dataframe.groupby('attribute')['versionMinorMinimumAttribute'].rank(method='first', ascending=False).astype(int) + 1)
	)

	dataframe = dataframe[elementsTarget].drop_duplicates(subset=elementsTarget[2:None], keep='last').reset_index(drop=True)

	return list(dataframe.to_records(index=False))

def getElementsMake(identifierToolClass: str, includeDeprecated: bool = False, versionMinorMaximum: int | None = None) -> list[tuple[str, list[str], str, list[str], str, bool, list[tuple[str, str]], int, int]]:
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

	dataframe: pandas.DataFrame = (getDataframe(includeDeprecated, versionMinorMaximum)
		[listColumns]
		.pipe(_sortCaseInsensitive, listColumns[sliceString] + listColumns[sliceNonString], listColumns[sliceNonString], [True] * len(listColumns[sliceString]) + [False] * len(listColumns[sliceNonString]))
		.drop_duplicates(listColumns[slice_drop_duplicates], keep='last')
		.reset_index(drop=True)
	)
	del listColumns

	elementsTarget: list[str] = ['ClassDefIdentifier', 'listStr4FunctionDef_args', 'kwarg_annotationIdentifier', 'listDefaults', 'classAs_astAttribute', 'overloadDefinition', 'listTupleCall_keywords', 'useMatchCase', 'versionMinorMinimum_match_args']

	# Calculate useMatchCase as countdown for each ClassDefIdentifier-versionMinorMinimum_match_args group
	# If only one version exists, useMatchCase should be 0 (no match-case needed)
	# If multiple versions exist, countdown from total count to 1
	# And as a guard for Python versions below the minimum.
	dataframe['useMatchCase'] = numpy.where(
		((versionsTotal := dataframe.groupby('ClassDefIdentifier')['versionMinorMinimum_match_args'].transform('nunique')) == 1)
		& (dataframe.groupby('ClassDefIdentifier')['versionMinorMinimum_match_args'].transform('max') <= pythonMinimumVersionMinor),
		0,
		numpy.maximum(1, versionsTotal - dataframe.groupby('ClassDefIdentifier')['versionMinorMinimum_match_args'].rank(method='first', ascending=False).astype(int) + 1)
	)

	# Create overloadDefinition flag - False until new logic added
	dataframe['overloadDefinition'] = False

	dataframe = dataframe[elementsTarget]
	return list(dataframe.to_records(index=False))

def getElementsTypeAlias(includeDeprecated: bool = False, versionMinorMaximum: int | None = None) -> list[tuple[str, list[str], int, int]]:
	listColumnsHARDCODED: list[str] = ['attribute', 'TypeAlias_hasDOTSubcategory', 'ClassDefIdentifier', 'versionMinorMinimumAttribute', 'classAs_astAttribute', 'TypeAlias_hasDOTIdentifier',]
	listColumns: list[str] = listColumnsHARDCODED
	del listColumnsHARDCODED
	sliceString: slice = slice(0, 3)
	sliceNonString: slice = slice(3, 4)
	slice_drop_duplicates: slice = slice(0, None)
	dataframe: pandas.DataFrame = (getDataframe(includeDeprecated, versionMinorMaximum)
		.query("attributeKind == '_field'")
		[listColumns]
		.pipe(_sortCaseInsensitive, listColumns[sliceString] + listColumns[sliceNonString], listColumns[sliceNonString], [True] * len(listColumns[sliceString]) + [False] * len(listColumns[sliceNonString]))
		.drop_duplicates(listColumns[slice_drop_duplicates], keep='last')
		.reset_index(drop=True)
	)
	del listColumns

	elementsTarget: list[str] = ['identifierTypeAlias', 'list4TypeAlias_value', 'useMatchCase', 'versionMinorMinimumAttribute']

	def makeColumn_list4TypeAlias_value(dataframeTarget: pandas.DataFrame):
		matchingRows = dataframe.loc[
			(dataframe['TypeAlias_hasDOTSubcategory'] == dataframeTarget['TypeAlias_hasDOTSubcategory']) &
			(dataframe['ClassDefIdentifier'] != "No") &
			(dataframe['versionMinorMinimumAttribute'] <= dataframeTarget['versionMinorMinimumAttribute']),
			['classAs_astAttribute', 'ClassDefIdentifier']
		].drop_duplicates().sort_values('ClassDefIdentifier', key=lambda x: x.str.lower())

		return matchingRows['classAs_astAttribute'].tolist(), str(matchingRows['ClassDefIdentifier'].tolist())

	dataframe[['list4TypeAlias_value', 'hashable_list4TypeAlias_value']] = dataframe.apply(makeColumn_list4TypeAlias_value, axis=1, result_type='expand') # pyright: ignore[reportArgumentType]
	dataframe.drop_duplicates(subset=['attribute', 'TypeAlias_hasDOTSubcategory', 'versionMinorMinimumAttribute', 'hashable_list4TypeAlias_value'], inplace=True)
	dataframe.drop(columns=['classAs_astAttribute', 'ClassDefIdentifier', 'hashable_list4TypeAlias_value'], inplace=True)

	dataframe = dataframe.sort_values('versionMinorMinimumAttribute', ascending=False).groupby('attribute')[dataframe.columns].apply(
		lambda group: group if group['TypeAlias_hasDOTSubcategory'].nunique() == 1 else pandas.concat([
			group,
			group.drop_duplicates(subset='TypeAlias_hasDOTSubcategory', keep='last')[['versionMinorMinimumAttribute']].drop_duplicates().assign(
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
			(dataframe['versionMinorMinimumAttribute'] <= dataframeTarget['versionMinorMinimumAttribute']),
			['TypeAlias_hasDOTSubcategory']
		].drop_duplicates()

		return [MakeName4TypeAlias(subcategory) for subcategory in matchingRows['TypeAlias_hasDOTSubcategory']]

	mask = dataframe['list4TypeAlias_value'] == "No"
	dataframe.loc[mask, 'list4TypeAlias_value'] = dataframe.loc[mask].apply(updateColumn_list4TypeAlias_value, axis=1)

	dataframe['identifierTypeAlias'] = dataframe['TypeAlias_hasDOTIdentifier'].where(
		dataframe.groupby('attribute')['TypeAlias_hasDOTSubcategory'].transform('nunique') == 1,
		dataframe['TypeAlias_hasDOTSubcategory'].where(
			dataframe['TypeAlias_hasDOTSubcategory'] != "No",
			dataframe['TypeAlias_hasDOTIdentifier']
		)
	)
	dataframe.drop(columns=['attribute', 'TypeAlias_hasDOTSubcategory', 'TypeAlias_hasDOTIdentifier'], inplace=True)
	dataframe['useMatchCase'] = numpy.where(
		((versionsTotal := dataframe.groupby('identifierTypeAlias')['versionMinorMinimumAttribute'].transform('nunique')) == 1)
		& (dataframe.groupby('identifierTypeAlias')['versionMinorMinimumAttribute'].transform('max') <= pythonMinimumVersionMinor),
		0,
		numpy.maximum(1, versionsTotal - dataframe.groupby('identifierTypeAlias')['versionMinorMinimumAttribute'].rank(method='first', ascending=False).astype(int) + 1)
	)

	dataframe = dataframe[elementsTarget]
	return list(dataframe.to_records(index=False))

def updateDataframe() -> None:
	# === Base Source Columns: Read-Only ===
	dataframe: pandas.DataFrame = getDataframe(includeDeprecated=True, versionMinorMaximum=None, modifyVersionMinorMinimum=False)

	_columns: list[str] = [
	# read from sources
	'ClassDefIdentifier',
	'deprecated',
	'base',
	'base_typing_TypeAlias',
	'match_args',
	'attribute',
	'attributeKind',
	'typeC',
	'type_field_type',
	'typeStub',
	'typeStub_typing_TypeAlias',
	'versionMajorData',
	'versionMinorData',
	'versionMicroData',

	# Purely a human choice
	'attributeRename',
	'move2keywordArguments',
	'defaultValue', # (for now)

	# columns computed from sources per row
	'classAs_astAttribute',
	'type',
	'typeSansNone',
	'canBeNone',
	'type_ast_expr',
	'typeSansNone_ast_expr',
	'ast_arg',
	'TypeAlias_hasDOTIdentifier',
	'TypeAlias_hasDOTSubcategory',

	# columns computed from sources per group
	'versionMinorMinimumClass',
	'versionMinorMinimum_match_args',
	'versionMinorMinimumAttribute',
	'listStr4FunctionDef_args',
	'listDefaults',
	'listTupleCall_keywords',

	# columns ought to be computed per row
	'list2Sequence',

	# columns ought to be computed per group
	'kwarg_annotationIdentifier',

	# columns computed from other columns per row
	'hashableListStr4FunctionDef_args',
	'hashableListDefaults',
	'hashableListTupleCall_keywords',

	# columns computed from other columns and a dictionary per row
	'typeGrab',
	'typeGrab_ast_expr',
]

	# Change the order of columns
	# dataframe = dataframe[_columns]

	# === Human Overrides (Purely Choice-Based) ===

	dictionary_attributeRenameBy_attribute: dict[str, str] = {
		'arg': 'Buffalo_buffalo_Buffalo_buffalo_buffalo_buffalo_Buffalo_buffalo',
		'asname': 'asName',
		'attr': 'attribute',
		'ctx': 'context',
		'elt': 'element',
		'elts': 'listElements',
		'func': 'callee',
		'keywords': 'list_keyword',
		'module': 'dotModule',
		'orelse': 'orElse',
	}

	dataframe['attributeRename'] = dataframe['attribute'].map(dictionary_attributeRenameBy_attribute).fillna(dataframe['attributeRename'])

	dictionary_attributeRenameByClassDefIdentifier: dict[tuple[str, str], str] = {
		('arguments', 'args'): 'list_arg',
		('AsyncFunctionDef', 'args'): 'argumentSpecification',
		('Call', 'args'): 'listParameters',
		('FunctionDef', 'args'): 'argumentSpecification',
		('ImportFrom', 'names'): 'list_alias',
		('Lambda', 'args'): 'argumentSpecification',
	}

	dataframe['attributeRename'] = dataframe[['ClassDefIdentifier', 'attribute']].apply(tuple, axis=1).map(dictionary_attributeRenameByClassDefIdentifier).fillna(dataframe['attributeRename'])

	def makeColumn_move2keywordArguments(dataframeTarget: pandas.DataFrame) -> str | bool:
		if dataframeTarget['attributeKind'] in ["No", "_attribute"]:
			return "No"
		elif dataframeTarget['attribute'] in ["type_comment"]:
			return 'Unpack'
		elif dataframeTarget['attribute'] in ["simple"]:
			return True
		else:
			return False
	dataframe['move2keywordArguments'] = dataframe.apply(makeColumn_move2keywordArguments, axis=1)

	dictionary_defaultValueBy_attribute: dict[str, str] = {
		'asname': "Make.Constant(None)",
		'bases': "Make.List()",
		'bound': "Make.Constant(None)",
		'cases': "Make.List()",
		'cause': "Make.Constant(None)",
		'ctx': "Make.Call(Make.Attribute(Make.Name('ast'), 'Load'))",
		'decorator_list': "Make.List()",
		'default_value': "Make.Constant(None)",
		'defaults': "Make.List()",
		'elts': "Make.List()",
		'exc': "Make.Constant(None)",
		'finalbody': "Make.List()",
		'format_spec': "Make.Constant(None)",
		'guard': "Make.Constant(None)",
		'keywords': "Make.List()",
		'kind': "Make.Constant(None)",
		'kw_defaults': "Make.List([Make.Constant(None)])",
		'kwarg': "Make.Constant(None)",
		'kwd_attrs': "Make.List()",
		'kwd_patterns': "Make.List()",
		'kwonlyargs': "Make.List()",
		'level': "Make.Constant(0)",
		'lower': "Make.Constant(None)",
		'msg': "Make.Constant(None)",
		'optional_vars': "Make.Constant(None)",
		'patterns': "Make.List()",
		'posonlyargs': "Make.List()",
		'rest': "Make.Constant(None)",
		'simple': "Make.Call(Make.Name('int'), [Make.Call(Make.Name('isinstance'), [Make.Name('target'), Make.Attribute(Make.Name('ast'), 'Name')])])",
		'step': "Make.Constant(None)",
		'type': "Make.Constant(None)",
		'type_comment': "Make.Constant(None)",
		'type_ignores': "Make.List()",
		'upper': "Make.Constant(None)",
		'vararg': "Make.Constant(None)",
	}

	dataframe['defaultValue'] = dataframe['attribute'].map(dictionary_defaultValueBy_attribute).fillna('No')

	dictionary_defaultValueByClassDefIdentifier: dict[tuple[str, str], str] = {
		('AnnAssign', 'value'): "Make.Constant(None)",
		('arg', 'annotation'): "Make.Constant(None)",
		('arguments', 'args'): "Make.List()",
		('AsyncFor', 'orelse'): "Make.List()",
		('AsyncFunctionDef', 'args'): "Make.Call(Make.Attribute(Make.Name('ast'), 'arguments'))",
		('AsyncFunctionDef', 'body'): "Make.List()",
		('AsyncFunctionDef', 'returns'): "Make.Constant(None)",
		('AsyncFunctionDef', 'type_params'): "Make.List()",
		('Call', 'args'): "Make.List()",
		('ClassDef', 'body'): "Make.List()",
		('ClassDef', 'type_params'): "Make.List()",
		('Dict', 'keys'): "Make.List([Make.Constant(None)])",
		('Dict', 'values'): "Make.List()",
		('ExceptHandler', 'body'): "Make.List()",
		('ExceptHandler', 'name'): "Make.Constant(None)",
		('For', 'orelse'): "Make.List()",
		('FunctionDef', 'args'): "Make.Call(Make.Attribute(Make.Name('ast'), 'arguments'))",
		('FunctionDef', 'body'): "Make.List()",
		('FunctionDef', 'returns'): "Make.Constant(None)",
		('FunctionDef', 'type_params'): "Make.List()",
		('If', 'orelse'): "Make.List()",
		('match_case', 'body'): "Make.List()",
		('MatchAs', 'name'): "Make.Constant(None)",
		('MatchAs', 'pattern'): "Make.Constant(None)",
		('MatchMapping', 'keys'): "Make.List()",
		('Return', 'value'): "Make.Constant(None)",
		('Try', 'orelse'): "Make.List()",
		('TryStar', 'orelse'): "Make.List()",
		('While', 'orelse'): "Make.List()",
		('Yield', 'value'): "Make.Constant(None)",
    }

	dataframe['defaultValue'] = dataframe[['ClassDefIdentifier', 'attribute']].apply(tuple, axis=1).map(dictionary_defaultValueByClassDefIdentifier).fillna(dataframe['defaultValue'])

	# Set 'defaultValue' for specific attributes
	dataframe.loc[
		(dataframe['attribute'].isin(["end_col_offset", "end_lineno"])) &
		(dataframe['typeStub'] == "int | None"),
		'defaultValue'
	] = "Make.Constant(None)"

	# === Row-Based Column Computation ===

	# Update 'classAs_astAttribute' column with formatted value
	def _makeClassAs_astAttribute(ClassDefIdentifier:str):
		return dump(Make.Attribute(Make.Name('ast'), ClassDefIdentifier))
	dataframe['classAs_astAttribute'] = dataframe['ClassDefIdentifier'].astype(str).map(_makeClassAs_astAttribute)

	# Update 'type' column with standardized formatting and accurate information
	# Get unique identifiers once
	identifiers: list[str] = cast(list[str], dataframe['ClassDefIdentifier'].dropna().unique().tolist())

	dataframe['type'] = (
		dataframe['typeStub']
		.where(dataframe['typeStub_typing_TypeAlias'] == 'No', dataframe['typeC'])
		.str.replace(
			r'\b(' + '|'.join(re.escape(identifier) for identifier in identifiers) + r')\b',
			r'ast.\1',
			regex=True
		)
		.astype(str).str.replace("Literal[True, False]", "bool", regex=False)
	)

	# Override column 'type' for class `ast.Constant`, attribute `value`
	dataframe.loc[
		(dataframe['ClassDefIdentifier'] == 'Constant') & (dataframe['attribute'] == 'value'),
		'type'
	] = "ConstantValueType"

	def update_canBeNone(dataframeTarget: pandas.DataFrame) -> str | bool:
		if dataframeTarget['type'] in ["No"]:
			return "No"
		elif ' | None' in dataframeTarget['type'] and 'list' in dataframeTarget['type']:
			return "list"
		elif ' | None' in dataframeTarget['type']:
			return True
		else:
			return False
	dataframe['canBeNone'] = dataframe.apply(update_canBeNone, axis=1)

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
	dataframe['typeGrab'] = dataframe['type'].replace({f"ast.{key}": value for key, value in dictionary_astSuperClasses.items()}, regex=True)
	dataframe['typeGrab_ast_expr'] = numpy.where(dataframe['typeGrab'] == 'No', 'No', dataframe['typeGrab'].apply(pythonCode2expr))

	def make_ast_arg(dataframeTarget: pandas.DataFrame) -> str:
		if cast(str | bool, dataframeTarget['move2keywordArguments']) != False:  # noqa: E712
			return "No"
		identifier: str = cast(str, dataframeTarget['attributeRename']) if cast(str, dataframeTarget['attributeRename']) != "No" else cast(str, dataframeTarget['attribute'])
		return dump(Make.arg(identifier, annotation=eval(cast(str, dataframeTarget['type_ast_expr']))))

	# Update 'ast_arg' column based on conditions
	dataframe['ast_arg'] = dataframe.apply(make_ast_arg, axis=1)

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
		return numpy.where(dataframe.groupby(columns)['versionMinorData'].transform('min') == versionMinor_astMinimumSupported,
			-1, dataframe.groupby(columns)['versionMinorData'].transform('min'))

	dataframe['versionMinorMinimum_match_args'] = computeVersionMinimum(['ClassDefIdentifier', 'match_args'])
	dataframe['versionMinorMinimumAttribute'] = computeVersionMinimum(['ClassDefIdentifier', 'attribute'])
	dataframe['versionMinorMinimumClass'] = computeVersionMinimum(['ClassDefIdentifier'])

	# Update 'listStr4FunctionDef_args', 'listDefaults', 'listTupleCall_keywords' columns based on match_args
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
	dataframe[['listStr4FunctionDef_args', 'listDefaults', 'listTupleCall_keywords']] = dataframe.apply(compute_listFunctionDef_args, axis=1) # pyright: ignore[reportUnknownArgumentType, reportArgumentType]

	# === Row-Based: Hashable Variants ===
	dataframe['hashableListStr4FunctionDef_args'] = dataframe['listStr4FunctionDef_args'].astype(str)
	dataframe['hashableListDefaults'] = dataframe['listDefaults'].astype(str)
	dataframe['hashableListTupleCall_keywords'] = dataframe['listTupleCall_keywords'].astype(str)

	# === Save Final Result ===
	dataframe.to_pickle(pathFilenameDataframeAST)

# if __name__ == "__main__":
# 	updateDataframe()