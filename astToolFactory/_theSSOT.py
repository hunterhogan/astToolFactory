"""Primarily: settings for this package.
Secondarily: hardcoded values until I implement a dynamic solution."""
from importlib import import_module as importlib_import_module
from inspect import getfile as inspect_getfile
from pathlib import Path
from tomli import load as tomli_load
import dataclasses

# TODO generate this for astToolkit.
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

pythonVersionMinorMinimum: int = 12
keywordArgumentsIdentifier: str = 'keywordArguments'

listPylanceErrorsHARDCODED: list[str] = ['annotation', 'arg', 'args', 'body', 'keys', 'name', 'names', 'op', 'orelse', 'pattern', 'returns', 'target', 'value',]
listPylanceErrorsHARDCODED.extend(['argtypes', 'bases', 'cases', 'comparators', 'decorator_list', 'defaults', 'elts', 'finalbody', 'generators', 'ifs', 'items',])
listPylanceErrorsHARDCODED.extend(['keywords', 'kw_defaults', 'kwd_patterns', 'ops', 'patterns', 'targets', 'type_params', 'values',])
listPylanceErrorsHARDCODED.extend(['asname', 'bound', 'cause', 'default_value', 'exc', 'format_spec', 'guard', 'kind', 'kwarg',])
listPylanceErrorsHARDCODED.extend(['lower', 'module', 'msg', 'optional_vars', 'rest', 'step', 'type_comment', 'type', 'upper', 'vararg',])

listPylanceErrors = listPylanceErrorsHARDCODED

# NOTE why Z0Z_?
# `settingsPackageToManufacture` is probably an acceptable way to handle this situation.
# But I am dissatisfied with the steps to create the information. On the one hand, `'astToolkit'`
# must be manually set, so I don't want to flag it with HARDCODED. On the other hand, 
# `Z0Z_pathRoot` is obviously specific to my environment. I suspect I need a different paradigm.
Z0Z_pathRoot = Path('/apps') 
Z0Z_PackageToManufactureIdentifier: str = 'astToolkit'
Z0Z_PackageToManufacturePath = Z0Z_pathRoot / Z0Z_PackageToManufactureIdentifier / Z0Z_PackageToManufactureIdentifier
settingsPackageToManufacture = PackageSettings(identifierPackage=Z0Z_PackageToManufactureIdentifier, pathPackage=Z0Z_PackageToManufacturePath)

