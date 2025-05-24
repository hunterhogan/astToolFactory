"""API for data. The rest of the package should be ignorant of the specifics of the data source.
This module provides a set of functions to interact with the data source, allowing for easy retrieval and manipulation of data."""
from astToolFactory import pythonVersionMinorMinimum, settingsPackage
from astToolkit import Be, DOT, dump, Make, NodeTourist, Then # pyright: ignore[reportUnknownVariableType]
from collections.abc import Sequence
from typing import cast, TypeAlias, TypedDict
from Z0Z_tools import raiseIfNone
import ast
import numpy
import pandas
import re

# TODO datacenter needs to do all data manipulation, not factory.py
# TODO more and better pandas usage

pathFilenameDataframeAST = settingsPackage.pathPackage / 'dataframeAST.pkl'
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

class DictionaryGrabElements(TypedDict):
	listTypesByVersion: ListTypesByVersion
	TypeAlias_hasDOTIdentifier: str

class DictionaryTypeAliasElements(TypedDict):
	TypeAlias_hasDOTIdentifier: str
	versionData: dict[int, list[str]]

class DictionaryTypeAliasAttribute(TypedDict):
	TypeAlias_hasDOTIdentifier: str
	subcategories: dict[str, dict[int, list[str]]]

class DictionaryMatchArgs(TypedDict):
	kwarg: str
	listDefaults: list[str]
	listStr4FunctionDef_args: list[str]
	listTupleCall_keywords: list[tuple[str, str]]

class DictionaryClassDef(TypedDict):
	classAs_astAttribute: str
	versionMinorMinimumClass: dict[int, dict[int, DictionaryMatchArgs]]

def _sortCaseInsensitive(dataframe: pandas.DataFrame, columns: Sequence[str]) -> pandas.DataFrame:
	dataframeCopy = dataframe.copy()
	for columnName in columns:
		dataframeCopy[columnName] = dataframe[columnName].str.lower()  # pyright: ignore[reportUnknownMemberType]

	sorted_index = dataframeCopy.sort_values(by=columns).index
	return dataframe.loc[sorted_index]

def getDataframe(includeDeprecated: bool, versionMinorMaximum: int | None, modifyVersionMinorMinimum: bool = True, *indices: str) -> pandas.DataFrame:
	dataframe = pandas.read_pickle(pathFilenameDataframeAST)

	if not includeDeprecated:
		dataframe = dataframe[~dataframe['deprecated']]

	if versionMinorMaximum is not None:
		dataframe = dataframe[dataframe['versionMinorData'] <= versionMinorMaximum]

	if modifyVersionMinorMinimum:
		columnsVersion = ['versionMinorMinimumAttribute', 'versionMinorMinimumClass', 'versionMinorMinimum_match_args']
		dataframe[columnsVersion] = dataframe[columnsVersion].where(dataframe[columnsVersion] > pythonVersionMinorMinimum, -1)
	if indices:
		dataframe = dataframe.set_index(list(indices)) 

	return dataframe

def getElementsBe(includeDeprecated: bool = False, versionMinorMaximum: int | None = None) -> Sequence[DictionaryToolBe]:
	listElementsHARDCODED = ['ClassDefIdentifier', 'classAs_astAttribute', 'versionMinorMinimumClass']
	listElements = listElementsHARDCODED

	dataframe = getDataframe(includeDeprecated, versionMinorMaximum)

	dataframe = dataframe[listElements].drop_duplicates()

	return dataframe.to_dict(orient='records')  # pyright: ignore[reportReturnType]

def getElementsClassIsAndAttribute(includeDeprecated: bool = False, versionMinorMaximum: int | None = None) -> dict[str, dict[str, Dictionary_type_ast_expr]]:
	return getElementsDOT(includeDeprecated, versionMinorMaximum)

