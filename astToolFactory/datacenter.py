import re
import ast
from astToolkit import dump, Be, Then, NodeTourist, Make, DOT # pyright: ignore[reportUnknownVariableType]
from Z0Z_tools import raiseIfNone
from collections.abc import Sequence
from astToolFactory import pathFilenameDataframeAST, pythonVersionMinorMinimum
from typing import cast, NamedTuple, TypeAlias, TypedDict
import pandas

# TODO datacenter needs to do all data manipulation, not the toolFactory
# TODO more and better pandas usage
# TODO or better, get rid of Pandas and use the original sources

Attribute: TypeAlias = str
Version: TypeAlias = int
ListTypesASTformAsStr: TypeAlias = list[str]
TupleTypesForVersion: TypeAlias = tuple[Version, ListTypesASTformAsStr]
ListTypesByVersion: TypeAlias = list[TupleTypesForVersion]

class Call_keywords(NamedTuple):
	argIdentifier: str
	keywordValue: str

class DictionaryAstExprType(TypedDict):
	versionMinorMinimumAttribute: int
	type_ast_expr: str

class DictionaryToolBe(TypedDict):
	ClassDefIdentifier: str
	classAs_astAttribute: str
	versionMinorMinimumClass: int

class DictionaryMatchArgs(TypedDict):
	kwarg: str
	listDefaults: list[str]
	listStr4FunctionDef_args: list[str]
	listTupleCall_keywords: list[Call_keywords]

class DictionaryClassDef(TypedDict):
	classAs_astAttribute: str
	versionMinorMinimumClass: dict[int, dict[int, DictionaryMatchArgs]]

def _sortCaseInsensitive(dataframe: pandas.DataFrame, columns: Sequence[str]) -> pandas.DataFrame:
	dataframeCopy = dataframe.copy()
	for columnName in columns:
		dataframeCopy[columnName] = dataframe[columnName].str.lower() # pyright: ignore[reportUnknownMemberType]

	sorted_index = dataframeCopy.sort_values(by=columns).index # pyright: ignore[reportUnknownMemberType]
	return dataframe.loc[sorted_index]

def getDataframe(deprecated: bool, versionMinorMaximum: int | None, *indices: str) -> pandas.DataFrame:
	dataframe = pandas.read_pickle(pathFilenameDataframeAST)

	if not deprecated:
		dataframe = dataframe[~dataframe['deprecated']]

	if versionMinorMaximum is not None:
		dataframe = dataframe[dataframe['versionMinorData'] <= versionMinorMaximum]

	columnsVersion = ['versionMinorMinimumAttribute', 'versionMinorMinimumClass', 'versionMinorMinimum_match_args']
	dataframe[columnsVersion] = dataframe[columnsVersion].where(dataframe[columnsVersion] > pythonVersionMinorMinimum, -1)

	if indices:
		dataframe.set_index(keys=indices) # pyright: ignore[reportUnknownMemberType]

	return dataframe

def getElementsBe(deprecated: bool = False, versionMinorMaximum: int | None = None) -> Sequence[DictionaryToolBe]:
	listElementsHARDCODED = ['ClassDefIdentifier', 'classAs_astAttribute', 'versionMinorMinimumClass']
	listElements = listElementsHARDCODED

	dataframe = getDataframe(deprecated, versionMinorMaximum)

	dataframe = dataframe[listElements].drop_duplicates()

	return dataframe.to_dict(orient='records') # pyright: ignore[reportReturnType]

def getElementsClassIsAndAttribute(deprecated: bool = False, versionMinorMaximum: int | None = None) -> dict[str, dict[str, DictionaryAstExprType]]:
	return getElementsDOT(deprecated, versionMinorMaximum)

