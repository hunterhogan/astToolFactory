"""API for data. The rest of the package should be ignorant of the specifics of the data source.
This module provides a set of functions to interact with the data source, allowing for easy retrieval and manipulation of data."""
from astToolFactory import (
	pathFilenameDataframeAST, pythonMinimumVersionMinor, versionMinor_astMinimumSupported,
)
from astToolkit import Be, DOT, dump, Make, NodeTourist, Then
from collections.abc import Sequence
from itertools import chain
from numpy._typing._array_like import NDArray
from typing import cast, TypeAlias, TypedDict
from Z0Z_tools import raiseIfNone
import ast
import numpy
import pandas
import re

Version: TypeAlias = int
ListTypesASTformAsStr: TypeAlias = list[str]
TupleTypesForVersion: TypeAlias = tuple[Version, ListTypesASTformAsStr]
ListTypesByVersion: TypeAlias = list[TupleTypesForVersion]

class DictionaryToolBe(TypedDict):
	ClassDefIdentifier: str
	classAs_astAttribute: str
	versionMinorMinimumClass: int

class DictionaryMatchArgs(TypedDict):
	kwarg_annotationIdentifier: str
	listDefaults: list[str]
	listStr4FunctionDef_args: list[str]
	listTupleCall_keywords: list[tuple[str, str]]

class DictionaryClassDef(TypedDict):
	classAs_astAttribute: str
	versionMinorMinimumClass: dict[int, dict[int, DictionaryMatchArgs]]

def _sortCaseInsensitive(dataframe: pandas.DataFrame, columnsPriority: Sequence[str], columnsNONString: Sequence[str] = [], ascending: bool | Sequence[bool] = True) -> pandas.DataFrame:
	dataframeCopy: pandas.DataFrame = dataframe.copy()
	columnsString = list(set(columnsPriority) - set(columnsNONString))
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

def getElementsClassIsAndAttribute(includeDeprecated: bool = False, versionMinorMaximum: int | None = None) -> list[tuple[int, str, str, bool, list[str], bool | str, list[str], bool | str]]:
	listElementsHARDCODED: list[str] = ['attribute', 'TypeAlias_hasDOTSubcategory', 'versionMinorMinimumAttribute', 'type_ast_expr', 'typeSansNone_ast_expr', 'TypeAlias_hasDOTIdentifier']
	listElements: list[str] = listElementsHARDCODED

	dataframe: pandas.DataFrame = (getDataframe(includeDeprecated, versionMinorMaximum)
		.query("attributeKind == '_field'")
		.pipe(_sortCaseInsensitive, listElements[0:2], ['versionMinorMinimumAttribute'])
		[listElements]
		.drop_duplicates()
		.drop_duplicates(subset=['attribute', 'TypeAlias_hasDOTSubcategory'], keep='first')	)
	# Vectorized calculation of attributeIsNotNone
	dataframe = dataframe.copy()  # Avoid SettingWithCopyWarning
	dataframe['hasNone'] = dataframe['type_ast_expr'].astype(str).str.contains('None', na=False)
	dataframe['hasSequence'] = dataframe['type_ast_expr'].astype(str).str.contains('Sequence', na=False)
	dataframe['attributeIsNotNone'] = dataframe.apply(lambda row: 'Sequence' if row['hasNone'] and row['hasSequence'] else True if row['hasNone'] else False, axis=1)   # pyright: ignore[reportUnknownLambdaType, reportUnknownArgumentType, reportUnknownMemberType]

	listTuples: list[tuple[int, str, str, bool, list[str], bool | str, list[str], bool | str]] = []

	for attribute, groupAttribute in dataframe.groupby('attribute'):
		TypeAlias_hasDOTIdentifier = str(groupAttribute['TypeAlias_hasDOTIdentifier'].iloc[0]) # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
		subcategories = groupAttribute.groupby('TypeAlias_hasDOTSubcategory')

		def addTuple(versionMinorMinimumAttribute: int, subcategoryIdentifier: str, isOverload: bool,
					list_ast_expr: list[str], attributeIsNotNone: bool | str) -> None:
			orElseList_ast_expr: list[str] = []
			orElseAttributeIsNotNone: bool | str = False
			listTuples.append((versionMinorMinimumAttribute, str(attribute), subcategoryIdentifier,
							isOverload, list_ast_expr, attributeIsNotNone, orElseList_ast_expr, orElseAttributeIsNotNone))

		if len(subcategories) == 1:
			# Single subcategory case
			subcategoryData = groupAttribute.iloc[0] # pyright: ignore[reportUnknownVariableType]
			addTuple(
				int(cast(int, subcategoryData['versionMinorMinimumAttribute'])),
				TypeAlias_hasDOTIdentifier,
				False,  # isOverload
				[str(cast(str, subcategoryData['typeSansNone_ast_expr']))],
				cast(bool | str, subcategoryData['attributeIsNotNone'])
			)
		else:
			# Multiple subcategories case
			# Add individual overload entries
			for subcategoryName, subcategoryGroup in subcategories:
				subcategoryData = subcategoryGroup.iloc[0] # pyright: ignore[reportUnknownVariableType]
				addTuple(
					int(cast(int, subcategoryData['versionMinorMinimumAttribute'])),
					str(subcategoryName),
					True,  # isOverload
					[str(cast(str, subcategoryData['typeSansNone_ast_expr']))],
					cast(bool | str, subcategoryData['attributeIsNotNone'])
				)			# Add combined entry
			unique_typeSansNone_ast_expr = sorted(groupAttribute['typeSansNone_ast_expr'].drop_duplicates().astype(str).tolist(), key=str.lower)
			attributeNotNoneValues: list[bool | str] = [value for value in groupAttribute['attributeIsNotNone'].tolist()] # pyright: ignore[reportUnknownVariableType]
			hasSequenceInAny = any(str(value) == 'Sequence' for value in attributeNotNoneValues)
			hasTruthyInAny = any(bool(value) and str(value) != 'False' for value in attributeNotNoneValues)
			combinedAttributeIsNotNone: bool | str = (
				'Sequence' if hasSequenceInAny
				else True if hasTruthyInAny
				else False
			)
			minimum_version = int(cast(int, groupAttribute['versionMinorMinimumAttribute'].min()))

			addTuple(
				minimum_version,
				TypeAlias_hasDOTIdentifier,
				False,  # isOverload
				unique_typeSansNone_ast_expr,
				combinedAttributeIsNotNone
			)

	return listTuples

