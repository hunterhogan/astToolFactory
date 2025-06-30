"""Extract `__match_args__` from Python.asdl across multiple Python versions."""

from astToolFactory import settingsManufacturing, settingsPackage
from astToolkit import identifierDotAttribute
from pathlib import Path
from typing import Any, Protocol, TYPE_CHECKING, TypedDict
from Z0Z_tools import importLogicalPath2Identifier, raiseIfNone
import sys

if TYPE_CHECKING:
	from collections.abc import Callable

# Configuration
filenameAsdl: str = 'Python.asdl'
formatRelativePathVersionMinor = '_py3{versionMinor}'
rangeVersionMinor = range(settingsManufacturing.versionMinor_astMinimumSupported, raiseIfNone(settingsManufacturing.versionMinorMaximum) + 1)
relativePathCpython: str = 'cpython'

class VersionDifferenceData(TypedDict):
	"""Structure for version difference data."""

	versions: list[int]
	match_args: dict[int, tuple[str, ...]]

class AnalysisStatistics(TypedDict):
	"""Structure for analysis statistics."""

	total_classes: int
	stable_classes: int
	variable_classes: int
	versions_analyzed: list[int]

class VersionAnalysisResult(TypedDict):
	"""Structure for version analysis result."""

	stable_classes: list[str]
	version_differences: dict[str, VersionDifferenceData]
	statistics: AnalysisStatistics

class asdlModuleProtocol(Protocol):
	"""Protocol for ASDL parser modules across Python versions.

	(AI generated docstring)

	Defines the interface for ASDL parser modules that can parse Python.asdl files.
	This protocol ensures compatibility across different Python version implementations.

	"""

	def parse(self, pathFilename: str) -> Any:
		"""Parse an ASDL file and return the parsed structure.

		(AI generated docstring)

		Parameters
		----------
		pathFilename : str
			Path to the ASDL file to parse.

		Returns
		-------
		Any
			Parsed ASDL structure containing type definitions.

		"""
		...

class asdlParsedProtocol(Protocol):
	"""Protocol for parsed ASDL structures.

	(AI generated docstring)

	Defines the interface for parsed ASDL structures that contain type definitions.
	The parsed structure provides access to the ASDL definitions through the `dfns` attribute.

	"""

	dfns: list[Any]

def getPathFilename_asdl(versionMinor: int) -> Path:
	"""Create physical path filename for Python.asdl file."""
	relativePathVersionMinor = formatRelativePathVersionMinor.format(versionMinor=versionMinor)
	return settingsPackage.pathPackage / relativePathCpython / relativePathVersionMinor / filenameAsdl

def getLogicalPath_asdl(versionMinor: int) -> identifierDotAttribute:
	"""Create logical path for ASDL module import."""
	relativePathVersionMinor = formatRelativePathVersionMinor.format(versionMinor=versionMinor)
	return f'{settingsPackage.identifierPackage}.{relativePathCpython}.{relativePathVersionMinor}.asdl'

def extract_match_args_ForVersion(versionMinor: int) -> dict[str, tuple[str, ...]]:
	"""Extract `__match_args__` tuples for a specific Python version.

	(AI generated docstring)

	Parses the Python.asdl file for the specified Python version and extracts
	the field names that become `__match_args__` tuples for each AST `class`.
	Handles both Sum types and Product types from the ASDL grammar.

	Parameters
	----------
	versionMinor : int
		Python version minor number (e.g., 10, 11, 12).

	Returns
	-------
	dictionaryMatchArguments : dict[str, tuple[str, ...]]
		Mapping from AST `class` names to their `__match_args__` tuples.

	"""
	asdl_parse: Callable[[str], asdlParsedProtocol] = importLogicalPath2Identifier(getLogicalPath_asdl(versionMinor), 'parse')
	asdlModule: asdlParsedProtocol = asdl_parse(str(getPathFilename_asdl(versionMinor)))

	dictionaryMatchArguments: dict[str, tuple[str, ...]] = {}
	dictionaryMatchArguments["AST"] = ()

	for typeDefinition in asdlModule.dfns:
		typeName = typeDefinition.name
		typeValue = typeDefinition.value

		# Check if this is a Sum type, using duck typing to handle version differences
		if hasattr(typeValue, 'types') and hasattr(typeValue, 'attributes'):
			# Sum types are abstract base classes with multiple constructors
			dictionaryMatchArguments[typeName] = ()

			for constructor in typeValue.types:
				className = constructor.name
				fieldNames = tuple(field.name for field in constructor.fields if field.name is not None)
				dictionaryMatchArguments[className] = fieldNames

		# Check if this is a Product type
		elif hasattr(typeValue, 'fields') and hasattr(typeValue, 'attributes'):
			# Product types have a single constructor
			className = typeName
			fieldNames = tuple(field.name for field in typeValue.fields if field.name is not None)
			dictionaryMatchArguments[className] = fieldNames

	return dictionaryMatchArguments

def extract_match_args_allVersions() -> dict[int, dict[str, tuple[str, ...]]]:
	"""Extract match arguments from all available Python versions.

	(AI generated docstring)

	Extracts `__match_args__` tuples for each configured Python version.
	Uses the configured version range to determine which versions to process.
	Handles missing or invalid versions gracefully by continuing with available versions.

	Returns
	-------
	dictionaryByVersion : dict[str, dict[str, tuple[str, ...]]]
		Mapping from version identifiers to their respective AST `class` match arguments.

	"""
	dictionaryByVersion: dict[int, dict[str, tuple[str, ...]]] = {}

	for versionMinor in rangeVersionMinor:
		dictionaryMatchArgumentsForVersion = extract_match_args_ForVersion(versionMinor)
		dictionaryByVersion[versionMinor] = dictionaryMatchArgumentsForVersion

	return dictionaryByVersion

