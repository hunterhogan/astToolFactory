"""API for data. The rest of the package should be ignorant of the specifics of the data source.
This module provides a set of functions to interact with the data source, allowing for easy retrieval and manipulation of data."""
from astToolFactory import pythonMinimumVersionMinor, settingsPackage
from astToolkit import Be, DOT, dump, Make, NodeTourist, Then
from collections import defaultdict
from collections.abc import Sequence
from itertools import chain
from pathlib import Path
from typing import cast, TypeAlias, TypedDict
from Z0Z_tools import raiseIfNone
import ast
import numpy
import pandas
import re

# TODO datacenter needs to do all data manipulation, not factory.py
# TODO more and better pandas usage

pathFilenameDataframeAST: Path = settingsPackage.pathPackage / 'dataframeAST.pkl'
versionMinor_astMinimumSupported = 9

Attribute: TypeAlias = str
Version: TypeAlias = int
ListTypesASTformAsStr: TypeAlias = list[str]
TupleTypesForVersion: TypeAlias = tuple[Version, ListTypesASTformAsStr]
ListTypesByVersion: TypeAlias = list[TupleTypesForVersion]

class DictionaryToolBe(TypedDict):
	ClassDefIdentifier: str
	classAs_astAttribute: str
	versionMinorMinimumClass: int

class DictionaryMatchArgs(TypedDict):
	kwarg: str
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

	return dataframe.to_dict(orient='records')   # pyright: ignore[reportReturnType]

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
			subcategoryData = groupAttribute.iloc[0]
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
				subcategoryData = subcategoryGroup.iloc[0]
				addTuple(
					int(subcategoryData['versionMinorMinimumAttribute']),
					str(subcategoryName),
					True,  # isOverload
					[str(subcategoryData['typeSansNone_ast_expr'])],
					subcategoryData['attributeIsNotNone']
				)			# Add combined entry
			unique_typeSansNone_ast_expr = sorted(groupAttribute['typeSansNone_ast_expr'].drop_duplicates().astype(str).tolist(), key=str.lower)
			attributeNotNoneValues = [val for val in groupAttribute['attributeIsNotNone'].tolist()]
			hasSequenceInAny = any(str(val) == 'Sequence' for val in attributeNotNoneValues)
			hasTruthyInAny = any(bool(val) and str(val) != 'False' for val in attributeNotNoneValues)
			combinedAttributeIsNotNone: bool | str = (
				'Sequence' if hasSequenceInAny
				else True if hasTruthyInAny
				else False
			)
			minimum_version = int(groupAttribute['versionMinorMinimumAttribute'].min())

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

def getElementsMake(includeDeprecated: bool = False, versionMinorMaximum: int | None = None) -> dict[str, DictionaryClassDef]:
	listElementsHARDCODED: list[str] = [
	'ClassDefIdentifier',
	'classAs_astAttribute',
	'list2Sequence',
	'versionMinorMinimumClass',
	'versionMinorMinimum_match_args',
	'hashableListStr4FunctionDef_args',
	'hashableListDefaults',
	'hashableListTupleCall_keywords',
	'kwargAnnotation',
	'listStr4FunctionDef_args',
	'listDefaults',
	'listTupleCall_keywords',
	]
	listElements: list[str] = listElementsHARDCODED
	columnsHashable: slice = slice(0, 9)

	dataframe: pandas.DataFrame = (getDataframe(includeDeprecated, versionMinorMaximum)
		.query("attribute != 'No'")
		.pipe(_sortCaseInsensitive, ['ClassDefIdentifier'], ['versionMinorMinimumClass', 'versionMinorMinimum_match_args'])
	)

	def compute_kwarg(group: pandas.Series) -> str:   # pyright: ignore[reportMissingTypeArgument, reportUnknownParameterType]
		list_kwargAnnotation: list[str] = sorted(value for value in group.unique() if value != "No")
		return 'OR'.join(list_kwargAnnotation) if list_kwargAnnotation else "No"
	dataframe['kwarg'] = (dataframe.groupby(['ClassDefIdentifier', 'versionMinorMinimum_match_args'])['kwargAnnotation'].transform(compute_kwarg))   # pyright: ignore[reportUnknownArgumentType]

	dataframe = dataframe.drop(columns=['kwargAnnotation'])
	listElements.insert(listElements.index('kwargAnnotation'), 'kwarg')
	listElements.remove('kwargAnnotation')

	# TODO keep='last' is necessary for ast.FunctionDef.type_params when `pythonVersionMinorMinimum` == 12
	# But I don't think that should be necessary, so investigate why it is.
	dataframe = dataframe.drop_duplicates(subset=listElements[columnsHashable], keep='last')

	def idkHowToNameThingsOrFollowInstructions(groupbyClassVersion: pandas.DataFrame) -> dict[int, DictionaryMatchArgs]:
		return {
			row['versionMinorMinimum_match_args']: {
				'kwarg': row['kwarg'],
				'listDefaults': row['listDefaults'],
				'listStr4FunctionDef_args': row['listStr4FunctionDef_args'],
				'listTupleCall_keywords': row['listTupleCall_keywords']
			}
			for _rowIndex, row in groupbyClassVersion.iterrows()   # pyright: ignore[reportUnknownVariableType]
		}

	dictionaryClassDef: dict[str, DictionaryClassDef] = {}
	for ClassDefIdentifier, class_group in dataframe.groupby('ClassDefIdentifier', sort=False):
		dictionaryClassDef[cast(str, ClassDefIdentifier)] = {
			'classAs_astAttribute': class_group['classAs_astAttribute'].iloc[0],   # pyright: ignore[reportUnknownMemberType]
			'versionMinorMinimumClass': {}
		}
		for versionMinorMinimumClass, groupbyClassVersion in class_group.groupby('versionMinorMinimumClass'):
			dictionaryClassDef[cast(str, ClassDefIdentifier)]['versionMinorMinimumClass'][cast(int, versionMinorMinimumClass)] = idkHowToNameThingsOrFollowInstructions(groupbyClassVersion)
	return dictionaryClassDef

