"""AST dataframe manufacturing assembly line.

(AI generated docstring)

This module is the executor for manufacturing the authoritative AST dataframe used by
`astToolFactory`. The public entry point `updateDataframe` builds a base dataframe from source
material, applies selector-based policy decisions from
`astToolFactory.datacenter._dataframeUpdateAnnex`, computes derived columns required for code
generation, aggregates per-class lists, and persists the final dataframe.

Selector-based updates are expressed as mappings from a `SelectorSpecification` to a `column__value`.
A selector specification is a `NamedTuple` whose field names are dataframe columns and whose values
are the required cell values for a row to match. `getSelectorFromSpecification` turns that
specification into a boolean row selector, and `dictionaryToUpdateDataframe` applies the resulting
assignment.

"""
from __future__ import annotations

#=SIN= ast classes evaluated during runtime.
#pyright: reportUnusedImport=false
from annotationlib import Format, get_annotations
from ast import (
	alias, arg, arguments, Attribute, boolop, cmpop, comprehension, ExceptHandler, expr, expr_context, Interpolation, keyword, match_case,
	Name, operator, pattern, stmt, Subscript, TemplateStr, type_param, TypeIgnore, unaryop, withitem)
from astToolFactory import Column__ClassDefIdentifier_attribute, column__value, noMinimum, settingsManufacturing, settingsPackage
from astToolFactory.cpython import getDictionary_match_args
from astToolFactory.datacenter._dataframeUpdateAnnex import (
	_columns, attributeRename__, attributeType__ClassDefIdentifier_attribute, defaultValue__,
	dictionary_defaultValue_ast_arg_Call_keyword_orElse, move2keywordArguments__)
from astToolFactory.filesystem import gatherObjects, writeDataframe
from astToolkit import (
	ast_attributes, ast_attributes_int, ast_attributes_type_comment, Be, DOT, IfThis, Make, NodeChanger, NodeTourist, Then)
from astToolkit.changeDef import makeDictionaryClassDef
from astToolkit.filesystem import parsePathFilename2astModule
from astToolkit.ohWow import pythonCode2ast_expr
from collections.abc import Mapping
from functools import cache
from hunterMakesPy import raiseIfNone
from itertools import repeat
from operator import attrgetter
from typing import cast, TYPE_CHECKING, TypeIs
import ast
import builtins
import polars
import typeshed_client

if TYPE_CHECKING:
	from astToolFactory import Column__attribute, SelectorSpecification
	from collections.abc import Callable
	from pathlib import Path
	from polars.datatypes import DataTypeClass

# TODO `Make.Break`, `Make.Continue`, and `Make.Pass` are missing `**keywordArguments: Unpack[ast_attributes]`.

#======== HARDCODED values. TODO: eliminate ======================

_attributeTypeVarHARDCODED: str = '_EndPositionT'

#======== ast Functions ==========================================

@cache
def _get_astModule_astStub() -> ast.Module:
	"""Parse the `ast.pyi` stub file from typeshed.

	(AI generated docstring)

	Retrieves and parses the official `ast` module stub from the typeshed
	repository. This parsed AST serves as the Single Source of Truth for
	the structure of AST nodes across Python versions.

	The result is cached to avoid repeated filesystem I/O and parsing.

	Returns
	-------
	module : ast.Module
		The parsed AST of the `ast.pyi` file.

	"""
	ImaSearchContext: typeshed_client.SearchContext = typeshed_client.get_search_context(typeshed=settingsManufacturing.pathRoot_typeshed)
	return parsePathFilename2astModule(raiseIfNone(typeshed_client.get_stub_file('ast', search_context=ImaSearchContext)))

def _make_astAttribute(ClassDefIdentifier: str) -> ast.expr:
	"""Construct an `ast.Attribute` expression for a class name.

	(AI generated docstring)

	Creates an AST node representing `ast.ClassName` (e.g., `ast.FunctionDef`).
	This is used when generating code that needs to reference AST classes.

	Parameters
	----------
	ClassDefIdentifier : str
		The name of the AST class (e.g., `'FunctionDef'`).

	Returns
	-------
	node : ast.expr
		An expression node representing `ast.ClassDefIdentifier`.

	"""
	return Make.Attribute(Make.Name('ast'), ClassDefIdentifier)

def _make_keywordOrList(attributePROXY: dict[str, str | bool | ast.expr]) -> ast.keyword:
	"""Construct an `ast.keyword` for an argument with a default fallback.

	(AI generated docstring)

	Helper function for `_fixMutable_defaultValue`. It creates a keyword
	argument node where the value is conditionally handled:
	- If `list2Sequence` is `True`, it wraps the value in a `list()` call when the value is
		not the sentinel.
	- It uses an `orElse` expression (sentinel pattern) to handle defaults.

	Parameters
	----------
	attributePROXY : dict[str, str | bool | ast.expr]
		A dictionary containing details about the attribute ('attributeRename',
		'list2Sequence', 'orElse', 'attribute').

	Returns
	-------
	node : ast.keyword
		The constructed keyword argument AST node.

	"""
	keywordValue: ast.expr = Make.Name(cast('str', attributePROXY['attributeRename']))
	if attributePROXY['list2Sequence'] is True:
		keywordValue = Make.IfExp(test=keywordValue, body=Make.Call(Make.Name('list'), [keywordValue]), orElse=cast('ast.expr', attributePROXY['orElse']))
	else:
		keywordValue = Make.Or.join([keywordValue, cast('ast.expr', attributePROXY['orElse'])])
	return Make.keyword(cast('str', attributePROXY['attribute']), keywordValue)

