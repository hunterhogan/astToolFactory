"""API for data. The rest of the package should be ignorant of the specifics of the data source.
This module provides a set of functions to interact with the data source, allowing for easy retrieval and manipulation of data."""
from astToolFactory import (
	pathFilenameDataframeAST, pythonMinimumVersionMinor, versionMinor_astMinimumSupported,
)
from astToolkit import Be, DOT, dump, Make, NodeTourist, Then
from collections.abc import Sequence
from typing import cast, TypedDict
from Z0Z_tools import raiseIfNone
import ast
import numpy
import pandas
import re

class DictionaryToolBe(TypedDict):
	ClassDefIdentifier: str
	classAs_astAttribute: str
	versionMinorMinimumClass: int

def _sortCaseInsensitive(dataframe: pandas.DataFrame, columnsPriority: Sequence[str], columnsNONString: Sequence[str] = [], ascending: bool | Sequence[bool] = True) -> pandas.DataFrame:
	dataframeCopy: pandas.DataFrame = dataframe.copy()
	columnsString = list(set(columnsPriority).difference(set(columnsNONString)))
	dataframeCopy[columnsString] = dataframe[columnsString].map(str.lower)

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
		dataframe[columnsVersion] = dataframe[columnsVersion].where(dataframe[columnsVersion] > pythonMinimumVersionMinor, -1)
	if indices:
		dataframe = dataframe.set_index(list(indices))  # pyright: ignore[reportUnknownMemberType]

	return dataframe

def getElementsBe(includeDeprecated: bool = False, versionMinorMaximum: int | None = None) -> list[DictionaryToolBe]:
	listElementsHARDCODED: list[str] = ['ClassDefIdentifier', 'classAs_astAttribute', 'versionMinorMinimumClass']
	listElements: list[str] = listElementsHARDCODED

	dataframe: pandas.DataFrame = (getDataframe(includeDeprecated, versionMinorMaximum)
		[listElements]
		.drop_duplicates()
		.pipe(_sortCaseInsensitive, ['ClassDefIdentifier'], ['versionMinorMinimumClass'])
	)

	return cast(list[DictionaryToolBe], dataframe.to_dict(orient='records'))

