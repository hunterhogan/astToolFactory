"""AST dataframe manufacturing assembly line.

(AI generated docstring)

This module is the executor for manufacturing the authoritative AST dataframe used by
`astToolFactory`. The public entry point `updateDataframe` builds a base dataframe from
source material, applies selector-based policy decisions from
`astToolFactory.datacenter._dataframeUpdateAnnex`, computes derived columns required for
code generation, aggregates per-class lists, and persists the final dataframe.

Selector-based updates are expressed as mappings from a `SelectorSpecification` to a
`column__value`. A selector specification is a `NamedTuple` whose field names are
dataframe columns and whose values are the required cell values for a row to match.
`getSelectorFromSpecification` turns that specification into a boolean row selector, and
`dictionaryToUpdateDataframe` applies the resulting assignment.

"""
# pyright: reportUnusedImport=false
from ast import (
	alias, arg, arguments, Attribute, boolop, cmpop, comprehension, ExceptHandler, expr, expr_context, Interpolation,
	keyword, match_case, Name, operator, pattern, stmt, Subscript, TemplateStr, type_param, TypeIgnore, unaryop, withitem)
from astToolFactory import (
	Column__ClassDefIdentifier_attribute, column__value, noMinimum, SelectorSpecification, settingsManufacturing)
from astToolFactory.cpython import getDictionary_match_args
from astToolFactory.datacenter._dataframeUpdateAnnex import (
	_columns, attributeRename__, attributeType__ClassDefIdentifier_attribute, defaultValue__,
	dictionary_defaultValue_ast_arg_Call_keyword_orElse, kwarg_annotationIdentifier__, move2keywordArguments__)
from astToolFactory.datacenter._dataServer import _sortCaseInsensitive, getDataframe
from astToolkit import (
	ast_attributes, ast_attributes_int, ast_attributes_type_comment, Be, ConstantValueType as _ConstantValue, DOT, Grab,
	IfThis, Make, NodeChanger, NodeTourist, parsePathFilename2astModule, Then)
from astToolkit.transformationTools import makeDictionaryClassDef, pythonCode2ast_expr
from collections.abc import Mapping
from functools import cache
from hunterMakesPy import raiseIfNone
from more_itertools import loops
from numpy.typing import ArrayLike
from operator import getitem
from typing import Any, cast
import ast
import builtins
import numpy
import pandas
import typeshed_client

# ======= HARDCODED values. TODO: eliminate ======================

_attributeTypeVarHARDCODED: str = '_EndPositionT'

# ======= ast Functions ==========================================

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
	keywordValue: ast.expr = Make.Name(cast(str, attributePROXY['attributeRename']))
	if attributePROXY['list2Sequence'] is True:
		keywordValue = Make.IfExp(test=keywordValue, body=Make.Call(Make.Name('list'), [keywordValue]), orElse=cast(ast.expr, attributePROXY['orElse']))
	else:
		keywordValue = Make.Or.join([keywordValue, cast(ast.expr, attributePROXY['orElse'])])
	return Make.keyword(cast(str, attributePROXY['attribute']), keywordValue)

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
	ast_keyword: ast.keyword = getitem(raiseIfNone(NodeTourist(
					findThis = IfThis.isAllOf(
						Be.Call.funcIs(IfThis.isAttributeNamespaceIdentifier(namespace, identifier))
						, Be.Call.keywordsIs(Be.at(0, IfThis.is_keywordIdentifier('default')))
					)
					, doThat = Then.extractIt(DOT.keywords)
				).captureLastMatch(_get_astModule_astStub())
			)
			, 0
		)

	_attributeTypeVar_default: str = ast.unparse(ast_keyword.value)

	NodeTourist[ast.AnnAssign, Mapping[str, str]](findThis=Be.AnnAssign.targetIs(Be.Name)
		, doThat=Then.updateKeyValueIn(key=lambda node: cast(ast.Name, node.target).id
			, value=lambda node: ast.unparse(node.annotation)
			, dictionary=dictionary_Attributes)
	).visit(astClassDef)

	for _attribute in dictionary_Attributes:
		_attributeTypeVar: str = _attributeTypeVarHARDCODED
		dictionary_Attributes[_attribute] = dictionary_Attributes[_attribute].replace(_attributeTypeVar, _attributeTypeVar_default)
	return dictionary_Attributes

# ======= pandas functions =========================================

# ------- TODO implement this fake function --------------------------------