def _makeNameDumped(subcategoryName: str) -> str:
	return dump(Make.Name(subcategoryName))

def getElementsTypeAlias(includeDeprecated: bool = False, versionMinorMaximum: int | None = None) -> list[tuple[str, list[str], int, int]]:
	# START keep this
	listElementsHARDCODED: list[str] = [
		'attribute',
		'TypeAlias_hasDOTSubcategory',
		'versionMinorMinimumAttribute',
		'ClassDefIdentifier',
		'classAs_astAttribute',
		'TypeAlias_hasDOTIdentifier',
		]
	listElements: list[str] = listElementsHARDCODED
	# END keep this

	# relationships between columns
		# by each 'attribute'
		# has at least one 'versionMinorMinimumAttribute',
		# has one overall 'TypeAlias_hasDOTIdentifier',
		# 	each 'TypeAlias_hasDOTSubcategory',
		# 	has at least one 'versionMinorMinimumAttribute',
		# 		the value(s) might be higher than the smallest overall 'versionMinorMinimumAttribute',
		# 	has at least one 'classAs_astAttribute',
		# 		which we want to sort using 'ClassDefIdentifier' because in the future, 'classAs_astAttribute' will be an ast object but 'ClassDefIdentifier' will always be a string,

	# output
	# the tuple
	# TypeAlias_hasDOTIdentifier, list4TypeAlias_value, useMatchCase, versionMinorMinimum

	# source of values
	# TypeAlias_hasDOTIdentifier = 'TypeAlias_hasDOTIdentifier' | 'TypeAlias_hasDOTSubcategory'
	# list4TypeAlias_value = list['classAs_astAttribute'] (the column) | list[TypeAlias_hasDOTIdentifier] (the variable)
	# 		if there is more than one versionMinorMinimumAttribute, then the elements of for each version's list are the elements whose versionMinorMinimumAttribute is <= the versionMinorMinimum being aggregated
	# useMatchCase = 0 (+1 for each unique value of versionMinorMinimumAttribute > pythonMinimumVersionMinor; then +1 if any versionMinorMinimumAttribute <= pythonMinimumVersionMinor)
	# versionMinorMinimum = 'versionMinorMinimumAttribute'

	# sorting: the sort is partially based on columns that are NOT in the tuples
	# 1. 'attribute', CaseInsensitive, ascending
	# 2. TypeAlias_hasDOTIdentifier (the variable/tuple value)
	# 	A. 'TypeAlias_hasDOTSubcategory' before 'TypeAlias_hasDOTIdentifier'
	# 		a. 'TypeAlias_hasDOTSubcategory', CaseInsensitive, ascending
	# 		b. versionMinorMinimum, _descending_, which should cause useMatchCase to be descending
	# 	B. 'TypeAlias_hasDOTIdentifier'
	# 		a. versionMinorMinimum, _descending_, which should cause useMatchCase to be descending

	# use _sortCaseInsensitive for sorting
	# use _sortCaseInsensitive for sorting
	# ONLY use _sortCaseInsensitive for sorting
	# do not sort columns any other way
	# ONLY use _sortCaseInsensitive for sorting

	# list4TypeAlias_value is sorted within the list, CaseInsensitive, ascending

	# no lambda. period. NO. lambda. period. no lambda.
	# no intermediate data structures
	# no `for`, no `iterrows`, no loops.
	# no intermediate data structures
	# no duplicate statements: if even one line is a duplicate, I will reject the entire thing
	# no intermediate data structures, which means no dictionaries
	# no new functions
	# no intermediate data structures
	# no new classes

	# Relatively good code
	dataframe: pandas.DataFrame = (getDataframe(includeDeprecated, versionMinorMaximum)
		.query("attributeKind == '_field'")
		.pipe(_sortCaseInsensitive, listElements[0:2], ['versionMinorMinimumAttribute'])
		[listElements]
		.drop_duplicates()
	)

	# Sort class attributes within groups
	dataframe = _sortCaseInsensitive(dataframe, ['classAs_astAttribute'])

	# Add subcategory count and version count per attribute
	subcategoryCounts = dataframe.groupby('attribute')['TypeAlias_hasDOTSubcategory'].nunique().reset_index()
	subcategoryCounts.columns = ['attribute', 'subcategoryCount']

	versionCounts = dataframe.groupby('attribute')['versionMinorMinimumAttribute'].nunique().reset_index()
	versionCounts.columns = ['attribute', 'versionCount']

	dataframe = dataframe.merge(subcategoryCounts, on='attribute')
	dataframe = dataframe.merge(versionCounts, on='attribute')	# Calculate useMatchCase: 1 if any version is above minimum Python version, 0 otherwise
	versionAboveMinimum = dataframe[dataframe['versionMinorMinimumAttribute'] > pythonMinimumVersionMinor]
	attributesNeedingMatchCase = versionAboveMinimum['attribute'].unique() if not versionAboveMinimum.empty else []
	useMatchCaseData = versionCounts.copy()
	useMatchCaseData['useMatchCase'] = useMatchCaseData['attribute'].isin(attributesNeedingMatchCase).astype(int)

	dataframe = dataframe.merge(useMatchCaseData[['attribute', 'useMatchCase']], on='attribute')

	# Convert numpy int64 to regular int for versions
	dataframe['versionMinorMinimumAttribute'] = dataframe['versionMinorMinimumAttribute'].astype(int)

	# Collect results
	allResults = []

	# Single subcategory case - use TypeAlias_hasDOTIdentifier with classAs_astAttribute values
	singleSubcategoryData = dataframe[dataframe['subcategoryCount'] == 1]
	if not singleSubcategoryData.empty:
		singleResults = singleSubcategoryData.groupby(['TypeAlias_hasDOTIdentifier', 'versionMinorMinimumAttribute', 'useMatchCase'])['classAs_astAttribute'].agg(list).reset_index()
		singleResults.columns = ['TypeAlias_hasDOTIdentifier', 'versionMinorMinimum', 'useMatchCase', 'list4TypeAlias_value']
		allResults.append(singleResults)

	# Multiple subcategory case - individual subcategory entries
	multipleSubcategoryData = dataframe[dataframe['subcategoryCount'] > 1]
	if not multipleSubcategoryData.empty:
		subcategoryResults = multipleSubcategoryData.groupby(['TypeAlias_hasDOTSubcategory', 'versionMinorMinimumAttribute', 'useMatchCase'])['classAs_astAttribute'].agg(list).reset_index()
		subcategoryResults.columns = ['TypeAlias_hasDOTIdentifier', 'versionMinorMinimum', 'useMatchCase', 'list4TypeAlias_value']
		allResults.append(subcategoryResults)
				# Combined entries using dumped subcategory names
		combinedEntries = multipleSubcategoryData.drop_duplicates(['attribute', 'TypeAlias_hasDOTIdentifier', 'versionMinorMinimumAttribute', 'useMatchCase'])
		# Create mapping of subcategory names to dumped names per attribute
		subcategoryNames = multipleSubcategoryData[['attribute', 'TypeAlias_hasDOTSubcategory']].drop_duplicates()
		subcategoryNames['dumpedName'] = subcategoryNames['TypeAlias_hasDOTSubcategory'].apply(_makeNameDumped)
		dumpedNamesPerAttribute = subcategoryNames.groupby('attribute')['dumpedName'].agg(list).reset_index()

		combinedEntries = combinedEntries.merge(dumpedNamesPerAttribute, on='attribute')
		combinedEntries['list4TypeAlias_value'] = combinedEntries['dumpedName']
		combinedResults = combinedEntries[['TypeAlias_hasDOTIdentifier', 'versionMinorMinimumAttribute', 'useMatchCase', 'list4TypeAlias_value']].copy()
		combinedResults.columns = ['TypeAlias_hasDOTIdentifier', 'versionMinorMinimum', 'useMatchCase', 'list4TypeAlias_value']
		allResults.append(combinedResults)

	# Combine all results
	finalData = pandas.concat(allResults, ignore_index=True)
	# Sort lists within each entry - apply sorted to each list
	finalData['list4TypeAlias_value'] = finalData['list4TypeAlias_value'].apply(sorted)
		# Add attribute information for sorting
	attributeMapping = dataframe[['TypeAlias_hasDOTIdentifier', 'attribute']].drop_duplicates()
	subcategoryMapping = dataframe[['TypeAlias_hasDOTSubcategory', 'attribute']].drop_duplicates()
	subcategoryMapping.columns = ['TypeAlias_hasDOTIdentifier', 'attribute']
	allAttributeMapping = pandas.concat([attributeMapping, subcategoryMapping]).drop_duplicates()

	finalData = finalData.merge(allAttributeMapping, on='TypeAlias_hasDOTIdentifier', how='left')
	finalData['isSubcategory'] = finalData['TypeAlias_hasDOTIdentifier'].isin(dataframe['TypeAlias_hasDOTSubcategory'])

	# Final sorting: attribute (case-insensitive), subcategories before main identifiers, then version descending
	sortedData = _sortCaseInsensitive(
		finalData,
		['attribute', 'isSubcategory', 'versionMinorMinimum'],
		['isSubcategory', 'versionMinorMinimum'],
		ascending=[True, True, False]
	)

	return list(sortedData[['TypeAlias_hasDOTIdentifier', 'list4TypeAlias_value', 'useMatchCase', 'versionMinorMinimum']].to_records(index=False))