def getElementsClassIsAndAttribute(includeDeprecated: bool = False, versionMinorMaximum: int | None = None):
	listElementsHARDCODED: list[str] = [
		'attribute',
		'TypeAlias_hasDOTSubcategory',
		'versionMinorMinimumAttribute',
		'typeSansNone_ast_expr',
		'typeSansNone',
		'TypeAlias_hasDOTIdentifier',
		'canBeNone',
		]
	listElements: list[str] = listElementsHARDCODED
	del listElementsHARDCODED
	elementsTarget = ['identifierTypeOfNode', 'overloadDefinition', 'canBeNone', 'attribute', 'list_ast_expr', 'useMatchCase', 'versionMinorMinimumAttribute']

	dataframe: pandas.DataFrame = (getDataframe(includeDeprecated, versionMinorMaximum)
		.query("attributeKind == '_field'")
		# version is sorted descending
		.pipe(_sortCaseInsensitive, listElements[0:3], [listElements[2]], [True, True, False])
		[listElements]
		# ClassDefIdentifier + attribute can lead to different values for versionMinorMinimumAttribute,
		# since ClassDefIdentifier is not implicated by this function, we need to keep the lowest
		# versionMinorMinimumAttribute; hence, we use keep='last' after having sorted descending.
		.drop_duplicates(subset=listElements[0:2], keep='last')
		.reset_index(drop=True)
	)

	# Add 'overloadDefinition' based on group size
	# dataframe['overloadDefinition'] = dataframe.groupby('attribute')['attribute'].transform(lambda x: len(x) > 1)
	dataframe['overloadDefinition'] = dataframe.groupby('attribute').transform('size') > 1 # pyright: ignore[reportUnknownMemberType]
	del listElements

	# Get unique (attribute, versionMinorMinimumAttribute) pairs and create new rows
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
			typeSansNone_ast_expr="No",
			typeSansNone="No",
			canBeNone="Not calculated"
		)
		[dataframe.columns]  # Reorder columns to match original
	)

	# Concatenate and sort into place by attribute group
	dataframe = (
		pandas.concat([dataframe, dataframeImplementationFunctionDefinitions], ignore_index=True)
		.assign(__sequence_in_group=lambda df: df.groupby('attribute').cumcount())
		.sort_values(['attribute', '__sequence_in_group'], kind='stable')
		.drop(columns='__sequence_in_group')
	)
	del dataframeImplementationFunctionDefinitions

	dataframe['identifierTypeOfNode'] = dataframe['TypeAlias_hasDOTSubcategory'].where( # pyright: ignore[reportUnknownMemberType]
		dataframe['overloadDefinition'], dataframe['TypeAlias_hasDOTIdentifier']
	)
	dataframe.drop(columns=['TypeAlias_hasDOTIdentifier', 'TypeAlias_hasDOTSubcategory',], inplace=True)

	def calculate_canBeNone(dataframeTarget: pandas.DataFrame) -> str | bool:
		matchingRows = dataframe[ # pyright: ignore[reportUnknownVariableType]
			(dataframe['attribute'] == dataframeTarget['attribute']) &
			(dataframe['canBeNone'] != "Not calculated") &
			(dataframe['versionMinorMinimumAttribute'] <= dataframeTarget['versionMinorMinimumAttribute'])
		]['canBeNone']

		if (matchingRows == False).all():  # noqa: E712
			return False
		elif any(matchingRows.apply(lambda x: isinstance(x, str))): # pyright: ignore[reportUnknownLambdaType, reportUnknownMemberType, reportUnknownArgumentType]
			return cast(str, matchingRows.loc[matchingRows.apply(lambda x: isinstance(x, str))].iloc[0]) # pyright: ignore[reportUnknownLambdaType, reportUnknownMemberType, reportUnknownArgumentType]
		elif (matchingRows == True).any():  # noqa: E712
			return True
		else:
			return "Not calculated"

	dataframe.loc[dataframe['canBeNone'] == "Not calculated", 'canBeNone'] = dataframe[dataframe['canBeNone'] == "Not calculated"].apply(calculate_canBeNone, axis=1)

	def makeColumn_list_ast_expr(dataframeTarget: pandas.DataFrame) -> list[str]:   # pyright: ignore[reportUnknownParameterType, reportMissingTypeArgument]
		if cast(bool, dataframeTarget['overloadDefinition']):
			return [cast(str, dataframeTarget['typeSansNone_ast_expr'])]
		matchingRows = dataframe.loc[ # pyright: ignore[reportUnknownVariableType]
			(dataframe['attribute'] == dataframeTarget['attribute']) &
			(dataframe['typeSansNone'] != "No") &
			(dataframe['versionMinorMinimumAttribute'] <= dataframeTarget['versionMinorMinimumAttribute']),
			'typeSansNone_ast_expr'
		].drop_duplicates()

		return sorted(matchingRows # pyright: ignore[reportUnknownArgumentType]
				, key=lambda ast_expr: dataframe.loc[dataframe['typeSansNone_ast_expr'] == ast_expr, 'typeSansNone'].iloc[0].lower() # pyright: ignore[reportUnknownLambdaType, reportUnknownMemberType]
		)

	dataframe['list_ast_expr'] = dataframe.apply(makeColumn_list_ast_expr, axis=1)
	dataframe.drop(columns=['typeSansNone_ast_expr', 'typeSansNone',], inplace=True)

	dataframe['useMatchCase'] = numpy.where(
		((versionsTotal := dataframe.groupby('identifierTypeOfNode')['versionMinorMinimumAttribute'].transform('nunique')) == 1)
		& (dataframe.groupby('identifierTypeOfNode')['versionMinorMinimumAttribute'].transform('max') <= pythonMinimumVersionMinor),
		0,
		numpy.maximum(1, versionsTotal - dataframe.groupby('identifierTypeOfNode')['versionMinorMinimumAttribute'].rank(method='first', ascending=False).astype(int) + 1)
	)

	dataframe = dataframe[elementsTarget]
	return list(dataframe.to_records(index=False))  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]

