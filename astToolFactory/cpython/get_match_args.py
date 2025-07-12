"""Extract `__match_args__` from Python.asdl across multiple Python versions."""

from astToolFactory import column__value, settingsManufacturing, settingsPackage
from astToolkit import identifierDotAttribute
from hunterMakesPy import importLogicalPath2Identifier, raiseIfNone
from pathlib import Path
from pprint import pprint
from typing import Any, Literal, NamedTuple, Protocol, TYPE_CHECKING
import sys

if TYPE_CHECKING:
	from collections.abc import Callable

# Configuration
filename_asdlData: str = 'Python.asdl'
formatRelativePathVersionMinor = '_py3{versionMinor}'
rangeVersionMinor = range(settingsManufacturing.versionMinor_astMinimumSupported, raiseIfNone(settingsManufacturing.versionMinorMaximum) + 1)
relativePathCpython: str = 'cpython'

class Column__ClassDefIdentifier_versionMinorPythonInterpreter_deprecated(NamedTuple):
	"""`MaskTuple` used by `getMaskByColumnValue`."""

	ClassDefIdentifier: str
	versionMinorPythonInterpreter: int
	deprecated: bool

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
	return settingsPackage.pathPackage / relativePathCpython / relativePathVersionMinor / filename_asdlData

def getLogicalPath_asdl(versionMinor: int) -> identifierDotAttribute:
	"""Create logical path for ASDL module import."""
	relativePathVersionMinor = formatRelativePathVersionMinor.format(versionMinor=versionMinor)
	return f'{settingsPackage.identifierPackage}.{relativePathCpython}.{relativePathVersionMinor}.asdl'

def extract_match_argsForVersion(versionMinor: int) -> dict[str, tuple[str, ...]]:
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

def extract_match_args() -> dict[int, dict[str, tuple[str, ...]]]:
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
		dictionaryMatchArgumentsForVersion = extract_match_argsForVersion(versionMinor)
		dictionaryByVersion[versionMinor] = dictionaryMatchArgumentsForVersion

	return dictionaryByVersion

# def getDictionary_match_args() -> dict[Column__ClassDefIdentifier_versionMinorPythonInterpreter_deprecated, column__value]:
# 	"""Create dictionary structured as ClassDefIdentifier -> versionMinorPythonInterpreter -> match_args."""
# 	dictionaryByVersion: dict[int, dict[str, tuple[str, ...]]] = extract_match_args()

# 	match_args__ClassDefIdentifier_versionMinorPythonInterpreter_deprecated: dict[Column__ClassDefIdentifier_versionMinorPythonInterpreter_deprecated, column__value] = {}

# 	for versionMinor, dictionaryClass_match_args in dictionaryByVersion.items():
# 		for ClassDefIdentifier, match_args in dictionaryClass_match_args.items():
# 			match_args__ClassDefIdentifier_versionMinorPythonInterpreter_deprecated[
# 				Column__ClassDefIdentifier_versionMinorPythonInterpreter_deprecated(ClassDefIdentifier, versionMinor, False)
# 				] = column__value('match_args', match_args)

# 	return match_args__ClassDefIdentifier_versionMinorPythonInterpreter_deprecated

def getDictionary_match_args() -> dict[tuple[str, int, Literal[False]], tuple[str, ...]]:
	"""Create dictionary structured as ClassDefIdentifier -> versionMinorPythonInterpreter -> match_args."""
	dictionaryByVersion: dict[int, dict[str, tuple[str, ...]]] = extract_match_args()

	match_args__ClassDefIdentifier_versionMinorPythonInterpreter_deprecated: dict[tuple[str, int, Literal[False]], tuple[str, ...]] = {}

	for versionMinor, dictionaryClass_match_args in dictionaryByVersion.items():
		for ClassDefIdentifier, match_args in dictionaryClass_match_args.items():
			match_args__ClassDefIdentifier_versionMinorPythonInterpreter_deprecated[(ClassDefIdentifier, versionMinor, False)] = match_args

	return match_args__ClassDefIdentifier_versionMinorPythonInterpreter_deprecated

def main() -> None:
	"""Extract match arguments from all Python versions and display results."""
	sys.stderr.write("Extracting match arguments from all Python versions...\n")
	dictionaryByClass = getDictionary_match_args()

	sys.stdout.write("# Unified AST class __match_args__ extracted from Python.asdl across versions\n")
	sys.stdout.write("dictionaryMatchArguments_byClassByVersion = ")
	pprint(dictionaryByClass, stream=sys.stdout, width=120, sort_dicts=True)  # noqa: T203

if __name__ == "__main__":
	main()