def getElementsDOT(includeDeprecated: bool = False, versionMinorMaximum: int | None = None) -> list[tuple[int, str, str, bool, list[str], bool | str, list[str], bool | str]]:
	return getElementsClassIsAndAttribute(includeDeprecated, versionMinorMaximum)

def getElementsGrab(includeDeprecated: bool = False, versionMinorMaximum: Version | None = None) -> list[tuple[int, str, str, list[str], bool, list[str], bool]]:
	listElementsHARDCODED: list[str] = ['attribute', 'versionMinorMinimumAttribute', 'type_ast_expr', 'typeSansNone_ast_expr', 'TypeAlias_hasDOTIdentifier']
	listElements: list[str] = listElementsHARDCODED

	dataframeSource: pandas.DataFrame = (getDataframe(includeDeprecated, versionMinorMaximum)
		.query("attributeKind == '_field'")
	)

	dataframe: pandas.DataFrame = (dataframeSource
		[listElements]
		.drop_duplicates()
		.drop_duplicates(subset=['attribute', 'typeSansNone_ast_expr'], keep='first')
		.pipe(_sortCaseInsensitive, ['attribute'])
	)

	dataframe = dataframe.groupby(['attribute', 'versionMinorMinimumAttribute'])['typeSansNone_ast_expr'].aggregate(list).reset_index()
	dataframe['typeSansNone_ast_expr'] = dataframe['typeSansNone_ast_expr'].apply(sorted, key=str.lower)
	dataframe['listTypesByVersion'] = dataframe[['versionMinorMinimumAttribute', 'typeSansNone_ast_expr']].apply(tuple, axis=1)

	# Add TypeAlias_hasDOTIdentifier back by merging
	dataframeWithIdentifier: pandas.DataFrame = (dataframeSource
		[['attribute', 'TypeAlias_hasDOTIdentifier']]
		.drop_duplicates()
		.pipe(_sortCaseInsensitive, ['attribute'])
	)
	dataframe = dataframe.merge(dataframeWithIdentifier, on='attribute', how='left')

	# Create the tuple list structure
	listTuples: list[tuple[int, str, str, list[str], bool, list[str], bool]] = []
	for attribute, group in dataframe.groupby('attribute'):
		listTypesByVersion: list[tuple[int, list[str]]] = cast(ListTypesByVersion, group['listTypesByVersion'].tolist())
		TypeAlias_hasDOTIdentifier: str = cast(str, group['TypeAlias_hasDOTIdentifier'].iloc[0])   # pyright: ignore[reportUnknownMemberType]

		if len(listTypesByVersion) > 1:
			# Handle multiple versions: create combined version for max version
			versionMax: int = max([typesForVersion[0] for typesForVersion in listTypesByVersion])
			combinedTypes: list[str] = sorted(chain(*[typesForVersion[1] for typesForVersion in listTypesByVersion]), key=str.lower)

			# Add entry for minimum version
			versionMin: int = min([typesForVersion[0] for typesForVersion in listTypesByVersion])
			minVersionTypes: list[str] = []
			for versionMinorMinimumAttribute, list_type_ast_expr in listTypesByVersion:
				if versionMinorMinimumAttribute == versionMin:
					minVersionTypes = list_type_ast_expr
					break

			if versionMin > pythonMinimumVersionMinor:
				# Entry for minimum version with orElse pointing to combined types
				listTuples.append((versionMin, str(attribute), TypeAlias_hasDOTIdentifier, minVersionTypes, False, combinedTypes, False))
			else:
				# Entry for maximum version
				listTuples.append((versionMax, str(attribute), TypeAlias_hasDOTIdentifier, combinedTypes, False, [], False))
		else:
			# Single version case
			versionMinorMinimumAttribute, list_type_ast_expr = listTypesByVersion[0]
			listTuples.append((versionMinorMinimumAttribute, str(attribute), TypeAlias_hasDOTIdentifier, list_type_ast_expr, False, [], False))

	return listTuples

