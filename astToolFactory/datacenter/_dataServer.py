"""API for data. The rest of the package should be ignorant of the specifics of the data source.

This module provides a set of functions to interact with the data source, allowing for easy retrieval and manipulation of data.

"""

from __future__ import annotations

from astToolFactory import noMinimum, settingsManufacturing
from astToolFactory.filesystem import gatherObjects, readDataframe
from typing import Any, cast, TYPE_CHECKING
import polars

if TYPE_CHECKING:
	from pathlib import Path
	import ast

def _makeColumn_guardVersion(dataframe: polars.LazyFrame, byColumn: str) -> polars.LazyFrame:
	"""No summary.

	Column 'guardVersion' = False unless:
	- A `byColumn`-'versionMinorMinimum' group is larger than 1, then 'guardVersion' is a countdown
		from the total number of versions in the group.
	- Or if the only member of a group has a python version greater than `pythonMinimumVersionMinor`.

	"""
	versionsTotal: polars.Expr = polars.col('versionMinorMinimum').n_unique().over(byColumn)
	return dataframe.with_columns(
		polars.when(
			(versionsTotal == 1)
			& (polars.col('versionMinorMinimum').max().over(byColumn) <= settingsManufacturing.pythonMinimumVersionMinor)
		)
		.then(0)
		.otherwise(
			(versionsTotal.cast(polars.Int64)
				- polars.col('versionMinorMinimum').rank('ordinal', descending=True).over(byColumn).cast(polars.Int64)
				+ 1).clip(lower_bound=1)
		)
		.alias('guardVersion')
	)

def getDataframe(*indices: str, **keywordArguments: Any) -> polars.DataFrame:
	pathFilename: Path = keywordArguments.get('pathFilename') or settingsManufacturing.pathFilenameDataframeAST
	includeDeprecated: bool = keywordArguments.get('includeDeprecated') or settingsManufacturing.includeDeprecated
	versionMinorMaximum: int | None = keywordArguments.get('versionMinorMaximum') or settingsManufacturing.versionMinorMaximum
	modifyVersionMinorMinimum: bool = keywordArguments.get('modifyVersionMinorMinimum', True)

	dataframe: polars.LazyFrame = readDataframe(pathFilename).lazy()
	if not includeDeprecated:
		dataframe = dataframe.filter(~polars.col('deprecated'))
	if versionMinorMaximum is not None:
		dataframe = dataframe.filter(polars.col('versionMinorPythonInterpreter') <= versionMinorMaximum)
	if modifyVersionMinorMinimum:
		columnsVersion: list[str] = ['versionMinorMinimumAttribute', 'versionMinorMinimumClass', 'versionMinorMinimum_match_args']
		dataframe = dataframe.with_columns(
			polars.when(polars.col(columnsVersion) > settingsManufacturing.pythonMinimumVersionMinor)
			.then(polars.col(columnsVersion)).otherwise(noMinimum)
		)
	if indices:
		dataframe = dataframe.select(*indices, polars.all().exclude(indices))
	return dataframe.collect()

def _getTableBe(**keywordArguments: Any) -> polars.DataFrame:
	listColumnsHARDCODED: list[str] = ['ClassDefIdentifier', 'versionMinorMinimumClass', 'classAs_astAttribute', 'listTupleAttributes']
	listColumns: list[str] = listColumnsHARDCODED
	del listColumnsHARDCODED
	return (getDataframe(**keywordArguments).lazy()
		.select(listColumns)
		.unique(subset=listColumns[:2], keep='first', maintain_order=True)
		.sort(polars.col(listColumns[0]).str.to_lowercase(), listColumns[1], descending=[False, True], maintain_order=True)
		.collect())

def getElementsBe(_identifierToolClass: str, **keywordArguments: Any) -> list[tuple[str, int, ast.expr, list[tuple[str, ast.expr, int]]]]:
	return cast('list[tuple[str, int, ast.expr, list[tuple[str, ast.expr, int]]]]', _getTableBe(**keywordArguments).rows())

