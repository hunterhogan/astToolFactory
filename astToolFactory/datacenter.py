"""API for data. The rest of the package should be ignorant of the specifics of the data source.
This module provides a set of functions to interact with the data source, allowing for easy retrieval and manipulation of data."""
from astToolFactory import pythonVersionMinorMinimum, settingsPackage
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

class Dictionary_type_ast_expr(TypedDict):
	versionMinorMinimumAttribute: int
	type_ast_expr: str
	typeSansNone_ast_expr: str
	TypeAlias_hasDOTIdentifier: str

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

def _sortCaseInsensitive(dataframe: pandas.DataFrame, columns: Sequence[str]) -> pandas.DataFrame:
	dataframeCopy: pandas.DataFrame = dataframe.copy()
	for columnName in columns:
		dataframeCopy[columnName] = dataframe[columnName].str.lower() # pyright: ignore[reportUnknownMemberType]

	sorted_index = dataframeCopy.sort_values(by=columns).index
	return dataframe.loc[sorted_index]

def getDataframe(includeDeprecated: bool, versionMinorMaximum: int | None, modifyVersionMinorMinimum: bool = True, *indices: str) -> pandas.DataFrame:
	dataframe: pandas.DataFrame = pandas.read_pickle(pathFilenameDataframeAST)

	if not includeDeprecated:
		dataframe = dataframe[~dataframe['deprecated']]

	if versionMinorMaximum is not None:
		dataframe = dataframe[dataframe['versionMinorData'] <= versionMinorMaximum]

	if modifyVersionMinorMinimum:
		columnsVersion: list[str] = ['versionMinorMinimumAttribute', 'versionMinorMinimumClass', 'versionMinorMinimum_match_args']
		dataframe[columnsVersion] = dataframe[columnsVersion].where(dataframe[columnsVersion] > pythonVersionMinorMinimum, -1)
	if indices:
		dataframe = dataframe.set_index(list(indices))  # pyright: ignore[reportUnknownMemberType]

	return dataframe

def getElementsBe(includeDeprecated: bool = False, versionMinorMaximum: int | None = None) -> list[DictionaryToolBe]:
	listElementsHARDCODED: list[str] = ['ClassDefIdentifier', 'classAs_astAttribute', 'versionMinorMinimumClass']
	listElements: list[str] = listElementsHARDCODED

	dataframe: pandas.DataFrame = getDataframe(includeDeprecated, versionMinorMaximum)

	dataframe = dataframe[listElements].drop_duplicates()

	return dataframe.to_dict(orient='records')   # pyright: ignore[reportReturnType]