def getElementsDOT(includeDeprecated: bool = False, versionMinorMaximum: int | None = None):
	return getElementsClassIsAndAttribute(includeDeprecated, versionMinorMaximum)

def getElementsGrab(includeDeprecated: bool = False, versionMinorMaximum: int | None = None) -> list[tuple[str, list[str], str, int, int]]:
	# START keep this; do not delete.
	listElementsHARDCODED: list[str] = ['TypeAlias_hasDOTIdentifier', 'typeSansNone_ast_expr', 'attribute', 'typeSansNone', 'versionMinorMinimumAttribute']
	listElements: list[str] = listElementsHARDCODED
	elementsTarget: list[str] = ['TypeAlias_hasDOTIdentifier', 'list_ast_expr', 'attribute', 'useMatchCase', 'versionMinorMinimumAttribute']
	# END keep this; do not delete.

	# Prepare the DataFrame with the necessary columns and sort it.
	dataframe = (getDataframe(includeDeprecated, versionMinorMaximum)
		.query("attributeKind == '_field'")
		[listElements]
		.pipe(_sortCaseInsensitive, columnsPriority=listElements[2:None], columnsNONString=[listElements[-1]], ascending=[True, True, False])
		.drop_duplicates(subset=listElements[2:4], keep='last')
	)

	def makeColumn_list_ast_expr(dataframeTarget: pandas.DataFrame) -> list[str]:   # pyright: ignore[reportUnknownParameterType, reportMissingTypeArgument]
		# Find all rows in the DataFrame that match the current row's 'attribute' and 'versionMinorMinimumAttribute'
		matchingRows = dataframe.loc[ # pyright: ignore[reportUnknownVariableType]
			(dataframe['attribute'] == dataframeTarget['attribute']) &
			(dataframe['versionMinorMinimumAttribute'] <= dataframeTarget['versionMinorMinimumAttribute']),
			'typeSansNone_ast_expr'
		]

		return sorted(matchingRows # pyright: ignore[reportUnknownArgumentType]
				, key=lambda ast_expr: dataframe.loc[dataframe['typeSansNone_ast_expr'] == ast_expr, 'typeSansNone'].iloc[0].lower() # pyright: ignore[reportUnknownLambdaType, reportUnknownMemberType]
		)

	dataframe['list_ast_expr'] = dataframe.apply(makeColumn_list_ast_expr, axis=1)

	dataframe['useMatchCase'] = numpy.where(
		((versionsTotal := dataframe.groupby('attribute')['versionMinorMinimumAttribute'].transform('nunique')) == 1)
		& (dataframe.groupby('attribute')['versionMinorMinimumAttribute'].transform('max') <= pythonMinimumVersionMinor),
		0,
		numpy.maximum(1, versionsTotal - dataframe.groupby('attribute')['versionMinorMinimumAttribute'].rank(method='first', ascending=False).astype(int) + 1)
	)

	dataframe = dataframe[elementsTarget].drop_duplicates(subset=elementsTarget[2:None], keep='last').reset_index(drop=True)

	return list(dataframe.to_records(index=False))  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]

