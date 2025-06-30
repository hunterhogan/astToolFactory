"""Primary: settings for this package.

Secondary: settings for manufacturing.
Tertiary: hardcoded values until I implement a dynamic solution.
"""
from copy import deepcopy
from importlib import import_module as importlib_import_module
from inspect import getfile as inspect_getfile
from pathlib import Path
from tomli import loads as tomli_loads
import dataclasses

"""Eliminate hardcoding"""
listPyrightErrorsHARDCODED: list[str] = ['args', 'body', 'keys', 'kw_defaults', 'name', 'names', 'op', 'orelse', 'target', 'value']
listPyrightErrors: list[str] = listPyrightErrorsHARDCODED
# TODO Can I dynamically set this by reading it from typeshed or somewhere else?
# The value will change once a year
versionMinor_astMinimumSupportedHARDCODED = 9
pathRelativeRoot_typeshedHARDCODED: Path = Path('typings/stdlib')

try:
	identifierPackagePACKAGING: str = tomli_loads(Path("../pyproject.toml").read_text())["project"]["name"]
except Exception:  # noqa: BLE001
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

pathRoot_typeshed: Path = Path(settingsPackage.pathPackage, '..', pathRelativeRoot_typeshedHARDCODED)

@dataclasses.dataclass
class ManufacturedPackageSettings(PackageSettings):
	isort_code: dict[str, int | str | list[str]] = dataclasses.field(default_factory=dict[str, int | str | list[str]])
	identifiers: dict[str, str] = dataclasses.field(default_factory=dict[str, str])
	astSuperClasses: dict[str, str] = dataclasses.field(default_factory=dict[str, str])
	pythonMinimumVersionMinor: int = 12
	pathFilenameDataframeAST: Path = dataclasses.field(default=settingsPackage.pathPackage / 'dataframeAST.pkl')
	keywordArgumentsIdentifier: str = 'keywordArguments'
	versionMinor_astMinimumSupported: int = versionMinor_astMinimumSupportedHARDCODED
	includeDeprecated: bool = False
	versionMinorMaximum: int | None = 13

PackageToManufactureIdentifier: str = 'astToolkit'
# NOTE why Z0Z_?
# `settingsPackageToManufacture` is probably an acceptable way to handle this situation.
# But I am dissatisfied with the steps to create the information. On the one hand, `'astToolkit'`
# must be manually set, so I don't want to flag it with HARDCODED. On the other hand,
# `Z0Z_pathRoot` is obviously specific to my environment. I suspect I need a different paradigm.
Z0Z_pathRoot = Path('/apps')
Z0Z_PackageToManufacturePath = Z0Z_pathRoot / PackageToManufactureIdentifier / PackageToManufactureIdentifier

dictionaryIdentifiers: dict[str, str] = {
	'Be': 'Be',
	'boolopJoinMethod': '_boolopJoinMethod',
	'DOT': 'DOT',
	'Grab': 'Grab',
	'Make': 'Make',
	'operatorJoinMethod': '_operatorJoinMethod',
}

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

# TODO Settings for isort are currently in two places: here and my personal VS Code JSON settings file.
# I don't know how to create a single _authority_ for the settings. "EditorConfig" might be relevant.
isort_codeConfiguration: dict[str, int | str | list[str]] = {
	"combine_as_imports": True,
	"force_alphabetical_sort_within_sections": True,
	"from_first": True,
	"honor_noqa": True,
	"include_trailing_comma": True,
	"indent": "\t",
	"line_length": 120,
	"lines_after_imports": 1,
	"lines_between_types": 0,
	"multi_line_output": 5,
	"no_sections": True,
	"skip": ["__init__.py"],
	"use_parentheses": True,
}

settings_astToolkit = ManufacturedPackageSettings(
	identifierPackage=PackageToManufactureIdentifier,
	pathPackage=Z0Z_PackageToManufacturePath,
	identifiers=dictionaryIdentifiers,
	isort_code=isort_codeConfiguration,
	astSuperClasses=dictionary_astSuperClasses,
)

# 1) An abstract, predictable identifier for the "factory"
# 2) Infrastructure for more than one group of settings
# It will probably never be used but it's the "right" way to design this
settingsManufacturing: ManufacturedPackageSettings = deepcopy(settings_astToolkit)