def getElementsDOT(deprecated: bool = False, versionMinorMaximum: int | None = None) -> dict[str, dict[str, DictionaryAstExprType]]:
	listElements = ['attribute', 'TypeAliasSubcategory', 'versionMinorMinimumAttribute', 'type_ast_expr']

	dataframe = getDataframe(deprecated, versionMinorMaximum)
	dataframe = dataframe[dataframe['attributeKind'] == '_field']
	dataframe = _sortCaseInsensitive(dataframe, listElements[0:2])
	dataframe = dataframe[listElements].drop_duplicates()

	# Keep the entry with the lowest versionMinorMinimumAttribute for each (attribute, TypeAliasSubcategory)
	dataframe = dataframe.sort_values('versionMinorMinimumAttribute') # pyright: ignore[reportUnknownMemberType]
	dataframe = dataframe.drop_duplicates(subset=['attribute', 'TypeAliasSubcategory'], keep='first')

	# Structure as nested dictionary
	dataframe['nested'] = dataframe.apply( # pyright: ignore[reportUnknownMemberType]
		lambda row: {'versionMinorMinimumAttribute': row['versionMinorMinimumAttribute'], 'type_ast_expr': row['type_ast_expr']}, # pyright: ignore[reportUnknownLambdaType, reportUnknownArgumentType]
		axis=1
	)

	return (dataframe.set_index(['attribute', 'TypeAliasSubcategory'])['nested'].unstack().apply(lambda column: column.dropna().to_dict(), axis=1).to_dict() )  # pyright: ignore[reportUnknownLambdaType, reportUnknownVariableType, reportUnknownArgumentType, reportUnknownMemberType]

def getElementsGrab(deprecated: bool = False, versionMinorMaximum: Version | None = None) -> dict[Attribute, ListTypesByVersion]:
	listElementsHARDCODED = ['attribute', 'versionMinorMinimumAttribute', 'type_ast_expr']
	listElements = listElementsHARDCODED

	dataframe = getDataframe(deprecated, versionMinorMaximum)

	dataframe = dataframe[dataframe['attributeKind'] == '_field']

	dataframe = dataframe[listElements]
	dataframe = dataframe.drop_duplicates()
	dataframe = dataframe.drop_duplicates(subset=['attribute', 'type_ast_expr'], keep='first')
	dataframe = dataframe.groupby(['attribute', 'versionMinorMinimumAttribute'])['type_ast_expr'].aggregate(list).reset_index()
	dataframe['type_ast_expr'] = dataframe['type_ast_expr'].apply(sorted, key=str.lower) # pyright: ignore[reportUnknownMemberType]
	dataframe['listTypesByVersion'] = dataframe[['versionMinorMinimumAttribute', 'type_ast_expr']].apply(tuple, axis=1) # pyright: ignore[reportUnknownMemberType]
	return dataframe.groupby('attribute')['listTypesByVersion'].aggregate(list).to_dict()

def getElementsMake(deprecated: bool = False, versionMinorMaximum: int | None = None) -> dict[str, DictionaryClassDef]:
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

	dataframe = getDataframe(deprecated, versionMinorMaximum)
	dataframe = dataframe[dataframe['attribute'] != "No"]
	dataframe = dataframe[listElements].drop_duplicates(subset=listElements[0:6])

	def compute_kwarg(group: pandas.Series) -> str: # pyright: ignore[reportMissingTypeArgument, reportUnknownParameterType]
		list_kwargAnnotation = sorted(value for value in group.unique() if value != "No")
		return 'OR'.join(list_kwargAnnotation) if list_kwargAnnotation else "No"
	dataframe['kwarg'] = (dataframe.groupby(['ClassDefIdentifier', 'versionMinorMinimum_match_args'])['kwargAnnotation'].transform(compute_kwarg)) # pyright: ignore[reportUnknownArgumentType]

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
			for _rowIndex, row in groupbyClassVersion.iterrows() # pyright: ignore[reportUnknownVariableType]
		}

	dictionaryClassDef: dict[str, DictionaryClassDef] = {}
	for ClassDefIdentifier, class_group in dataframe.groupby('ClassDefIdentifier', sort=False):
		dictionaryClassDef[cast(str, ClassDefIdentifier)] = {
			'classAs_astAttribute': class_group['classAs_astAttribute'].iloc[0], # pyright: ignore[reportUnknownMemberType]
			'versionMinorMinimumClass': {}
		}
		for versionMinorMinimumClass, groupbyClassVersion in class_group.groupby('versionMinorMinimumClass'):
			dictionaryClassDef[cast(str, ClassDefIdentifier)]['versionMinorMinimumClass'][cast(int, versionMinorMinimumClass)] = idkHowToNameThingsOrFollowInstructions(groupbyClassVersion)
	return dictionaryClassDef

