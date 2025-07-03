from ast import (
	alias, arg, arguments, Attribute, boolop, cmpop, comprehension, ExceptHandler, expr, expr_context, keyword, match_case,
	Name, operator, pattern, stmt, Subscript, type_param, TypeIgnore, unaryop, withitem,
)
from astToolFactory import column__value, MaskTuple, pathRoot_typeshed, settingsManufacturing
from astToolFactory._datacenter import _sortCaseInsensitive, getDataframe
from astToolFactory._datacenterAnnex import (
	_columns, attributeRename__, attributeType__ClassDefIdentifier_attribute, defaultValue__,
	dictionary_defaultValue_ast_arg_Call_keyword_orElse, move2keywordArguments__, Column__ClassDefIdentifier_versionMinorMinimum_match_args
)
from astToolFactory.cpython import getDictionary_match_args
from astToolkit import (
	Be, ConstantValueType as _ConstantValue, DOT, IfThis, Make, NodeChanger, NodeTourist, parsePathFilename2astModule,
	Then,
)
from astToolkit.transformationTools import makeDictionaryClassDef
from collections import ChainMap
from collections.abc import Callable, Mapping, Sequence
from functools import cache
from typing import Any, NamedTuple, cast
from Z0Z_tools import raiseIfNone
import ast
import numpy
import pandas
import typeshed_client

"""Use idiomatic pandas.
- No `lambda`, except `key=lambda`.
- No intermediate data structures.
- A dataframe is a data structure: no intermediate dataframes.
- A column is a data structure: no intermediate columns.
- No `for`, no `iterrows`, no loops, no loops hidden in comprehension.
- No `zip`.
- No new classes.
- No helper dataframes, no helper classes.
- Use idiomatic pandas.
"""

def _computeVersionMinimum(dataframe: pandas.DataFrame, list_byColumns: list[str], columnNameTarget: str) -> pandas.DataFrame:
	dataframe[columnNameTarget] = numpy.where(
		dataframe.groupby(list_byColumns)["versionMinorPythonInterpreter"].transform("min") == settingsManufacturing.versionMinor_astMinimumSupported,
		-1,
		dataframe.groupby(list_byColumns)["versionMinorPythonInterpreter"].transform("min"),
	)
	return dataframe

@cache
def _get_astModule_astStub() -> ast.Module:
	ImaSearchContext: typeshed_client.SearchContext = typeshed_client.get_search_context(typeshed=pathRoot_typeshed)
	return parsePathFilename2astModule(raiseIfNone(typeshed_client.get_stub_file("ast", search_context=ImaSearchContext)))