def _makeDictionaryAnnotations(astClassDef: ast.ClassDef) -> dict[str, str]:
	"""Extract attribute type annotations from a class definition.

	(AI generated docstring)

	Parses a `ClassDef` node (typically `_Attributes` from the stub file) to
	extract variable annotations (`AnnAssign`). It also resolves `TypeVar`
	defaults to concrete types to ensure the extracted types are usable.

	Parameters
	----------
	astClassDef : ast.ClassDef
		The class definition node to parse.

	Returns
	-------
	dictionary_Attributes : dict[str, str]
		A dictionary mapping attribute names to their unparsed type strings.

	"""
	dictionary_Attributes: dict[str, str] = {}

	namespace: str = 'typing_extensions'
	identifier: str = 'TypeVar'
	ast_keyword: ast.keyword = raiseIfNone(NodeTourist[ast.Call, ast.keyword | None](
		findThis=Be.Call.funcIs(IfThis.isAttributeNamespaceIdentifier(namespace, identifier))
		, doThat=NodeTourist[ast.keyword, ast.keyword](
			findThis=IfThis.is_keywordIdentifier('default')
			, doThat=cast('Callable[[ast.keyword], ast.keyword]', Then.extractIt)
		).captureLastMatch
	).captureLastMatch(_get_astModule_astStub()))

	_attributeTypeVar_default: str = ast.unparse(ast_keyword.value)  # ruff: ignore[used-dummy-variable]

	NodeTourist[ast.AnnAssign, Mapping[str, str]](findThis=Be.AnnAssign.targetIs(Be.Name)
		, doThat=Then.updateKeyValueIn(key=lambda node: cast('ast.Name', node.target).id
			, value=lambda node: ast.unparse(node.annotation)
			, dictionary=dictionary_Attributes)
	).visit(astClassDef)

	for _attribute in dictionary_Attributes:  # ruff: ignore[used-dummy-variable]
		_attributeTypeVar: str = _attributeTypeVarHARDCODED  # ruff: ignore[used-dummy-variable]
		dictionary_Attributes[_attribute] = dictionary_Attributes[_attribute].replace(_attributeTypeVar, _attributeTypeVar_default)
	return dictionary_Attributes

#======== Dataframe functions =========================================

def _getDataFromInterpreter() -> polars.DataFrame:
	pathFilename: Path = settingsPackage.pathPackage / 'datacenter' / 'probeInterpreter.csv'
	dictionaryColumnTypeInterpreter: dict[str, DataTypeClass] = {
		'ClassDefIdentifier': polars.String,
		'versionMajorPythonInterpreter': polars.Int64,
		'versionMinorPythonInterpreter': polars.Int64,
		'versionMicroPythonInterpreter': polars.Int64,
		'base': polars.String,
	}
	return (polars.scan_csv(pathFilename, has_header=False, schema=dictionaryColumnTypeInterpreter)
		.unique(subset=['ClassDefIdentifier', 'versionMinorPythonInterpreter'], keep='last', maintain_order=True)
		.collect())

def _getDataFromPythonFiles(dataframe: polars.DataFrame) -> polars.DataFrame:
	"""Populate the dataframe with AST structure extracted from the `ast.pyi` stub and from low-level ASDL files.

	(AI generated docstring)

	This function parses the official `ast.pyi` stub file to establish the
	Single Source of Truth for AST class definitions. It identifies every
	class, its fields (via `match_args`), and its attributes (via the
	shadowy `_Attributes` TypedDict mechanism).

	See also `getDictionary_match_args` for extracting `match_args` from ASDL files.

	The function creates two types of rows for each class.
	1. `_field` is defined in `match_args` and represents a primary AST field.
	2. `_attribute` is defined via `_Attributes` and represents metadata like line numbers.

	Parameters
	----------
	dataframe : polars.DataFrame
		The initial dataframe containing `ClassDefIdentifier`s and versions.

	Returns
	-------
	dataframe : polars.DataFrame
		The dataframe expanded with rows for every field and attribute of
		every AST class, populated with type information and deprecation status.

	"""
	def amIDeprecated(ClassDefIdentifier: str) -> bool:
		"""Determine if an AST class is marked with the `@deprecated` decorator.

		(AI generated docstring)

		Parameters
		----------
		ClassDefIdentifier : str
			The name of the class to inspect.

		Returns
		-------
		isDeprecated : bool
			`True` if the class definition in the stub file has a decorator
			named `deprecated`, `False` otherwise.

		"""
		return bool(NodeTourist(IfThis.isCallIdentifier('deprecated'), doThat=Then.extractIt).captureLastMatch(dictionaryClassDef[ClassDefIdentifier]))


	def getThe_Attributes(ClassDefIdentifier: str) -> dict[str, str]:
		"""Extract the subset of `_Attributes` that a specific class adopts.

		(AI generated docstring)

		In the stub file, classes do not list `lineno` or `end_col_offset` directly.
		Instead, they inherit from a generic that unpacks a TypedDict named
		`_Attributes`. This function parses that unpacking logic.

		Parameters
		----------
		ClassDefIdentifier : str
			The name of the class to inspect.

		Returns
		-------
		the_Attributes : dict[str, str]
			A dictionary mapping attribute names (e.g., `lineno`) to their
			type strings, containing only those attributes applicable to this class.

		"""
		the_Attributes: dict[str, str] = {}
		_attribute_ast_expr: ast.expr | None = NodeTourist[ast.Subscript, ast.Name](  # ruff: ignore[used-dummy-variable]
			findThis=Be.Subscript.valueIs(IfThis.isNameIdentifier('Unpack'))
			, doThat=Then.extractIt(DOT.slice)
		).captureLastMatch(dictionaryClassDef[ClassDefIdentifier])

		if _attribute_ast_expr:
			_EndPositionT: ast.expr | None = NodeTourist[ast.Subscript, ast.expr](findThis=Be.Subscript, doThat=Then.extractIt(DOT.slice)).captureLastMatch(_attribute_ast_expr)  # ruff: ignore[used-dummy-variable]
			if _EndPositionT:
				the_Attributes = dict.fromkeys(dictionary_Attributes, ast.unparse(_EndPositionT))
			else:
				the_Attributes = dictionary_Attributes
		return the_Attributes


	def get_attributeType(dddataframeee: dict[str, str]) -> str:
		"""Resolve the type annotation of a field from the stub file.

		(AI generated docstring)

		This function acts as a resolver that goes back to the `ClassDef` in the
		parsed stub to find the specific `AnnAssign` for a field found in
		`match_args`. It qualifies AST classes with `ast` and replaces the
		private typeshed constant-value alias with `ast_ConstantValue`.

		Parameters
		----------
		dddataframeee : dict[str, str]
			The class identifier and attribute name whose annotation is required.

		Returns
		-------
		attributeType : str
			The string representation of the type annotation for the field.

		"""
		def findThis(node: ast.AST) -> TypeIs[Name]:
			return Be.Name(node) and (node.id == '_ConstantValue'
				or (node.id in vars(ast) and isinstance(getattr(ast, node.id), type) and issubclass(getattr(ast, node.id), ast.AST)))

		def doThat(node: ast.Name) -> ast.expr:
			if node.id == '_ConstantValue':
				return Make.Name('ast_ConstantValue')
			return Make.Attribute(Make.Name('ast'), node.id)
		dddataframeee['attributeType'] = ast.unparse(NodeChanger[ast.Name, ast.expr](findThis, doThat).visit(raiseIfNone(NodeTourist[ast.AnnAssign, ast.expr](
				findThis=Be.AnnAssign.targetIs(IfThis.isNameIdentifier(dddataframeee['attribute']))
				, doThat=Then.extractIt(DOT.annotation)
				).captureLastMatch(dictionaryClassDef[dddataframeee['ClassDefIdentifier']]))))

		dddataframeee['attributeType'] = dddataframeee['attributeType'].replace('builtins.str', 'str')