def getElementsDOT(includeDeprecated: bool = False, versionMinorMaximum: int | None = None) -> dict[str, dict[str, Dictionary_type_ast_expr]]:
	listElementsHARDCODED = ['attribute', 'TypeAlias_hasDOTSubcategory', 'versionMinorMinimumAttribute', 'type_ast_expr', 'typeSansNone_ast_expr', 'TypeAlias_hasDOTIdentifier']
	listElements = listElementsHARDCODED

	dataframe = getDataframe(includeDeprecated, versionMinorMaximum)
	dataframe = dataframe[dataframe['attributeKind'] == '_field']
	dataframe = _sortCaseInsensitive(dataframe, listElements[0:2])
	dataframe = dataframe[listElements].drop_duplicates()
	# Keep the entry with the lowest versionMinorMinimumAttribute for each (attribute, TypeAlias_hasDOTSubcategory)
	dataframe = dataframe.sort_values('versionMinorMinimumAttribute') 
	dataframe = dataframe.drop_duplicates(subset=['attribute', 'TypeAlias_hasDOTSubcategory'], keep='first')

	# Structure as nested dictionary
	dataframe['nested'] = dataframe.apply( 
		lambda row: {'versionMinorMinimumAttribute': row['versionMinorMinimumAttribute'], 'type_ast_expr': row['type_ast_expr'], 'typeSansNone_ast_expr': row['typeSansNone_ast_expr'], 'TypeAlias_hasDOTIdentifier': row['TypeAlias_hasDOTIdentifier']},  # pyright: ignore[reportUnknownArgumentType, reportUnknownLambdaType]
		axis=1
	)

	return (dataframe.set_index(['attribute', 'TypeAlias_hasDOTSubcategory'])['nested'].unstack().apply(lambda column: column.dropna().to_dict(), axis=1).to_dict() )   # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType, reportUnknownVariableType, reportUnknownLambdaType]

def getElementsGrab(includeDeprecated: bool = False, versionMinorMaximum: Version | None = None) -> dict[Attribute, DictionaryGrabElements]:
	listElementsHARDCODED = ['attribute', 'versionMinorMinimumAttribute', 'type_ast_expr', 'typeSansNone_ast_expr', 'TypeAlias_hasDOTIdentifier']
	listElements = listElementsHARDCODED

	dataframe = getDataframe(includeDeprecated, versionMinorMaximum)

	dataframe = dataframe[dataframe['attributeKind'] == '_field']

	dataframe = dataframe[listElements]
	dataframe = dataframe.drop_duplicates()
	dataframe = dataframe.drop_duplicates(subset=['attribute', 'typeSansNone_ast_expr'], keep='first')
	dataframe = dataframe.groupby(['attribute', 'versionMinorMinimumAttribute'])['typeSansNone_ast_expr'].aggregate(list).reset_index()
	dataframe['typeSansNone_ast_expr'] = dataframe['typeSansNone_ast_expr'].apply(sorted, key=str.lower) 
	dataframe['listTypesByVersion'] = dataframe[['versionMinorMinimumAttribute', 'typeSansNone_ast_expr']].apply(tuple, axis=1) 
	
	# Add TypeAlias_hasDOTIdentifier back by merging
	dataframeWithIdentifier = getDataframe(includeDeprecated, versionMinorMaximum)
	dataframeWithIdentifier = dataframeWithIdentifier[dataframeWithIdentifier['attributeKind'] == '_field']
	dataframeWithIdentifier = dataframeWithIdentifier[['attribute', 'TypeAlias_hasDOTIdentifier']].drop_duplicates()
	dataframe = dataframe.merge(dataframeWithIdentifier, on='attribute', how='left')
	
	# Group by attribute and create the final structure
	dictionaryGrabElements: dict[Attribute, DictionaryGrabElements] = {}
	for attribute, group in dataframe.groupby('attribute'):
		listTypesByVersion = cast(ListTypesByVersion, group['listTypesByVersion'].tolist())
		TypeAlias_hasDOTIdentifier = cast(str, group['TypeAlias_hasDOTIdentifier'].iloc[0])  # pyright: ignore[reportUnknownMemberType]
		dictionaryGrabElements[str(attribute)] = DictionaryGrabElements(
			listTypesByVersion=listTypesByVersion,
			TypeAlias_hasDOTIdentifier=TypeAlias_hasDOTIdentifier
		)
	return dictionaryGrabElements