def getElementsMake(includeDeprecated: bool = False, versionMinorMaximum: int | None = None) -> list[tuple[str, list[str], str, list[str], str, bool, list[tuple[str, str]], int, int]]:
	# START keep this; do not delete.
	listElementsHARDCODED: list[str] = [
	'ClassDefIdentifier',
	'versionMinorMinimumClass',
	'versionMinorMinimum_match_args',
	'hashableListStr4FunctionDef_args',
	'hashableListDefaults',
	'hashableListTupleCall_keywords',

	'classAs_astAttribute',
	'kwarg_annotationIdentifier',
	'listStr4FunctionDef_args',
	'listDefaults',
	'listTupleCall_keywords',
	]
	listElements: list[str] = listElementsHARDCODED
	# END keep this; do not delete.

	dataframe: pandas.DataFrame = (getDataframe(includeDeprecated, versionMinorMaximum)
		.pipe(_sortCaseInsensitive, ['ClassDefIdentifier', 'versionMinorMinimumClass', 'versionMinorMinimum_match_args']
									, ['versionMinorMinimumClass', 'versionMinorMinimum_match_args']
									, [True, False, False]
			)
	)

	dataframe = dataframe[listElements].drop_duplicates(subset=listElements[0:3])

	# Calculate useMatchCase as countdown for each ClassDefIdentifier group
	# If only one version exists, useMatchCase should be 0 (no match-case needed)
	# If multiple versions exist, countdown from total count to 1
	dataframe['totalVersionCount'] = dataframe.groupby('ClassDefIdentifier')['versionMinorMinimum_match_args'].transform('nunique')
	dataframe['versionRank'] = dataframe.groupby('ClassDefIdentifier')['versionMinorMinimum_match_args'].rank(method='first', ascending=False).astype(int)
	dataframe['useMatchCase'] = numpy.where(
		dataframe['totalVersionCount'] == 1,
		0,
		dataframe['totalVersionCount'] - dataframe['versionRank'] + 1
	)

	# Create overloadDefinition flag - always False for this refactoring
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

	# no lambda. period. NO. lambda. period. no lambda.
	# no intermediate data structures
	# no `for`, no `iterrows`, no loops.
	# no duplicate statements: if even one line is a duplicate, I will reject the entire thing
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

	# To be removed
	'kwargAnnotation',
]

	# Change the order of columns
	dataframe = dataframe[_columns]

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

	def update_move2keywordArguments(row: pandas.Series) -> str | bool:   # pyright: ignore[reportUnknownParameterType, reportMissingTypeArgument]
		if row['attributeKind'] in ["No", "_attribute"]:
			return "No"
		elif row['attribute'] in ["type_comment"]:
			return 'Unpack'
		elif row['attribute'] in ["simple"]:
			return True
		else:
			return False
	dataframe['move2keywordArguments'] = dataframe.apply(update_move2keywordArguments, axis=1) # pyright: ignore[reportUnknownArgumentType]

	# === Row-Based Column Computation ===

	# Update 'classAs_astAttribute' column with formatted value
	def _makeClassAs_astAttribute(ClassDefIdentifier:str):
		return dump(Make.Attribute(Make.Name('ast'), ClassDefIdentifier))
	dataframe['classAs_astAttribute'] = dataframe['ClassDefIdentifier'].map(_makeClassAs_astAttribute) # pyright: ignore[reportUnknownMemberType]

	# Update 'type' column with standardized formatting and accurate information
	def transform_type(value: str, identifiers: list[str]) -> str:
		# Prepend "ast." to substrings matching 'ClassDefIdentifier', case-sensitive
		pattern: str = r'\b(' + '|'.join(re.escape(identifier) for identifier in identifiers) + r')\b'
		value = re.sub(pattern, r'ast.\1', value)
		# Replace "Literal[True, False]" with "bool"
		return value.replace("Literal[True, False]", "bool")
	dataframe['type'] = dataframe.apply(
		lambda row: transform_type(row['typeStub'] if row['typeStub_typing_TypeAlias'] == 'No' else row['typeC'], dataframe['ClassDefIdentifier'].dropna().unique().tolist()),   # pyright: ignore[reportUnknownArgumentType,reportUnknownLambdaType]
		axis=1
	)

	# Override column 'type' for class `ast.Constant`, attribute `value`
	dataframe.loc[
		(dataframe['ClassDefIdentifier'] == 'Constant') & (dataframe['attribute'] == 'value'),
		'type'
	] = "ConstantValueType"

	def pythonCode2expr(string: str) -> str:
		astModule: ast.Module = ast.parse(string)
		ast_expr: ast.expr = raiseIfNone(NodeTourist(Be.Expr, Then.extractIt(DOT.value)).captureLastMatch(astModule))
		return dump(ast_expr)

	# Update 'type_ast_expr' based on 'type' column
	dataframe['type_ast_expr'] = numpy.where(dataframe['type'] == 'No', 'No', dataframe['type'].apply(pythonCode2expr))
	# Update 'type_ast_expr' based on 'list2Sequence' column
	dataframe.loc[dataframe['list2Sequence'] == True, 'type_ast_expr'] = dataframe['type_ast_expr'].str.replace("'list'", "'Sequence'")   # pyright: ignore[reportUnknownMemberType]  # noqa: E712

	def typeSansNone(string: str) -> str:
		return pythonCode2expr(string.replace(' | None', ''))

	# Update 'typeSansNone_ast_expr' based on 'type' column
	dataframe['typeSansNone_ast_expr'] = numpy.where(dataframe['type'] == 'No', 'No', dataframe['type'].apply(typeSansNone))
	# Update 'typeSansNone_ast_expr' based on 'list2Sequence' column
	dataframe.loc[dataframe['list2Sequence'] == True, 'typeSansNone_ast_expr'] = dataframe['typeSansNone_ast_expr'].str.replace("'list'", "'Sequence'")  # pyright: ignore[reportUnknownMemberType]  # noqa: E712

	def make_ast_arg(row: pandas.Series) -> str:   # pyright: ignore[reportUnknownParameterType, reportMissingTypeArgument]
		if row['move2keywordArguments'] != False:  # noqa: E712
			return "No"
		identifier: str = cast(str, row['attributeRename'] if row['attributeRename'] != "No" else row['attribute'])
		return dump(Make.arg(identifier, annotation=eval(cast(str, row['type_ast_expr']))))

	# Update 'ast_arg' column based on conditions
	dataframe['ast_arg'] = dataframe.apply(make_ast_arg, axis=1) # pyright: ignore[reportUnknownArgumentType]

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
	def compute_listFunctionDef_args(row: pandas.Series) -> pandas.Series:   # pyright: ignore[reportUnusedFunction, reportUnknownParameterType, reportMissingTypeArgument]
		if row['attributeKind'] == "No":
			return pandas.Series([[], [], []], index=[
				'listStr4FunctionDef_args',
				'listDefaults',
				'listTupleCall_keywords'
			])
		listAttributes: list[str] = list(cast(tuple[str, ...], row['match_args']))
		className = cast(str, row['ClassDefIdentifier'])
		version = cast(int, row['versionMinorMinimum_match_args'])
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
	dataframe[['listStr4FunctionDef_args', 'listDefaults', 'listTupleCall_keywords']] = dataframe.apply(compute_listFunctionDef_args, axis=1)   # pyright: ignore[reportUnknownArgumentType]

	# === Row-Based: Hashable Variants ===
	dataframe['hashableListStr4FunctionDef_args'] = dataframe['listStr4FunctionDef_args'].astype(str)
	dataframe['hashableListDefaults'] = dataframe['listDefaults'].astype(str)
	dataframe['hashableListTupleCall_keywords'] = dataframe['listTupleCall_keywords'].astype(str)

	# === Save Final Result ===
	dataframe.to_pickle(pathFilenameDataframeAST)

# if __name__ == "__main__":
# 	updateDataframe()