def _getTableDOT(**keywordArguments: Any) -> polars.DataFrame:
	listColumnsHARDCODED: list[str] = ['attribute', 'TypeAlias_hasDOTSubcategory', 'versionMinorMinimumAttribute', 'type_ast_expr', 'attributeType', 'TypeAlias_hasDOTIdentifier']
	listColumns: list[str] = listColumnsHARDCODED
	del listColumnsHARDCODED
	dataframe: polars.DataFrame = (getDataframe(**keywordArguments).lazy()
		.filter(polars.col('attributeKind') == '_field')
		.select(listColumns)
		.sort(listColumns[2], descending=True, maintain_order=True)
		.sort(polars.col(listColumns[:2]).str.to_lowercase(), maintain_order=True)
		.unique(subset=listColumns[:2], keep='last', maintain_order=True)
		.rename({listColumns[2]: 'versionMinorMinimum'})
		.collect())
	definitions: polars.LazyFrame = (dataframe.lazy().with_row_index('次Source')
		.with_columns((polars.len().over('attribute') > 1).alias('overloadDefinition'))
		.with_columns(polars.when('overloadDefinition')
			.then(polars.lit([False, True])).otherwise(polars.lit([False])).alias('summary'))
		.explode('summary')
		.with_columns((polars.col('overloadDefinition') & ~polars.col('summary')).alias('overloadDefinition'))
		.with_columns(polars.when('overloadDefinition')
			.then('TypeAlias_hasDOTSubcategory').otherwise('TypeAlias_hasDOTIdentifier').alias('identifierTypeOfNode'))
		.sort('attribute', 'summary', maintain_order=True)
		.unique(subset=['identifierTypeOfNode', 'versionMinorMinimum'], keep='first', maintain_order=True)
		.with_row_index('次Definition'))
	values: polars.LazyFrame = dataframe.lazy().with_row_index('次Member').select(
		'attribute', '次Member', 'attributeType', polars.col('versionMinorMinimum').alias('versionMinorCandidate')
	)
	groups: polars.LazyFrame = (definitions.select('次Definition', '次Source', 'attribute', 'overloadDefinition', 'versionMinorMinimum')
		.join(values, on='attribute', how='inner', maintain_order='left_right')
		.filter(
			(polars.col('overloadDefinition') & (polars.col('次Source') == polars.col('次Member')))
			| (~polars.col('overloadDefinition') & (polars.col('versionMinorCandidate') <= polars.col('versionMinorMinimum')))
		)
		.unique(subset=['次Definition', 'attributeType'], keep='first', maintain_order=True)
		.sort('次Definition', polars.col('attributeType').str.to_lowercase(), maintain_order=True)
		.group_by('次Definition', maintain_order=True).agg(polars.col('次Member').alias('boxOf次Member')))
	dataframeDefinitions: polars.DataFrame = (definitions.join(groups, on='次Definition', how='left', maintain_order='left')
		.pipe(_makeColumn_guardVersion, 'identifierTypeOfNode')
		.select('identifierTypeOfNode', 'overloadDefinition', 'attribute', 'boxOf次Member', 'guardVersion', 'versionMinorMinimum')
		.collect())
	return dataframeDefinitions.replace_column(
		dataframeDefinitions.get_column_index('boxOf次Member'),
		gatherObjects(dataframe.get_column('type_ast_expr'), dataframeDefinitions.get_column('boxOf次Member')).rename('list_ast_expr')
	)

def getElementsDOT(_identifierToolClass: str, **keywordArguments: Any) -> list[tuple[str, bool, str, list[ast.expr], int, int]]:
	return cast('list[tuple[str, bool, str, list[ast.expr], int, int]]', _getTableDOT(**keywordArguments).rows())

