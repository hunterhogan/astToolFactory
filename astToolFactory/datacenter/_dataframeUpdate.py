# pyright: reportUnusedImport=false
from ast import (
	alias, arg, arguments, Attribute, boolop, cmpop, comprehension, ExceptHandler, expr, expr_context, keyword, match_case,
	Name, operator, pattern, stmt, Subscript, type_param, TypeIgnore, unaryop, withitem)
from astToolFactory import column__value, MaskTuple, noMinimum, pathRoot_typeshed, settingsManufacturing
from astToolFactory.cpython import getDictionary_match_args
from astToolFactory.datacenter._dataframeUpdateAnnex import (
	_columns, attributeRename__, attributeType__ClassDefIdentifier_attribute, Column__ClassDefIdentifier_attribute,
	defaultValue__, dictionary_defaultValue_ast_arg_Call_keyword_orElse, move2keywordArguments__)
from astToolFactory.datacenter._dataServer import _sortCaseInsensitive, getDataframe
from astToolkit import (
	Be, ConstantValueType as _ConstantValue, DOT, Grab, IfThis, Make, NodeChanger, NodeTourist,
	parsePathFilename2astModule, Then)
from astToolkit.transformationTools import makeDictionaryClassDef, pythonCode2ast_expr
from collections.abc import Mapping
from functools import cache
from hunterMakesPy import raiseIfNone
from numpy.typing import ArrayLike
from typing import Any, cast
import ast
import builtins
import numpy
import pandas
import typeshed_client

# TODO `kwarg_annotationIdentifier` does not seem to update in some cases.

# TODO remove hardcoding.
_attributeTypeVarHARDCODED = '_EndPositionT'
_attributeTypeVar_defaultHARDCODED = 'int | None'

def _computeVersionMinimum(dataframe: pandas.DataFrame, list_byColumns: list[str], columnNameTarget: str) -> pandas.DataFrame:
	dataframe[columnNameTarget] = numpy.where(
		dataframe.groupby(list_byColumns)["versionMinorPythonInterpreter"].transform("min") == settingsManufacturing.versionMinor_astMinimumSupported
		, noMinimum
		, dataframe.groupby(list_byColumns)["versionMinorPythonInterpreter"].transform("min")
	)
	return dataframe

@cache
def _get_astModule_astStub() -> ast.Module:
	ImaSearchContext: typeshed_client.SearchContext = typeshed_client.get_search_context(typeshed=pathRoot_typeshed)
	return parsePathFilename2astModule(raiseIfNone(typeshed_client.get_stub_file("ast", search_context=ImaSearchContext)))

