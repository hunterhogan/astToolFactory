from __future__ import annotations

from astToolFactory import settingsManufacturing
from astToolkit import Make
from hunterMakesPy.filesystemToolkit import settings_autoflakeDEFAULT, writePython
from pathlib import PurePosixPath
from typing import cast, TYPE_CHECKING
import ast
import pickle
import polars

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
	pythonSource: str = ast.unparse(astModule)
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
				if "def " + astClass in line:
					# get the last occurrence of the match in the source code
					lineno = splitlinesNumber + 1
			listTypeIgnore.append(Make.TypeIgnore(lineno, tag))
		astModule = ast.parse(pythonSource)
		astModule.type_ignores.extend(listTypeIgnore)
		ast.fix_missing_locations(astModule)
		pythonSource = ast.unparse(astModule)
		pythonSource = "# ruff: noqa: A002\n" + pythonSource
		pythonSource = pythonSource.replace("# type: ignore[", "# pyright: ignore[")
		pythonSource = pythonSource.replace("# type: ignore", "# noqa: ")
	pathFilenameModule: PurePosixPath = PurePosixPath(settingsManufacturing.pathPackage, identifierModule + settingsManufacturing.fileExtension)
	settings: dict[str, dict[str, list[str] | bool]] = {'autoflake': settings_autoflakeDEFAULT}
	cast("list[str]", settings['autoflake']['additional_imports']).append(settingsManufacturing.identifierPackage)
	writePython(pythonSource, pathFilenameModule)
