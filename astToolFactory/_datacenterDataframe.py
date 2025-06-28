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

"""Use idiomatic pandas.
- No `lambda`, except `key=lambda`.
- No intermediate data structures.
- A dataframe is a data structure: no intermediate dataframes.
- A so-called mask is an intermediate dataframe: no "masks".
- A column is a data structure: no intermediate columns.
- No `for`, no `iterrows`, no loops, no loops hidden in comprehension.
- No `zip`.
- No new functions.
- No new classes.
- No helper dataframes, no helper functions, no helper classes.
- Use idiomatic pandas.
"""


def updateDataframe() -> None:  # noqa: C901, PLR0915
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

	ImaSearchContext: typeshed_client.SearchContext = typeshed_client.get_search_context(typeshed=pathRoot_typeshed)
	astModule_astStub: ast.Module = parsePathFilename2astModule(raiseIfNone(typeshed_client.get_stub_file("ast", search_context=ImaSearchContext)))

	dictionaryClassDef: dict[str, ast.ClassDef] = makeDictionaryClassDef(astModule_astStub)
	list_astIf_sys_version_info: list[ast.If] = []
	NodeTourist(Be.If.testIs(Be.Compare.leftIs(IfThis.isAttributeNamespaceIdentifier("sys", "version_info")))
		, doThat=Then.appendTo(list_astIf_sys_version_info)
		).visit(astModule_astStub)

	dictionaryIdentifier2astIf: dict[str, ast.If] = {}
	for astIf in list_astIf_sys_version_info:
		NodeTourist(Be.ClassDef, Then.updateKeyValueIn(DOT.name, lambda _node: astIf, dictionaryIdentifier2astIf)).visit(astIf)  # noqa: B023

	def get_match_argsByVersionGuard(dataframeTarget: pandas.DataFrame) -> pandas.Series:
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

		body: list[ast.stmt] | None = NodeTourist(findThis_body
											, Then.extractIt(cast("Callable[[ast.If], list[ast.stmt]]", DOT.body))
											).captureLastMatch(dictionaryClassDef[cast("str", dataframeTarget["ClassDefIdentifier"])])

		dataframeTarget["match_args"] = None  # Default value for the column

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

	dataframe["match_args"] = dataframe[["ClassDefIdentifier", "versionMinorPythonInterpreter"]].apply(get_match_argsByVersionGuard, axis="columns")
	dataframe.attrs["drop_duplicates"].extend(["match_args"])

	dataframe.pipe(
		_sortCaseInsensitive,
		["ClassDefIdentifier", "versionMinorPythonInterpreter"],
		caseInsensitive=[True, False],
		ascending=[True, False],
	)
	# Assign 'match_args' from 'versionMinorPythonInterpreter' < your version.
	dataframe["match_args"] = dataframe.groupby("ClassDefIdentifier")["match_args"].bfill()
	# Because Python 3.9 does not have `__match_args__`, Assign 'match_args' from 'versionMinorPythonInterpreter' > your version.
	dataframe["match_args"] = dataframe.groupby("ClassDefIdentifier")["match_args"].ffill()

	# Fill missing 'match_args' values with empty tuple
	dataframe["match_args"] = dataframe["match_args"].apply(lambda x: () if pandas.isna(x) else x) # pyright: ignore[reportUnknownArgumentType, reportUnknownLambdaType]

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

	dataframe = cast(
		"pandas.DataFrame",
		pandas.concat([dataframe, newRowsFrom_match_args(dataframe)], ignore_index=True, axis="rows"),  # pyright: ignore[reportCallIssue, reportArgumentType]
	)
	# `(function) extend: Any` because concat sucks  # noqa: ERA001
	dataframe.attrs["drop_duplicates"].extend(["attribute"])
	dataframe["type"] = dataframe[["ClassDefIdentifier", "attribute"]].apply(tuple, axis="columns").map(type__ClassDefIdentifier_attribute).fillna(dataframe["type"])
	dataframe = dataframe.drop_duplicates(subset=dataframe.attrs["drop_duplicates"], keep="last")

	def pythonCode2expr(string: str) -> Any:
		astModule: ast.Module = ast.parse(string)
		ast_expr: ast.expr = raiseIfNone(NodeTourist(Be.Expr, Then.extractIt(DOT.value)).captureLastMatch(astModule))
		return ast_expr

	def newRows_attributes(dataframeTarget: pandas.DataFrame) -> pandas.DataFrame:
		_attribute_ast_expr = NodeTourist(
			Be.Subscript.valueIs(IfThis.isNameIdentifier("Unpack")),
			Then.extractIt(DOT.slice),
		).captureLastMatch(dictionaryClassDef[cast("str", dataframeTarget["ClassDefIdentifier"])])
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

	# dataframe = cast("pandas.DataFrame", pandas.concat([dataframe, newRows_attributes(dataframe)], ignore_index=True, axis="rows"))
	# dataframe = dataframe.drop_duplicates(subset=dataframe.attrs["drop_duplicates"])

	# Create 'attributeRename'
	dataframe["attributeRename"] = pandas.Series(data=dataframe["attribute"], index=dataframe.index, dtype=str, name="attributeRename", copy=True)
	dataframe["attributeRename"] = dataframe["attribute"].map(attributeRename__attribute).fillna(dataframe["attributeRename"])
	dataframe["attributeRename"] = dataframe[["ClassDefIdentifier", "attribute"]].apply(tuple, axis="columns").map(attributeRename__ClassDefIdentifier_attribute).fillna(dataframe["attributeRename"])

	dataframe["move2keywordArguments"] = False  # Default value for the column
	dataframe["move2keywordArguments"] = dataframe["attributeKind"].map(move2keywordArguments__attributeKind).fillna(dataframe["move2keywordArguments"])
	dataframe["move2keywordArguments"] = dataframe["attribute"].map(move2keywordArguments__attribute).fillna(dataframe["move2keywordArguments"])

	dataframe["defaultValue"] = "No"  # Default value for the column
	dataframe["defaultValue"] = dataframe["attribute"].map(defaultValue__attribute).fillna(dataframe["defaultValue"])
	dataframe["defaultValue"] = dataframe[["ClassDefIdentifier", "attribute"]].apply(tuple, axis="columns").map(defaultValue__ClassDefIdentifier_attribute).fillna(dataframe["defaultValue"])
	dataframe["defaultValue"] = dataframe[["type", "attribute"]].apply(tuple, axis="columns").map(defaultValue__type_attribute).fillna(dataframe["defaultValue"])

	def makeColumn_classAs_astAttribute(ClassDefIdentifier: str) -> ast.expr:
		return Make.Attribute(Make.Name("ast"), ClassDefIdentifier)

	dataframe["classAs_astAttribute"] = dataframe["ClassDefIdentifier"].astype(str).map(makeColumn_classAs_astAttribute)

	# Create 'list2Sequence' based on 'type' and 'astSuperClasses'
	dataframe["list2Sequence"] = pandas.Series(data=False, index=dataframe.index, dtype=bool, name="list2Sequence")
	containsListSuperClass = pandas.Series(data=False, index=dataframe.index, dtype=bool)
	for ClassDefIdentifier in settingsManufacturing.astSuperClasses:
		containsListSuperClass |= dataframe["type"].str.contains("list", regex=False, na=False) & dataframe["type"].str.contains(ClassDefIdentifier, regex=False, na=False)
	dataframe.loc[containsListSuperClass, "list2Sequence"] = True
	del containsListSuperClass

	# Create 'type_ast_expr' based on columns 'type' and 'list2Sequence'
	dataframe.loc[dataframe["list2Sequence"], "type_ast_expr"] = dataframe["type"].str.replace("list", "Sequence").apply(pythonCode2expr)
	dataframe.loc[~dataframe["list2Sequence"], "type_ast_expr"] = dataframe["type"].apply(pythonCode2expr)
	dataframe.loc[dataframe["type"] == "No", "type_ast_expr"] = "No"

	# Create 'type_astSuperClasses' with TypeVar substitutions
	dataframe["type_astSuperClasses"] = dataframe["type"].replace(
		{f"ast.{ClassDefIdentifier}": identifierTypeVar for ClassDefIdentifier, identifierTypeVar in settingsManufacturing.astSuperClasses.items()},
		regex=True,
	)
	# Create 'type_astSuperClasses_ast_expr'
	dataframe["type_astSuperClasses_ast_expr"] = numpy.where(dataframe["type_astSuperClasses"] == "No", "No", dataframe["type_astSuperClasses"].apply(pythonCode2expr))

	def makeColumn_ast_arg(dataframeTarget: pandas.DataFrame) -> Any:
		if cast("str | bool", dataframeTarget["move2keywordArguments"]) != False:  # noqa: E712
			return "No"
		return Make.arg(cast("str", dataframeTarget["attributeRename"]), annotation=cast("ast.expr", dataframeTarget["type_ast_expr"]))

	dataframe["ast_arg"] = dataframe.apply(makeColumn_ast_arg, axis="columns")

	# Create TypeAlias_hasDOTIdentifier
	dataframe["TypeAlias_hasDOTIdentifier"] = numpy.where(dataframe["attributeKind"] == "_field", "hasDOT" + cast("str", dataframe["attribute"]), "No")

	# Create TypeAlias_hasDOTSubcategory
	dataframe["TypeAlias_hasDOTSubcategory"] = numpy.where(
		(attribute := dataframe["TypeAlias_hasDOTIdentifier"]) == "No",
		"No",
		cast("str", attribute) + "_" + dataframe["type"].str.replace("|", "Or", regex=False).str.replace("[", "_", regex=False).str.replace("[\\] ]", "", regex=True).str.replace("ast.", "", regex=False),
	)

	# --- Group-Based Column Computation ---
	def computeVersionMinimum(list_byColumns: list[str]) -> numpy.ndarray[tuple[int, ...], numpy.dtype[numpy.int64]]:
		return numpy.where(
			dataframe.groupby(list_byColumns)["versionMinorPythonInterpreter"].transform("min") == settingsManufacturing.versionMinor_astMinimumSupported,
			-1,
			dataframe.groupby(list_byColumns)["versionMinorPythonInterpreter"].transform("min"),
		)

	dataframe["versionMinorMinimum_match_args"] = computeVersionMinimum(["ClassDefIdentifier", "match_args"])
	dataframe["versionMinorMinimumAttribute"] = computeVersionMinimum(["ClassDefIdentifier", "attribute"])
	dataframe["versionMinorMinimumClass"] = computeVersionMinimum(["ClassDefIdentifier"])

	def make3Columns4ClassMake(
		dataframeTarget: pandas.DataFrame,
	) -> tuple[pandas.Series, pandas.Series, pandas.Series, pandas.Series]:
		matchingRows: pandas.DataFrame = dataframe[(dataframe["ClassDefIdentifier"] == cast("str", dataframeTarget["ClassDefIdentifier"])) & (dataframe["versionMinorMinimum_match_args"] == cast("int", dataframeTarget["versionMinorMinimum_match_args"]))]

		matchingRows_listTupleAttributes = matchingRows[matchingRows["attributeKind"] == "_field"].copy()
		dataframeTarget["listTupleAttributes"] = matchingRows_listTupleAttributes.drop_duplicates(subset="attribute")[["attribute", "type_ast_expr"]].apply(tuple, axis="columns").tolist()

		matchingRows["attribute"] = pandas.Categorical(matchingRows["attribute"], categories=matchingRows["match_args"].iloc[0], ordered=True)

		matchingRows_listCall_keyword: pandas.DataFrame = matchingRows[matchingRows["move2keywordArguments"] != "No"].copy(deep=True)
		matchingRows = matchingRows[matchingRows["move2keywordArguments"] == False].sort_values("attribute")  # noqa: E712
		matchingRows_listDefaults = matchingRows[matchingRows["defaultValue"] != "No"].copy(deep=True)

		dataframeTarget["listFunctionDef_args"] = matchingRows.drop_duplicates(subset="attribute")["ast_arg"].tolist()
		dataframeTarget["listDefaults"] = matchingRows_listDefaults.drop_duplicates(subset="attribute")["defaultValue"].tolist()

		matchingRows_listCall_keyword = matchingRows_listCall_keyword[matchingRows_listCall_keyword["move2keywordArguments"] != "Unpack"].drop_duplicates(subset="attribute").sort_values("attribute")

		def make_keyword(thisIsNotA_row: pandas.DataFrame) -> Any:
			if cast("bool", thisIsNotA_row["move2keywordArguments"]):
				keywordValue: ast.expr = cast("ast.expr", thisIsNotA_row["defaultValue"])
			else:
				keywordValue = Make.Name(cast("str", thisIsNotA_row["attributeRename"]))
				if thisIsNotA_row["list2Sequence"] is True:
					keywordValue = Make.Call(Make.Name("list"), [keywordValue])
			return Make.keyword(cast("str", thisIsNotA_row["attribute"]), keywordValue)

		matchingRows_listCall_keyword["Call_keyword"] = matchingRows_listCall_keyword.apply(make_keyword, axis="columns")
		dataframeTarget["listCall_keyword"] = matchingRows_listCall_keyword["Call_keyword"].tolist()

		return (
			dataframeTarget["listFunctionDef_args"],
			dataframeTarget["listDefaults"],
			dataframeTarget["listCall_keyword"],
			dataframeTarget["listTupleAttributes"],
		)

	dataframe[["listFunctionDef_args", "listDefaults", "listCall_keyword", "listTupleAttributes"]] = dataframe.apply(make3Columns4ClassMake, axis="columns", result_type="expand")

	dataframe.to_pickle(settingsManufacturing.pathFilenameDataframeAST)

if __name__ == "__main__":
	updateDataframe()