def _getDataFromInterpreter(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	"""Populate the dataframe with data from the running Python interpreter.

	(AI generated docstring)

	Currently a placeholder. This function is intended to extract baseline
	information (like available classes) directly from the executing interpreter.

	Parameters
	----------
	dataframe : pandas.DataFrame
		The initial dataframe.

	Returns
	-------
	dataframe : pandas.DataFrame
		The dataframe, potentially augmented with interpreter-derived data.

	"""
	# TODO Columns to create using the Python Interpreter,
	# from version 3.settingsManufacturing.versionMinor_astMinimumSupported
	# to version 3.settingsManufacturing.versionMinorMaximum, inclusive.
	# 'ClassDefIdentifier',
	# 'versionMajorPythonInterpreter',
	# 'versionMinorPythonInterpreter',
	# 'versionMicroPythonInterpreter',
	# 'base',
	return dataframe

# ------- Extract/collect data from outside sources --------------------------------

def _getDataFromPythonFiles(dataframe: pandas.DataFrame) -> pandas.DataFrame:
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
	dataframe : pandas.DataFrame
		The initial dataframe containing `ClassDefIdentifier`s and versions.

	Returns
	-------
	dataframe : pandas.DataFrame
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
		return bool(NodeTourist(IfThis.isCallIdentifier('deprecated'), doThat=Then.extractIt).captureLastMatch(Make.Module(cast(list[ast.stmt], dictionaryClassDef[ClassDefIdentifier].decorator_list))))

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
		_attribute_ast_expr: ast.expr | None = NodeTourist(
			findThis=Be.Subscript.valueIs(IfThis.isNameIdentifier('Unpack'))
			, doThat=Then.extractIt(DOT.slice)
		).captureLastMatch(dictionaryClassDef[ClassDefIdentifier])

		if _attribute_ast_expr:
			_EndPositionT: ast.expr | None = NodeTourist(findThis=Be.Subscript, doThat=Then.extractIt(DOT.slice)).captureLastMatch(_attribute_ast_expr)
			if _EndPositionT:
				the_Attributes = dict.fromkeys(dictionary_Attributes, ast.unparse(_EndPositionT))
			else:
				the_Attributes = dictionary_Attributes
		return the_Attributes

	def newRowsFrom_attributes(dataframeTarget: pandas.DataFrame) -> pandas.DataFrame:
		"""Generate dataframe rows for attributes defined via `_Attributes`.

		(AI generated docstring)

		This function finds all the "extra" attributes (like line numbers and
		column offsets) that are technically part of the class but are defined
		via the `_Attributes` mechanism in the stub file. It adds them to the
		dataframe with `attributeKind` set to `_attribute`.

		Parameters
		----------
		dataframeTarget : pandas.DataFrame
			The dataframe containing the classes to process.

		Returns
		-------
		dataframe : pandas.DataFrame
			A new dataframe containing only the rows representing these attributes.

		"""
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
		"""Generate dataframe rows for fields defined in `match_args`.

		(AI generated docstring)

		This function explodes the `match_args` tuple for each class into
		individual rows. These rows represent the primary fields of the AST node
		(e.g., `body`, `test`, `orelse`). It adds them to the dataframe with
		`attributeKind` set to `_field`.

		Parameters
		----------
		dataframeTarget : pandas.DataFrame
			The dataframe containing the classes and their `match_args` tuples.

		Returns
		-------
		dataframe : pandas.DataFrame
			A new dataframe containing only the rows representing these fields.

		"""
		def get_attributeType(dddataframeee: pandas.DataFrame) -> pandas.Series:
			"""Resolve the type annotation of a field from the stub file.

			(AI generated docstring)

			This function acts as a resolver that goes back to the `ClassDef` in the
			parsed stub to find the specific `AnnAssign` for a field found in
			`match_args`. It uses `eval` to resolve internal `ast` TypeAliases
			into concrete types for cleaner extraction.

			Parameters
			----------
			dddataframeee : pandas.DataFrame
				A dataframe (or series masquerading as one depending on apply context)
				representing the rows being processed.

			Returns
			-------
			attributeType : pandas.Series
				The string representation of the type annotation for the field.

			"""
			dddataframeee['attributeType'] = ast.unparse(NodeChanger[ast.Name, ast.expr](
				findThis=lambda node: Be.Name(node) and isinstance(eval(node.id), type) and issubclass(eval(node.id), ast.AST)  # noqa: S307
				, doThat=lambda node: Make.Attribute(Make.Name('ast'), eval(node.id).__name__)  # noqa: S307
				).visit(raiseIfNone(NodeTourist[ast.AnnAssign, ast.expr](
					findThis = Be.AnnAssign.targetIs(IfThis.isNameIdentifier(cast(str, dddataframeee['attribute'])))
					, doThat = Then.extractIt(DOT.annotation)
					).captureLastMatch(dictionaryClassDef[cast(str, dddataframeee['ClassDefIdentifier'])]))))

			dddataframeee['attributeType'] = dddataframeee['attributeType'].replace('builtins.str', 'str')
# https://github.com/python/cpython/issues/143661

			return dddataframeee['attributeType']

		dataframeTarget = dataframeTarget[dataframeTarget['match_args'] != ()]

		# Explode match_args tuples into separate rows
		dataframeTarget = dataframeTarget.assign(attribute=dataframeTarget['match_args']).explode('attribute').reset_index(drop=True)
		# Add required columns
		dataframeTarget['attributeKind'] = '_field'

		dataframeTarget['attributeType'] = dataframeTarget.apply(get_attributeType, axis='columns', result_type='expand')

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

	new_match_args: pandas.Series = (dataframe[['ClassDefIdentifier', 'versionMinorPythonInterpreter', 'deprecated']]
		.apply(tuple, axis='columns')
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

# ------- Refine and compute data: transformations create distinct values per row --------------------------------

def _fixMutable_defaultValue(dataframe: pandas.DataFrame) -> pandas.DataFrame:
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
	dataframe : pandas.DataFrame
		The dataframe to transform.

	Returns
	-------
	dataframe : pandas.DataFrame
		The dataframe with updated defaults and arguments for mutable types.

	Raises
	------
	ValueError
		If an attribute is inconsistent across uses or is incorrectly marked
		as a keyword argument.

	"""
	for specifiedColumnsAndValues, orElse in dictionary_defaultValue_ast_arg_Call_keyword_orElse.items():
		selector: pandas.Series[bool] = getSelectorFromSpecification(dataframe, specifiedColumnsAndValues)

		attributePROXY = dataframe.loc[selector, ['attribute', 'attributeType', 'attributeRename', 'move2keywordArguments', 'list2Sequence']].drop_duplicates().to_dict(orient='records')

		if len(attributePROXY) > 1:
			message: str = f"Your current system assumes attribute '{attributePROXY[0]['attribute']}' is the same whenever it is used, but this function got {len(attributePROXY)} variations."
			raise ValueError(message)

		attributePROXY = cast(dict[str, str | bool | ast.expr], attributePROXY[0])
		if attributePROXY['move2keywordArguments'] != 'False':
			message = f"Your current system assumes attribute '{attributePROXY['attribute']}' is not a keyword argument, but this function got {attributePROXY}."
			raise ValueError(message)

		dataframe.loc[selector, 'defaultValue'] = Make.Constant(None) # pyright: ignore[reportArgumentType, reportCallIssue]
		attributeType: str = cast(str, attributePROXY['attributeType']) + ' | None'
		if attributePROXY['list2Sequence'] is True:
			attributeType = attributeType.replace('list', 'Sequence')
		dataframe.loc[selector, 'ast_arg'] = Make.arg(cast(str, attributePROXY['attributeRename']), annotation=pythonCode2ast_expr(attributeType)) # pyright: ignore[reportArgumentType, reportCallIssue]
		attributePROXY['orElse'] = orElse
		dataframe.loc[selector, 'Call_keyword'] = _make_keywordOrList(attributePROXY) # pyright: ignore[reportArgumentType, reportCallIssue]
	return dataframe

def _makeColumn_ast_arg(dataframe: pandas.DataFrame) -> pandas.DataFrame:
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
	dataframe : pandas.DataFrame
		The dataframe containing attribute names and their corresponding
		AST-based type expressions.

	Returns
	-------
	dataframe : pandas.DataFrame
		The dataframe with a new column `ast_arg`, containing `ast.arg` nodes
		or `'No'` if the attribute is handled via keyword arguments.

	See Also
	--------
	`_makeColumn_type_ast_expr` : The **Type Construction Step** that builds
		the `type_ast_expr` used here.

	"""
	dataframe['ast_arg'] = 'No'

	selectorAttributeArguments: pandas.Series[bool] = dataframe['move2keywordArguments'] == 'False'

	def make_ast_arg(row: pandas.Series) -> ast.arg:
		return Make.arg(row['attributeRename'], annotation=cast(ast.expr, row['type_ast_expr']))

	dataframe.loc[selectorAttributeArguments, 'ast_arg'] = dataframe[selectorAttributeArguments].apply(make_ast_arg, axis='columns')
	return dataframe

def _makeColumn_kwarg_annotationIdentifierHARDCODED(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	"""TODO Implement a function to create/update `kwarg_annotationIdentifier`.

	Possible values, all `str`:
		ast_attributes_int
		ast_attributes_type_comment
		ast_attributes
		No

	The THREE TypedDict I use in method signatures: ast_attributes, ast_attributes_int, ast_attributes_type_comment
	The ONLY hardcoded values allowed in the function: ast_attributes, ast_attributes_int, ast_attributes_type_comment. No
	`lineno`. No `type_comment`. No `int`. No `str | None`.

	Flow: IF THIS WERE NOT PANDAS. Don't make a 'temporary dictionary': do everything the smart way with idiomatic pandas. I don't
		know how to think in the pandas paradigm, so I'm not good at designing flow for idiomatic pandas.
	- Assign `No`, but re-assign if the ClassDefIdentifier qualifies.
	- Per ClassDefIdentifier, versionMinor:
		- make a temporary dictionary of the keyword arguments I am putting in a TypedDict
			- the identifier of the parameter
			- the annotation of the parameter
		- if column attributeKind == '_attribute', then add columns 'attributeRename, attributeType' to the temporary dictionary
		- if column move2keywordArguments == 'No' or 'False', do nothing special
		- NOTE possibly not what you are expecting: if column move2keywordArguments == 'True', do nothing special: do NOT add
			'attributeRename, attributeType' to the temporary dictionary because attributeRename will not be in the dictionary that gets Unpack
		- if column move2keywordArguments == 'Unpack', then add columns 'attributeRename, attributeType' to the temporary dictionary

		- So far, this ought to be smart, generic, extensible logic. If I decide I want `type_params` for only FunctionDef for only
			version 12, for example, to be a keyword argument that is 'hidden' in the TypedDict, then I just need to change
			move2keywordArguments == 'Unpack' for that line. It is easy and important to write the above code to work this way.

		- Inspect the temporary dictionary; cases and actions:
			- It is empty, don't do anything: `kwarg_annotationIdentifier` will remain 'No'.
			- The key:value items match one of the three TypedDict above, assign the identifier of the TypedDict to `kwarg_annotationIdentifier`.
			- else NotImplemented with a message telling future me which function needs to be updated with what functionality: the
				missing functionality is that the temporary dictionary doesn't match the available options.

	I've imported ast_attributes, ast_attributes_int, ast_attributes_type_comment from astToolkit. If I were to change the
	dictionaries or add new dictionaries, there will be a temporary Catch-22: the new dictionaries will not be in the existing
	version of astToolkit, so this function will not be able to match them.
	"""
	dataframe = dictionaryToUpdateDataframe(kwarg_annotationIdentifier__, dataframe)
	dataframe['kwarg_annotationIdentifier'] = dataframe['kwarg_annotationIdentifier'].fillna('No')
	return dataframe

def _makeColumn_list2Sequence(dataframe: pandas.DataFrame) -> pandas.DataFrame:
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
	dataframe : pandas.DataFrame
		The dataframe containing attribute type definitions to analyze.

	Returns
	-------
	dataframe : pandas.DataFrame
		The dataframe with a new boolean column `list2Sequence`, set to `True`
		for attributes that match the covariant transformation criteria.

	See Also
	--------
	`_makeColumn_type_ast_expr` : The **Type Construction Step** that uses this
		decision to modify type expressions.
	`_makeColumn_ast_arg` : The **Usage Step** that uses those expressions to
		build function arguments.

	"""
	dataframe['list2Sequence'] = (
		dataframe['attributeType'].str.contains('list', regex=False, na=False)
		& dataframe['attributeType'].str.contains('|'.join(settingsManufacturing.astSuperClasses), regex=True, na=False)
	)
	return dataframe

def _makeColumn_type_ast_expr(dataframe: pandas.DataFrame) -> pandas.DataFrame:
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
	dataframe : pandas.DataFrame
		The dataframe containing raw type strings (`attributeType`) and the
		covariance flags (`list2Sequence`).

	Returns
	-------
	dataframe : pandas.DataFrame
		The dataframe with a new column `type_ast_expr`, containing the `ast.expr`
		representation of the attribute's type.

	See Also
	--------
	`_makeColumn_list2Sequence` : The **Decision Step** that flags which rows
		need the `list` -> `Sequence` replacement used here.
	`_makeColumn_ast_arg` : The **Usage Step** that consumes these AST expressions.

	"""
	dataframe['type_ast_expr'] = 'No'
	dataframe.loc[dataframe['list2Sequence'], 'type_ast_expr'] = dataframe['attributeType'].str.replace('list', 'Sequence').apply(cast(Any, pythonCode2ast_expr))
	dataframe.loc[~dataframe['list2Sequence'], 'type_ast_expr'] = dataframe['attributeType'].apply(cast(Any, pythonCode2ast_expr))

	dataframe.loc[dataframe['attribute'] == 'str', 'type_ast_expr'] = cast(Any, pythonCode2ast_expr(string='builtins.str')) # <-- This is called "irony" because the parameter name is `string`, the parameter type is `str`, and I am using this function that I made a long time ago to fix the new `ast.Interpolation.str`. https://github.com/python/cpython/issues/143661
	return dataframe

def _makeColumnCall_keyword(dataframe: pandas.DataFrame) -> pandas.DataFrame:
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
	dataframe : pandas.DataFrame
		The dataframe with `attributeRename`, `list2Sequence`, and `defaultValue`.

	Returns
	-------
	dataframe : pandas.DataFrame
		The dataframe with a new column `Call_keyword`.

	"""
	dataframe['Call_keyword'] = 'No'

	selectorCall_keyword: pandas.Series[bool] = (dataframe['attributeKind'] == '_field') & (dataframe['move2keywordArguments'] != 'No') & (dataframe['move2keywordArguments'] != 'Unpack')

	selector_defaultValue: pandas.Series[bool] = selectorCall_keyword & (dataframe['move2keywordArguments'] == 'True')

	def make_ast_keywordWith_defaultValue(dataframeTarget: pandas.Series) -> ast.keyword:
		return Make.keyword(dataframeTarget['attribute'], dataframeTarget['defaultValue'])

	dataframe.loc[selector_defaultValue, 'Call_keyword'] = dataframe.loc[selector_defaultValue].apply(make_ast_keywordWith_defaultValue, axis='columns')

	selectorNameValue: pandas.Series[bool] = selectorCall_keyword & (dataframe['move2keywordArguments'] != 'True')

	def make_ast_keywordFrom_attributeRename(dataframeTarget: pandas.Series) -> ast.keyword:
		keywordValue: ast.expr = Make.Name(dataframeTarget['attributeRename'])
		if dataframeTarget['list2Sequence'] is True:
			keywordValue = Make.Call(Make.Name('list'), [keywordValue])
		return Make.keyword(dataframeTarget['attribute'], keywordValue)

	dataframe.loc[selectorNameValue, 'Call_keyword'] = dataframe.loc[selectorNameValue].apply(make_ast_keywordFrom_attributeRename, axis='columns')
	return dataframe

# ------- Aggregate data: transformations create identical values in their group ------------

def _makeColumn_list4TypeAlias(dataframe: pandas.DataFrame) -> pandas.DataFrame:
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
	dataframe : pandas.DataFrame
		The dataframe containing `TypeAlias_hasDOTSubcategory` and version
		information.

	Returns
	-------
	dataframe : pandas.DataFrame
		The dataframe populated with `list4TypeAlias_value` (the list of AST
		expressions) and `hashable_list4TypeAlias_value` (for efficient
		groupings).

	"""
	dataframe['list4TypeAlias_value'] = pandas.Series(data='No', index=dataframe.index, dtype=object)
	dataframe['hashable_list4TypeAlias_value'] = pandas.Series(data='No', index=dataframe.index, dtype=str)

	def compute_list4TypeAliasByRow(dataframeTarget: pandas.DataFrame) -> tuple[list[ast.expr], str]:
		"""Calculate the type union for a specific TypeAlias configuration.

		(AI generated docstring)

		This helper function finds all rows belonging to the same TypeAlias
		subcategory that are valid for the current row's version context (less
		than or equal to `versionMinorMinimumAttribute`). It effectively
		reconstructs the `Union[...]` of types that exists at that specific
		point in the version history.

		Parameters
		----------
		dataframeTarget : pandas.DataFrame
			The specific row (as a Series-like DataFrame) being processed.

		Returns
		-------
		elementList : tuple[list[ast.expr], str]
			A tuple containing the list of AST expressions for the types and a
			hashable string representation of the identifiers.

		"""
		selectorSubcategory: pandas.Series[bool] = (
			(dataframe['attributeKind'] == '_field')
			& ~ (dataframe['deprecated'])
			& (dataframe['TypeAlias_hasDOTSubcategory'] == dataframeTarget['TypeAlias_hasDOTSubcategory'])
			& (dataframe['versionMinorMinimumAttribute'] <= dataframeTarget['versionMinorMinimumAttribute'])
		)
		if not selectorSubcategory.any():
			return [], '[]'
		matchingRows: pandas.DataFrame = (
			dataframe.loc[selectorSubcategory, ['classAs_astAttribute', 'ClassDefIdentifier']]
			.drop_duplicates(subset='ClassDefIdentifier')
			.sort_values('ClassDefIdentifier', key=lambda x: x.str.lower())
	)
		return matchingRows['classAs_astAttribute'].tolist(), str(matchingRows['ClassDefIdentifier'].tolist())

	selector_assign: pandas.Series[bool] = dataframe['attributeKind'] == '_field'
	computed_values: pandas.DataFrame = dataframe[selector_assign].apply(compute_list4TypeAliasByRow, axis='columns', result_type='expand')
	computed_values.columns = ['list4TypeAlias_value', 'hashable_list4TypeAlias_value']
	dataframe.loc[selector_assign, ['list4TypeAlias_value', 'hashable_list4TypeAlias_value']] = computed_values
	return dataframe

def _makeColumn_list4TypeAliasSubcategories(dataframe: pandas.DataFrame) -> pandas.DataFrame:
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
	dataframe : pandas.DataFrame
		The dataframe containing `TypeAlias_hasDOTSubcategory`.

	Returns
	-------
	dataframe : pandas.DataFrame
		The dataframe with a new column `list4TypeAliasSubcategories`
		containing lists of possible variant names.

	"""
	dataframe['list4TypeAliasSubcategories'] = 'No'

	selector_field: pandas.Series[bool] = (dataframe['attributeKind'] == '_field')

	def compute_list4TypeAliasSubcategories(groupBy: pandas.DataFrame) -> list[ast.expr]:
		"""Collect unique subcategory names for a group of related attributes.

		(AI generated docstring)

		Parameters
		----------
		groupBy : pandas.DataFrame
			A subset of the dataframe grouped by `attribute`.

		Returns
		-------
		list_names : list[ast.expr]
			A sorted list of `ast.Name` nodes representing the unique,
			non-deprecated subcategory identifiers found in the group.

		"""
		groupBy = groupBy[groupBy['TypeAlias_hasDOTSubcategory'] != 'No']
		groupBy = groupBy[~groupBy['deprecated']]
		TypeAlias_hasDOTSubcategory = groupBy['TypeAlias_hasDOTSubcategory'].unique()
		return [Make.Name(subcategory) for subcategory in sorted(TypeAlias_hasDOTSubcategory, key=lambda x: x.lower())]

	# Create a mapping from attribute to subcategory names
	list4TypeAliasSubcategories__attributeKind_attribute: dict[str, list[ast.expr]] = {}
	for attribute, groupBy in dataframe[selector_field].groupby('attribute'):
		list4TypeAliasSubcategories__attributeKind_attribute[str(attribute)] = compute_list4TypeAliasSubcategories(groupBy)

	# Map the subcategory names to the appropriate rows using pandas map
	dataframe.loc[selector_field, 'list4TypeAliasSubcategories'] = dataframe.loc[selector_field, 'attribute'].map(list4TypeAliasSubcategories__attributeKind_attribute)

	return dataframe

def _makeColumnsFourLists(dataframe: pandas.DataFrame) -> pandas.DataFrame:
	"""Aggregate attributes into lists for class definitions and calls.

	(AI generated docstring)

	This function is an **Aggregation Step**. It groups rows by `ClassDefIdentifier`
	and version, then compiles lists of attributes, arguments, defaults, and
	keywords for each group. These lists are essentially "pre-baked" structures
	ready for code generation templates (like `Call` nodes or `FunctionDef`
	args).

	It creates four columns:
	- `listTupleAttributes`: List of (name, type) tuples for all fields.
	- `listFunctionDef_args`: List of `ast.arg` nodes for function signatures.
	- `listDefaults`: List of default values for those arguments.
	- `listCall_keyword`: List of `ast.keyword` nodes for constructor calls.

	Parameters
	----------
	dataframe : pandas.DataFrame
		The dataframe containing individual attribute rows.

	Returns
	-------
	dataframe : pandas.DataFrame
		The dataframe updated with columns containing aggregated lists.

	"""
	dictionaryTupleAttributes: dict[tuple[str, int], list[tuple[str, ast.expr]]] = {}
	dictionaryFunctionDef_args: dict[tuple[str, int], list[ast.arg]] = {}
	dictionaryDefaults: dict[tuple[str, int], list[ast.expr]] = {}
	dictionaryCall_keyword: dict[tuple[str, int], list[ast.keyword]] = {}

	for (ClassDefIdentifier, versionMinorMinimum_match_args), dataframeGroupBy in dataframe.groupby(['ClassDefIdentifier', 'versionMinorMinimum_match_args']):  # ty:ignore[not-iterable]
		groupKey: tuple[str, int] = (ClassDefIdentifier, versionMinorMinimum_match_args) # pyright: ignore[reportAssignmentType]
		match_argsCategoricalSort: tuple[str, ...] = dataframeGroupBy['match_args'].iloc[0]
		dataframeGroupBy['attribute'] = pandas.Categorical(dataframeGroupBy['attribute'], categories=match_argsCategoricalSort, ordered=True)
		dataframeGroupBy: pandas.DataFrame = dataframeGroupBy.sort_values(['attribute', 'versionMinorMinimum_match_args'], ascending=[True, False])

		dataframeGroupBy = dataframeGroupBy[dataframeGroupBy['attributeKind'] == '_field']

		dictionaryTupleAttributes[groupKey] = (dataframeGroupBy.copy().drop_duplicates(subset='attribute')[['attribute', 'type_ast_expr']].apply(tuple, axis='columns').tolist())

		dictionaryFunctionDef_args[groupKey] = (dataframeGroupBy[dataframeGroupBy['move2keywordArguments'] == 'False']
																.copy().drop_duplicates(subset='attribute')['ast_arg'].tolist())

		dictionaryDefaults[groupKey] = (dataframeGroupBy[(dataframeGroupBy['defaultValue'] != 'No')
			& (dataframeGroupBy['move2keywordArguments'] == 'False')].copy().drop_duplicates(subset='attribute')['defaultValue'].tolist())

		dictionaryCall_keyword[groupKey] = (dataframeGroupBy[(dataframeGroupBy['move2keywordArguments'] != 'No')
			& (dataframeGroupBy['move2keywordArguments'] != 'Unpack')].drop_duplicates(subset='attribute')['Call_keyword'].tolist())
	dataframe['listTupleAttributes'] = (dataframe[['ClassDefIdentifier', 'versionMinorMinimum_match_args']].apply(tuple, axis='columns').map(dictionaryTupleAttributes).fillna(dataframe['listTupleAttributes']))
	dataframe['listFunctionDef_args'] = (dataframe[['ClassDefIdentifier', 'versionMinorMinimum_match_args']].apply(tuple, axis='columns').map(dictionaryFunctionDef_args).fillna(dataframe['listFunctionDef_args']))
	dataframe['listDefaults'] = (dataframe[['ClassDefIdentifier', 'versionMinorMinimum_match_args']].apply(tuple, axis='columns').map(dictionaryDefaults).fillna(dataframe['listDefaults']))
	dataframe['listCall_keyword'] = (dataframe[['ClassDefIdentifier', 'versionMinorMinimum_match_args']].apply(tuple, axis='columns').map(dictionaryCall_keyword).fillna(dataframe['listCall_keyword']))
	return dataframe

def _makeColumnTypeAlias_hasDOTSubcategory(dataframe: pandas.DataFrame) -> pandas.DataFrame:
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
	dataframe : pandas.DataFrame
		The dataframe containing `TypeAlias_hasDOTIdentifier` and raw
		`attributeType` strings.

	Returns
	-------
	dataframe : pandas.DataFrame
		The dataframe with a new column `TypeAlias_hasDOTSubcategory`
		containing the generated identifiers.

	"""
	dataframe['TypeAlias_hasDOTSubcategory'] = 'No'
	selector_hasDOTIdentifier: pandas.Series[bool] = dataframe['TypeAlias_hasDOTIdentifier'] != 'No'
	dataframe.loc[selector_hasDOTIdentifier, 'TypeAlias_hasDOTSubcategory'] = dataframe['TypeAlias_hasDOTIdentifier'] + '_' + dataframe['attributeType'].str.replace('|', 'Or').str.replace('[', '_').str.replace('[\\] ]', '', regex=True).str.replace('ast.', '')
	return dataframe

def _makeColumnsVersionMinimum(dataframe: pandas.DataFrame, list_byColumns: list[str], columnNameTarget: str) -> pandas.DataFrame:
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
	dataframe : pandas.DataFrame
		The dataframe to process.
	list_byColumns : list[str]
		List of column names to group by (identifying the feature).
	columnNameTarget : str
		Name of the new column to be created with the minimum version.

	Returns
	-------
	dataframe : pandas.DataFrame
		The dataframe with the new minimum version column.

	"""
	dataframe[columnNameTarget] = numpy.where(
		dataframe.groupby(list_byColumns)['versionMinorPythonInterpreter'].transform('min') == settingsManufacturing.versionMinor_astMinimumSupported
		, noMinimum
		, dataframe.groupby(list_byColumns)['versionMinorPythonInterpreter'].transform('min')
	)
	return dataframe

# ------- Generalized functions ----------------------------------------

def dictionaryToUpdateDataframe(dictionary: Mapping[SelectorSpecification, column__value], dataframe: pandas.DataFrame) -> pandas.DataFrame:
	"""Apply a selector-to-assignment dictionary to update dataframe cells in place.

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
	dataframe : pandas.DataFrame
		Dataframe to update. Modified in place and also returned.

	Returns
	-------
	dataframe : pandas.DataFrame
		The same dataframe, modified with all assignments applied.

	See Also
	--------
	`getSelectorFromSpecification` : Converts a selector specification to a boolean `pandas.Series`.
	`astToolFactory.datacenter._dataframeUpdateAnnex` : Module docstring explains
		the complete selector-based dataframe update system.

	"""
	for specifiedColumnsAndValues, assign in dictionary.items():
		dataframe.loc[getSelectorFromSpecification(dataframe, specifiedColumnsAndValues), assign.column] = assign.value
	return dataframe

def getSelectorFromSpecification(dataframe: pandas.DataFrame, specifiedColumnsAndValues: SelectorSpecification) -> pandas.Series:
	"""Convert a selector specification to a boolean row selector for a dataframe.

	(AI generated docstring)

	This function translates the declarative selector specification into an executable boolean
	`pandas.Series`. Each field in the tuple becomes an equality test against the
	corresponding dataframe column. All tests are combined with logical AND, so a
	row is selected only if *all* field values match.

	Parameters
	----------
	dataframe : pandas.DataFrame
		Dataframe to build the selector for.
	specifiedColumnsAndValues : SelectorSpecification
		A `NamedTuple` whose field names are column names and whose field values
		are the values to match.

	Returns
	-------
	selector : pandas.Series
		Boolean series with `True` for rows matching all conditions.

	See Also
	--------
	`dictionaryToUpdateDataframe` : Applies the selector to perform assignments.
	`astToolFactory.datacenter._dataframeUpdateAnnex` : Module docstring explains
		the complete selector-based dataframe update system.

	"""
	return pandas.concat([*[dataframe[column] == value for column, value in specifiedColumnsAndValues._asdict().items()]], axis=1).all(axis=1)

# ======= The Function ======================================================

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

	The function modifies data in place and relies heavily on this module's stages and
	`_dataframeUpdateAnnex` configuration dictionaries.

	"""
	dataframe: pandas.DataFrame = getDataframe(includeDeprecated=True, versionMinorMaximum=settingsManufacturing.versionMinorMaximum, modifyVersionMinorMinimum=False)

	# TODO think of a clever, simple way to optionally apply this instead of toggling comments.
	# columns: reorder; drop columns, but they might be recreated later in the flow.  # noqa: ERA001
	# dataframe = dataframe[_columns]  # noqa: ERA001

	# TODO Get data using the Python Interpreter.
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

	dataframe = _getDataFromPythonFiles(dataframe)

	dataframe['attributeRename'] = pandas.Series(data=dataframe['attribute'], index=dataframe.index, dtype=str, name='attributeRename', copy=True)
	dataframe = dictionaryToUpdateDataframe(attributeRename__, dataframe)

	dataframe['move2keywordArguments'] = pandas.Series(data='False', index=dataframe.index, dtype=str, name='move2keywordArguments')
	dataframe = dictionaryToUpdateDataframe(move2keywordArguments__, dataframe)

	dataframe = dictionaryToUpdateDataframe(attributeType__ClassDefIdentifier_attribute, dataframe)

	dataframe['defaultValue'] = pandas.Series(data='No', index=dataframe.index, dtype=str, name='defaultValue')
	dataframe = dictionaryToUpdateDataframe(defaultValue__, dataframe)

	dataframe = _makeColumn_kwarg_annotationIdentifierHARDCODED(dataframe)

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
	dataframe = _makeColumnsVersionMinimum(dataframe, ['ClassDefIdentifier', 'match_args'], 'versionMinorMinimum_match_args')
	dataframe = _makeColumnsVersionMinimum(dataframe, ['ClassDefIdentifier', 'attribute'], 'versionMinorMinimumAttribute')
	dataframe = _makeColumnsVersionMinimum(dataframe, ['ClassDefIdentifier'], 'versionMinorMinimumClass')
	dataframe = _makeColumnCall_keyword(dataframe)
	dataframe = _fixMutable_defaultValue(dataframe)
	dataframe = _sortCaseInsensitive(dataframe, ['ClassDefIdentifier', 'versionMinorPythonInterpreter', 'attribute'], caseInsensitive=[True, False, True], ascending=[True, False, True])
	# TODO Figure out overload for `Make`
	dataframe = _makeColumnsFourLists(dataframe)

	dataframe.to_pickle(settingsManufacturing.pathFilenameDataframeAST)

if __name__ == '__main__':
	updateDataframe()
