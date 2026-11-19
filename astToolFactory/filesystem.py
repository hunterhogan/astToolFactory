from __future__ import annotations

from astToolFactory import settingsManufacturing
from astToolkit import Be, Make, NodeChanger
from hunterMakesPy.kitFilesystem import settings_autoflakeDEFAULT, settings_isortDEFAULT, writePython
from inspect import cleandoc
from pathlib import PurePosixPath
from textwrap import indent
from typing import cast, TYPE_CHECKING
import ast
import pickle
import polars
import re as regex

if TYPE_CHECKING:
	from pathlib import Path

def readDataframe(pathFilename: Path) -> polars.DataFrame:
	with pathFilename.open('rb') as file:
		columns: dict[str, list[object]]
		schema: polars.Schema
		columns, schema = pickle.load(file)  # ruff: ignore[suspicious-pickle-usage]
	return polars.DataFrame(columns, schema=schema)

def writeDataframe(dataframe: polars.DataFrame, pathFilename: Path) -> None:
	with pathFilename.open('wb') as file:
		pickle.dump((dataframe.to_dict(as_series=False), dataframe.schema), file)

def gatherObjects(values: polars.Series, indices: polars.Series) -> polars.Series:
	return polars.Series(values.name, map(polars.Series.to_list, map(values.gather, indices)), dtype=polars.Object)

def _indentDocstring(astExpr: ast.Expr) -> ast.Expr:
	if Be.Constant(astExpr.value) and isinstance(docstring := astExpr.value.value, str) and '\n' in docstring:
		astExpr.value.value = cleandoc(docstring)
		summary, newline, description = astExpr.value.value.partition('\n')
		if newline:
			indentation: str = ' ' * astExpr.col_offset
			astExpr.value.value = summary + newline + indent(description, indentation) + newline + indentation
	return astExpr

def writeModule(astModule: ast.Module, identifierModule: str) -> None:
	"""Write an AST module to disk, handling type ignores and formatting.

	Parameters
	----------
	astModule : ast.Module
		The AST module to write.
	identifierModule : str
		The stem for the module file.
	"""
	ast.fix_missing_locations(astModule)
	# The first unparse establishes the column of each docstring in the generated source.
	astModule = ast.parse(ast.unparse(astModule), type_comments=True)
	pythonSource: str = ast.unparse(NodeChanger(Be.Expr, _indentDocstring).visit(astModule))
# TODO https://github.com/hunterhogan/astToolFactory/issues/3
	if "Grab" in identifierModule:
		pythonSource = "# ruff: noqa: B009, B010\n" + pythonSource

	if "Make" in identifierModule:

		listTypeIgnore: list[ast.TypeIgnore] = []
		lineno: int = 0
		for astClass, tag in [
			("keyword", "[reportInconsistentOverload]"),
			("MatchClass", "[reportSelfClsParameterName]"),
			("MatchSingleton", "FBT001"),
		]:
			for splitlinesNumber, line in enumerate(pythonSource.splitlines()):
				if line.lstrip().startswith(f"def {astClass}("):
					# get the last occurrence of the match in the source code
					lineno = splitlinesNumber + 1
			listTypeIgnore.append(Make.TypeIgnore(lineno, tag))
		astModule = ast.parse(pythonSource)
		astModule.type_ignores.extend(listTypeIgnore)
		ast.fix_missing_locations(astModule)
		pythonSource = ast.unparse(astModule)
		pythonSource = "# ruff: noqa: A002\n" + pythonSource
		pythonSource = regex.sub(r"(?m)^([ ]+def (?:keyword|MatchClass)\(.*) # type: ignore(?=\[)"
			, r"\1 # pyright: ignore", pythonSource)
		pythonSource = regex.sub(r"(?m)^([ ]+def MatchSingleton\(.*) # type: ignore(?=FBT001$)"
			, r"\1 # noqa: ", pythonSource)
	pathFilenameModule: PurePosixPath = PurePosixPath(settingsManufacturing.pathPackage, identifierModule + settingsManufacturing.fileExtension)
	writePython(pythonSource, pathFilenameModule, settings={
		'autoflake': {
			**settings_autoflakeDEFAULT,
			'additional_imports': [*cast('list[str]', settings_autoflakeDEFAULT['additional_imports']), settingsManufacturing.identifierPackage],
		},
		'isort': {**settings_isortDEFAULT, 'indent': '    '},
	})