def _getTableGrab(**keywordArguments: Any) -> polars.DataFrame:
	listColumnsHARDCODED: list[str] = ['attribute', 'type_astSuperClasses', 'versionMinorMinimumAttribute', 'TypeAlias_hasDOTIdentifier', 'type_astSuperClasses_ast_expr']
	listColumns: list[str] = listColumnsHARDCODED
	del listColumnsHARDCODED
	dataframe: polars.DataFrame = (getDataframe(**keywordArguments).lazy()
		.filter(polars.col('attributeKind') == '_field')
		.select(listColumns)
		.sort(listColumns[2], descending=True, maintain_order=True)
		.sort(polars.col(listColumns[:2]).str.to_lowercase(), maintain_order=True)
		.unique(subset=listColumns[:2], keep='last', maintain_order=True)
		.rename({listColumns[1]: 'attributeType', listColumns[2]: 'versionMinorMinimum', listColumns[4]: 'type_ast_expr'})
		.collect())
	definitions: polars.LazyFrame = dataframe.lazy().with_row_index('次Definition')
	values: polars.LazyFrame = definitions.select(
		'attribute', 'attributeType', polars.col('次Definition').alias('次Member'),
		polars.col('versionMinorMinimum').alias('versionMinorCandidate')
	)
	groups: polars.LazyFrame = (definitions.select('次Definition', 'attribute', 'versionMinorMinimum')
		.join(values, on='attribute', how='inner', maintain_order='left_right')
		.filter(polars.col('versionMinorCandidate') <= polars.col('versionMinorMinimum'))
		.sort('次Definition', polars.col('attributeType').str.to_lowercase(), maintain_order=True)
		.group_by('次Definition', maintain_order=True).agg(polars.col('次Member').alias('boxOf次Member')))
	dataframeDefinitions: polars.DataFrame = (definitions.join(groups, on='次Definition', how='left', maintain_order='left')
		.pipe(_makeColumn_guardVersion, 'attribute')
		.select('TypeAlias_hasDOTIdentifier', 'boxOf次Member', 'attribute', 'guardVersion', 'versionMinorMinimum')
		.unique(subset=['attribute', 'guardVersion', 'versionMinorMinimum'], keep='last', maintain_order=True)
		.collect())
	return dataframeDefinitions.replace_column(
		dataframeDefinitions.get_column_index('boxOf次Member'),
		gatherObjects(dataframe.get_column('type_ast_expr'), dataframeDefinitions.get_column('boxOf次Member')).rename('list_ast_expr')
	)

def getElementsGrab(_identifierToolClass: str, **keywordArguments: Any) -> list[tuple[str, list[ast.expr], str, int, int]]:
	return cast('list[tuple[str, list[ast.expr], str, int, int]]', _getTableGrab(**keywordArguments).rows())

def _getTableMake(**keywordArguments: Any) -> polars.DataFrame:
	listColumnsHARDCODED: list[str] = ['ClassDefIdentifier', 'versionMinorMinimumClass', 'versionMinorMinimum_match_args', 'listFunctionDef_args', 'kwarg_annotationIdentifier', 'listDefaults', 'classAs_astAttribute', 'listCall_keyword']
	listColumns: list[str] = listColumnsHARDCODED
	del listColumnsHARDCODED
	return (getDataframe(**keywordArguments).lazy()
		.select(listColumns)
		.sort(polars.col(listColumns[0]).str.to_lowercase(), *listColumns[1:3], descending=[False, True, True], maintain_order=True)
		.unique(subset=listColumns[:3], keep='first', maintain_order=True)
		.rename({listColumns[2]: 'versionMinorMinimum'})
		.pipe(_makeColumn_guardVersion, 'ClassDefIdentifier')
		.with_columns(polars.lit(value=False).alias('overloadDefinition'))
		.select('ClassDefIdentifier', 'listFunctionDef_args', 'kwarg_annotationIdentifier', 'listDefaults', 'classAs_astAttribute',
			'overloadDefinition', 'listCall_keyword', 'guardVersion', 'versionMinorMinimum')
		.collect())

def getElementsMake(_identifierToolClass: str, **keywordArguments: Any) -> list[tuple[str, list[ast.arg], str, list[ast.expr], ast.expr, bool, list[ast.keyword], int, int]]:
	return cast('list[tuple[str, list[ast.arg], str, list[ast.expr], ast.expr, bool, list[ast.keyword], int, int]]', _getTableMake(**keywordArguments).rows())