# https://github.com/python/cpython/issues/143661

		return dddataframeee['attributeType']

	dictionaryClassDef: dict[str, ast.ClassDef] = makeDictionaryClassDef(_get_astModule_astStub())
	dictionary_Attributes: dict[str, str] = _makeDictionaryAnnotations(dictionaryClassDef['_Attributes'])
	dataframeClass: polars.LazyFrame = polars.DataFrame({
		'ClassDefIdentifier': list(dictionaryClassDef),
		'deprecated': list(map(amIDeprecated, dictionaryClassDef)),
	}).lazy()
	dictionary_match_args = getDictionary_match_args()
	dataframe_match_args: polars.LazyFrame = polars.DataFrame(list(dictionary_match_args),
		schema=['ClassDefIdentifier', 'versionMinorPythonInterpreter', 'deprecated'], orient='row'
	).lazy().with_columns(polars.Series('match_args', dictionary_match_args.values(), dtype=polars.List(polars.String)))
	dataframe_match_args = dataframe_match_args.rename({'deprecated': 'deprecatedASDL'})
	dataframe = (dataframe.lazy().join(dataframeClass, on='ClassDefIdentifier', how='left', maintain_order='left')
		.join(dataframe_match_args, on=['ClassDefIdentifier', 'versionMinorPythonInterpreter'], how='left', maintain_order='left')
		.with_columns(polars.coalesce('deprecatedASDL', 'deprecated').alias('deprecated'),
			polars.col('match_args').fill_null(polars.lit([], dtype=polars.List(polars.String))))
		.drop('deprecatedASDL')
		.collect())
	"""NOTE deprecated classes are not defined in asdl and they do not have match_args in ast.pyi. The match_args values in the dataframe
	for deprecated classes were created manually. If the dataframe were reset or eliminated, there is not currently a process to
	recreate the match_args for deprecated classes."""

	attributeType__ClassDefIdentifier_attribute: dict[Column__ClassDefIdentifier_attribute, column__value] = {
		Column__ClassDefIdentifier_attribute(ClassDefIdentifier, attribute)
		: column__value(column='attributeType', value=attributeType)
			for ClassDefIdentifier in dataframe['ClassDefIdentifier'].unique(maintain_order=True)
				for attribute, attributeType in getThe_Attributes(ClassDefIdentifier).items()
	}
	dataframeAttributes: polars.LazyFrame = polars.DataFrame(list(attributeType__ClassDefIdentifier_attribute),
		schema=['ClassDefIdentifier', 'attribute'], orient='row'
	).lazy().with_columns(polars.Series('attributeTypeMetadata',
		map(attrgetter('value'), attributeType__ClassDefIdentifier_attribute.values()), dtype=polars.String))
	dataframeFields: polars.DataFrame = (dataframe.lazy().select('ClassDefIdentifier', polars.col('match_args').alias('attribute'))
		.explode('attribute', empty_as_null=False).unique(maintain_order=True).collect())
	dataframeFields = dataframeFields.lazy().with_columns(polars.Series('attributeTypeField',
		map(get_attributeType, dataframeFields.to_dicts()), dtype=polars.String)).collect()
	return (dataframe.lazy()
		.join(dataframeAttributes.group_by('ClassDefIdentifier').agg(polars.col('attribute').alias('attributes')),
			on='ClassDefIdentifier', how='left', maintain_order='left')
		.join(polars.LazyFrame({'attributeKind': ['No', '_field', '_attribute']}), how='cross', maintain_order='left')
		.with_columns(polars.when(polars.col('attributeKind') == '_field').then(polars.col('match_args'))
			.when(polars.col('attributeKind') == '_attribute').then(polars.col('attributes'))
			.otherwise(polars.lit(['No'])).alias('attribute'))
		.explode('attribute', empty_as_null=False, keep_nulls=False)
		.join(dataframeFields.lazy(), on=['ClassDefIdentifier', 'attribute'], how='left', maintain_order='left')
		.join(dataframeAttributes, on=['ClassDefIdentifier', 'attribute'], how='left', maintain_order='left')
		.with_columns(polars.when(polars.col('attributeKind') == '_field').then(polars.col('attributeTypeField'))
			.when(polars.col('attributeKind') == '_attribute').then(polars.col('attributeTypeMetadata'))
			.otherwise(polars.lit('No')).alias('attributeType'))
		.drop('attributes', 'attributeTypeField', 'attributeTypeMetadata')
		.collect())

