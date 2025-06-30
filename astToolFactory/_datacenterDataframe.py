from ast import (
	alias, arg, arguments, Attribute, boolop, cmpop, comprehension, ExceptHandler, expr, expr_context, keyword,
	literal_eval, match_case, Name, operator, pattern, stmt, Subscript, type_param, TypeIgnore, unaryop, withitem,
)
from astToolFactory import pathRoot_typeshed, settingsManufacturing
from astToolFactory._datacenter import _sortCaseInsensitive, getDataframe
from astToolFactory._datacenterAnnex import (
	_columns, attributeRename__attribute, attributeRename__ClassDefIdentifier_attribute, defaultValue__attribute,
	defaultValue__ClassDefIdentifier_attribute, defaultValue__type_attribute, move2keywordArguments__attribute,
	move2keywordArguments__attributeKind, type__ClassDefIdentifier_attribute,
)
from astToolFactory.cpython import getDictionary_match_args
from astToolkit import (
	Be, ConstantValueType as _ConstantValue, DOT, dump, identifierDotAttribute, IfThis, Make, NodeChanger, NodeTourist,
	parsePathFilename2astModule, Then,
)
from astToolkit.transformationTools import makeDictionaryClassDef
from collections.abc import Callable, Mapping, Sequence
from functools import cache
from typing import Any, cast, Literal, TypeIs
from Z0Z_tools import raiseIfNone
import ast
import numpy
import pandas
import typeshed_client