def _getDataFromStubFile(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	dataframe["match_args"] = (dataframe[["ClassDefIdentifier", "versionMinorPythonInterpreter", "deprecated"]]
							.apply(tuple, axis="columns")
							.map(getDictionary_match_args())
							.fillna(dataframe["match_args"]))
	"""NOTE deprecated classes are not defined in asdl and they do not have match_args in ast.pyi. The match_args values in the dataframe
	for deprecated classes were created manually. If the dataframe were reset or eliminated, there is not currently a process to
	recreate the match_args for deprecated classes."""
	dataframe.attrs["drop_duplicates"].extend(["match_args"])

	dictionaryClassDef: dict[str, ast.ClassDef] = makeDictionaryClassDef(_get_astModule_astStub())
	def amIDeprecated(ClassDefIdentifier: str) -> bool:
		return bool(NodeTourist(IfThis.isCallIdentifier("deprecated"), doThat=Then.extractIt).captureLastMatch(Make.Module(cast("list[ast.stmt]", dictionaryClassDef[ClassDefIdentifier].decorator_list))))

	dataframe["deprecated"] = pandas.Series(data=False, index=dataframe.index, dtype=bool, name="deprecated")
	dataframe["deprecated"] = dataframe["ClassDefIdentifier"].apply(amIDeprecated)

	def newRowsFrom_match_args(dataframeTarget: pandas.DataFrame) -> pandas.DataFrame:
		dataframeTarget = dataframeTarget[dataframeTarget["match_args"] != ()]

		# Explode match_args tuples into separate rows
		dataframeTarget = dataframeTarget.assign(attribute=dataframeTarget["match_args"]).explode("attribute").reset_index(drop=True)
		# Add required columns
		dataframeTarget["attributeKind"] = "_field"

		def get_type_ast_expr(dddataframeee: pandas.DataFrame) -> tuple[pandas.Series, pandas.Series]:
			attribute: str = cast("str", dddataframeee["attribute"])
			if attribute == 'n':
				# TODO remove when `ast.Num` is updated
				attribute = 'value'
			getAnnotation = NodeTourist[ast.AnnAssign, ast.expr](
				Be.AnnAssign.targetIs(IfThis.isNameIdentifier(attribute)),
				Then.extractIt(DOT.annotation),
			)

			ClassDefIdentifier: str = cast("str", dddataframeee["ClassDefIdentifier"])
			if ClassDefIdentifier == 'NameConstant':
				ClassDefIdentifier = 'Constant'

			type_ast_expr: ast.expr = raiseIfNone(getAnnotation.captureLastMatch(dictionaryClassDef[ClassDefIdentifier]))

			type_ast_expr = NodeChanger(Be.Subscript.valueIs(IfThis.isNameIdentifier("Literal")), Then.replaceWith(Make.Name("bool"))).visit(type_ast_expr)

			dddataframeee["type_ast_expr"] = NodeChanger[ast.Name, ast.expr](
				lambda node: Be.Name(node) and isinstance(eval(node.id), type) and issubclass(eval(node.id), ast.AST),  # noqa: S307
				lambda node: Make.Attribute(Make.Name("ast"), eval(node.id).__name__),  # noqa: S307
			).visit(type_ast_expr)
			dddataframeee["attributeType"] = ast.unparse(cast("ast.AST", dddataframeee["type_ast_expr"]))

			return dddataframeee["type_ast_expr"], dddataframeee["attributeType"]

		dataframeTarget[["type_ast_expr", "attributeType"]] = dataframeTarget.apply(get_type_ast_expr, axis="columns", result_type="expand")
		return dataframeTarget

	dataframe = pandas.concat(objs=[dataframe, newRowsFrom_match_args(dataframe)], axis="index", ignore_index=True)

	dataframe.attrs["drop_duplicates"].extend(["attribute"])
	dataframe = dictionary2Dataframe(attributeType__ClassDefIdentifier_attribute, dataframe)
	dataframe = dataframe.drop_duplicates(subset=dataframe.attrs["drop_duplicates"], keep="last")

	def newRows_attributes(dataframeTarget: pandas.DataFrame) -> pandas.DataFrame:
		"""TODO If there is 'match_args', each element of 'match_args' is an attribute."""
		_attribute_ast_expr = NodeTourist(
			Be.Subscript.valueIs(IfThis.isNameIdentifier("Unpack"))
			, Then.extractIt(DOT.slice)
		).captureLastMatch(dictionaryClassDef[cast("str", dataframeTarget["ClassDefIdentifier"])])
		"""
		).captureLastMatch(dictionaryClassDef[cast("str", dataframeTarget["ClassDefIdentifier"])])
						~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
	TypeError: unhashable type: 'Series'
		"""

		if _attribute_ast_expr:
			if Be.Name(_attribute_ast_expr):
				_attributes = int | None
			elif Be.Subscript(_attribute_ast_expr):
				_attributes = int
		else:
			_attributes = None

		dataframeTarget["attributeKind"] = "_attribute"
		# TODO get class _Attributes, and get the key names and annotations
		dictionary_Attributes: dict[str, ast.expr] = {}
		NodeTourist[ast.AnnAssign, Mapping[str, ast.expr]](
			findThis=Be.AnnAssign.targetIs(Be.Name),
			doThat=Then.updateKeyValueIn(DOT.target(DOT.id), DOT.annotation, dictionary_Attributes),  # pyright: ignore[reportCallIssue, reportArgumentType, reportUnknownArgumentType]
		).visit(dictionaryClassDef[cast("str", dataframeTarget["ClassDefIdentifier"])])

		Make.ClassDef(
			name="_Attributes",
			bases=[ast.Name("TypedDict"), ast.Subscript(value=ast.Name("Generic"), slice=ast.Name("_EndPositionT"))],
			body=[
				Make.AnnAssign(target=ast.Name("lineno", ast.Store()), annotation=ast.Name("int")),
				Make.AnnAssign(target=ast.Name("col_offset", ast.Store()), annotation=ast.Name("int")),
				Make.AnnAssign(target=ast.Name("end_lineno", ast.Store()), annotation=ast.Name("_EndPositionT")),
				Make.AnnAssign(target=ast.Name("end_col_offset", ast.Store()), annotation=ast.Name("_EndPositionT")),
			],
		)
		return dataframeTarget

	# dataframe = pandas.concat(objs=[dataframe, newRows_attributes(dataframe)], axis="index", ignore_index=True)  # noqa: ERA001
	# dataframe = dataframe.drop_duplicates(subset=dataframe.attrs["drop_duplicates"])  # noqa: ERA001

	return dataframe

def _make_astAttribute(ClassDefIdentifier: str) -> ast.expr:
	return Make.Attribute(Make.Name("ast"), ClassDefIdentifier)

def _make_keywordOrList(attributePROXY: dict[str, str | bool | ast.expr]) -> ast.keyword:
	keywordValue = Make.Name(cast("str", attributePROXY["attributeRename"]))
	if attributePROXY["list2Sequence"] is True:
		keywordValue = Make.IfExp(test=keywordValue, body=Make.Call(Make.Name("list"), [keywordValue]), orElse=cast("ast.expr", attributePROXY['orElse']))
	else:
		keywordValue = Make.Or.join([keywordValue, cast("ast.expr", attributePROXY['orElse'])])
	return Make.keyword(cast("str", attributePROXY["attribute"]), keywordValue)

def _make4ColumnsOfLists(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	dictionaryTupleAttributes: dict[tuple[str, int], list[tuple[str, ast.expr]]] = {}
	dictionaryFunctionDef_args: dict[tuple[str, int], list[ast.arg]] = {}
	dictionaryDefaults: dict[tuple[str, int], list[ast.expr]] = {}
	dictionaryCall_keyword: dict[tuple[str, int], list[ast.keyword]] = {}

	for (ClassDefIdentifier, versionMinorMinimum_match_args), dataframeGroupBy in dataframe.groupby(["ClassDefIdentifier", "versionMinorMinimum_match_args"]):
		groupKey: tuple[str, int] = (ClassDefIdentifier, versionMinorMinimum_match_args)
		match_argsCategoricalSort: tuple[str, ...] = dataframeGroupBy["match_args"].iloc[0]
		dataframeGroupBy["attribute"] = pandas.Categorical(dataframeGroupBy["attribute"], categories=match_argsCategoricalSort, ordered=True)
		dataframeGroupBy: pandas.DataFrame = dataframeGroupBy.sort_values(["attribute", 'versionMinorMinimum_match_args'], ascending=[True, False])  # noqa: PLW2901

		dataframeGroupBy = dataframeGroupBy[dataframeGroupBy["attributeKind"] == "_field"]  # noqa: PLW2901

		dictionaryTupleAttributes[groupKey] = (dataframeGroupBy.copy().drop_duplicates(subset="attribute")[["attribute", "type_ast_expr"]].apply(tuple, axis="columns").tolist())

		dictionaryFunctionDef_args[groupKey] = (dataframeGroupBy[dataframeGroupBy["move2keywordArguments"] == False]  # noqa: E712
																.copy().drop_duplicates(subset="attribute")["ast_arg"].tolist())

		dictionaryDefaults[groupKey] = (dataframeGroupBy[(dataframeGroupBy["defaultValue"] != "No")
			& (dataframeGroupBy["move2keywordArguments"] == False)].copy().drop_duplicates(subset="attribute")["defaultValue"].tolist())  # noqa: E712

		dictionaryCall_keyword[groupKey] = (dataframeGroupBy[(dataframeGroupBy["move2keywordArguments"] != "No")
			& (dataframeGroupBy["move2keywordArguments"] != "Unpack")].drop_duplicates(subset="attribute")["Call_keyword"].tolist())

	dataframe["listTupleAttributes"] = (dataframe[["ClassDefIdentifier", "versionMinorMinimum_match_args"]].apply(tuple, axis="columns").map(dictionaryTupleAttributes).fillna(dataframe["listTupleAttributes"]))
	dataframe["listFunctionDef_args"] = (dataframe[["ClassDefIdentifier", "versionMinorMinimum_match_args"]].apply(tuple, axis="columns").map(dictionaryFunctionDef_args).fillna(dataframe["listFunctionDef_args"]))
	dataframe["listDefaults"] = (dataframe[["ClassDefIdentifier", "versionMinorMinimum_match_args"]].apply(tuple, axis="columns").map(dictionaryDefaults).fillna(dataframe["listDefaults"]))
	dataframe["listCall_keyword"] = (dataframe[["ClassDefIdentifier", "versionMinorMinimum_match_args"]].apply(tuple, axis="columns").map(dictionaryCall_keyword).fillna(dataframe["listCall_keyword"]))

	return dataframe

def _makeColumn_ast_arg(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	columnNew = "ast_arg"
	dataframe[columnNew] = pandas.Series(data="No", index=dataframe.index, dtype="object", name=columnNew, copy=True)
	def workhorse(dataframeTarget: pandas.DataFrame) -> Any:
		if cast("str | bool", dataframeTarget["move2keywordArguments"]) != False:  # noqa: E712
			return "No"
		return Make.arg(cast("str", dataframeTarget["attributeRename"]), annotation=cast("ast.expr", dataframeTarget["type_ast_expr"]))

	dataframe[columnNew] = dataframe.apply(workhorse, axis="columns")
	return dataframe

def _makeColumn_list2Sequence(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	columnNew = "list2Sequence"
	dataframe[columnNew] = pandas.Series(data=False, index=dataframe.index, dtype=bool, name=columnNew)
	for ClassDefIdentifier in settingsManufacturing.astSuperClasses:
		mask_attributeType = dataframe["attributeType"].str.contains("list", na=False) & dataframe["attributeType"].str.contains(ClassDefIdentifier, na=False)
		dataframe.loc[mask_attributeType, columnNew] = True
	return dataframe

def _makeColumn_type_ast_expr(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	columnNew = 'type_ast_expr'
	dataframe[columnNew] = pandas.Series(data='No', index=dataframe.index, dtype="object", name=columnNew)
	dataframe.loc[dataframe["list2Sequence"], columnNew] = dataframe["attributeType"].str.replace("list", "Sequence").apply(_pythonCode2expr)
	dataframe.loc[~dataframe["list2Sequence"], columnNew] = dataframe["attributeType"].apply(_pythonCode2expr)
	return dataframe

def _makeColumnCall_keyword(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	def workhorse(dataframeTarget: pandas.DataFrame) -> Any:
		if cast("bool", (dataframeTarget['attributeKind'] == "_field") & ((dataframeTarget['move2keywordArguments'] != "No") & (dataframeTarget['move2keywordArguments'] != "Unpack"))):
			if cast("bool", dataframeTarget["move2keywordArguments"]):
				keywordValue: ast.expr = cast("ast.expr", dataframeTarget["defaultValue"])
			else:
				keywordValue = Make.Name(cast("str", dataframeTarget["attributeRename"]))
				if dataframeTarget["list2Sequence"] is True:
					keywordValue = Make.Call(Make.Name("list"), [keywordValue])
			return Make.keyword(cast("str", dataframeTarget["attribute"]), keywordValue)
		return "No"

	dataframe["Call_keyword"] = dataframe.apply(workhorse, axis="columns")
	return dataframe

def _makeColumnTypeAlias_hasDOTSubcategory(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	columnNew = 'TypeAlias_hasDOTSubcategory'
	dataframe[columnNew] = pandas.Series(data="No", index=dataframe.index, dtype="object", name=columnNew, copy=True)
	mask_hasDOTIdentifier = dataframe["TypeAlias_hasDOTIdentifier"] != "No"
	dataframe.loc[mask_hasDOTIdentifier, columnNew] = dataframe["TypeAlias_hasDOTIdentifier"] + "_" + dataframe["attributeType"].str.replace("|", "Or").str.replace("[", "_").str.replace("[\\] ]", "", regex=True).str.replace("ast.", "")
	return dataframe

def _moveMutable_defaultValue(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	for columnValue, orElse in dictionary_defaultValue_ast_arg_Call_keyword_orElse.items():
		maskByColumnValue = getMaskByColumnValue(dataframe, columnValue)

		attributePROXY = dataframe.loc[maskByColumnValue, ["attribute", "attributeType", "attributeRename", "move2keywordArguments", "list2Sequence"]].drop_duplicates().to_dict(orient="records")

		if len(attributePROXY) > 1:
			message = f"Your current system assumes attribute '{attributePROXY[0]['attribute']}' is the same whenever it is used, but this function got {len(attributePROXY)} variations."
			raise ValueError(message)

		attributePROXY = cast("dict[str, str | bool | ast.expr]", attributePROXY[0])
		if cast("bool", attributePROXY["move2keywordArguments"]):
			message = f"Your current system assumes attribute '{attributePROXY['attribute']}' is not a keyword argument, but this function got {attributePROXY}."
			raise ValueError(message)

		dataframe.loc[maskByColumnValue, "defaultValue"] = Make.Constant(None) # pyright: ignore[reportCallIssue, reportArgumentType]
		attributeType = cast("str", attributePROXY["attributeType"]) + " | None"
		if attributePROXY["list2Sequence"] is True:
			attributeType = attributeType.replace("list", "Sequence")
		dataframe.loc[maskByColumnValue, "ast_arg"] = Make.arg(cast("str", attributePROXY["attributeRename"]), annotation=cast("ast.expr", _pythonCode2expr(attributeType))) # pyright: ignore[reportCallIssue, reportArgumentType]
		attributePROXY['orElse'] = orElse
		dataframe.loc[maskByColumnValue, "Call_keyword"] = _make_keywordOrList(attributePROXY) # pyright: ignore[reportCallIssue, reportArgumentType]

	return dataframe

def _pythonCode2expr(string: str) -> Any:
	"""Convert *one* expression as a string of Python code to an `ast.expr`."""
	astModule: ast.Module = ast.parse(string)
	return raiseIfNone(NodeTourist(Be.Expr, Then.extractIt(DOT.value)).captureLastMatch(astModule))

def dictionary2Dataframe(dictionary: Mapping[MaskTuple, column__value], dataframe: pandas.DataFrame) -> pandas.DataFrame:
	"""Convert a hyper-marked-up dictionary to columns and values in a dataframe."""
	for columnValueMask, assign in dictionary.items():
		dataframe.loc[getMaskByColumnValue(dataframe, columnValueMask), assign.column] = assign.value
	return dataframe

def getMaskByColumnValue(dataframe: pandas.DataFrame, columnValue: MaskTuple) -> pandas.Series:
	"""Convert a specialized `NamedTuple`, which is an arbitrary number of column-names and row-values, to a `True`/`False` mask for a dataframe."""
	return pandas.concat([*[dataframe[column] == value for column, value in columnValue._asdict().items()]], axis=1).all(axis=1)

def updateDataframe() -> None:
	dataframe: pandas.DataFrame = getDataframe(includeDeprecated=True, versionMinorMaximum=settingsManufacturing.versionMinorMaximum, modifyVersionMinorMinimum=False)

	# columns: reorder; drop columns, but they might be recreated later in the flow.  # noqa: ERA001
	# dataframe = dataframe[_columns]  # noqa: ERA001

	# Set dtypes for existing columns
	dataframe = dataframe.astype({
		"ClassDefIdentifier": "string",
		"versionMajorPythonInterpreter": "int64",
		"versionMinorPythonInterpreter": "int64",
		"versionMicroPythonInterpreter": "int64",
		"base": "string",
	})

	dataframe.attrs["drop_duplicates"] = ["ClassDefIdentifier", "versionMinorPythonInterpreter"]

	# TODO Columns to create using the Python Interpreter,
	# from version 3.settingsManufacturing.versionMinor_astMinimumSupported
	# to version 3.settingsManufacturing.versionMinorMaximum, inclusive.
	# 'ClassDefIdentifier',
	# 'versionMajorPythonInterpreter',
	# 'versionMinorPythonInterpreter',
	# 'versionMicroPythonInterpreter',
	# 'base',

	# TODO finish `_getDataFromStubFile`
	dataframe = _getDataFromStubFile(dataframe)

	dataframe["attributeRename"] = pandas.Series(data=dataframe["attribute"], index=dataframe.index, dtype=str, name="attributeRename", copy=True)
	dataframe = dictionary2Dataframe(attributeRename__, dataframe)

	dataframe["move2keywordArguments"] = pandas.Series(data=False, index=dataframe.index, dtype=object, name="move2keywordArguments", copy=True)
	dataframe = dictionary2Dataframe(move2keywordArguments__, dataframe)

	dataframe["defaultValue"] = pandas.Series(data="No", index=dataframe.index, dtype=str, name="defaultValue", copy=True)
	dataframe = dictionary2Dataframe(defaultValue__, dataframe)

	dataframe["classAs_astAttribute"] = dataframe["ClassDefIdentifier"].astype(str).map(_make_astAttribute)
	dataframe = _makeColumn_list2Sequence(dataframe)
	dataframe = _makeColumn_type_ast_expr(dataframe)
	dataframe["type_astSuperClasses"] = dataframe["attributeType"].replace({f"ast.{ClassDefIdentifier}": identifierTypeVar for ClassDefIdentifier, identifierTypeVar in settingsManufacturing.astSuperClasses.items()}, regex=True)
	dataframe = _makeColumn_ast_arg(dataframe)
	dataframe["type_astSuperClasses_ast_expr"] = numpy.where(dataframe["type_astSuperClasses"] == "No", "No", dataframe["type_astSuperClasses"].apply(_pythonCode2expr))
	dataframe["TypeAlias_hasDOTIdentifier"] = numpy.where(dataframe["attributeKind"] == "_field", "hasDOT" + cast("str", dataframe["attribute"]), "No")
	dataframe = _makeColumnTypeAlias_hasDOTSubcategory(dataframe)
	dataframe = _computeVersionMinimum(dataframe, ["ClassDefIdentifier", "match_args"], "versionMinorMinimum_match_args")
	dataframe = _computeVersionMinimum(dataframe, ["ClassDefIdentifier", "attribute"], "versionMinorMinimumAttribute")
	dataframe = _computeVersionMinimum(dataframe, ["ClassDefIdentifier"], "versionMinorMinimumClass")
	dataframe = _makeColumnCall_keyword(dataframe)
	dataframe = _moveMutable_defaultValue(dataframe)
	dataframe = _sortCaseInsensitive(dataframe, ["ClassDefIdentifier", "versionMinorPythonInterpreter", "attribute"]
								, caseInsensitive=[True, False, True], ascending=[True, False, True])
	# TODO Figure out overload for `Make`
	dataframe = _make4ColumnsOfLists(dataframe)

	dataframe.to_pickle(settingsManufacturing.pathFilenameDataframeAST)

if __name__ == "__main__":
	updateDataframe()