def updateDataframe() -> None:
	dataframe: pandas.DataFrame = getDataframe(includeDeprecated=True, versionMinorMaximum=None, modifyVersionMinorMinimum=False)

	_columns: list[str] = ['ClassDefIdentifier',
	'classAs_astAttribute',
	'deprecated',
	'base',
	'base_typing_TypeAlias',
	'match_args',

	'attribute',
	'attributeKind',
	'type',
	'kwargAnnotation',
	'TypeAlias_hasDOTSubcategory',
	'type_ast_expr',

	'typeC',
	'type_field_type',
	'typeStub',
	'typeStub_typing_TypeAlias',

	'versionMinorMinimumClass',
	'versionMinorMinimum_match_args',
	'versionMinorMinimumAttribute',
	'versionMajorData',
	'versionMinorData',
	'versionMicroData',

	'attributeRename',
	'list2Sequence',
	'defaultValue',
	'keywordArguments',

	'ast_arg',
	'listStr4FunctionDef_args',
	'listDefaults',
	'listTupleCall_keywords',
	'TypeAlias_hasDOTIdentifier',
]

	# Change the order of columns
	# dataframe = dataframe[_columns]

	# Update 'classAs_astAttribute' column with formatted value
	dataframe['classAs_astAttribute'] = dataframe['ClassDefIdentifier'].apply(
		lambda attribute: dump(Make.Attribute(Make.Name('ast'), attribute))    # pyright: ignore[reportUnknownLambdaType, reportUnknownArgumentType]
	)

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

	# TODO add logic for column 'attributeRename' similar to 'type' column override
	# `ImportFrom.module`: "dotModule"

	# Override column 'type' for class `ast.Constant`, attribute `value`
	dataframe.loc[
		(dataframe['ClassDefIdentifier'] == 'Constant') & (dataframe['attribute'] == 'value'),
		'type'
	] = "ConstantValueType"

	dataframe['versionMinorMinimum_match_args'] = numpy.where(
		dataframe.groupby(['ClassDefIdentifier', 'match_args'])['versionMinorData'].transform('min') == versionMinor_astMinimumSupported,
		-1,
		dataframe.groupby(['ClassDefIdentifier', 'match_args'])['versionMinorData'].transform('min')
	)

	dataframe['versionMinorMinimumAttribute'] = numpy.where(
		dataframe.groupby(['ClassDefIdentifier', 'attribute'])['versionMinorData'].transform('min') == versionMinor_astMinimumSupported,
		-1,
		dataframe.groupby(['ClassDefIdentifier', 'attribute'])['versionMinorData'].transform('min')
	)

	dataframe['versionMinorMinimumClass'] = numpy.where(
		dataframe.groupby('ClassDefIdentifier')['versionMinorData'].transform('min') == versionMinor_astMinimumSupported,
		-1,
		dataframe.groupby('ClassDefIdentifier')['versionMinorData'].transform('min')
	)

	def str2expr(string: str) -> str:
		astModule: ast.Module = ast.parse(string)
		ast_expr: ast.expr = raiseIfNone(NodeTourist(Be.Expr, Then.extractIt(DOT.value)).captureLastMatch(astModule))
		return dump(ast_expr)

	def typeSansNone(string: str) -> str:
		return str2expr(string.replace(' | None', ''))

	# Update 'type_ast_expr' based on 'type' column
	dataframe['type_ast_expr'] = numpy.where(dataframe['type'] == 'No', 'No', dataframe['type'].apply(str2expr))

	# Update 'type_ast_expr' based on 'list2Sequence' column
	dataframe.loc[dataframe['list2Sequence'] == True, 'type_ast_expr'] = dataframe['type_ast_expr'].str.replace("'list'", "'Sequence'")   # pyright: ignore[reportUnknownMemberType]  # noqa: E712

	# Update 'type_ast_expr' based on 'type' column
	dataframe['typeSansNone_ast_expr'] = numpy.where(dataframe['type'] == 'No', 'No', dataframe['type'].apply(typeSansNone))

	# Update 'type_ast_expr' based on 'list2Sequence' column
	dataframe.loc[dataframe['list2Sequence'] == True, 'typeSansNone_ast_expr'] = dataframe['typeSansNone_ast_expr'].str.replace("'list'", "'Sequence'")  # pyright: ignore[reportUnknownMemberType]  # noqa: E712

	# Update 'ast_arg' column based on conditions
	dataframe['ast_arg'] = dataframe.apply(
		lambda row: "No" if row['attribute'] == "No" else dump(Make.arg(row['attributeRename'] if row['attributeRename'] != "No" else row['attribute'], eval(row['type_ast_expr']))),   # pyright: ignore[reportUnknownArgumentType, reportUnknownLambdaType]
		axis=1
	)

	# Add TypeAlias_hasDOTIdentifier computation
	dataframe['TypeAlias_hasDOTIdentifier'] = numpy.where(
		dataframe['attributeKind'] == '_field',
		"hasDOT" + cast(str, dataframe['attribute']),
		"No"
	)

	# Add TypeAlias_hasDOTSubcategory computation
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

	# Update 'listStr4FunctionDef_args', 'listDefaults', 'listTupleCall_keywords' columns based on match_args
	def compute_listFunctionDef_args(row: pandas.Series) -> pandas.Series:   # pyright: ignore[reportUnknownParameterType, reportMissingTypeArgument]
		if row['attribute'] == "No":
			return pandas.Series([
				"No",
				"No",
				"No"
			], index=[
				'listStr4FunctionDef_args',
				'listDefaults',
				'listTupleCall_keywords'
			])
		listAttributes = cast(str, row['match_args']).replace("'","").replace(" ","").split(',')
		className = cast(str, row['ClassDefIdentifier'])
		version = cast(int, row['versionMinorMinimum_match_args'])
		listStr4FunctionDef_args: list[str] = []
		listDefaults: list[str] = []
		listTupleCall_keywords: list[tuple[str, str]] = []
		for attributeTarget in listAttributes:
			argIdentifier: str = attributeTarget
			keywordValue: str = attributeTarget
			matching_row: pandas.DataFrame = dataframe[
				(dataframe['attribute'] == attributeTarget) &
				(dataframe['ClassDefIdentifier'] == className) &
				(dataframe['versionMinorMinimum_match_args'] == version)
			]
			if not matching_row.empty:
				if matching_row.iloc[0]['keywordArguments']:
					keywordValue = cast(str, matching_row.iloc[0]['defaultValue'])
				else:
					ast_arg: str = cast(str, matching_row.iloc[0]['ast_arg'])
					if matching_row.iloc[0]['attributeRename'] != "No":
						keywordValue = cast(str, matching_row.iloc[0]['attributeRename'])
					keywordValue = f"ast.Name('{keywordValue}')"
					if matching_row.iloc[0]['list2Sequence']:
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

	# Create hashable versions of list columns for duplicate detection
	dataframe['hashableListStr4FunctionDef_args'] = dataframe['listStr4FunctionDef_args'].astype(str)
	dataframe['hashableListDefaults'] = dataframe['listDefaults'].astype(str)
	dataframe['hashableListTupleCall_keywords'] = dataframe['listTupleCall_keywords'].astype(str)

	dataframe.to_pickle(pathFilenameDataframeAST)

# if __name__ == "__main__":
# 	updateDataframe()