"""Use idiomatic pandas.
- No `lambda`, except `key=lambda`.
- No intermediate data structures.
- A dataframe is a data structure: no intermediate dataframes.
- A so-called mask is an intermediate dataframe: no "masks".
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
	match_args__ClassDefIdentifier_versionMinorPythonInterpreter_deprecated = getDictionary_match_args()
	dataframe["match_args"] = (dataframe[["ClassDefIdentifier", "versionMinorPythonInterpreter", "deprecated"]]
							.apply(tuple, axis="columns")
							.map(match_args__ClassDefIdentifier_versionMinorPythonInterpreter_deprecated)
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
			getAnnotation = NodeTourist[ast.AnnAssign, ast.expr](
				Be.AnnAssign.targetIs(IfThis.isNameIdentifier(cast("str", dddataframeee["attribute"]))),
				Then.extractIt(DOT.annotation),
			)

			type_ast_expr: ast.expr = raiseIfNone(getAnnotation.captureLastMatch(dictionaryClassDef[cast("str", dddataframeee["ClassDefIdentifier"])]))

			type_ast_expr = NodeChanger(Be.Subscript.valueIs(IfThis.isNameIdentifier("Literal")), Then.replaceWith(Make.Name("bool"))).visit(type_ast_expr)

			dddataframeee["type_ast_expr"] = NodeChanger[ast.Name, ast.expr](
				lambda node: Be.Name(node) and isinstance(eval(node.id), type) and issubclass(eval(node.id), ast.AST),  # noqa: S307
				lambda node: Make.Attribute(Make.Name("ast"), eval(node.id).__name__),  # noqa: S307
			).visit(type_ast_expr)
			dddataframeee["type"] = ast.unparse(cast("ast.AST", dddataframeee["type_ast_expr"]))

			return dddataframeee["type_ast_expr"], dddataframeee["type"]

		dataframeTarget[["type_ast_expr", "type"]] = dataframeTarget.apply(get_type_ast_expr, axis="columns", result_type="expand")
		return dataframeTarget

	dataframe = pandas.concat(objs=[dataframe, newRowsFrom_match_args(dataframe)], axis="index", ignore_index=True)

	dataframe.attrs["drop_duplicates"].extend(["attribute"])
	dataframe["type"] = dataframe[["ClassDefIdentifier", "attribute"]].apply(tuple, axis="columns").map(type__ClassDefIdentifier_attribute).fillna(dataframe["type"])
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

def _make_keywordOrList(dataframeTarget: pandas.DataFrame) -> Any:
	if cast("bool", dataframeTarget["move2keywordArguments"]):
		keywordValue: ast.expr = cast("ast.expr", dataframeTarget["defaultValue"])
	else:
		keywordValue = Make.Name(cast("str", dataframeTarget["attributeRename"]))
		if dataframeTarget["list2Sequence"] is True:
			keywordValue = Make.Call(Make.Name("list"), [keywordValue])
	keywordValue = Make.Or.join([keywordValue, Make.List()])
	return Make.keyword(cast("str", dataframeTarget["attribute"]), keywordValue)

def _make3Columns4ClassMakePlus1Column(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	def make3Columns4ClassMakePlus1Column(dataframeTarget: pandas.DataFrame) -> tuple[pandas.Series, pandas.Series, pandas.Series, pandas.Series]:
		matchingRows: pandas.DataFrame = dataframe[(dataframe["ClassDefIdentifier"] == cast("str", dataframeTarget["ClassDefIdentifier"]))
									& (dataframe["versionMinorMinimum_match_args"] == cast("int", dataframeTarget["versionMinorMinimum_match_args"]))]

		matchingRows_listTupleAttributes = matchingRows[matchingRows["attributeKind"] == "_field"].copy()
		dataframeTarget["listTupleAttributes"] = matchingRows_listTupleAttributes.drop_duplicates(subset="attribute")[["attribute", "type_ast_expr"]].apply(tuple, axis="columns").tolist()

		matchingRows["attribute"] = pandas.Categorical(matchingRows["attribute"], categories=matchingRows["match_args"].iloc[0], ordered=True)

		matchingRows_listCall_keyword: pandas.DataFrame = matchingRows[matchingRows["move2keywordArguments"] != "No"].copy(deep=True)
		matchingRows = matchingRows[matchingRows["move2keywordArguments"] == False].sort_values("attribute")  # noqa: E712
		matchingRows_listDefaults = matchingRows[matchingRows["defaultValue"] != "No"].copy(deep=True)

		dataframeTarget["listFunctionDef_args"] = matchingRows.drop_duplicates(subset="attribute")["ast_arg"].tolist()
		dataframeTarget["listDefaults"] = matchingRows_listDefaults.drop_duplicates(subset="attribute")["defaultValue"].tolist()

		matchingRows_listCall_keyword = matchingRows_listCall_keyword[matchingRows_listCall_keyword["move2keywordArguments"] != "Unpack"].drop_duplicates(subset="attribute").sort_values("attribute")

		dataframeTarget["listCall_keyword"] = matchingRows_listCall_keyword["Call_keyword"].tolist()

		return (
			dataframeTarget["listFunctionDef_args"],
			dataframeTarget["listDefaults"],
			dataframeTarget["listCall_keyword"],
			dataframeTarget["listTupleAttributes"],
		)

	dataframe[["listFunctionDef_args", "listDefaults", "listCall_keyword", "listTupleAttributes"]] = dataframe.apply(make3Columns4ClassMakePlus1Column, axis="columns", result_type="expand")

	return dataframe

def _makeColumn_ast_arg(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	def makeColumn_ast_arg(dataframeTarget: pandas.DataFrame) -> Any:
		if cast("str | bool", dataframeTarget["move2keywordArguments"]) != False:  # noqa: E712
			return "No"
		return Make.arg(cast("str", dataframeTarget["attributeRename"]), annotation=cast("ast.expr", dataframeTarget["type_ast_expr"]))

	dataframe["ast_arg"] = dataframe.apply(makeColumn_ast_arg, axis="columns")
	return dataframe

def _makeColumn_attributeRename(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	dataframe["attributeRename"] = pandas.Series(data=dataframe["attribute"], index=dataframe.index, dtype=str, name="attributeRename", copy=True)
	dataframe["attributeRename"] = dataframe["attribute"].map(attributeRename__attribute).fillna(dataframe["attributeRename"])
	dataframe["attributeRename"] = dataframe[["ClassDefIdentifier", "attribute"]].apply(tuple, axis="columns").map(attributeRename__ClassDefIdentifier_attribute).fillna(dataframe["attributeRename"])
	return dataframe

def _makeColumn_defaultValue(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	dataframe["defaultValue"] = "No"  # Default value for the column
	dataframe["defaultValue"] = dataframe["attribute"].map(defaultValue__attribute).fillna(dataframe["defaultValue"])
	dataframe["defaultValue"] = dataframe[["ClassDefIdentifier", "attribute"]].apply(tuple, axis="columns").map(defaultValue__ClassDefIdentifier_attribute).fillna(dataframe["defaultValue"])
	dataframe["defaultValue"] = dataframe[["type", "attribute"]].apply(tuple, axis="columns").map(defaultValue__type_attribute).fillna(dataframe["defaultValue"])
	return dataframe

def _makeColumn_list2Sequence(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	dataframe["list2Sequence"] = pandas.Series(data=False, index=dataframe.index, dtype=bool, name="list2Sequence")
	containsListSuperClass = pandas.Series(data=False, index=dataframe.index, dtype=bool)
	for ClassDefIdentifier in settingsManufacturing.astSuperClasses:
		containsListSuperClass |= dataframe["type"].str.contains("list", regex=False, na=False) & dataframe["type"].str.contains(ClassDefIdentifier, regex=False, na=False)
	dataframe.loc[containsListSuperClass, "list2Sequence"] = True
	return dataframe

def _makeColumn_move2keywordArguments(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	dataframe["move2keywordArguments"] = False  # Default value for the column
	dataframe["move2keywordArguments"] = dataframe["attributeKind"].map(move2keywordArguments__attributeKind).fillna(dataframe["move2keywordArguments"])
	dataframe["move2keywordArguments"] = dataframe["attribute"].map(move2keywordArguments__attribute).fillna(dataframe["move2keywordArguments"])
	return dataframe

def _makeColumn_type_ast_expr(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	dataframe.loc[dataframe["list2Sequence"], "type_ast_expr"] = dataframe["type"].str.replace("list", "Sequence").apply(_pythonCode2expr)
	dataframe.loc[~dataframe["list2Sequence"], "type_ast_expr"] = dataframe["type"].apply(_pythonCode2expr)
	dataframe.loc[dataframe["type"] == "No", "type_ast_expr"] = "No"
	return dataframe

def _makeColumn_type_astSuperClasses(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	dataframe["type_astSuperClasses"] = dataframe["type"].replace(
		{f"ast.{ClassDefIdentifier}": identifierTypeVar for ClassDefIdentifier, identifierTypeVar in settingsManufacturing.astSuperClasses.items()},
		regex=True,
	)
	return dataframe

def _makeColumn_type_astSuperClasses_ast_expr(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	dataframe["type_astSuperClasses_ast_expr"] = numpy.where(dataframe["type_astSuperClasses"] == "No", "No", dataframe["type_astSuperClasses"].apply(_pythonCode2expr))
	return dataframe

def _makeColumn_versionMinorMinimum_match_args(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	return _computeVersionMinimum(dataframe, ["ClassDefIdentifier", "match_args"], "versionMinorMinimum_match_args")

def _makeColumn_versionMinorMinimumAttribute(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	return _computeVersionMinimum(dataframe, ["ClassDefIdentifier", "attribute"], "versionMinorMinimumAttribute")

def _makeColumn_versionMinorMinimumClass(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	return _computeVersionMinimum(dataframe, ["ClassDefIdentifier"], "versionMinorMinimumClass")

def _makeColumnCall_keyword(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	def makeColumnCall_keyword(dataframeTarget: pandas.DataFrame) -> Any:
		if cast("bool", (dataframeTarget['attributeKind'] == "_field") & ((dataframeTarget['move2keywordArguments'] != "No") & (dataframeTarget['move2keywordArguments'] != "Unpack"))):
			if cast("bool", dataframeTarget["move2keywordArguments"]):
				keywordValue: ast.expr = cast("ast.expr", dataframeTarget["defaultValue"])
			else:
				keywordValue = Make.Name(cast("str", dataframeTarget["attributeRename"]))
				if dataframeTarget["list2Sequence"] is True:
					keywordValue = Make.Call(Make.Name("list"), [keywordValue])
			keywordValue = Make.Or.join([keywordValue, Make.List()])
			return Make.keyword(cast("str", dataframeTarget["attribute"]), keywordValue)
		return "No"

	dataframe["Call_keyword"] = dataframe.apply(makeColumnCall_keyword, axis="columns")
	return dataframe

def _makeColumnTypeAlias_hasDOTIdentifier(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	dataframe["TypeAlias_hasDOTIdentifier"] = numpy.where(dataframe["attributeKind"] == "_field", "hasDOT" + cast("str", dataframe["attribute"]), "No")
	return dataframe

def _makeColumnTypeAlias_hasDOTSubcategory(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	dataframe["TypeAlias_hasDOTSubcategory"] = numpy.where(
		(attribute := dataframe["TypeAlias_hasDOTIdentifier"]) == "No",
		"No",
		cast("str", attribute) + "_" + dataframe["type"].str.replace("|", "Or", regex=False).str.replace("[", "_", regex=False).str.replace("[\\] ]", "", regex=True).str.replace("ast.", "", regex=False),
	)
	return dataframe

def _pythonCode2expr(string: str) -> Any:
	astModule: ast.Module = ast.parse(string)
	return raiseIfNone(NodeTourist(Be.Expr, Then.extractIt(DOT.value)).captureLastMatch(astModule))

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

	dataframe = _makeColumn_attributeRename(dataframe)
	dataframe = _makeColumn_move2keywordArguments(dataframe)
	dataframe = _makeColumn_defaultValue(dataframe)
	dataframe["classAs_astAttribute"] = dataframe["ClassDefIdentifier"].astype(str).map(_make_astAttribute)
	dataframe = _makeColumn_list2Sequence(dataframe)
	dataframe = _makeColumn_type_ast_expr(dataframe)
	dataframe = _makeColumn_type_astSuperClasses(dataframe)
	dataframe = _makeColumn_ast_arg(dataframe)
	dataframe = _makeColumn_type_astSuperClasses_ast_expr(dataframe)
	dataframe = _makeColumnTypeAlias_hasDOTIdentifier(dataframe)
	dataframe = _makeColumnTypeAlias_hasDOTSubcategory(dataframe)
	dataframe = _makeColumn_versionMinorMinimum_match_args(dataframe)
	dataframe = _makeColumn_versionMinorMinimumAttribute(dataframe)
	dataframe = _makeColumn_versionMinorMinimumClass(dataframe)
	dataframe = _makeColumnCall_keyword(dataframe)
	dataframe = _make3Columns4ClassMakePlus1Column(dataframe)

	dataframe.to_pickle(settingsManufacturing.pathFilenameDataframeAST)

if __name__ == "__main__":
	updateDataframe()