def getElementsMake(includeDeprecated: bool = False, versionMinorMaximum: int | None = None) -> dict[str, DictionaryClassDef]:
	listElementsHARDCODED = [
	'ClassDefIdentifier',
	'classAs_astAttribute',
	'list2Sequence',
	'kwargAnnotation',
	'versionMinorMinimumClass',
	'versionMinorMinimum_match_args',
	'listStr4FunctionDef_args', 
	'listDefaults', 
	'listTupleCall_keywords',
	]
	listElements = listElementsHARDCODED

	dataframe = getDataframe(includeDeprecated, versionMinorMaximum)
	dataframe = dataframe[dataframe['attribute'] != "No"]
	dataframe = dataframe[listElements].drop_duplicates(subset=listElements[0:6])

	def compute_kwarg(group: pandas.Series) -> str:  # pyright: ignore[reportMissingTypeArgument, reportUnknownParameterType]
		list_kwargAnnotation = sorted(value for value in group.unique() if value != "No")
		return 'OR'.join(list_kwargAnnotation) if list_kwargAnnotation else "No"
	dataframe['kwarg'] = (dataframe.groupby(['ClassDefIdentifier', 'versionMinorMinimum_match_args'])['kwargAnnotation'].transform(compute_kwarg))  # pyright: ignore[reportUnknownArgumentType]

	dataframe = dataframe.drop(columns=['kwargAnnotation'])

	dataframeHashable = dataframe.copy()
	columnsLists = ['listStr4FunctionDef_args', 'listDefaults', 'listTupleCall_keywords']
	dataframeHashable[columnsLists] = dataframeHashable[columnsLists].astype(str)
	dataframeHashable = dataframeHashable.drop_duplicates()
	indicesToKeep = dataframeHashable.index

	dataframe = dataframe.loc[indicesToKeep]

	def idkHowToNameThingsOrFollowInstructions(groupbyClassVersion: pandas.DataFrame) -> dict[int, DictionaryMatchArgs]:
		return {
			row['versionMinorMinimum_match_args']: {
				'kwarg': row['kwarg'],
				'listDefaults': row['listDefaults'],
				'listStr4FunctionDef_args': row['listStr4FunctionDef_args'],
				'listTupleCall_keywords': row['listTupleCall_keywords']
			}
			for _rowIndex, row in groupbyClassVersion.iterrows()  # pyright: ignore[reportUnknownVariableType]
		}

	dictionaryClassDef: dict[str, DictionaryClassDef] = {}
	for ClassDefIdentifier, class_group in dataframe.groupby('ClassDefIdentifier', sort=False):
		dictionaryClassDef[cast(str, ClassDefIdentifier)] = {
			'classAs_astAttribute': class_group['classAs_astAttribute'].iloc[0],  # pyright: ignore[reportUnknownMemberType]
			'versionMinorMinimumClass': {}
		}
		for versionMinorMinimumClass, groupbyClassVersion in class_group.groupby('versionMinorMinimumClass'):
			dictionaryClassDef[cast(str, ClassDefIdentifier)]['versionMinorMinimumClass'][cast(int, versionMinorMinimumClass)] = idkHowToNameThingsOrFollowInstructions(groupbyClassVersion)
	return dictionaryClassDef

def getElementsTypeAlias(includeDeprecated: bool = False, versionMinorMaximum: int | None = None) -> dict[str, DictionaryTypeAliasAttribute]:
	listElementsHARDCODED = ['attribute', 'TypeAlias_hasDOTSubcategory', 'versionMinorMinimumAttribute', 'classAs_astAttribute', 'TypeAlias_hasDOTIdentifier']
	listElements = listElementsHARDCODED

	dataframe = getDataframe(includeDeprecated, versionMinorMaximum)

	dataframe = dataframe[dataframe['attributeKind'] == '_field']

	dataframe = _sortCaseInsensitive(dataframe, listElements[0:2])

	dataframe = dataframe[listElements].drop_duplicates()

	dictionaryAttribute: dict[str, DictionaryTypeAliasAttribute] = {}
	
	# First group by attribute to get the TypeAlias_hasDOTIdentifier
	for attribute, attribute_group in dataframe.groupby('attribute'):
		TypeAlias_hasDOTIdentifier = str(attribute_group['TypeAlias_hasDOTIdentifier'].iloc[0]) # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType]
		subcategories: dict[str, dict[int, list[str]]] = {}
		
		# Then group by TypeAlias_hasDOTSubcategory and versionMinorMinimumAttribute
		grouped = attribute_group.groupby(['TypeAlias_hasDOTSubcategory', 'versionMinorMinimumAttribute'])
		for (typeAlias_hasDOTSubcategory, versionMinorMinimumAttribute), group in grouped:
			listClassDefIdentifier = sorted(group['classAs_astAttribute'].unique(), key=lambda x: str(x).lower())
			if typeAlias_hasDOTSubcategory not in subcategories:
				subcategories[typeAlias_hasDOTSubcategory] = {}
			subcategories[typeAlias_hasDOTSubcategory][int(versionMinorMinimumAttribute)] = listClassDefIdentifier
		
		dictionaryAttribute[str(attribute)] = DictionaryTypeAliasAttribute(
			TypeAlias_hasDOTIdentifier=TypeAlias_hasDOTIdentifier,
			subcategories=subcategories
		)
	
	return dictionaryAttribute

