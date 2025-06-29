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
from astToolkit import (
	Be, ConstantValueType as _ConstantValue, DOT, dump, identifierDotAttribute, IfThis, Make, NodeChanger, NodeTourist,
	parsePathFilename2astModule, Then,
)
from astToolkit.transformationTools import makeDictionaryClassDef
from collections.abc import Callable, Mapping, Sequence
from typing import Any, cast, Literal, TypeIs
from Z0Z_tools import raiseIfNone
import ast
import numpy
import pandas
import typeshed_client
from functools import cache

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

def _get_match_argsByVersionGuard(dataframeTarget: pandas.DataFrame) -> pandas.Series:
	def filterByVersion(node: ast.AST, *, orelse: bool = False) -> TypeIs[ast.If] | bool:
		return (Be.If(node)
			and Be.Compare(node.test)
			and IfThis.isAttributeNamespaceIdentifier("sys", "version_info")(node.test.left)
			and Be.Tuple(node.test.comparators[0])
			and IfThis.isConstant_value(dataframeTarget["versionMinorPythonInterpreter"] + int(orelse))(node.test.comparators[0].elts[1]))

	def findThis_body(node: ast.AST) -> TypeIs[ast.If] | bool:
		return (filterByVersion(node, orelse=False)
			and IfThis.isAssignAndTargets0Is(IfThis.isNameIdentifier("__match_args__"))(cast("ast.If", node).body[0]))

	def findThis_orelse(node: ast.AST) -> TypeIs[ast.If] | bool:
		return (filterByVersion(node, orelse=True)
				and cast("ast.If", node).orelse
				and IfThis.isAssignAndTargets0Is(IfThis.isNameIdentifier("__match_args__"))(cast("ast.If", node).orelse[0])) # pyright: ignore[reportReturnType]

	def getNaked_match_args() -> list[ast.stmt] | None:
		dictionaryIdentifier2astIf: dict[str, ast.If] = _getDictionaryIdentifier2astIf()
		body: list[ast.stmt] | None = None
		if ((nodeIf := dictionaryIdentifier2astIf.get(cast("str", dataframeTarget["ClassDefIdentifier"])))
			# `node` is an `ast.If` node. dataframeTarget['ClassDefIdentifier'] is in `ast.If.body`.  # noqa: ERA001
		and filterByVersion(nodeIf, orelse=False)):
			# And, version == dataframeTarget['versionMinorPythonInterpreter']  # noqa: ERA001
			def findThis_match_args(node: ast.AST) -> TypeIs[ast.ClassDef] | bool:
				return (IfThis.isClassDefIdentifier(cast("str", dataframeTarget["ClassDefIdentifier"]))(node)
				# look for dataframeTarget['ClassDefIdentifier'] and return match_args or None  # noqa: ERA001
					and IfThis.isAssignAndTargets0Is(IfThis.isNameIdentifier("__match_args__"))(cast("ast.ClassDef", node).body[0]))

			body = NodeTourist(findThis_match_args, Then.extractIt(cast("Callable[[ast.ClassDef], list[ast.stmt]]", DOT.body))).captureLastMatch(nodeIf)
		return body

	dictionaryClassDef: dict[str, ast.ClassDef] = makeDictionaryClassDef(_get_astModule_astStub())
	body: list[ast.stmt] | None = NodeTourist(findThis_body
									, Then.extractIt(cast("Callable[[ast.If], list[ast.stmt]]", DOT.body))
									).captureLastMatch(dictionaryClassDef[cast("str", dataframeTarget["ClassDefIdentifier"])])

	dataframeTarget["match_args"] = None

	if body:
		dataframeTarget["match_args"] = literal_eval(cast("ast.Assign", body[0]).value)
	else:
		orelse: list[ast.stmt] | None = NodeTourist(findThis_orelse
										, Then.extractIt(cast("Callable[[ast.If], list[ast.stmt]]", DOT.orelse))
										).captureLastMatch(dictionaryClassDef[cast("str", dataframeTarget["ClassDefIdentifier"])])
		if orelse:
			dataframeTarget["match_args"] = literal_eval(cast("ast.Assign", orelse[0]).value)
		else:
			naked_match_args: list[ast.stmt] | None = getNaked_match_args()
			if naked_match_args:
				dataframeTarget["match_args"] = literal_eval(cast("ast.Assign", naked_match_args[0]).value)
	return dataframeTarget["match_args"]