def _fixMutable_defaultValue(dataframe: polars.DataFrame) -> polars.DataFrame:
	"""Implement the sentinel pattern for mutable default values.

	(AI generated docstring)

	Python forbids mutable default arguments. This function identifies attributes
	that require mutable defaults (like lists) and transforms them to use the
	`None` sentinel pattern.

	For matching attributes:
	1. Sets the signature default to `None`.
	2. Updates the type annotation to allow `None` (e.g., `list[X] | None`).
	3. Updates the `ast_arg` node to reflect these changes.
	4. Updates `Call_keyword` to use logic that swaps `None` for the mutable factory.

	It uses `dictionary_defaultValue_ast_arg_Call_keyword_orElse` to look up
	the appropriate factory expression (e.g., `[]`, `ast.Load()`).

	Parameters
	----------
	dataframe : polars.DataFrame
		The dataframe to transform.

	Returns
	-------
	dataframe : polars.DataFrame
		The dataframe with updated defaults and arguments for mutable types.

	"""
	dictionary: dict[Column__attribute | Column__ClassDefIdentifier_attribute, column__value] = dict(zip(
		dictionary_defaultValue_ast_arg_Call_keyword_orElse,
		map(column__value, repeat('orElse'), dictionary_defaultValue_ast_arg_Call_keyword_orElse.values()),
		strict=True,
	))
	dataframe = dictionaryToUpdateDataframe(dictionary,
		dataframe.lazy().with_columns(polars.lit(None, dtype=polars.Object).alias('orElse')).collect())
	dataframeMutable: polars.DataFrame = (dataframe.lazy().with_row_index('rowIndex')
		.filter(polars.col('orElse').is_not_null())
		.with_columns((polars.when(polars.col('list2Sequence'))
			.then(polars.col('attributeType').str.replace_all('list', 'Sequence', literal=True))
			.otherwise(polars.col('attributeType')) + ' | None').alias('attributeType')).collect())
	dataframeMutable = dataframeMutable.lazy().with_columns(polars.Series('type_ast_expr',
		map(pythonCode2ast_expr, dataframeMutable['attributeType']), dtype=polars.Object)).collect()
	dataframeMutable = dataframeMutable.lazy().with_columns(
		polars.Series('ast_argMutable', map(Make.arg, dataframeMutable['attributeRename'], dataframeMutable['type_ast_expr'], strict=True), dtype=polars.Object),
		polars.Series('Call_keywordMutable', map(_make_keywordOrList, dataframeMutable.to_dicts()), dtype=polars.Object),
	).collect()
	return (dataframe.lazy().with_row_index('rowIndex')
		.join(dataframeMutable.lazy().select('rowIndex', 'ast_argMutable', 'Call_keywordMutable'),
			on='rowIndex', how='left', maintain_order='left')
		.with_columns(
			polars.when(polars.col('orElse').is_not_null()).then(polars.lit(Make.Constant(None), allow_object=True))
				.otherwise(polars.col('defaultValue')).alias('defaultValue'),
			polars.when(polars.col('orElse').is_not_null()).then(polars.col('ast_argMutable'))
				.otherwise(polars.col('ast_arg')).alias('ast_arg'),
			polars.when(polars.col('orElse').is_not_null()).then(polars.col('Call_keywordMutable'))
				.otherwise(polars.col('Call_keyword')).alias('Call_keyword'),
		).drop('rowIndex', 'orElse', 'ast_argMutable', 'Call_keywordMutable').collect())

def _makeColumn_ast_arg(dataframe: polars.DataFrame) -> polars.DataFrame:
	"""Generate `ast.arg` nodes for function signatures using prepared types.

	(AI generated docstring)

	This function is the **Usage Step** in the type processing assembly line.
	It constructs the actual AST nodes representing function arguments (`ast.arg`)
	that will be used to generate code (e.g., `_toolGrab.py`).

	It relies on `attributeRename` for the argument name and `type_ast_expr`
	(created by `_makeColumn_type_ast_expr`) for the type annotation. This separation
	ensures that complex type logic (like covariance and special string handling)
	is resolved before this function simply assembles the components.

	If an attribute is marked `move2keywordArguments` (e.g., it belongs in a
	`TypedDict` or is `Unpack`ed), no individual `ast.arg` is created.

	Parameters
	----------
	dataframe : polars.DataFrame
		The dataframe containing attribute names and their corresponding
		AST-based type expressions.

	Returns
	-------
	dataframe : polars.DataFrame
		The dataframe with a new column `ast_arg`, containing `ast.arg` nodes
		or null if the attribute is handled via keyword arguments.

	See Also
	--------
	`_makeColumn_type_ast_expr` : The **Type Construction Step** that builds
		the `type_ast_expr` used here.

	"""
	dataframeArguments: polars.DataFrame = (dataframe.lazy().with_row_index('rowIndex')
		.filter(polars.col('move2keywordArguments') == 'False')
		.select('rowIndex', 'attributeRename', 'type_ast_expr').collect())
	dataframeArguments = dataframeArguments.lazy().with_columns(polars.Series('ast_arg',
		map(Make.arg, dataframeArguments['attributeRename'], dataframeArguments['type_ast_expr'], strict=True), dtype=polars.Object)).collect()
	return (dataframe.lazy().with_row_index('rowIndex').join(dataframeArguments.lazy().select('rowIndex', 'ast_arg'),
		on='rowIndex', how='left', maintain_order='left').drop('rowIndex').collect())

def _makeColumn_kwarg_annotationIdentifier(dataframe: polars.DataFrame) -> polars.DataFrame:
	list_byColumns: list[str] = ['ClassDefIdentifier', 'versionMinorPythonInterpreter']
	dataframeAnnotations: polars.LazyFrame = (polars.DataFrame([
		get_annotations(ast_attributes, format=Format.STRING),
		get_annotations(ast_attributes_int, format=Format.STRING),
		get_annotations(ast_attributes_type_comment, format=Format.STRING),
		{},
	]).lazy().with_columns(polars.Series('kwarg_annotationIdentifier',
		['ast_attributes', 'ast_attributes_int', 'ast_attributes_type_comment', 'No']))
		.unpivot(index='kwarg_annotationIdentifier', variable_name='attributeRename', value_name='attributeType')
		.group_by('kwarg_annotationIdentifier').agg(polars.struct('attributeRename', 'attributeType')
			.filter(polars.col('attributeType').is_not_null()).unique().sort().alias('annotations')))
	dataframeKeywords: polars.LazyFrame = (dataframe.lazy().group_by(list_byColumns)
		.agg(polars.struct('attributeRename', 'attributeType')
			.filter((polars.col('attributeKind') == '_attribute') | (polars.col('move2keywordArguments') == 'Unpack'))
			.unique().sort().alias('annotations'))
		.join(dataframeAnnotations, on='annotations', how='left').drop('annotations'))
	return dataframe.lazy().join(dataframeKeywords, on=list_byColumns, how='left', maintain_order='left').collect()