def getElementsClassIsAndAttribute(includeDeprecated: bool = False, versionMinorMaximum: int | None = None) -> list[tuple[int, str, str, bool, list[str], bool, list[str], bool]]:
	listElementsHARDCODED: list[str] = ['attribute', 'TypeAlias_hasDOTSubcategory', 'versionMinorMinimumAttribute', 'type_ast_expr', 'typeSansNone_ast_expr', 'TypeAlias_hasDOTIdentifier']
	listElements: list[str] = listElementsHARDCODED

	dataframe: pandas.DataFrame = (getDataframe(includeDeprecated, versionMinorMaximum)
		.query("attributeKind == '_field'")
		.pipe(_sortCaseInsensitive, listElements[0:2])
		[listElements]
		.drop_duplicates()
		.sort_values('versionMinorMinimumAttribute')
		.drop_duplicates(subset=['attribute', 'TypeAlias_hasDOTSubcategory'], keep='first')
	)

	listTuples: list[tuple[int, str, str, bool, list[str], bool, list[str], bool]] = []
	for attribute, groupAttribute in dataframe.groupby('attribute'):
		TypeAlias_hasDOTIdentifier = str(groupAttribute['TypeAlias_hasDOTIdentifier'].iloc[0]) # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType]

		subcategories: dict[str, pandas.Series] = {} # pyright: ignore[reportUnknownVariableType, reportMissingTypeArgument]
		for TypeAlias_hasDOTSubcategory, groupSubcategory in groupAttribute.groupby('TypeAlias_hasDOTSubcategory'):
			subcategories[str(TypeAlias_hasDOTSubcategory)] = groupSubcategory.iloc[0]
		
		if len(subcategories) == 1: # pyright: ignore[reportUnknownArgumentType]
			_single_subcategory_name, single_subcategory_data = next(iter(subcategories.items())) # pyright: ignore[reportUnknownArgumentType, reportUnknownVariableType]
			versionMinorMinimumAttribute = int(cast(int, single_subcategory_data['versionMinorMinimumAttribute']))
			isOverload = False
			list_ast_expr = [str(single_subcategory_data['typeSansNone_ast_expr'])] # pyright: ignore[reportUnknownArgumentType]
			attributeIsNotNone = 'None' in str(single_subcategory_data['type_ast_expr']) # pyright: ignore[reportUnknownArgumentType]
			orElseList_ast_expr: list[str] = []
			orElseAttributeIsNotNone = False
			
			listTuples.append((versionMinorMinimumAttribute, str(attribute), TypeAlias_hasDOTIdentifier, isOverload, list_ast_expr, attributeIsNotNone, orElseList_ast_expr, orElseAttributeIsNotNone))
		else:
			unique_typeSansNone_ast_expr: list[str] = sorted(set(
				str(subcategory_data['typeSansNone_ast_expr'])  # pyright: ignore[reportUnknownArgumentType]
				for subcategory_data in subcategories.values() # pyright: ignore[reportUnknownVariableType]
			))
			has_none_in_any_type = any('None' in str(subcategory_data['type_ast_expr']) for subcategory_data in subcategories.values()) # pyright: ignore[reportUnknownVariableType, reportUnknownArgumentType]
			
			for TypeAlias_hasDOTSubcategory, subcategory_data in subcategories.items(): # pyright: ignore[reportUnknownVariableType]
				versionMinorMinimumAttribute = int(cast(int, subcategory_data['versionMinorMinimumAttribute']))
				isOverload = True
				list_ast_expr = [str(subcategory_data['typeSansNone_ast_expr'])] # pyright: ignore[reportUnknownArgumentType]
				attributeIsNotNone = 'None' in str(subcategory_data['type_ast_expr']) # pyright: ignore[reportUnknownArgumentType]
				orElseList_ast_expr: list[str] = []
				orElseAttributeIsNotNone = False
				
				listTuples.append((versionMinorMinimumAttribute, str(attribute), TypeAlias_hasDOTSubcategory, isOverload, list_ast_expr, attributeIsNotNone, orElseList_ast_expr, orElseAttributeIsNotNone))
			
			minimum_version = min(int(cast(int, subcategory_data['versionMinorMinimumAttribute'])) for subcategory_data in subcategories.values()) # pyright: ignore[reportUnknownVariableType]
			orElseList_ast_expr = []
			orElseAttributeIsNotNone = False
			listTuples.append((minimum_version, str(attribute), TypeAlias_hasDOTIdentifier, False, unique_typeSansNone_ast_expr, has_none_in_any_type, orElseList_ast_expr, orElseAttributeIsNotNone))

	return listTuples

def getElementsDOT(includeDeprecated: bool = False, versionMinorMaximum: int | None = None) -> list[tuple[int, str, str, bool, list[str], bool, list[str], bool]]:
	return getElementsClassIsAndAttribute(includeDeprecated, versionMinorMaximum)

def getElementsGrab(includeDeprecated: bool = False, versionMinorMaximum: Version | None = None) -> list[tuple[int, str, str, list[str], bool, list[str], bool]]:
	listElementsHARDCODED: list[str] = ['attribute', 'versionMinorMinimumAttribute', 'type_ast_expr', 'typeSansNone_ast_expr', 'TypeAlias_hasDOTIdentifier']
	listElements: list[str] = listElementsHARDCODED

	dataframe: pandas.DataFrame = getDataframe(includeDeprecated, versionMinorMaximum)

	dataframe = dataframe[dataframe['attributeKind'] == '_field']

	dataframe = dataframe[listElements]
	dataframe = dataframe.drop_duplicates()
	dataframe = dataframe.drop_duplicates(subset=['attribute', 'typeSansNone_ast_expr'], keep='first')
	dataframe = dataframe.groupby(['attribute', 'versionMinorMinimumAttribute'])['typeSansNone_ast_expr'].aggregate(list).reset_index()
	dataframe['typeSansNone_ast_expr'] = dataframe['typeSansNone_ast_expr'].apply(sorted, key=str.lower) 
	dataframe['listTypesByVersion'] = dataframe[['versionMinorMinimumAttribute', 'typeSansNone_ast_expr']].apply(tuple, axis=1) 
	
	# Add TypeAlias_hasDOTIdentifier back by merging
	dataframeWithIdentifier: pandas.DataFrame = getDataframe(includeDeprecated, versionMinorMaximum)
	dataframeWithIdentifier = dataframeWithIdentifier[dataframeWithIdentifier['attributeKind'] == '_field']
	dataframeWithIdentifier = dataframeWithIdentifier[['attribute', 'TypeAlias_hasDOTIdentifier']].drop_duplicates()
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
			
			if versionMin > pythonVersionMinorMinimum:
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

	dataframe: pandas.DataFrame = getDataframe(includeDeprecated, versionMinorMaximum)
	dataframe = dataframe[dataframe['attribute'] != "No"]
	# dataframe = dataframe[listElements].drop_duplicates(subset=listElements[columnsHashable])

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