def getDictionary_match_args() -> dict[str, dict[int, tuple[str, ...]]]:
	"""Create dictionary structured as ClassDefIdentifier -> versionMinorPythonInterpreter -> match_args."""
	dictionaryByVersion: dict[int, dict[str, tuple[str, ...]]] = extract_match_args_allVersions()

	dictionaryByClass: dict[str, dict[int, tuple[str, ...]]] = {}

	for versionMinor, classDict in dictionaryByVersion.items():
		for className, matchArgs in classDict.items():
			if className not in dictionaryByClass:
				dictionaryByClass[className] = {}
			dictionaryByClass[className][versionMinor] = matchArgs

	return dictionaryByClass

def analyzeVersionDifferences(*, write2stdout: bool = False) -> VersionAnalysisResult:
	"""Analyze differences in match arguments across Python versions."""
	dictionaryByClass: dict[str, dict[int, tuple[str, ...]]] = getDictionary_match_args()

	setStableClasses: set[str] = set()
	dictionaryVersionDifferences: dict[str, VersionDifferenceData] = {}

	for className, versionDict in dictionaryByClass.items():
		listMatchArgsAcrossVersions: list[tuple[str, ...]] = list(versionDict.values())

		# Check if match args are identical across all versions
		if len(set(listMatchArgsAcrossVersions)) == 1:
			setStableClasses.add(className)
		else:
			dictionaryVersionDifferences[className] = {
				'versions': sorted(versionDict.keys()),
				'match_args': versionDict
			}

	setVersionsAnalyzed: set[int] = set()
	for versionDict in dictionaryByClass.values():
		setVersionsAnalyzed.update(versionDict.keys())

	resultAnalysis: VersionAnalysisResult = {
		'stable_classes': sorted(setStableClasses),
		'version_differences': dictionaryVersionDifferences,
		'statistics': {
			'total_classes': len(dictionaryByClass),
			'stable_classes': len(setStableClasses),
			'variable_classes': len(dictionaryVersionDifferences),
			'versions_analyzed': sorted(setVersionsAnalyzed)
		}
	}

	if write2stdout:
		ImaIndent = " " * 4
		statistics = resultAnalysis['statistics']

		sys.stdout.write("\n# Version Differences Analysis\n")
		sys.stdout.write(f"# Total classes: {statistics['total_classes']}\n")
		sys.stdout.write(f"# Stable classes: {statistics['stable_classes']}\n")
		sys.stdout.write(f"# Variable classes: {statistics['variable_classes']}\n")
		sys.stdout.write(f"# Versions analyzed: {statistics['versions_analyzed']}\n\n")

		if dictionaryVersionDifferences:
			sys.stdout.write("# Classes with version differences:\n")
			for className in sorted(dictionaryVersionDifferences.keys()):
				sys.stdout.write(f"{ImaIndent}{className}:\n")
				versionData = dictionaryVersionDifferences[className]['match_args']
				for versionMinor in sorted(versionData.keys()):
					matchArgs = versionData[versionMinor]
					if matchArgs:
						argumentsString = ", ".join(f'"{argumentName}"' for argumentName in matchArgs)
						sys.stdout.write(f"{ImaIndent}{ImaIndent}py3{versionMinor}: ({argumentsString})\n")
					else:
						sys.stdout.write(f"{ImaIndent}{ImaIndent}py3{versionMinor}: ()\n")
				sys.stdout.write("\n")

	return resultAnalysis

def main(*, analyzeDifferences: bool = False) -> None:
	"""Extract match arguments from all Python versions and display results."""
	sys.stderr.write("Extracting match arguments from all Python versions...\n")
	dictionaryByClass = getDictionary_match_args()

	ImaIndent = " " * 4
	# Write the unified results as Python code
	sys.stdout.write("\n# Unified AST class __match_args__ extracted from Python.asdl across versions\n")
	sys.stdout.write("# Structure: ClassDefIdentifier -> versionMinorPythonInterpreter -> match_args\n")
	sys.stdout.write("dictionaryMatchArguments_byClassByVersion = {\n")

	for className in sorted(dictionaryByClass.keys()):
		sys.stdout.write(f'{ImaIndent}"{className}": {{\n')
		versionDict = dictionaryByClass[className]

		for versionMinor in sorted(versionDict.keys()):
			matchArgs = versionDict[versionMinor]
			if matchArgs:
				argumentsString = ", ".join(f'"{argumentName}"' for argumentName in matchArgs)
				sys.stdout.write(f'{ImaIndent}{ImaIndent}"{versionMinor}": ({argumentsString}),\n')
			else:
				sys.stdout.write(f'{ImaIndent}{ImaIndent}"{versionMinor}": (),\n')

		sys.stdout.write(f'{ImaIndent}}},\n')

	sys.stdout.write("}\n")

	if analyzeDifferences:
		analyzeVersionDifferences(write2stdout=True)

if __name__ == "__main__":
	main(analyzeDifferences=False)  # Set to True to analyze differences and print them