def _makeColumn_list2Sequence(dataframe: polars.DataFrame) -> polars.DataFrame:
	"""Identify attributes that require `list` to `Sequence` covariance transformation.

	(AI generated docstring)

	This function is the **Decision Step** in the type processing assembly line.
	It tags attributes whose types are lists of AST nodes so that `astToolkit`
	can later treat them as covariant Sequences.

	In Python, `list` is mutable and therefore invariant. If `astToolkit`
	strictly used `list[ast.stmt]`, users could not pass a `list[ast.Assign]`
	(a subtype of `ast.stmt`) without upsetting type checkers. By identifying
	these attributes here, we enable downstream functions like
	`_makeColumn_type_ast_expr` to generate type signatures using `Sequence`,
	allowing covariance (safe read-only access) where appropriate.

	The function uses a vectorized regular expression scan to identify
	attributes whose types involve `list` containing any of the superclasses
	defined in `settingsManufacturing.astSuperClasses`.

	Parameters
	----------
	dataframe : polars.DataFrame
		The dataframe containing attribute type definitions to analyze.

	Returns
	-------
	dataframe : polars.DataFrame
		The dataframe with a new boolean column `list2Sequence`, set to `True`
		for attributes that match the covariant transformation criteria.

	See Also
	--------
	`_makeColumn_type_ast_expr` : The **Type Construction Step** that uses this
		decision to modify type expressions.
	`_makeColumn_ast_arg` : The **Usage Step** that uses those expressions to
		build function arguments.

	"""
	return dataframe.lazy().with_columns((polars.col('attributeType').str.contains('list', literal=True)
		& polars.col('attributeType').str.contains('|'.join(settingsManufacturing.astSuperClasses)))
		.alias('list2Sequence')).collect()

def _makeColumn_type_ast_expr(dataframe: polars.DataFrame) -> polars.DataFrame:
	"""Convert type strings into AST expressions, applying covariance logic.

	(AI generated docstring)

	This function is the **Type Construction Step** in the type processing
	assembly line. It transforms the raw string representation of a type (from
	the stub file) into a manipulatable AST expression (`ast.expr`).

	It acts on the decision made by `_makeColumn_list2Sequence`:
	- If `list2Sequence` is `True`, it replaces `list` with `Sequence` in the
		type string before parsing.
	- Otherwise, it parses the type string as-is.

	It also cleans up specific oddities, such as replacing the simple string
	`'str'` with a fully qualified `builtins.str` to avoid conflicts with
	Python's `ast.Str` (deprecated) or interpolation issues.

	Parameters
	----------
	dataframe : polars.DataFrame
		The dataframe containing raw type strings (`attributeType`) and the
		covariance flags (`list2Sequence`).

	Returns
	-------
	dataframe : polars.DataFrame
		The dataframe with a new column `type_ast_expr`, containing the `ast.expr`
		representation of the attribute's type.

	See Also
	--------
	`_makeColumn_list2Sequence` : The **Decision Step** that flags which rows
		need the `list` -> `Sequence` replacement used here.
	`_makeColumn_ast_arg` : The **Usage Step** that consumes these AST expressions.

	"""
	dataframeTypes: polars.DataFrame = dataframe.lazy().select(polars.when(polars.col('attribute') == 'str')
		.then(polars.lit('builtins.str'))
		.when(polars.col('list2Sequence')).then(polars.col('attributeType').str.replace_all('list', 'Sequence', literal=True))
		.otherwise(polars.col('attributeType')).alias('attributeType')).collect()
	return dataframe.lazy().with_columns(polars.Series('type_ast_expr',
		map(pythonCode2ast_expr, dataframeTypes['attributeType']), dtype=polars.Object)).collect()

def _makeColumnCall_keyword(dataframe: polars.DataFrame) -> polars.DataFrame:
	"""Generate `ast.keyword` nodes for constructor calls; these are used in the call to `ast` not in `Make`.

	(AI generated docstring)

	This function constructs the keyword arguments used when instantiating
	AST nodes. It handles normal fields and special cases like lists (which
	may need to be explicitly cast to `list` if the input is a generic
	Sequence).

	Attributes marked with `move2keywordArguments` that are not 'Unpack'
	are treated as keyword-only arguments using their default values.

	Parameters
	----------
	dataframe : polars.DataFrame
		The dataframe with `attributeRename`, `list2Sequence`, and `defaultValue`.

	Returns
	-------
	dataframe : polars.DataFrame
		The dataframe with a new column `Call_keyword`.

	"""
	def make_ast_keywordWith_defaultValue(attribute: str, defaultValue: ast.expr) -> ast.keyword:
		return Make.keyword(attribute, defaultValue)

	def make_ast_keywordFrom_attributeRename(parameters: tuple[str, str, bool]) -> ast.keyword:
		attribute, attributeRename, list2Sequence = parameters
		keywordValue: ast.expr = Make.Name(attributeRename)
		if list2Sequence:
			keywordValue = Make.Call(Make.Name('list'), [keywordValue])
		return Make.keyword(attribute, keywordValue)

	dataframeKeywords: polars.DataFrame = (dataframe.lazy().with_row_index('rowIndex')
		.filter(polars.col('attributeKind') == '_field', ~polars.col('move2keywordArguments').is_in(['No', 'Unpack']))
		.select('rowIndex', 'attribute', 'attributeRename', 'list2Sequence', 'defaultValue', 'move2keywordArguments').collect())
	dataframeDefaults: polars.DataFrame = dataframeKeywords.lazy().filter(polars.col('move2keywordArguments') == 'True').collect()
	dataframeNames: polars.DataFrame = dataframeKeywords.lazy().filter(polars.col('move2keywordArguments') != 'True').collect()
	dataframeDefaults = dataframeDefaults.lazy().with_columns(polars.Series('Call_keyword_default',
		map(make_ast_keywordWith_defaultValue, dataframeDefaults['attribute'], dataframeDefaults['defaultValue'], strict=True), dtype=polars.Object)).collect()
	dataframeNames = dataframeNames.lazy().with_columns(polars.Series('Call_keyword_name',
		map(make_ast_keywordFrom_attributeRename, zip(dataframeNames['attribute'], dataframeNames['attributeRename'],
			dataframeNames['list2Sequence'], strict=True)), dtype=polars.Object)).collect()
	return (dataframe.lazy().with_row_index('rowIndex')
		.join(dataframeDefaults.lazy().select('rowIndex', 'Call_keyword_default'), on='rowIndex', how='left', maintain_order='left')
		.join(dataframeNames.lazy().select('rowIndex', 'Call_keyword_name'), on='rowIndex', how='left', maintain_order='left')
		.with_columns(polars.when(polars.col('move2keywordArguments') == 'True').then(polars.col('Call_keyword_default'))
			.otherwise(polars.col('Call_keyword_name')).alias('Call_keyword'))
		.drop('rowIndex', 'Call_keyword_default', 'Call_keyword_name').collect())