def getElementsTypeAlias(includeDeprecated: bool = False, versionMinorMaximum: int | None = None) -> list[tuple[int, str, list[str], list[str]]]:
	listElementsHARDCODED: list[str] = ['attribute', 'TypeAlias_hasDOTSubcategory', 'versionMinorMinimumAttribute', 'classAs_astAttribute', 'TypeAlias_hasDOTIdentifier']
	listElements: list[str] = listElementsHARDCODED

	dataframe: pandas.DataFrame = getDataframe(includeDeprecated, versionMinorMaximum)
	dataframe = dataframe[dataframe['attributeKind'] == '_field']
	dataframe = _sortCaseInsensitive(dataframe, listElements[0:2])
	dataframe = dataframe[listElements].drop_duplicates()

	def compute_combined_versions(group: pandas.DataFrame) -> dict[int, list[str]]:
		"""Combine and aggregate version data using pandas vectorized operations."""
		group = group.copy()
		group['classAs_astAttribute_lower'] = group['classAs_astAttribute'].str.lower() # pyright: ignore[reportUnknownMemberType]
		group = group.sort_values('classAs_astAttribute_lower')
		
		versionData: dict[int, list[str]] = {}
		for versionMinorMinimumAttribute, version_group in group.groupby('versionMinorMinimumAttribute'):
			versionData[int(cast(int, versionMinorMinimumAttribute))] = sorted(
				version_group['classAs_astAttribute'].unique(), 
				key=str.lower
			)
		
		if len(versionData) > 1:
			all_versions: list[int] = sorted(versionData.keys())
			max_version: int = max(all_versions)
			min_version: int = min(all_versions)
			
			combined_classes: list[str] = []
			for version_classes in versionData.values():
				combined_classes.extend(version_classes)
			combined_sorted = sorted(set(combined_classes), key=str.lower)
			
			if min_version <= pythonVersionMinorMinimum:
				aggregated_data: dict[int, list[str]] = {min_version: versionData[min_version]}
				if max_version > pythonVersionMinorMinimum:
					aggregated_data[max_version] = combined_sorted
				return aggregated_data
		
		return versionData

	listTuples: list[tuple[int, str, list[str], list[str]]] = []
	
	for _attribute, attribute_group in dataframe.groupby('attribute'):
		TypeAlias_hasDOTIdentifier = str(attribute_group['TypeAlias_hasDOTIdentifier'].iloc[0]) # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType]
		subcategories: dict[str, dict[int, list[str]]] = {}
		
		for TypeAlias_hasDOTSubcategory, subcategory_group in attribute_group.groupby('TypeAlias_hasDOTSubcategory'):
			subcategories[str(TypeAlias_hasDOTSubcategory)] = compute_combined_versions(subcategory_group)
		
		if len(subcategories) == 1:
			single_subcategory_data: dict[int, list[str]] = next(iter(subcategories.values()))
			for versionMinorData, listClassAs_astAttribute in single_subcategory_data.items():
				orElseListClassAs_astAttribute: list[str] = []
				listTuples.append((versionMinorData, TypeAlias_hasDOTIdentifier, listClassAs_astAttribute, orElseListClassAs_astAttribute))
		else:
			for TypeAlias_hasDOTSubcategory, subcategory_data in subcategories.items():
				for versionMinorData, listClassAs_astAttribute in subcategory_data.items():
					orElseListClassAs_astAttribute: list[str] = []
					listTuples.append((versionMinorData, TypeAlias_hasDOTSubcategory, listClassAs_astAttribute, orElseListClassAs_astAttribute))
			
			attributeDictionaryVersions: dict[int, list[str]] = defaultdict(list)
			for typeAliasSubcategory, dictionaryVersions in subcategories.items():
				astNameTypeAlias: ast.Name = Make.Name(typeAliasSubcategory)
				dumped_name: str = dump(astNameTypeAlias)
				
				if any(version <= pythonVersionMinorMinimum for version in dictionaryVersions.keys()):
					attributeDictionaryVersions[min(dictionaryVersions.keys())].append(dumped_name)
				else:
					attributeDictionaryVersions[min(dictionaryVersions.keys())].append(dumped_name)
					attributeDictionaryVersions[max(dictionaryVersions.keys())].append(dumped_name)
			
			for versionMinorData, listClassAs_astAttribute in attributeDictionaryVersions.items():
				orElseListClassAs_astAttribute: list[str] = []
				listTuples.append((versionMinorData, TypeAlias_hasDOTIdentifier, listClassAs_astAttribute, orElseListClassAs_astAttribute))
	
	return listTuples

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