def getElementsMake(includeDeprecated: bool = False, versionMinorMaximum: int | None = None) -> list[tuple[str, list[str], str, list[str], str, bool, list[tuple[str, str]], int, int]]:
	# START keep this; do not delete.
	listElementsHARDCODED: list[str] = [
	'ClassDefIdentifier',
	'versionMinorMinimumClass',
	'versionMinorMinimum_match_args',

	'listStr4FunctionDef_args',
	'kwarg_annotationIdentifier',
	'listDefaults',
	'classAs_astAttribute',
	'listTupleCall_keywords',
	]
	listElements: list[str] = listElementsHARDCODED
	# END keep this; do not delete.

	# Prepare the list of elements to be used in the DataFrame
	dataframe: pandas.DataFrame = (getDataframe(includeDeprecated, versionMinorMaximum)
		.pipe(_sortCaseInsensitive, listElements[0:3], listElements[1:3], [True, False, False])
		[listElements]
		.drop_duplicates(subset=listElements[0:3])
	)
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

	return list(dataframe[['ClassDefIdentifier', 'listStr4FunctionDef_args', 'kwarg_annotationIdentifier', 'listDefaults', 'classAs_astAttribute', 'overloadDefinition', 'listTupleCall_keywords', 'useMatchCase', 'versionMinorMinimum_match_args']].to_records(index=False)) # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType]