def updateDataframe():
	dataframe = getDataframe(includeDeprecated=True, versionMinorMaximum=None, modifyVersionMinorMinimum=False)

	_columns = ['ClassDefIdentifier',
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
		lambda attribute: dump(Make.Attribute(Make.Name('ast'), attribute))   # pyright: ignore[reportUnknownLambdaType, reportUnknownArgumentType]
	)

	# Update 'type' column with standardized formatting and accurate information
	def transform_type(value: str, identifiers: list[str]) -> str:
		# Prepend "ast." to substrings matching 'ClassDefIdentifier', case-sensitive
		pattern = r'\b(' + '|'.join(re.escape(identifier) for identifier in identifiers) + r')\b'
		value = re.sub(pattern, r'ast.\1', value)
		# Replace "Literal[True, False]" with "bool"
		return value.replace("Literal[True, False]", "bool")
	dataframe['type'] = dataframe.apply(
		lambda row: transform_type(row['typeStub'] if row['typeStub_typing_TypeAlias'] == 'No' else row['typeC'], dataframe['ClassDefIdentifier'].dropna().unique()),  # pyright: ignore[reportUnknownLambdaType, reportUnknownArgumentType, reportArgumentType]
		axis=1
	)

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

	def str2expr(string: str):
		astModule = ast.parse(string)
		ast_expr = raiseIfNone(NodeTourist(Be.Expr, Then.extractIt(DOT.value)).captureLastMatch(astModule))
		return dump(ast_expr)
	
	def typeSansNone(string: str) -> str:
		return str2expr(string.replace(' | None', ''))

	# Update 'type_ast_expr' based on 'type' column
	dataframe['type_ast_expr'] = numpy.where(dataframe['type'] == 'No', 'No', dataframe['type'].apply(str2expr))

	# Update 'type_ast_expr' based on 'list2Sequence' column
	dataframe.loc[dataframe['list2Sequence'] == True, 'type_ast_expr'] = dataframe['type_ast_expr'].str.replace("'list'", "'Sequence'")   # pyright: ignore[reportUnknownMemberType]

	# Update 'type_ast_expr' based on 'type' column
	dataframe['typeSansNone_ast_expr'] = numpy.where(dataframe['type'] == 'No', 'No', dataframe['type'].apply(typeSansNone))

	# Update 'type_ast_expr' based on 'list2Sequence' column
	dataframe.loc[dataframe['list2Sequence'] == True, 'typeSansNone_ast_expr'] = dataframe['typeSansNone_ast_expr'].str.replace("'list'", "'Sequence'")   # pyright: ignore[reportUnknownMemberType]

	# Update 'ast_arg' column based on conditions
	dataframe['ast_arg'] = dataframe.apply(
		lambda row: "No" if row['attribute'] == "No" else dump(Make.arg(row['attributeRename'] if row['attributeRename'] != "No" else row['attribute'], eval(row['type_ast_expr']))),  # pyright: ignore[reportUnknownLambdaType, reportUnknownArgumentType]
		axis=1
	)			# Add TypeAlias_hasDOTIdentifier computation
	dataframe['TypeAlias_hasDOTIdentifier'] = numpy.where(
		dataframe['attributeKind'] == '_field',
		"hasDOT" + cast(str, dataframe['attribute']), 
		"No"
	)

	# Add TypeAlias_hasDOTSubcategory computation
	processedTypeString = (
		dataframe['type']
		.str.replace('|', 'Or', regex=False)  # pyright: ignore[reportUnknownMemberType]
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
	def compute_listFunctionDef_args(row: pandas.Series) -> pandas.Series:  # pyright: ignore[reportMissingTypeArgument, reportUnknownParameterType]
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
			argIdentifier = attributeTarget
			keywordValue = attributeTarget
			matching_row = dataframe[
				(dataframe['attribute'] == attributeTarget) &
				(dataframe['ClassDefIdentifier'] == className) &
				(dataframe['versionMinorMinimum_match_args'] == version)
			]
			if not matching_row.empty:
				if matching_row.iloc[0]['keywordArguments']:
					keywordValue = cast(str, matching_row.iloc[0]['defaultValue'])
				else:
					ast_arg = cast(str, matching_row.iloc[0]['ast_arg'])
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
	dataframe[['listStr4FunctionDef_args', 'listDefaults', 'listTupleCall_keywords']] = dataframe.apply(compute_listFunctionDef_args, axis=1)  # pyright: ignore[reportUnknownArgumentType]
	dataframe.to_pickle(pathFilenameDataframeAST)

# if __name__ == "__main__":
# 	updateDataframe()