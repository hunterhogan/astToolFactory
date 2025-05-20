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
	attributeVersionMinorMinimum: int
	ast_exprType: str

class DictionaryToolBe(TypedDict):
	ClassDefIdentifier: str
	classAs_astAttribute: str
	classVersionMinorMinimum: int

class DictionaryMatchArgs(TypedDict):
	kwarg: str
	listDefaults: list[str]
	listStr4FunctionDef_args: list[str]
	listTupleCall_keywords: list[Call_keywords]

class DictionaryClassDef(TypedDict):
	classAs_astAttribute: str
	classVersionMinorMinimum: dict[int, dict[int, DictionaryMatchArgs]]

def _sortCaseInsensitive(dataframe: pandas.DataFrame, columns: Sequence[str]) -> pandas.DataFrame:
	dataframeCopy = dataframe.copy()
	for columnName in columns:
		dataframeCopy[columnName] = dataframe[columnName].str.lower() # pyright: ignore[reportUnknownMemberType]

	sorted_index = dataframeCopy.sort_values(by=columns).index # pyright: ignore[reportUnknownMemberType]
	return dataframe.loc[sorted_index]

cc=[
# Facts: class
'ClassDefIdentifier',
'deprecated',
'base',
'base_typing_TypeAlias',
'match_args',
# Facts: class + attribute
'attribute',
'attributeKind',
'typeC',
'type_field_type',
'typeStub',
'typeStub_typing_TypeAlias',
'versionMajor',
'versionMinor',
'versionMicro',

# Computed from only facts
'type',
'classVersionMinorMinimum',
'attributeVersionMinorMinimum',
'match_argsVersionMinorMinimum',
'classAs_astAttribute',
'kwargAnnotation',
'TypeAliasSubcategory',
'ast_exprType',

# Choices
'attributeRename',
'list2Sequence',
'defaultValue',
'keywordArguments',

# Computed
'ast_arg',
]

def getDataframe(deprecated: bool, versionMinorMaximum: int | None, *indices: str) -> pandas.DataFrame:
	dataframe = pandas.read_parquet(pathFilenameDataframeAST)

	if not deprecated:
		dataframe = dataframe[~dataframe['deprecated']]

	if versionMinorMaximum is not None:
		dataframe = dataframe[dataframe['versionMinor'] <= versionMinorMaximum]

	columnsVersion = ['attributeVersionMinorMinimum', 'classVersionMinorMinimum', 'match_argsVersionMinorMinimum']
	dataframe[columnsVersion] = dataframe[columnsVersion].where(dataframe[columnsVersion] > pythonVersionMinorMinimum, -1)

	if indices:
		dataframe.set_index(keys=indices) # pyright: ignore[reportUnknownMemberType]

	return dataframe

def getElementsBe(deprecated: bool = False, versionMinorMaximum: int | None = None) -> Sequence[DictionaryToolBe]:
	listElementsHARDCODED = ['ClassDefIdentifier', 'classAs_astAttribute', 'classVersionMinorMinimum']
	listElements = listElementsHARDCODED

	dataframe = getDataframe(deprecated, versionMinorMaximum)

	dataframe = dataframe[listElements].drop_duplicates()

	return dataframe.to_dict(orient='records') # pyright: ignore[reportReturnType]

def getElementsClassIsAndAttribute(deprecated: bool = False, versionMinorMaximum: int | None = None) -> dict[str, dict[str, DictionaryAstExprType]]:
	return getElementsDOT(deprecated, versionMinorMaximum)