def _makeColumn_list4TypeAlias(dataframe: polars.DataFrame) -> polars.DataFrame:
	"""Pre-compute the constituent AST elements for every TypeAlias variant.

	(AI generated docstring)

	This function is a **Pre-computation Step**. Because `_dataServer` cannot
	perform heavy computation at runtime, this function calculates the precise
	list of AST nodes (as `ast.expr` objects) that define each TypeAlias for
	every possible version state recorded in the dataframe.

	It iterates through the dataframe and, for each row, snapshots the
	cumulative union of types available to that TypeAlias up to that row's
	version. This allows `_dataServer` to simply select the correct
	pre-computed list rather than reconstructing it.

	Parameters
	----------
	dataframe : polars.DataFrame
		The dataframe containing `TypeAlias_hasDOTSubcategory` and version
		information.

	Returns
	-------
	dataframe : polars.DataFrame
		The dataframe populated with `list4TypeAlias_value` (the list of AST
		expressions) and `hashable_list4TypeAlias_value` (for efficient
		groupings).

	"""
	dataframe = _makeColumnsVersionMinimum(dataframe, ['ClassDefIdentifier', 'attribute'], 'versionMinorMinimumAttribute')
	list_byColumns: list[str] = ['TypeAlias_hasDOTSubcategory', 'versionMinorMinimumAttribute']
	dataframeVariants: polars.LazyFrame = (dataframe.lazy().filter(polars.col('attributeKind') == '_field')
		.select(list_byColumns).unique(maintain_order=True))
	dataframeMembers: polars.LazyFrame = (dataframe.lazy().with_row_index('rowIndex')
		.filter(polars.col('attributeKind') == '_field', ~polars.col('deprecated'))
		.select('TypeAlias_hasDOTSubcategory', 'ClassDefIdentifier', 'rowIndex',
			polars.col('versionMinorMinimumAttribute').alias('versionAvailable')))
	dataframeLists: polars.DataFrame = (dataframeVariants
		.join(dataframeMembers, on='TypeAlias_hasDOTSubcategory', how='left')
		.filter(polars.col('versionAvailable') <= polars.col('versionMinorMinimumAttribute'))
		.unique(subset=[*list_byColumns, 'ClassDefIdentifier'], keep='first', maintain_order=True)
		.sort(polars.col('ClassDefIdentifier').str.to_lowercase(), maintain_order=True)
		.group_by(list_byColumns).agg(polars.col('rowIndex').alias('indices'),
			polars.format('[{}]', polars.format("'{}'", polars.col('ClassDefIdentifier')).str.join(', '))
				.alias('hashable_list4TypeAlias_value'))
		.join(dataframeVariants, on=list_byColumns, how='right')
		.with_columns(polars.col('indices').fill_null(polars.lit([], dtype=polars.List(polars.UInt32))),
			polars.col('hashable_list4TypeAlias_value').fill_null('[]'))
		.collect())
	dataframeLists = dataframeLists.lazy().with_columns(gatherObjects(dataframe['classAs_astAttribute'], dataframeLists['indices'])
		.rename('list4TypeAlias_value')).collect()
	return (dataframe.lazy().join(dataframeLists.lazy().drop('indices'), on=list_byColumns, how='left', maintain_order='left').collect())

def _makeColumn_list4TypeAliasSubcategories(dataframe: polars.DataFrame) -> polars.DataFrame:
	"""Aggregate all possible subcategory identifiers for each TypeAlias.

	(AI generated docstring)

	This function is a **Pre-computation Step**. While
	`_makeColumn_list4TypeAlias` computes the *content* of each alias, this
	function computes the *set of variants* available for a given attribute.

	It generates a list of `ast.Name` nodes representing every subcategory
	(e.g., `['Context_3_8', 'Context_3_12']`) associated with an attribute.
	This list is attached to the dataframe, enabling `_dataServer` to see the
	full menu of available versions for guarding logic.

	Parameters
	----------
	dataframe : polars.DataFrame
		The dataframe containing `TypeAlias_hasDOTSubcategory`.

	Returns
	-------
	dataframe : polars.DataFrame
		The dataframe with a new column `list4TypeAliasSubcategories`
		containing lists of possible variant names.

	"""
	dataframeNames: polars.DataFrame = (dataframe.lazy()
		.filter(polars.col('attributeKind') == '_field', ~polars.col('deprecated'), polars.col('TypeAlias_hasDOTSubcategory') != 'No')
		.select('attribute', 'TypeAlias_hasDOTSubcategory').unique(maintain_order=True)
		.sort(polars.col('TypeAlias_hasDOTSubcategory').str.to_lowercase(), maintain_order=True).collect())
	dataframeNames = dataframeNames.lazy().with_columns(polars.Series('type_ast_expr',
		map(Make.Name, dataframeNames['TypeAlias_hasDOTSubcategory']), dtype=polars.Object)).collect()
	dataframeLists: polars.DataFrame = (dataframeNames.lazy().with_row_index('rowIndex')
		.group_by('attribute').agg(polars.col('rowIndex').alias('indices')).collect())
	dataframeLists = dataframeLists.lazy().with_columns(gatherObjects(dataframeNames['type_ast_expr'], dataframeLists['indices'])
		.rename('list4TypeAliasSubcategories')).collect()
	return (dataframe.lazy().join(dataframeLists.lazy().drop('indices'), on='attribute', how='left', maintain_order='left').collect())

