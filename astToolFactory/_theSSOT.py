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

# ww='''
# @classmethod
# def join(cls, expressions: Iterable[ast.expr], **keywordArguments: Unpack[_Attributes]) -> ast.expr:
# 	return operatorJoinMethod(cls, expressions, **keywordArguments)
# '''

# print(ast.dump(ast.parse(ww, type_comments=True), indent=None))
# import ast
# from ast import *  # noqa: E402, F403
# ruff: noqa: F405

# rr='''
# Assign(lineno=0,col_offset=0, [ast.Name('key', ast.Store())], value=Lambda(args=arguments(args=[arg('x', annotation=ast.Attribute(ast.Name('pandas'), 'Series'))]), body=Call(ast.Attribute(Attribute(ast.Name('x'), attr='str'), attr='lower'))))
# '''

# print(ast.unparse(ast.Module([eval(rr)])))