def getElementsTypeAlias(includeDeprecated: bool = False, versionMinorMaximum: int | None = None) -> list[tuple[str, list[str], int, int]]:
	# START keep this; do not delete.
	listElementsHARDCODED: list[str] = [
		'attribute',
		'TypeAlias_hasDOTSubcategory',
		'versionMinorMinimumAttribute',
		'ClassDefIdentifier',
		'classAs_astAttribute',
		'TypeAlias_hasDOTIdentifier',
		]
	listElements: list[str] = listElementsHARDCODED

	# Use idiomatic pandas.
	# no lambda.
	# no intermediate data structures
	# no `for`, no `iterrows`, no loops.
	# no duplicate statements.
	# Use idiomatic pandas.
	# END keep this; do not delete.

	def _makeNameDumped(subcategoryName: str) -> str:
		return dump(Make.Name(subcategoryName))

	dataframe: pandas.DataFrame = (getDataframe(includeDeprecated, versionMinorMaximum)
		.query("attributeKind == '_field'")
		[listElements]
		.drop_duplicates()
	)

	# Apply sorting
	dataframe = _sortCaseInsensitive(
		dataframe,
		['attribute', 'TypeAlias_hasDOTSubcategory', 'versionMinorMinimumAttribute'],
		['versionMinorMinimumAttribute'],
		ascending=[True, True, False]
	).reset_index()

	# Calculate derived columns using vectorized operations
	dataframe['subcategoryCount'] = dataframe.groupby('attribute')['TypeAlias_hasDOTSubcategory'].transform('nunique')
	dataframe['versionMinorMinimumAttribute'] = dataframe['versionMinorMinimumAttribute'].astype(int)

	# Calculate useMatchCase based on whether any version is above minimum Python version
	dataframe['useMatchCase'] = (
		dataframe.groupby('attribute')['versionMinorMinimumAttribute'].transform('max') > pythonMinimumVersionMinor
	).astype(int)

	# Determine identifier target
	dataframe['identifierTarget'] = numpy.where(
		dataframe['subcategoryCount'] == 1,
		dataframe['TypeAlias_hasDOTIdentifier'].astype(str),
		dataframe['TypeAlias_hasDOTSubcategory'].astype(str)
	)

	# Group and aggregate to get final result
	resultDataframe = (dataframe
		.groupby(['identifierTarget', 'versionMinorMinimumAttribute', 'useMatchCase'], sort=False)
		.aggregate({'classAs_astAttribute': list}) # pyright: ignore[reportUnknownMemberType]
		.reset_index()
	)

	# For multiple subcategory cases, create aggregated rows and insert them after the subcategory rows
	multipleSubcategoryMask = dataframe['subcategoryCount'] > 1
	if multipleSubcategoryMask.any():
		aggregatedRows = (dataframe[multipleSubcategoryMask][['attribute', 'TypeAlias_hasDOTIdentifier', 'versionMinorMinimumAttribute', 'TypeAlias_hasDOTSubcategory', 'useMatchCase']]
			.drop_duplicates()
			.assign(dumpedName=lambda df: df['TypeAlias_hasDOTSubcategory'].map(_makeNameDumped)) # pyright: ignore[reportUnknownMemberType]
			.groupby(['TypeAlias_hasDOTIdentifier', 'versionMinorMinimumAttribute', 'useMatchCase'])['dumpedName']
			.apply(list)
			.reset_index()
			.rename(columns={'TypeAlias_hasDOTIdentifier': 'identifierTarget', 'dumpedName': 'classAs_astAttribute'})
		)

		# Insert aggregated rows after their corresponding subcategory rows
		for _rowIndex, aggregatedRow in aggregatedRows.iterrows(): # pyright: ignore[reportUnknownVariableType]
			identifierTarget = str(cast(str, aggregatedRow['identifierTarget']))
			versionMinorMinimumAttribute = int(cast(int, aggregatedRow['versionMinorMinimumAttribute']))
			useMatchCase = int(cast(int, aggregatedRow['useMatchCase']))

			# Find the position of the last subcategory row for this group
			maskSubcategoryRows = (
				(resultDataframe['identifierTarget'].str.contains(f'{identifierTarget}_', na=False)) & # pyright: ignore[reportUnknownMemberType]
				(resultDataframe['versionMinorMinimumAttribute'] == versionMinorMinimumAttribute) &
				(resultDataframe['useMatchCase'] == useMatchCase)
			)

			if maskSubcategoryRows.any():
				insertPosition = resultDataframe[maskSubcategoryRows].index[-1] + 1
				resultDataframe = pandas.concat([
					resultDataframe.iloc[:insertPosition],
					pandas.DataFrame([aggregatedRow]), # pyright: ignore[reportUnknownArgumentType]
					resultDataframe.iloc[insertPosition:]
				], ignore_index=True)

	return list(resultDataframe
		.assign(classAs_astAttribute=lambda df: df['classAs_astAttribute'].apply(lambda classList: sorted(classList, key=str.lower))) # pyright: ignore[reportUnknownLambdaType, reportUnknownMemberType, reportUnknownArgumentType]
		[['identifierTarget', 'classAs_astAttribute', 'useMatchCase', 'versionMinorMinimumAttribute']].to_records(index=False)) # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]

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

	# columns aught to be computed per row
	'list2Sequence',

	# columns aught to be computed per group
	'kwarg_annotationIdentifier',

	# columns computed from other columns per row
	'hashableListStr4FunctionDef_args',
	'hashableListDefaults',
	'hashableListTupleCall_keywords',
]

	# Change the order of columns
	# dataframe = dataframe[_columns]

	# === Human Overrides (Purely Choice-Based) ===

	listAttributeRename: list[tuple[str, str]] = [
		('arg', 'Buffalo_buffalo_Buffalo_buffalo_buffalo_buffalo_Buffalo_buffalo'),
		('asname', 'asName'),
		('attr', 'attribute'),
		('ctx', 'context'),
		('elt', 'element'),
		('elts', 'listElements'),
		('func', 'callee'),
		('keywords', 'list_keyword'),
		('module', 'dotModule'),
		('orelse', 'orElse'),
	]
	for attribute, attributeRename in listAttributeRename:
		dataframe.loc[
			(dataframe['attribute'] == attribute),
			'attributeRename'
		] = attributeRename

	listAttributeRenamePerClass: list[tuple[str, str, str]] = [
		('arguments', 'args', 'list_arg'),
		('AsyncFunctionDef', 'args', 'argumentSpecification'),
		('Call', 'args', 'listParameters'),
		('FunctionDef', 'args', 'argumentSpecification'),
		('ImportFrom', 'names', 'list_alias'),
		('Lambda', 'args', 'argumentSpecification'),
	]
	for ClassDefIdentifier, attribute, attributeRename in listAttributeRenamePerClass:
		dataframe.loc[
			(dataframe['ClassDefIdentifier'] == ClassDefIdentifier) & (dataframe['attribute'] == attribute),
			'attributeRename'
		] = attributeRename

	def update_move2keywordArguments(dataframeTarget: pandas.DataFrame) -> str | bool:
		if dataframeTarget['attributeKind'] in ["No", "_attribute"]:
			return "No"
		elif dataframeTarget['attribute'] in ["type_comment"]:
			return 'Unpack'
		elif dataframeTarget['attribute'] in ["simple"]:
			return True
		else:
			return False
	dataframe['move2keywordArguments'] = dataframe.apply(update_move2keywordArguments, axis=1)

	# === Row-Based Column Computation ===

	# Update 'classAs_astAttribute' column with formatted value
	def _makeClassAs_astAttribute(ClassDefIdentifier:str):
		return dump(Make.Attribute(Make.Name('ast'), ClassDefIdentifier))
	dataframe['classAs_astAttribute'] = dataframe['ClassDefIdentifier'].map(_makeClassAs_astAttribute) # pyright: ignore[reportUnknownMemberType]

	# Update 'type' column with standardized formatting and accurate information
	# Get unique identifiers once
	identifiers: list[str] = cast(list[str], dataframe['ClassDefIdentifier'].dropna().unique().tolist()) # pyright: ignore[reportUnknownMemberType]

	dataframe['type'] = (
		dataframe['typeStub']
		.where(dataframe['typeStub_typing_TypeAlias'] == 'No', dataframe['typeC']) # pyright: ignore[reportUnknownMemberType]
		.str.replace(
			r'\b(' + '|'.join(re.escape(identifier) for identifier in identifiers) + r')\b',
			r'ast.\1',
			regex=True
		)
		.str.replace("Literal[True, False]", "bool", regex=False)
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
	dataframe['type_ast_expr'] = numpy.where(dataframe['type'] == 'No', 'No', dataframe['type'].apply(pythonCode2expr)) # pyright: ignore[reportUnknownMemberType]
	# Update 'type_ast_expr' based on 'list2Sequence' column
	dataframe.loc[dataframe['list2Sequence'] == True, 'type_ast_expr'] = dataframe['type_ast_expr'].str.replace("'list'", "'Sequence'")   # pyright: ignore[reportUnknownMemberType]  # noqa: E712

	dataframe['typeSansNone'] = dataframe['type'].replace(' \\| None', '', regex=True) # pyright: ignore[reportUnknownMemberType]
	# Update 'typeSansNone_ast_expr' based on 'type' column
	dataframe['typeSansNone_ast_expr'] = numpy.where(dataframe['typeSansNone'] == 'No', 'No', dataframe['typeSansNone'].apply(pythonCode2expr)) # pyright: ignore[reportUnknownMemberType]
	# Update 'typeSansNone_ast_expr' based on 'list2Sequence' column
	dataframe.loc[dataframe['list2Sequence'] == True, 'typeSansNone_ast_expr'] = dataframe['typeSansNone_ast_expr'].str.replace("'list'", "'Sequence'")  # pyright: ignore[reportUnknownMemberType]  # noqa: E712

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
		.str.replace('|', 'Or', regex=False)   # pyright: ignore[reportUnknownMemberType]
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
	def compute_listFunctionDef_args(dataframeTarget: pandas.DataFrame) -> pandas.Series: # pyright: ignore[reportUnknownParameterType, reportMissingTypeArgument]
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
	dataframe[['listStr4FunctionDef_args', 'listDefaults', 'listTupleCall_keywords']] = dataframe.apply(compute_listFunctionDef_args, axis=1) # pyright: ignore[reportUnknownArgumentType]

	# === Row-Based: Hashable Variants ===
	dataframe['hashableListStr4FunctionDef_args'] = dataframe['listStr4FunctionDef_args'].astype(str)
	dataframe['hashableListDefaults'] = dataframe['listDefaults'].astype(str)
	dataframe['hashableListTupleCall_keywords'] = dataframe['listTupleCall_keywords'].astype(str)

	# === Save Final Result ===
	dataframe.to_pickle(pathFilenameDataframeAST)

# if __name__ == "__main__":
# 	updateDataframe()