def _getDataFromStubFile(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	dictionaryClassDef: dict[str, ast.ClassDef] = makeDictionaryClassDef(_get_astModule_astStub())

	dataframe["match_args"] = dataframe[["ClassDefIdentifier", "versionMinorPythonInterpreter"]].apply(_get_match_argsByVersionGuard, axis="columns")
	dataframe.attrs["drop_duplicates"].extend(["match_args"])

	dataframe.pipe(_sortCaseInsensitive, ["ClassDefIdentifier", "versionMinorPythonInterpreter"], caseInsensitive=[True, False], ascending=[True, False])

	# Assign 'match_args' from 'versionMinorPythonInterpreter' < your version.
	dataframe["match_args"] = dataframe.groupby("ClassDefIdentifier")["match_args"].bfill()
	# Because Python 3.9 does not have `__match_args__`, Assign 'match_args' from 'versionMinorPythonInterpreter' > your version.
	dataframe["match_args"] = dataframe.groupby("ClassDefIdentifier")["match_args"].ffill()

	# Fill missing 'match_args' values with empty tuple
	dataframe["match_args"] = dataframe["match_args"].apply(lambda x: () if pandas.isna(x) else x) # pyright: ignore[reportUnknownArgumentType, reportUnknownLambdaType]
	# dataframe["match_args"] = dataframe["match_args"].fillna(())  # noqa: ERA001
	# TypeError: "value" parameter must be a scalar or dict, but you passed a "tuple"  # noqa: ERA001

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

	# dataframe = pandas.concat(objs=[dataframe, newRows_attributes(dataframe)], axis="index", ignore_index=True)
	# dataframe = dataframe.drop_duplicates(subset=dataframe.attrs["drop_duplicates"])

	return dataframe

def _getDictionaryIdentifier2astIf() -> dict[str, ast.If]:
	astModule_astStub = _get_astModule_astStub()
	list_astIf_sys_version_info: list[ast.If] = []
	NodeTourist(Be.If.testIs(Be.Compare.leftIs(IfThis.isAttributeNamespaceIdentifier("sys", "version_info")))
		, doThat=Then.appendTo(list_astIf_sys_version_info)
		).visit(astModule_astStub)
	dictionaryIdentifier2astIf: dict[str, ast.If] = {}
	for astIf in list_astIf_sys_version_info:
		NodeTourist(Be.ClassDef, Then.updateKeyValueIn(DOT.name, lambda _node: astIf, dictionaryIdentifier2astIf)).visit(astIf)  # noqa: B023
	return dictionaryIdentifier2astIf

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

 
# def _make3Columns4ClassMakePlus1Column(dataframe: pandas.DataFrame) -> pandas.DataFrame:
# 	def workhorse(dataframeTarget: pandas.DataFrame):
# 		dataframeTarget["attribute"] = pandas.Categorical(
# 			dataframeTarget["attribute"]
# 			, categories=dataframeTarget["match_args"].iloc[0]
# 			, ordered=True
# 		)

# 		maskTupleAttributes = dataframeTarget["attributeKind"] == "_field"
# 		maskFunctionDef_args = dataframeTarget["move2keywordArguments"] == False  # noqa: E712
# 		maskDefaults = dataframeTarget["defaultValue"] != "No"
# 		maskCall_keyword = (dataframeTarget["move2keywordArguments"] != "No") & (dataframeTarget["move2keywordArguments"] != "Unpack")

# 		listByColumns = ["ClassDefIdentifier", "versionMinorMinimum_match_args"]
# 		drop_duplicates = [*listByColumns, "attribute"]

# 		dataframeTarget["listTupleAttributes"] = (
# 			dataframeTarget[maskTupleAttributes]
# 			.drop_duplicates(subset=drop_duplicates)
# 			.groupby(listByColumns)
# 			[["attribute", "type_ast_expr"]]
# 			.transform(list)
# 			.groupby(level=0)
# 			.first()
# 		)

# 		dataframeTarget["listFunctionDef_args"] = (
# 			dataframeTarget[maskFunctionDef_args]
# 			.drop_duplicates(subset=drop_duplicates)
# 			.sort_values("attribute")
# 			.groupby(listByColumns)
# 			["ast_arg"]
# 			.transform(list)
# 		)

# 		dataframeTarget["listDefaults"] = (
# 			dataframeTarget[maskFunctionDef_args & maskDefaults]
# 			.drop_duplicates(subset=drop_duplicates)
# 			.groupby(listByColumns)
# 			["defaultValue"]
# 			.transform(list)
# 		)

# 		dataframeTarget["listCall_keyword"] = (
# 			dataframeTarget[maskCall_keyword]
# 			.drop_duplicates(subset=drop_duplicates)
# 			.sort_values("attribute")
# 			.groupby(listByColumns)
# 			["Call_keyword"]
# 			.transform(list)
# 		)

# 	dataframe[["listFunctionDef_args", "listDefaults", "listCall_keyword", "listTupleAttributes"]] = dataframe.apply(workhorse, axis="columns", result_type="expand")

# 	return dataframe

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
	# dataframe = dataframe[_columns]

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
	# dataframe = _getDataFromStubFile(dataframe)

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