def _makeColumnsFourLists(dataframe: polars.DataFrame) -> polars.DataFrame:
	"""Aggregate attributes into lists for class definitions and calls.

	(AI generated docstring)

	This function is an **Aggregation Step**. It groups rows by `ClassDefIdentifier`
	and version, then compiles lists of attributes, arguments, defaults, and
	keywords for each group. These lists are essentially "pre-baked" structures
	ready for code generation templates (like `Call` nodes or `FunctionDef`
	args).

	It creates four columns:
	- `listTupleAttributes`: List of (name, type, minimum minor version) tuples for all fields.
	- `listFunctionDef_args`: List of `ast.arg` nodes for function signatures.
	- `listDefaults`: List of default values for those arguments.
	- `listCall_keyword`: List of `ast.keyword` nodes for constructor calls.

	Parameters
	----------
	dataframe : polars.DataFrame
		The dataframe containing individual attribute rows.

	Returns
	-------
	dataframe : polars.DataFrame
		The dataframe updated with columns containing aggregated lists.

	"""
	list_byColumns: list[str] = ['ClassDefIdentifier', 'versionMinorMinimum_match_args']
	dataframeOrder: polars.LazyFrame = (dataframe.lazy().select(*list_byColumns, 'match_args')
		.unique(subset=list_byColumns, maintain_order=True)
		.select(*list_byColumns, polars.col('match_args').alias('attribute'),
			polars.int_ranges(0, polars.col('match_args').list.len()).alias('attributeIndex'))
		.explode('attribute', 'attributeIndex', empty_as_null=False))
	dataframeFields: polars.LazyFrame = (dataframe.lazy().with_row_index('rowIndex')
		.filter(polars.col('attributeKind') == '_field')
		.join(dataframeOrder, on=[*list_byColumns, 'attribute'], how='left', maintain_order='left')
		.sort('attributeIndex', 'versionMinorMinimum_match_args', descending=[False, True], maintain_order=True)
		.unique(subset=[*list_byColumns, 'attribute'], keep='first', maintain_order=True))
	dataframeGroups: polars.DataFrame = (dataframeFields.group_by(list_byColumns).agg(
		polars.col('rowIndex').alias('indicesAttributes'),
		polars.col('rowIndex').filter(polars.col('move2keywordArguments') == 'False').alias('indices_ast_arg'),
		polars.col('rowIndex').filter(polars.col('defaultValue').is_not_null(),
			polars.col('move2keywordArguments') == 'False').alias('indicesDefaults'),
		polars.col('rowIndex').filter(~polars.col('move2keywordArguments').is_in(['No', 'Unpack'])).alias('indices_keyword'),
	).join(dataframe.lazy().select(list_byColumns).unique(maintain_order=True), on=list_byColumns, how='right')
		.with_columns(polars.col('indicesAttributes', 'indices_ast_arg', 'indicesDefaults', 'indices_keyword')
			.fill_null(polars.lit([], dtype=polars.List(polars.UInt32))))
		.collect())
	dataframeGroups = dataframeGroups.lazy().with_columns(
		gatherObjects(polars.Series(dataframe.lazy().select('attribute', 'type_ast_expr', 'versionMinorMinimumAttribute').collect().rows(), dtype=polars.Object),
			dataframeGroups['indicesAttributes']).rename('listTupleAttributes'),
		gatherObjects(dataframe['ast_arg'], dataframeGroups['indices_ast_arg']).rename('listFunctionDef_args'),
		gatherObjects(dataframe['defaultValue'], dataframeGroups['indicesDefaults']).rename('listDefaults'),
		gatherObjects(dataframe['Call_keyword'], dataframeGroups['indices_keyword']).rename('listCall_keyword'),
	).collect()
	return (dataframe.lazy().join(dataframeGroups.lazy().drop('indicesAttributes', 'indices_ast_arg', 'indicesDefaults', 'indices_keyword'),
		on=list_byColumns, how='left', maintain_order='left').collect())

def _makeColumnTypeAlias_hasDOTSubcategory(dataframe: polars.DataFrame) -> polars.DataFrame:
	"""Construct unique identifiers for TypeAlias sub-variants based on type signatures.

	(AI generated docstring)

	This function is a **Pre-computation Step**. When a TypeAlias definition
	evolves across Python versions (e.g., gaining or losing members), simple
	names are insufficient. This function generates a deterministic,
	descriptive string (the 'subcategory') derived from the raw type signature
	(e.g., `A | B` becomes `A_Or_B`).

	These subcategory identifiers allow downstream functions to group and
	process specific versions of a TypeAlias isolated from others.

	Parameters
	----------
	dataframe : polars.DataFrame
		The dataframe containing `TypeAlias_hasDOTIdentifier` and raw
		`attributeType` strings.

	Returns
	-------
	dataframe : polars.DataFrame
		The dataframe with a new column `TypeAlias_hasDOTSubcategory`
		containing the generated identifiers.

	"""
	return dataframe.lazy().with_columns(polars.when(polars.col('TypeAlias_hasDOTIdentifier') != 'No')
		.then(polars.col('TypeAlias_hasDOTIdentifier') + '_' + polars.col('attributeType')
			.str.replace_all('|', 'Or', literal=True).str.replace_all('[', '_', literal=True)
			.str.replace_all('[\\] ]', '').str.replace_all('ast.', '', literal=True))
		.otherwise(polars.lit('No')).alias('TypeAlias_hasDOTSubcategory')).collect()

def _makeColumnsVersionMinimum(dataframe: polars.DataFrame, list_byColumns: list[str], columnNameTarget: str) -> polars.DataFrame:
	"""Calculate the minimum Python version required for a feature.

	(AI generated docstring)

	This function determines the lowest supported Python version for a specific
	set of columns (e.g., a class or an attribute) and records it in a new column.

	If the calculated minimum version matches `settingsManufacturing.versionMinor_astMinimumSupported`
	(the baseline supported version), the result is set to `noMinimum`.
	This optimization avoids generating unnecessary version guards for features
	that are available in all supported versions.

	Parameters
	----------
	dataframe : polars.DataFrame
		The dataframe to process.
	list_byColumns : list[str]
		List of column names to group by (identifying the feature).
	columnNameTarget : str
		Name of the new column to be created with the minimum version.

	Returns
	-------
	dataframe : polars.DataFrame
		The dataframe with the new minimum version column.

	"""
	versionMinimum: polars.Expr = polars.col('versionMinorPythonInterpreter').min().over(list_byColumns)
	return dataframe.lazy().with_columns(polars.when(versionMinimum == settingsManufacturing.versionMinor_astMinimumSupported)
		.then(noMinimum).otherwise(versionMinimum).alias(columnNameTarget)).collect()

def dictionaryToUpdateDataframe(dictionary: Mapping[SelectorSpecification, column__value], dataframe: polars.DataFrame) -> polars.DataFrame:
	"""Apply a selector-to-assignment dictionary to update dataframe cells.

	(AI generated docstring)

	This function is the executor of the selector-based dataframe update system. It
	iterates over each key-value pair in the dictionary, converts the key (a selector
	specification) to a boolean row selector, and assigns the value from `column__value`
	to the appropriate column for those rows.

	The function modifies existing cells but does not create new rows or columns.

	Parameters
	----------
	dictionary : Mapping[SelectorSpecification, column__value]
		Mapping from selector specifications to assignment tuples. Each selector
		specification selects rows by matching column values. Each `column__value` specifies the target
		column and the value to assign.
	dataframe : polars.DataFrame
		Dataframe to update.

	Returns
	-------
	dataframe : polars.DataFrame
		The dataframe with all assignments applied. Later matching assignments take precedence.

	See Also
	--------
	`getSelectorFromSpecification` : Converts a selector specification to a boolean `polars.Expr`.
	`astToolFactory.datacenter._dataframeUpdateAnnex` : Module docstring explains
		the complete selector-based dataframe update system.

	"""
	assignments: dict[str, polars.Expr] = {}
	for specifiedColumnsAndValues, assign in dictionary.items():
		assignments[assign.column] = (polars.when(getSelectorFromSpecification(specifiedColumnsAndValues))
			.then(polars.lit(assign.value, allow_object=True))
			.otherwise(assignments.get(assign.column, polars.col(assign.column))).alias(assign.column))
	return dataframe.lazy().with_columns(*assignments.values()).collect()