def _getDataFromInterpreter(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	# TODO Columns to create using the Python Interpreter,
	# from version 3.settingsManufacturing.versionMinor_astMinimumSupported
	# to version 3.settingsManufacturing.versionMinorMaximum, inclusive.
	# 'ClassDefIdentifier',
	# 'versionMajorPythonInterpreter',
	# 'versionMinorPythonInterpreter',
	# 'versionMicroPythonInterpreter',
	# 'base',
	return dataframe

def _getDataFromStubFile(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	def amIDeprecated(ClassDefIdentifier: str) -> bool:
		return bool(NodeTourist(IfThis.isCallIdentifier('deprecated'), doThat=Then.extractIt).captureLastMatch(Make.Module(cast(list[ast.stmt], dictionaryClassDef[ClassDefIdentifier].decorator_list))))

	def getThe_Attributes(ClassDefIdentifier: str) -> dict[str, str]:
		the_Attributes: dict[str, str] = {}
		_attribute_ast_expr = NodeTourist(
			findThis=Be.Subscript.valueIs(IfThis.isNameIdentifier('Unpack'))
			, doThat=Then.extractIt(DOT.slice)
		).captureLastMatch(dictionaryClassDef[ClassDefIdentifier])

		if _attribute_ast_expr:
			_EndPositionT = NodeTourist(findThis=Be.Subscript, doThat=Then.extractIt(DOT.slice)).captureLastMatch(_attribute_ast_expr)
			if _EndPositionT:
				the_Attributes = dict.fromkeys(dictionary_Attributes, ast.unparse(_EndPositionT))
			else:
				the_Attributes = dictionary_Attributes
		return the_Attributes

	def newRowsFrom_attributes(dataframeTarget: pandas.DataFrame) -> pandas.DataFrame:
		attributeType__ClassDefIdentifier_attribute: dict[Column__ClassDefIdentifier_attribute, column__value] = {
			Column__ClassDefIdentifier_attribute(ClassDefIdentifier, attribute)
			: column__value(column='attributeType', value=attributeType)
			for ClassDefIdentifier in dataframeTarget['ClassDefIdentifier'].drop_duplicates()
			for attribute, attributeType in getThe_Attributes(ClassDefIdentifier).items()
		}

		return pandas.concat([
			dataframeTarget[dataframeTarget['ClassDefIdentifier'] == key.ClassDefIdentifier].assign(
				attribute=key.attribute,
				attributeKind='_attribute',
				**{assign.column: assign.value}
			)
			for key, assign in attributeType__ClassDefIdentifier_attribute.items()
		], ignore_index=True)

	def newRowsFrom_match_args(dataframeTarget: pandas.DataFrame) -> pandas.DataFrame:
		def get_attributeType(dddataframeee: pandas.DataFrame) -> pandas.Series:
			"""`eval` "resolves" any TypeAlias identifier into an object from which we can get the type."""
			dddataframeee['attributeType'] = ast.unparse(NodeChanger[ast.Name, ast.expr](
				findThis=lambda node: Be.Name(node) and isinstance(eval(node.id), type) and issubclass(eval(node.id), ast.AST)  # noqa: S307
				, doThat=lambda node: Make.Attribute(Make.Name("ast"), eval(node.id).__name__)  # noqa: S307
				).visit(raiseIfNone(NodeTourist[ast.AnnAssign, ast.expr](
					findThis = Be.AnnAssign.targetIs(IfThis.isNameIdentifier(cast(str, dddataframeee['attribute'])))
					, doThat = Then.extractIt(DOT.annotation)
					).captureLastMatch(dictionaryClassDef[cast(str, dddataframeee['ClassDefIdentifier'])]))))

			return dddataframeee['attributeType']

		dataframeTarget = dataframeTarget[dataframeTarget['match_args'] != ()]

		# Explode match_args tuples into separate rows
		dataframeTarget = dataframeTarget.assign(attribute=dataframeTarget['match_args']).explode('attribute').reset_index(drop=True)
		# Add required columns
		dataframeTarget['attributeKind'] = "_field"

		dataframeTarget['attributeType'] = dataframeTarget.apply(get_attributeType, axis="columns", result_type="expand")

		return dataframeTarget

	dictionaryClassDef: dict[str, ast.ClassDef] = makeDictionaryClassDef(_get_astModule_astStub())
	dictionary_Attributes: dict[str, str] = _makeDictionaryAnnotations(dictionaryClassDef['_Attributes'])

	dataframe['deprecated'] = pandas.Series(data=False, index=dataframe.index, dtype=bool, name='deprecated')
	dataframe['deprecated'] = dataframe['ClassDefIdentifier'].apply(amIDeprecated)
	"""NOTE deprecated classes are not defined in asdl and they do not have match_args in ast.pyi. The match_args values in the dataframe
	for deprecated classes were created manually. If the dataframe were reset or eliminated, there is not currently a process to
	recreate the match_args for deprecated classes."""

	dataframe['match_args'] = pandas.Series(data=[()] * len(dataframe), index=dataframe.index, dtype=object, name='match_args')
	dataframe = dataframe.drop_duplicates(subset=dataframe.attrs['drop_duplicates'], keep='last')

	new_match_args = (dataframe[['ClassDefIdentifier', "versionMinorPythonInterpreter", 'deprecated']]
		.apply(tuple, axis="columns")
		.map(getDictionary_match_args())
		.fillna(dataframe['match_args'])) # NOTE if this logic were better, it would not use `fillna` and there still wouldn't be empty cells.
	dataframe.loc[:, 'match_args'] = new_match_args

	dataframe.attrs['drop_duplicates'].extend(['match_args'])

	dataframe = dataframe.drop_duplicates(subset=dataframe.attrs['drop_duplicates'], keep='last')

	dataframe['attribute'] = pandas.Series(data='No', index=dataframe.index, dtype=str, name='attribute')
	dataframe.attrs['drop_duplicates'].extend(['attribute'])
	dataframe['attributeKind'] = pandas.Series(data='No', index=dataframe.index, dtype=str, name='attributeKind')
	dataframe['attributeType'] = pandas.Series(data='No', index=dataframe.index, dtype=str, name='attributeType')

	# NOTE these two functions each create ~4 times more rows than necessary.
	dataframe = pandas.concat(objs=[dataframe, newRowsFrom_match_args(dataframe)], axis='index', ignore_index=True)
	dataframe = dataframe.drop_duplicates(subset=dataframe.attrs['drop_duplicates'], keep='last')

	dataframe = pandas.concat(objs=[dataframe, newRowsFrom_attributes(dataframe)], axis='index', ignore_index=True)

	return dataframe.drop_duplicates(subset=dataframe.attrs['drop_duplicates'], keep='last').reset_index(drop=True)

def _make_astAttribute(ClassDefIdentifier: str) -> ast.expr:
	return Make.Attribute(Make.Name("ast"), ClassDefIdentifier)

def _make_keywordOrList(attributePROXY: dict[str, str | bool | ast.expr]) -> ast.keyword:
	keywordValue = Make.Name(cast(str, attributePROXY["attributeRename"]))
	if attributePROXY["list2Sequence"] is True:
		keywordValue = Make.IfExp(test=keywordValue, body=Make.Call(Make.Name("list"), [keywordValue]), orElse=cast(ast.expr, attributePROXY['orElse']))
	else:
		keywordValue = Make.Or.join([keywordValue, cast(ast.expr, attributePROXY['orElse'])])
	return Make.keyword(cast(str, attributePROXY['attribute']), keywordValue)

def _make4ColumnsOfLists(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	dictionaryTupleAttributes: dict[tuple[str, int], list[tuple[str, ast.expr]]] = {}
	dictionaryFunctionDef_args: dict[tuple[str, int], list[ast.arg]] = {}
	dictionaryDefaults: dict[tuple[str, int], list[ast.expr]] = {}
	dictionaryCall_keyword: dict[tuple[str, int], list[ast.keyword]] = {}

	for (ClassDefIdentifier, versionMinorMinimum_match_args), dataframeGroupBy in dataframe.groupby(['ClassDefIdentifier', "versionMinorMinimum_match_args"]):  # ty:ignore[not-iterable]
		groupKey: tuple[str, int] = (ClassDefIdentifier, versionMinorMinimum_match_args) # pyright: ignore[reportAssignmentType]
		match_argsCategoricalSort: tuple[str, ...] = dataframeGroupBy['match_args'].iloc[0]
		dataframeGroupBy['attribute'] = pandas.Categorical(dataframeGroupBy['attribute'], categories=match_argsCategoricalSort, ordered=True)
		dataframeGroupBy: pandas.DataFrame = dataframeGroupBy.sort_values(['attribute', 'versionMinorMinimum_match_args'], ascending=[True, False])

		dataframeGroupBy = dataframeGroupBy[dataframeGroupBy['attributeKind'] == "_field"]

		dictionaryTupleAttributes[groupKey] = (dataframeGroupBy.copy().drop_duplicates(subset='attribute')[['attribute', "type_ast_expr"]].apply(tuple, axis="columns").tolist())

		dictionaryFunctionDef_args[groupKey] = (dataframeGroupBy[dataframeGroupBy["move2keywordArguments"] == False]  # noqa: E712
																.copy().drop_duplicates(subset='attribute')['ast_arg'].tolist())

		dictionaryDefaults[groupKey] = (dataframeGroupBy[(dataframeGroupBy["defaultValue"] != 'No')
			& (dataframeGroupBy["move2keywordArguments"] == False)].copy().drop_duplicates(subset='attribute')["defaultValue"].tolist())  # noqa: E712

		dictionaryCall_keyword[groupKey] = (dataframeGroupBy[(dataframeGroupBy["move2keywordArguments"] != 'No')
			& (dataframeGroupBy["move2keywordArguments"] != 'Unpack')].drop_duplicates(subset='attribute')["Call_keyword"].tolist())

	dataframe["listTupleAttributes"] = (dataframe[['ClassDefIdentifier', "versionMinorMinimum_match_args"]].apply(tuple, axis="columns").map(dictionaryTupleAttributes).fillna(dataframe["listTupleAttributes"]))
	dataframe["listFunctionDef_args"] = (dataframe[['ClassDefIdentifier', "versionMinorMinimum_match_args"]].apply(tuple, axis="columns").map(dictionaryFunctionDef_args).fillna(dataframe["listFunctionDef_args"]))
	dataframe["listDefaults"] = (dataframe[['ClassDefIdentifier', "versionMinorMinimum_match_args"]].apply(tuple, axis="columns").map(dictionaryDefaults).fillna(dataframe["listDefaults"]))
	dataframe["listCall_keyword"] = (dataframe[['ClassDefIdentifier', "versionMinorMinimum_match_args"]].apply(tuple, axis="columns").map(dictionaryCall_keyword).fillna(dataframe["listCall_keyword"]))

	return dataframe

def _makeColumn_ast_arg(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	columnNew = 'ast_arg'
	dataframe[columnNew] = pandas.Series(data='No', index=dataframe.index, dtype="object", name=columnNew)
	def workhorse(dataframeTarget: pandas.DataFrame) -> Any:
		if cast("str | bool", dataframeTarget["move2keywordArguments"]) != False:  # noqa: E712
			return 'No'
		return Make.arg(cast(str, dataframeTarget["attributeRename"]), annotation=cast(ast.expr, dataframeTarget["type_ast_expr"]))

	dataframe[columnNew] = dataframe.apply(workhorse, axis="columns")
	return dataframe

def _makeColumn_list2Sequence(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	columnNew = "list2Sequence"
	dataframe[columnNew] = pandas.Series(data=False, index=dataframe.index, dtype=bool, name=columnNew)
	for ClassDefIdentifier in settingsManufacturing.astSuperClasses:
		mask_attributeType = dataframe['attributeType'].str.contains("list", na=False) & dataframe['attributeType'].str.contains(ClassDefIdentifier, na=False)
		dataframe.loc[mask_attributeType, columnNew] = True
	return dataframe

def _makeColumn_list4TypeAlias(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	dataframe["list4TypeAlias_value"] = pandas.Series(data='No', index=dataframe.index, dtype=object)
	dataframe["hashable_list4TypeAlias_value"] = pandas.Series(data='No', index=dataframe.index, dtype=str)

	def compute_list4TypeAliasByRow(dataframeTarget: pandas.DataFrame) -> tuple[list[Any], str]:
		maskSubcategory = (
			(dataframe['attributeKind'] == "_field")
			& ~ (dataframe['deprecated'])
			& (dataframe["TypeAlias_hasDOTSubcategory"] == dataframeTarget["TypeAlias_hasDOTSubcategory"])
			& (dataframe["versionMinorMinimumAttribute"] <= dataframeTarget["versionMinorMinimumAttribute"])
		)
		if not maskSubcategory.any():
			return [], "[]"
		matchingRows = (
			dataframe.loc[maskSubcategory, ["classAs_astAttribute", 'ClassDefIdentifier']]
			.drop_duplicates(subset='ClassDefIdentifier')
			.sort_values('ClassDefIdentifier', key=lambda x: x.str.lower())
		)
		return matchingRows["classAs_astAttribute"].tolist(), str(matchingRows['ClassDefIdentifier'].tolist())

	mask_assign = dataframe['attributeKind'] == "_field"
	computed_values = dataframe[mask_assign].apply(compute_list4TypeAliasByRow, axis='columns', result_type="expand")
	computed_values.columns = ["list4TypeAlias_value", "hashable_list4TypeAlias_value"]
	dataframe.loc[mask_assign, ["list4TypeAlias_value", "hashable_list4TypeAlias_value"]] = computed_values
	return dataframe

def _makeColumn_list4TypeAliasSubcategories(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	mask_field = (dataframe['attributeKind'] == "_field")

	columnNew = 'list4TypeAliasSubcategories'
	dataframe[columnNew] = pandas.Series(data='No', index=dataframe.index, dtype=object, name=columnNew)

	def compute_list4TypeAliasSubcategories(groupBy: pandas.DataFrame) -> list[ast.expr]:
		groupBy = groupBy[groupBy["TypeAlias_hasDOTSubcategory"] != 'No']
		groupBy = groupBy[~groupBy['deprecated']]
		TypeAlias_hasDOTSubcategory = groupBy["TypeAlias_hasDOTSubcategory"].unique()
		return [Make.Name(subcategory) for subcategory in sorted(TypeAlias_hasDOTSubcategory, key=lambda x: x.lower())]

	# Create a mapping from attribute to subcategory names
	list4TypeAliasSubcategories__attributeKind_attribute: dict[str, list[ast.expr]] = {}
	for attribute, groupBy in dataframe[mask_field].groupby('attribute'):
		list4TypeAliasSubcategories__attributeKind_attribute[str(attribute)] = compute_list4TypeAliasSubcategories(groupBy)

	# Map the subcategory names to the appropriate rows using pandas map
	dataframe.loc[mask_field, 'list4TypeAliasSubcategories'] = dataframe.loc[mask_field, 'attribute'].map(list4TypeAliasSubcategories__attributeKind_attribute)

	return dataframe

def _makeColumn_type_ast_expr(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	columnNew = 'type_ast_expr'
	dataframe[columnNew] = pandas.Series(data='No', index=dataframe.index, dtype="object", name=columnNew)
	dataframe.loc[dataframe["list2Sequence"], columnNew] = dataframe['attributeType'].str.replace("list", "Sequence").apply(cast(Any, pythonCode2ast_expr))
	dataframe.loc[~dataframe["list2Sequence"], columnNew] = dataframe['attributeType'].apply(cast(Any, pythonCode2ast_expr))
	return dataframe

def _makeColumnCall_keyword(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	def workhorse(dataframeTarget: pandas.DataFrame) -> Any:
		if cast(bool, (dataframeTarget['attributeKind'] == "_field") & ((dataframeTarget['move2keywordArguments'] != 'No') & (dataframeTarget['move2keywordArguments'] != 'Unpack'))):
			if cast(bool, dataframeTarget["move2keywordArguments"]):
				keywordValue: ast.expr = cast(ast.expr, dataframeTarget["defaultValue"])
			else:
				keywordValue = Make.Name(cast(str, dataframeTarget["attributeRename"]))
				if dataframeTarget["list2Sequence"] is True:
					keywordValue = Make.Call(Make.Name("list"), [keywordValue])
			return Make.keyword(cast(str, dataframeTarget['attribute']), keywordValue)
		return 'No'

	dataframe["Call_keyword"] = dataframe.apply(workhorse, axis="columns")
	return dataframe

def _makeColumnTypeAlias_hasDOTSubcategory(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	columnNew = 'TypeAlias_hasDOTSubcategory'
	dataframe[columnNew] = pandas.Series(data='No', index=dataframe.index, dtype="object", name=columnNew)
	mask_hasDOTIdentifier = dataframe["TypeAlias_hasDOTIdentifier"] != 'No'
	dataframe.loc[mask_hasDOTIdentifier, columnNew] = dataframe["TypeAlias_hasDOTIdentifier"] + "_" + dataframe['attributeType'].str.replace("|", "Or").str.replace("[", "_").str.replace("[\\] ]", "", regex=True).str.replace("ast.", "")
	return dataframe

def _makeDictionaryAnnotations(astClassDef: ast.ClassDef) -> dict[str, str]:
	dictionary_Attributes: dict[str, str] = {}
	NodeTourist[ast.AnnAssign, Mapping[str, str]](findThis=Be.AnnAssign.targetIs(Be.Name)
		, doThat=Then.updateKeyValueIn(key=lambda node: cast(ast.Name, node.target).id
			, value=lambda node: ast.unparse(node.annotation)
			, dictionary=dictionary_Attributes)
	).visit(astClassDef)
	for _attribute in dictionary_Attributes:
		_attributeTypeVar = _attributeTypeVarHARDCODED
		_attributeTypeVar_default = _attributeTypeVar_defaultHARDCODED
		dictionary_Attributes[_attribute] = dictionary_Attributes[_attribute].replace(_attributeTypeVar, _attributeTypeVar_default)
	return dictionary_Attributes

def _moveMutable_defaultValue(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	for columnValue, orElse in dictionary_defaultValue_ast_arg_Call_keyword_orElse.items():
		maskByColumnValue = getMaskByColumnValue(dataframe, columnValue)

		attributePROXY = dataframe.loc[maskByColumnValue, ['attribute', 'attributeType', "attributeRename", "move2keywordArguments", "list2Sequence"]].drop_duplicates().to_dict(orient="records")

		if len(attributePROXY) > 1:
			message = f"Your current system assumes attribute '{attributePROXY[0]['attribute']}' is the same whenever it is used, but this function got {len(attributePROXY)} variations."
			raise ValueError(message)

		attributePROXY = cast("dict[str, str | bool | ast.expr]", attributePROXY[0])
		if cast(bool, attributePROXY["move2keywordArguments"]):
			message = f"Your current system assumes attribute '{attributePROXY['attribute']}' is not a keyword argument, but this function got {attributePROXY}."
			raise ValueError(message)

		dataframe.loc[maskByColumnValue, "defaultValue"] = Make.Constant(None) # pyright: ignore[reportArgumentType, reportCallIssue]
		attributeType = cast(str, attributePROXY['attributeType']) + " | None"
		if attributePROXY["list2Sequence"] is True:
			attributeType = attributeType.replace("list", "Sequence")
		dataframe.loc[maskByColumnValue, 'ast_arg'] = Make.arg(cast(str, attributePROXY["attributeRename"]), annotation=pythonCode2ast_expr(attributeType)) # pyright: ignore[reportArgumentType, reportCallIssue]
		attributePROXY['orElse'] = orElse
		dataframe.loc[maskByColumnValue, "Call_keyword"] = _make_keywordOrList(attributePROXY) # pyright: ignore[reportArgumentType, reportCallIssue]

	return dataframe

def dictionary2UpdateDataframe(dictionary: Mapping[MaskTuple, column__value], dataframe: pandas.DataFrame) -> pandas.DataFrame:
	"""Convert a hyper-marked-up dictionary to columns and values, but not new rows, in a dataframe."""
	for columnValueMask, assign in dictionary.items():
		dataframe.loc[getMaskByColumnValue(dataframe, columnValueMask), assign.column] = assign.value
	return dataframe

def getMaskByColumnValue(dataframe: pandas.DataFrame, columnValue: MaskTuple) -> pandas.Series:
	"""Convert a specialized `NamedTuple`, which is an arbitrary number of column-names and row-values, to a `True`/`False` mask for a dataframe."""
	return pandas.concat([*[dataframe[column] == value for column, value in columnValue._asdict().items()]], axis=1).all(axis=1)

def updateDataframe() -> None:
	dataframe: pandas.DataFrame = getDataframe(includeDeprecated=True, versionMinorMaximum=settingsManufacturing.versionMinorMaximum, modifyVersionMinorMinimum=False)

	# TODO think of a clever, simple way to optionally apply this instead of toggling comments.
	# columns: reorder; drop columns, but they might be recreated later in the flow.  # noqa: ERA001
	# dataframe = dataframe[_columns]  # noqa: ERA001

	# TODO Get data using the Python Interpreter,
	dataframe = _getDataFromInterpreter(dataframe)

	# Set dtypes for existing columns
	dataframe = dataframe.astype({
		'ClassDefIdentifier': 'string',
		'versionMajorPythonInterpreter': 'int64',
		'versionMinorPythonInterpreter': 'int64',
		'versionMicroPythonInterpreter': 'int64',
		'base': 'string',
	})

	dataframe.attrs['drop_duplicates'] = ['ClassDefIdentifier', 'versionMinorPythonInterpreter']

	dataframe = _getDataFromStubFile(dataframe)

	dataframe['attributeRename'] = pandas.Series(data=dataframe['attribute'], index=dataframe.index, dtype=str, name='attributeRename', copy=True)
	dataframe = dictionary2UpdateDataframe(attributeRename__, dataframe)

	dataframe['move2keywordArguments'] = pandas.Series(data=False, index=dataframe.index, dtype=object, name='move2keywordArguments')
	dataframe = dictionary2UpdateDataframe(move2keywordArguments__, dataframe)

	dataframe = dictionary2UpdateDataframe(attributeType__ClassDefIdentifier_attribute, dataframe)

	dataframe['defaultValue'] = pandas.Series(data='No', index=dataframe.index, dtype=str, name='defaultValue')
	dataframe = dictionary2UpdateDataframe(defaultValue__, dataframe)

	dataframe['classAs_astAttribute'] = dataframe['ClassDefIdentifier'].astype(str).map(_make_astAttribute)
	dataframe = _makeColumn_list2Sequence(dataframe)
	dataframe = _makeColumn_type_ast_expr(dataframe)
	dataframe['type_astSuperClasses'] = dataframe['attributeType'].replace({f'ast.{ClassDefIdentifier}': identifierTypeVar for ClassDefIdentifier, identifierTypeVar in settingsManufacturing.astSuperClasses.items()}, regex=True)
	dataframe = _makeColumn_ast_arg(dataframe)
	dataframe['type_astSuperClasses_ast_expr'] = numpy.where(dataframe['type_astSuperClasses'] == 'No', 'No', cast(ArrayLike, dataframe['type_astSuperClasses'].apply(cast(Any, pythonCode2ast_expr))))
	dataframe['TypeAlias_hasDOTIdentifier'] = numpy.where(dataframe['attributeKind'] == '_field', 'hasDOT' + cast(str, dataframe['attribute']), 'No')
	dataframe = _makeColumnTypeAlias_hasDOTSubcategory(dataframe)
	dataframe = _makeColumn_list4TypeAlias(dataframe)
	dataframe = _makeColumn_list4TypeAliasSubcategories(dataframe)
	dataframe = _computeVersionMinimum(dataframe, ['ClassDefIdentifier', 'match_args'], 'versionMinorMinimum_match_args')
	dataframe = _computeVersionMinimum(dataframe, ['ClassDefIdentifier', 'attribute'], 'versionMinorMinimumAttribute')
	dataframe = _computeVersionMinimum(dataframe, ['ClassDefIdentifier'], 'versionMinorMinimumClass')
	dataframe = _makeColumnCall_keyword(dataframe)
	dataframe = _moveMutable_defaultValue(dataframe)
	dataframe = _sortCaseInsensitive(dataframe, ['ClassDefIdentifier', 'versionMinorPythonInterpreter', 'attribute'], caseInsensitive=[True, False, True], ascending=[True, False, True])
	# TODO Figure out overload for `Make`
	dataframe = _make4ColumnsOfLists(dataframe)

	dataframe.to_pickle(settingsManufacturing.pathFilenameDataframeAST)

if __name__ == "__main__":
	updateDataframe()