def getElementsTypeAlias(deprecated: bool = False, versionMinorMaximum: int | None = None) -> dict[str, dict[str, dict[int, list[str]]]]:
	listElementsHARDCODED = ['attribute', 'TypeAliasSubcategory', 'versionMinorMinimumAttribute', 'classAs_astAttribute']
	listElements = listElementsHARDCODED

	dataframe = getDataframe(deprecated, versionMinorMaximum)

	dataframe = dataframe[dataframe['attributeKind'] == '_field']

	dataframe = _sortCaseInsensitive(dataframe, listElements[0:2])

	dataframe = dataframe[listElements].drop_duplicates()

	dictionaryAttribute: dict[str, dict[str, dict[int, list[str]]]] = {}
	grouped = dataframe.groupby(['attribute', 'TypeAliasSubcategory', 'versionMinorMinimumAttribute'])
	for (attribute, typeAliasSubcategory, versionMinorMinimumAttribute), group in grouped:
		listClassDefIdentifier = sorted(group['classAs_astAttribute'].unique(), key=lambda x: str(x).lower())
		if attribute not in dictionaryAttribute:
			dictionaryAttribute[attribute] = {}
		if typeAliasSubcategory not in dictionaryAttribute[attribute]:
			dictionaryAttribute[attribute][typeAliasSubcategory] = {}
		dictionaryAttribute[attribute][typeAliasSubcategory][int(versionMinorMinimumAttribute)] = listClassDefIdentifier
	return dictionaryAttribute