def getSelectorFromSpecification(specifiedColumnsAndValues: SelectorSpecification) -> polars.Expr:
	"""Convert a selector specification to a boolean row selector for a dataframe.

	(AI generated docstring)

	This function translates the declarative selector specification into an executable boolean
	`polars.Expr`. Each field in the tuple becomes an equality test against the
	corresponding dataframe column. All tests are combined with logical AND, so a
	row is selected only if *all* field values match.

	Parameters
	----------
	specifiedColumnsAndValues : SelectorSpecification
		A `NamedTuple` whose field names are column names and whose field values
		are the values to match.

	Returns
	-------
	selector : polars.Expr
		Boolean expression selecting rows matching all conditions.

	See Also
	--------
	`dictionaryToUpdateDataframe` : Applies the selector to perform assignments.
	`astToolFactory.datacenter._dataframeUpdateAnnex` : Module docstring explains
		the complete selector-based dataframe update system.

	"""
	return polars.all_horizontal(polars.col(column) == value for column, value in specifiedColumnsAndValues._asdict().items())

def updateDataframe() -> None:
	"""Orchestrate the creation and population of the AST dataframe.

	(AI generated docstring)

	This is the main entry point for the "Data Center". It executes the full
	assembly line to manufacture the primary dataframe used by `astToolFactory`.

	The process involves these stages.
	1. **Instantiation** creates the base dataframe from allowed versions.
	2. **Extraction** collects authoritative data about class definitions and attributes.
	3. **Refinement** applies selector-based overrides (renames, defaults, and type fixes).
	4. **Computation** calculates derived columns (types, `ast.arg`, and `ast.keyword`).
	5. **Aggregation** groups per-class values into lists for template use.
	6. **Persistence** saves the result to a pickle file.

	The function prepares a new dataframe using this module's stages and
	`_dataframeUpdateAnnex` configuration dictionaries.

	"""
	dataframe: polars.DataFrame = _getDataFromPythonFiles(_getDataFromInterpreter())
	dataframe = dataframe.lazy().with_columns(polars.col('attribute').alias('attributeRename'),
		polars.lit('False').alias('move2keywordArguments'), polars.lit(None, dtype=polars.Object).alias('defaultValue')).collect()
	dataframe = dictionaryToUpdateDataframe(attributeRename__, dataframe)
	dataframe = dictionaryToUpdateDataframe(move2keywordArguments__, dataframe)
	dataframe = dictionaryToUpdateDataframe(attributeType__ClassDefIdentifier_attribute, dataframe)
	dataframe = dictionaryToUpdateDataframe(defaultValue__, dataframe)
	dataframe = _makeColumn_kwarg_annotationIdentifier(dataframe)
	dataframe = dataframe.lazy().with_columns(polars.Series('classAs_astAttribute',
		map(_make_astAttribute, dataframe['ClassDefIdentifier']), dtype=polars.Object)).collect()
	dataframe = _makeColumn_list2Sequence(dataframe)
	dataframe = _makeColumn_type_ast_expr(dataframe)
	dataframe = dataframe.lazy().with_columns(polars.col('attributeType').str.replace_many(
		list(map('ast.'.__add__, settingsManufacturing.astSuperClasses)), list(settingsManufacturing.astSuperClasses.values()), leftmost=True)
		.alias('type_astSuperClasses')).collect()
	dataframe = _makeColumn_ast_arg(dataframe)
	dataframeTypes: polars.DataFrame = (dataframe.lazy().with_row_index('rowIndex')
		.filter(polars.col('type_astSuperClasses') != 'No').select('rowIndex', 'type_astSuperClasses').collect())
	dataframeTypes = dataframeTypes.lazy().with_columns(polars.Series('type_astSuperClasses_ast_expr',
		map(pythonCode2ast_expr, dataframeTypes['type_astSuperClasses']), dtype=polars.Object)).collect()
	dataframe = (dataframe.lazy().with_row_index('rowIndex')
		.join(dataframeTypes.lazy().select('rowIndex', 'type_astSuperClasses_ast_expr'), on='rowIndex', how='left', maintain_order='left')
		.drop('rowIndex').collect())
	dataframe = dataframe.lazy().with_columns(polars.when(polars.col('attributeKind') == '_field')
		.then(polars.lit('hasDOT') + polars.col('attribute')).otherwise(polars.lit('No')).alias('TypeAlias_hasDOTIdentifier')).collect()
	dataframe = _makeColumnTypeAlias_hasDOTSubcategory(dataframe)
	dataframe = _makeColumn_list4TypeAlias(dataframe)
	dataframe = _makeColumn_list4TypeAliasSubcategories(dataframe)
	dataframe = _makeColumnsVersionMinimum(dataframe, ['ClassDefIdentifier', 'match_args'], 'versionMinorMinimum_match_args')
	dataframe = _makeColumnsVersionMinimum(dataframe, ['ClassDefIdentifier'], 'versionMinorMinimumClass')
	dataframe = _makeColumnCall_keyword(dataframe)
	dataframe = _fixMutable_defaultValue(dataframe)
	dataframe = dataframe.lazy().sort(polars.col('ClassDefIdentifier').str.to_lowercase(), 'versionMinorPythonInterpreter',
		polars.col('attribute').str.to_lowercase(), descending=[False, True, False], maintain_order=True).collect()
	# TODO Figure out overload for `Make`
	dataframe = _makeColumnsFourLists(dataframe)
	writeDataframe(dataframe.lazy().select(_columns).collect(), settingsManufacturing.pathFilenameDataframeAST)

if __name__ == '__main__':
	updateDataframe()