def _getTableTypeAlias(**keywordArguments: Any) -> polars.DataFrame:
	listColumnsHARDCODED: list[str] = ['attribute', 'TypeAlias_hasDOTSubcategory', 'ClassDefIdentifier', 'versionMinorMinimumAttribute', 'classAs_astAttribute', 'TypeAlias_hasDOTIdentifier', 'list4TypeAlias_value', 'hashable_list4TypeAlias_value', 'list4TypeAliasSubcategories']
	listColumns: list[str] = listColumnsHARDCODED
	del listColumnsHARDCODED
	dataframe: polars.LazyFrame = (getDataframe(**(keywordArguments | {'modifyVersionMinorMinimum': False})).lazy()
		.filter(polars.col('attributeKind') == '_field')
		.select(listColumns)
		.sort(listColumns[3], descending=True, maintain_order=True)
		.sort(polars.col(listColumns[:3]).str.to_lowercase(), maintain_order=True)
		.unique(subset=listColumns[:4], keep='last', maintain_order=True)
		.rename({listColumns[3]: 'versionMinorMinimum'})
		.sort('versionMinorMinimum', maintain_order=True))
	if keywordArguments.get('modifyVersionMinorMinimum', True):
		dataframe = dataframe.with_columns(
			polars.when(polars.col('versionMinorMinimum') > settingsManufacturing.pythonMinimumVersionMinor)
			.then('versionMinorMinimum').otherwise(noMinimum).alias('versionMinorMinimum')
		)
	dataframe = dataframe.unique(subset=['attribute', 'TypeAlias_hasDOTSubcategory', 'versionMinorMinimum'], keep='last', maintain_order=True)
	summaries: polars.LazyFrame = (dataframe
		.filter(polars.col('TypeAlias_hasDOTSubcategory').n_unique().over('attribute') > 1)
		.unique(subset=['attribute', 'TypeAlias_hasDOTSubcategory'], keep='last', maintain_order=True)
		.unique(subset=['attribute', 'versionMinorMinimum'], keep='first', maintain_order=True)
		.select('attribute', 'TypeAlias_hasDOTSubcategory', 'versionMinorMinimum', polars.lit(value=True).alias('summary')))
	return (dataframe.join(summaries, on=['attribute', 'TypeAlias_hasDOTSubcategory', 'versionMinorMinimum'], how='left', maintain_order='left')
		.with_columns(polars.when(polars.col('summary').fill_null(value=False))
			.then(polars.lit([False, True])).otherwise(polars.lit([False])).alias('summary'))
		.explode('summary')
		.with_columns(
			polars.when('summary').then(polars.lit('No')).otherwise('TypeAlias_hasDOTSubcategory').alias('TypeAlias_hasDOTSubcategory'),
			polars.when('summary').then('list4TypeAliasSubcategories').otherwise('list4TypeAlias_value').alias('list4TypeAlias_value')
		)
		.sort('attribute', 'summary', maintain_order=True)
		.with_columns(polars.when(
			(polars.col('TypeAlias_hasDOTSubcategory').n_unique().over('attribute') == 1)
			| (polars.col('TypeAlias_hasDOTSubcategory') == 'No')
		).then('TypeAlias_hasDOTIdentifier').otherwise('TypeAlias_hasDOTSubcategory').alias('identifierTypeAlias'))
		.pipe(_makeColumn_guardVersion, 'identifierTypeAlias')
		.sort('identifierTypeAlias', 'versionMinorMinimum', descending=[False, True], maintain_order=True)
		.select('identifierTypeAlias', 'list4TypeAlias_value', 'guardVersion', 'versionMinorMinimum')
		.collect())

def getElementsTypeAlias(**keywordArguments: Any) -> list[tuple[str, list[ast.expr], int, int]]:
	"""Retrieve and refine TypeAlias definitions for code generation.

	(AI generated docstring)

	This function is the **Runtime Assembly Step**. It queries the
	pre-computed dataframe for TypeAlias information matching the user's
	requested Python version range.

	Because the user's constraints (e.g., 'minimum Python 3.10') may differ
	from the dataframe's full history, pre-computed values alone are not
	enough. This function:
	1. Filters the data to the matching versions.
	2. Identifies whether a TypeAlias needs multiple version-guarded
		definitions or if it can collapse into a single definition.
	3. Applies version guards (`_makeColumn_guardVersion`) to the final set.

	It serves as the bridge between the comprehensive, pre-calculated history
	and the specific requirements of the current generation task.

	Parameters
	----------
	keywordArguments : Any
		Filtering arguments passed to `getDataframe` (e.g.,
		`versionMinorMinimum`, `includeDeprecated`).

	Returns
	-------
	elements : list[tuple[str, list[ast.expr], int, int]]
		A list of tuples, each representing a TypeAlias definition:
		(Identifier, List of Types, Guard Version, Minimum Minor Version).

	"""
	return cast('list[tuple[str, list[ast.expr], int, int]]', _getTableTypeAlias(**keywordArguments).rows())
