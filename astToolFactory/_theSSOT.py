"""Primarily: settings for this package.
Secondarily: hardcoded values until I implement a dynamic solution."""
from importlib import import_module as importlib_import_module
from inspect import getfile as inspect_getfile
from pathlib import Path
from tomli import load as tomli_load
import dataclasses

try:
	identifierPackagePACKAGING: str = tomli_load(Path("pyproject.toml").open('rb'))["project"]["name"]
except Exception:
	identifierPackagePACKAGING = "astToolFactory"

def getPathPackageINSTALLING() -> Path:
	pathPackage: Path = Path(inspect_getfile(importlib_import_module(identifierPackagePACKAGING)))
	if pathPackage.is_file():
		pathPackage = pathPackage.parent
	return pathPackage

@dataclasses.dataclass
class PackageSettings:

	fileExtension: str = dataclasses.field(default='.py', metadata={'evaluateWhen': 'installing'})
	"""Default file extension for generated code files."""

	identifierPackage: str = dataclasses.field(default = identifierPackagePACKAGING, metadata={'evaluateWhen': 'packaging'})
	"""Name of this package, used for import paths and configuration."""

	pathPackage: Path = dataclasses.field(default_factory=getPathPackageINSTALLING, metadata={'evaluateWhen': 'installing'})
	"""Absolute path to the installed package directory."""

settingsPackage = PackageSettings()

pythonMinimumVersionMinor: int = 12
keywordArgumentsIdentifier: str = 'keywordArguments'

pathFilenameDataframeAST: Path = settingsPackage.pathPackage / 'dataframeAST.pkl'
versionMinor_astMinimumSupported = 9

dictionaryIdentifiers: dict[str, str] = {
	'Be': 'Be',
	'boolopJoinMethod': '_boolopJoinMethod',
	'ClassIsAndAttribute': 'ClassIsAndAttribute',
	'DOT': 'DOT',
	'Grab': 'Grab',
	'Make': 'Make',
	'operatorJoinMethod': '_operatorJoinMethod',
	}
listPyrightErrorsHARDCODED: list[str] = ['args', 'body', 'keys', 'kw_defaults', 'name', 'names', 'op', 'orelse', 'target', 'value',]

listPyrightErrors = listPyrightErrorsHARDCODED

# NOTE why Z0Z_?
# `settingsPackageToManufacture` is probably an acceptable way to handle this situation.
# But I am dissatisfied with the steps to create the information. On the one hand, `'astToolkit'`
# must be manually set, so I don't want to flag it with HARDCODED. On the other hand,
# `Z0Z_pathRoot` is obviously specific to my environment. I suspect I need a different paradigm.
Z0Z_pathRoot = Path('/apps')
Z0Z_PackageToManufactureIdentifier: str = 'astToolkit'
Z0Z_PackageToManufacturePath = Z0Z_pathRoot / Z0Z_PackageToManufactureIdentifier / Z0Z_PackageToManufactureIdentifier
settingsPackageToManufacture = PackageSettings(identifierPackage=Z0Z_PackageToManufactureIdentifier, pathPackage=Z0Z_PackageToManufacturePath)

isort_codeConfiguration: dict[str, int | str | list[str]] = {
	"combine_as_imports": True,
	"force_alphabetical_sort_within_sections": True,
	"from_first": True,
	"honor_noqa": True,
	"include_trailing_comma": True,
	"indent": "\t",
	"line_length": 100,
	"lines_after_imports": 1,
	"lines_between_types": 0,
	"multi_line_output": 5,
	"no_sections": True,
	"skip": ["__init__.py"],
	"use_parentheses": True,
}

settingsPackageToManufacture.isort_codeConfiguration = isort_codeConfiguration # pyright: ignore[reportAttributeAccessIssue]
dictionary_astSuperClasses: dict[str, str] = {
	'AST': '木',
	'boolop': '布尔符',
	'cmpop': '比符',
	'Constant': '常',
	'excepthandler': '拦',
	'expr_context': '工位',
	'expr': '工',
	'mod': '本',
	'operator': '二符',
	'pattern': '俪',
	'stmt': '口',
	'type_ignore': '忽',
	'type_param': '形',
	'unaryop': '一符',
}