def getElementsDOT(deprecated: bool = False, versionMinorMaximum: int | None = None) -> dict[str, dict[str, DictionaryAstExprType]]:
	listElements = ['attribute', 'TypeAliasSubcategory', 'attributeVersionMinorMinimum', 'ast_exprType']

	dataframe = getDataframe(deprecated, versionMinorMaximum)
	dataframe = dataframe[dataframe['attributeKind'] == '_field']
	dataframe['ast_exprType'] = dataframe['ast_exprType'].str.replace(" | None", "")
	dataframe = _sortCaseInsensitive(dataframe, listElements[0:2])
	dataframe = dataframe[listElements].drop_duplicates()

	# Keep the entry with the lowest attributeVersionMinorMinimum for each (attribute, TypeAliasSubcategory)
	dataframe = dataframe.sort_values('attributeVersionMinorMinimum')
	dataframe = dataframe.drop_duplicates(subset=['attribute', 'TypeAliasSubcategory'], keep='first')

	# Structure as nested dictionary
	dataframe['nested'] = dataframe.apply(
		lambda row: {'attributeVersionMinorMinimum': row['attributeVersionMinorMinimum'], 'ast_exprType': row['ast_exprType']},
		axis=1
	)

	return (
		dataframe
		.set_index(['attribute', 'TypeAliasSubcategory'])['nested']
		.unstack()
		.apply(lambda column: column.dropna().to_dict(), axis=1)
		.to_dict()
	)

def getElementsGrab(deprecated: bool = False, versionMinorMaximum: Version | None = None) -> dict[Attribute, ListTypesByVersion]:
	listElementsHARDCODED = ['attribute', 'attributeVersionMinorMinimum', 'ast_exprType']
	listElements = listElementsHARDCODED

	dataframe = getDataframe(deprecated, versionMinorMaximum)

	dataframe = dataframe[dataframe['attributeKind'] == '_field']

	dataframe.loc[dataframe['list2Sequence'] == True, 'ast_exprType'] = dataframe['ast_exprType'].str.replace("'list'", "'Sequence'") # pyright: ignore[reportUnknownMemberType]  # noqa: E712
	dataframe = dataframe[listElements]
	dataframe = dataframe.drop_duplicates()
	dataframe = dataframe.drop_duplicates(subset=['attribute', 'ast_exprType'], keep='first')
	dataframe = dataframe.groupby(['attribute', 'attributeVersionMinorMinimum'])['ast_exprType'].aggregate(list).reset_index()
	dataframe['ast_exprType'] = dataframe['ast_exprType'].apply(sorted, key=str.lower) # pyright: ignore[reportUnknownMemberType]
	dataframe['listTypesByVersion'] = dataframe[['attributeVersionMinorMinimum', 'ast_exprType']].apply(tuple, axis=1) # pyright: ignore[reportUnknownMemberType]
	return dataframe.groupby('attribute')['listTypesByVersion'].aggregate(list).to_dict()