def updateDataframe():
	dataframe = pandas.read_pickle(pathFilenameDataframeAST)

	columns = ['ClassDefIdentifier',
	'classAs_astAttribute',
	'deprecated',
	'base',
	'base_typing_TypeAlias',
	'match_args',

	'attribute',
	'attributeKind',
	'type',
	'kwargAnnotation',
	'TypeAliasSubcategory',
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
]

	# Change the order of columns
	dataframe = dataframe[columns]

	# Update 'classAs_astAttribute' column with formatted value
	# NOTE, evaluating eliminating Pandas: easily replaced with astToolkit
	dataframe['classAs_astAttribute'] = dataframe['ClassDefIdentifier'].apply(
		# lambda attribute: f"ast.Attribute(ast.Name('ast'), '{attribute}')"
		lambda attribute: dump(Make.Attribute(Make.Name('ast'), attribute)) # pyright: ignore[reportUnknownArgumentType, reportUnknownLambdaType]
	)

	# Update 'type' column with standardized formatting and accurate information
	# NOTE, evaluating eliminating Pandas: Most is easily replaced with astToolkit, some will require a little thinking
	def transform_type(value: str, identifiers: list[str]) -> str:
		# Prepend "ast." to substrings matching 'ClassDefIdentifier', case-sensitive
		pattern = r'\b(' + '|'.join(re.escape(identifier) for identifier in identifiers) + r')\b'
		value = re.sub(pattern, r'ast.\1', value)
		# Replace "Literal[True, False]" with "bool"
		# NOTE, evaluating eliminating Pandas: easily replaced with astToolkit
		return value.replace("Literal[True, False]", "bool")
	dataframe['type'] = dataframe.apply(
		lambda row: transform_type(row['typeStub'] if row['typeStub_typing_TypeAlias'] == 'No' else row['typeC'], dataframe['ClassDefIdentifier'].dropna().unique()), # pyright: ignore[reportUnknownArgumentType, reportArgumentType, reportUnknownLambdaType]
		axis=1
	)

	# Update TypeAliasSubcategory based on attributeKind
	# NOTE, evaluating eliminating Pandas: the column, 'attributeKind' is one of the few advantages of 
	# using Pandas because after I set the column, it is very easy to segregate data into three groups
	# Nevertheless, I can more-or-less recreate the code I used to create the column.
	dataframe.loc[dataframe['attributeKind'] == 'No', 'TypeAliasSubcategory'] = 'No'
	dataframe.loc[dataframe['attributeKind'] == '_attribute', 'TypeAliasSubcategory'] = 'No'
	dataframe.loc[dataframe['attributeKind'] == '_field', 'TypeAliasSubcategory'] = (
		dataframe['type']
		.str.replace('|', 'Or', regex=False) # pyright: ignore[reportUnknownMemberType]
		.str.replace('[', '_', regex=False)
		.str.replace('ast.', '', regex=False)
		.str.replace(']', '', regex=False)
		.str.replace(' ', '', regex=False)
	)

	# Update versionMinorMinimumClass based on ClassDefIdentifier
	# NOTE, evaluating eliminating Pandas: 
	versionMinor_astMinimumSupported = 9
	dataframe['versionMinorMinimumClass'] = dataframe.groupby('ClassDefIdentifier')['versionMinorData'].transform(
		lambda x: -1 if x.min() == versionMinor_astMinimumSupported else x.min() # pyright: ignore[reportUnknownArgumentType, reportUnknownLambdaType, reportUnknownMemberType]
	)
	# Update versionMinorMinimum_match_args based on ClassDefIdentifier and match_args
	dataframe['versionMinorMinimum_match_args'] = dataframe.groupby(['ClassDefIdentifier', 'match_args'])['versionMinorData'].transform(
		lambda x: -1 if x.min() == versionMinor_astMinimumSupported else x.min() # pyright: ignore[reportUnknownArgumentType, reportUnknownLambdaType, reportUnknownMemberType]
	)
	# Update versionMinorMinimumAttribute based on ClassDefIdentifier and attribute
	dataframe['versionMinorMinimumAttribute'] = dataframe.groupby(['ClassDefIdentifier', 'attribute'])['versionMinorData'].transform(
		lambda x: -1 if x.min() == versionMinor_astMinimumSupported else x.min() # pyright: ignore[reportUnknownArgumentType, reportUnknownLambdaType, reportUnknownMemberType]
	)

	def str2expr(string: str):
		astModule = ast.parse(string)
		ast_expr = raiseIfNone(NodeTourist(Be.Expr, Then.extractIt(DOT.value)).captureLastMatch(astModule))
		return dump(ast_expr)

	# Update 'type_ast_expr' based on 'type' column
	dataframe['type_ast_expr'] = dataframe['type'].apply(lambda x: 'No' if x == 'No' else str2expr(x)) # pyright: ignore[reportUnknownArgumentType, reportUnknownLambdaType]

	# Update 'type_ast_expr' based on 'list2Sequence' column
	dataframe.loc[dataframe['list2Sequence'] == True, 'type_ast_expr'] = dataframe['type_ast_expr'].str.replace("'list'", "'Sequence'") # pyright: ignore[reportUnknownMemberType]  # noqa: E712

	# Update 'ast_arg' column based on conditions
	dataframe['ast_arg'] = dataframe.apply(
		lambda row: "No" if row['attribute'] == "No" else dump(Make.arg(row['attributeRename'] if row['attributeRename'] != "No" else row['attribute'], eval(row['type_ast_expr']))), # pyright: ignore[reportUnknownArgumentType, reportUnknownLambdaType]
		axis=1
	)	

	def compute_listFunctionDef_args(row: pandas.Series) -> pandas.Series: # pyright: ignore[reportUnknownParameterType, reportMissingTypeArgument]
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
		listStr4FunctionDef_args = []
		listDefaults = []
		listTupleCall_keywords = []
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
						listDefaults.append(cast(str, matching_row.iloc[0]['defaultValue'])) # pyright: ignore[reportUnknownMemberType]
					listStr4FunctionDef_args.append(ast_arg) # pyright: ignore[reportUnknownMemberType]
			listTupleCall_keywords.append(Call_keywords(argIdentifier, keywordValue)) # pyright: ignore[reportUnknownMemberType]
		return pandas.Series([listStr4FunctionDef_args, listDefaults, listTupleCall_keywords], index=[ # pyright: ignore[reportUnknownArgumentType]
			'listStr4FunctionDef_args',
			'listDefaults',
			'listTupleCall_keywords'
		])
	dataframe[['listStr4FunctionDef_args', 'listDefaults', 'listTupleCall_keywords']] = dataframe.apply(compute_listFunctionDef_args, axis=1) # pyright: ignore[reportUnknownArgumentType]
	dataframe.to_pickle(pathFilenameDataframeAST)

# updateDataframe()