def getElementsMake(deprecated: bool = False, versionMinorMaximum: int | None = None) -> dict[str, DictionaryClassDef]:
	listElementsHARDCODED = [
	'ClassDefIdentifier',
	'classAs_astAttribute',
	'match_args',
	'attribute',
	'attributeRename',
	'list2Sequence',
	'ast_arg',
	'defaultValue',
	'keywordArguments',
	'kwargAnnotation',
	'classVersionMinorMinimum',
	'match_argsVersionMinorMinimum',
	]
	listElements = listElementsHARDCODED

	dataframe = getDataframe(deprecated, versionMinorMaximum)

	dataframe = dataframe[dataframe['attribute'] != "No"]
	dataframe = dataframe[listElements].drop_duplicates()

	def compute_listFunctionDef_args(row: pandas.Series) -> pandas.Series: # pyright: ignore[reportUnknownParameterType, reportMissingTypeArgument]
		listAttributes: list[str] = cast(str, row['match_args']).replace("'","").replace(" ","").split(',')  # Split 'match_args' into a list
		className = cast(str, row['ClassDefIdentifier'])
		version = cast(int, row['match_argsVersionMinorMinimum'])
		listStr4FunctionDef_args: list[str] = []
		listDefaults: list[str] = []
		listTupleCall_keywords: list[Call_keywords] = []
		for attributeTarget in listAttributes:
			argIdentifier = attributeTarget
			keywordValue = attributeTarget
			matching_row = dataframe[
				(dataframe['attribute'] == attributeTarget) &
				(dataframe['ClassDefIdentifier'] == className) &
				(dataframe['match_argsVersionMinorMinimum'] == version)
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
						ast_arg = ast_arg.replace("'list'", "'Sequence'")
					if matching_row.iloc[0]['defaultValue'] != "No":
						listDefaults.append(cast(str, matching_row.iloc[0]['defaultValue']))
					listStr4FunctionDef_args.append(ast_arg)
			listTupleCall_keywords.append(Call_keywords(argIdentifier, keywordValue))

		return pandas.Series([listStr4FunctionDef_args, listDefaults, listTupleCall_keywords],
							index=['listStr4FunctionDef_args', 'listDefaults', 'listTupleCall_keywords'])

	# Apply the function to create the new columns
	dataframe[['listStr4FunctionDef_args', 'listDefaults', 'listTupleCall_keywords']] = dataframe.apply(compute_listFunctionDef_args, axis=1) # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType]

	def compute_kwarg(group: pandas.Series) -> str: # pyright: ignore[reportUnknownParameterType, reportMissingTypeArgument]
		list_kwargAnnotation = sorted(value for value in group.unique() if value != "No")
		return 'OR'.join(list_kwargAnnotation) if list_kwargAnnotation else "No"
	dataframe['kwarg'] = (dataframe.groupby(['ClassDefIdentifier', 'match_argsVersionMinorMinimum'])['kwargAnnotation'].transform(compute_kwarg)) # pyright: ignore[reportUnknownArgumentType]

	dataframe = dataframe.drop(columns=['match_args', 'attribute', 'attributeRename', 'ast_arg', 'defaultValue', 'keywordArguments', 'kwargAnnotation'])

	# Convert columns to strings for drop_duplicates (since lists aren't hashable)
	dataframeHashable = dataframe.copy()
	columnsLists = ['listStr4FunctionDef_args', 'listDefaults', 'listTupleCall_keywords']
	dataframeHashable[columnsLists] = dataframeHashable[columnsLists].astype(str)
	dataframeHashable = dataframeHashable.drop_duplicates()
	indicesToKeep = dataframeHashable.index

	# Filter the original dataframe to keep only the unique rows
	dataframe = dataframe.loc[indicesToKeep]

	# Create the nested dictionary structure
	def idkHowToNameThingsOrFollowInstructions(groupbyClassVersion: pandas.DataFrame) -> dict[int, DictionaryMatchArgs]: # pyright: ignore[reportUnknownParameterType, reportMissingTypeArgument]
		return {
			row['match_argsVersionMinorMinimum']: {
				'kwarg': row['kwarg'],
				'listDefaults': row['listDefaults'],
				'listStr4FunctionDef_args': row['listStr4FunctionDef_args'],
				'listTupleCall_keywords': row['listTupleCall_keywords']
			}
			for _elephino, row in groupbyClassVersion.iterrows() # pyright: ignore[reportUnknownVariableType]
		}

	ImaAIGeneratedDictionaryWithTheStupidestIdentifier: dict[str, DictionaryClassDef] = {}
	for ClassDefIdentifier, class_group in dataframe.groupby('ClassDefIdentifier', sort=False):
		ImaAIGeneratedDictionaryWithTheStupidestIdentifier[cast(str, ClassDefIdentifier)] = {
			'classAs_astAttribute': class_group['classAs_astAttribute'].iloc[0], # pyright: ignore[reportUnknownMemberType]
			'classVersionMinorMinimum': {}
		}

		for classVersionMinorMinimum, groupbyClassVersion in class_group.groupby('classVersionMinorMinimum'):
			ImaAIGeneratedDictionaryWithTheStupidestIdentifier[cast(str, ClassDefIdentifier)]['classVersionMinorMinimum'][cast(int, classVersionMinorMinimum)] = idkHowToNameThingsOrFollowInstructions(groupbyClassVersion)

	return ImaAIGeneratedDictionaryWithTheStupidestIdentifier

def getElementsTypeAlias(deprecated: bool = False, versionMinorMaximum: int | None = None) -> dict[str, dict[str, dict[int, list[str]]]]:
	listElementsHARDCODED = ['attribute', 'TypeAliasSubcategory', 'attributeVersionMinorMinimum', 'classAs_astAttribute']
	listElements = listElementsHARDCODED

	dataframe = getDataframe(deprecated, versionMinorMaximum)

	dataframe = dataframe[dataframe['attributeKind'] == '_field']

	dataframe = _sortCaseInsensitive(dataframe, listElements[0:2])

	dataframe = dataframe[listElements].drop_duplicates()

	dictionaryAttribute: dict[str, dict[str, dict[int, list[str]]]] = {}
	grouped = dataframe.groupby(['attribute', 'TypeAliasSubcategory', 'attributeVersionMinorMinimum'])
	for (attribute, typeAliasSubcategory, attributeVersionMinorMinimum), group in grouped:
		listClassDefIdentifier = sorted(group['classAs_astAttribute'].unique(), key=lambda x: str(x).lower())
		if attribute not in dictionaryAttribute:
			dictionaryAttribute[attribute] = {}
		if typeAliasSubcategory not in dictionaryAttribute[attribute]:
			dictionaryAttribute[attribute][typeAliasSubcategory] = {}
		dictionaryAttribute[attribute][typeAliasSubcategory][int(attributeVersionMinorMinimum)] = listClassDefIdentifier
	return dictionaryAttribute

"""
cc=['ClassDefIdentifier',
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
'ast_exprType',

'typeC',
'type_field_type',
'typeStub',
'typeStub_typing_TypeAlias',

'classVersionMinorMinimum',
'match_argsVersionMinorMinimum',
'attributeVersionMinorMinimum',
'versionMajor',
'versionMinor',
'versionMicro',

'attributeRename',
'list2Sequence',
'defaultValue',
'keywordArguments',

'ast_arg',]
df=df[cc]

# Update 'classAs_astAttribute' column with formatted value
df['classAs_astAttribute'] = df['ClassDefIdentifier'].apply(
    lambda attribute: f"ast.Attribute(ast.Name('ast'), '{attribute}')"
)

# Update 'type' column based on conditions and transformations
import re
def transform_type(value, identifiers):
    # Prepend "ast." to substrings matching 'ClassDefIdentifier', case-sensitive
    pattern = r'\b(' + '|'.join(re.escape(identifier) for identifier in identifiers) + r')\b'
    value = re.sub(pattern, r'ast.\1', value)
    # Replace "Literal[True, False]" with "bool"
    return value.replace("Literal[True, False]", "bool")
df['type'] = df.apply(
    lambda row: transform_type(
        row['typeStub'] if row['typeStub_typing_TypeAlias'] == 'No' else row['typeC'],
        df['ClassDefIdentifier'].dropna().unique()
    ),
    axis=1
)

# Update TypeAliasSubcategory based on attributeKind
df.loc[df['attributeKind'] == 'No', 'TypeAliasSubcategory'] = 'No'
df.loc[df['attributeKind'] == '_attribute', 'TypeAliasSubcategory'] = 'No'
df.loc[df['attributeKind'] == '_field', 'TypeAliasSubcategory'] = (
    df['type']
    .str.replace('|', 'Or', regex=False)
    .str.replace('[', '_', regex=False)
    .str.replace('ast.', '', regex=False)
    .str.replace(']', '', regex=False)
    .str.replace(' ', '', regex=False)
)

# Update classVersionMinorMinimum based on ClassDefIdentifier
df['classVersionMinorMinimum'] = df.groupby('ClassDefIdentifier')['versionMinor'].transform(
    lambda x: -1 if x.min() == 9 else x.min()
)
# Update match_argsVersionMinorMinimum based on ClassDefIdentifier and match_args
df['match_argsVersionMinorMinimum'] = df.groupby(['ClassDefIdentifier', 'match_args'])['versionMinor'].transform(
    lambda x: -1 if x.min() == 9 else x.min()
)
# Update attributeVersionMinorMinimum based on ClassDefIdentifier and attribute
df['attributeVersionMinorMinimum'] = df.groupby(['ClassDefIdentifier', 'attribute'])['versionMinor'].transform(
    lambda x: -1 if x.min() == 9 else x.min()
)

"""
