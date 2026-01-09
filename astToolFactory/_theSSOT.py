"""Primary: settings for this package.

Secondary: settings for manufacturing.
Tertiary: hardcoded values until I implement a dynamic solution.
"""
from astToolFactory._theSSOTannex import (
	dictionary_astSuperClasses, dictionaryIdentifiers, PackageToManufactureIdentifier, pathPackageToManufacture)
from copy import deepcopy
from hunterMakesPy import PackageSettings
from pathlib import Path
from typing import Any, NamedTuple, NotRequired, TypedDict, TypeVar
import ast
import dataclasses

# TODO In general, now that Py3.9 is not supported, AFAIK, the package doesn't need the "deprecated" flag anymore. IIRC, I created
# it to deal with the deprecated subclasses of `ast.Constant`.

"""Eliminate hardcoding"""
pathRelativeRoot_typeshedHARDCODED: Path = Path('typings/stdlib')
# https://github.com/hunterhogan/astToolFactory/issues/2
versionMinor_astMinimumSupportedHARDCODED = 10

identifierPackagePACKAGING = "astToolFactory"
settingsPackage = PackageSettings(identifierPackageFALLBACK=identifierPackagePACKAGING)

class column__value(NamedTuple):
	"""A column name and its value."""

	column: str
	value: Any

MaskTuple = TypeVar('MaskTuple', bound=NamedTuple, covariant=True)

pathRoot_typeshed: Path = Path(settingsPackage.pathPackage, '..', pathRelativeRoot_typeshedHARDCODED).resolve()

@dataclasses.dataclass(slots=True)
class ManufacturedPackageSettings(PackageSettings):
	astSuperClasses: dict[str, str] = dataclasses.field(default_factory=dict[str, str])
	identifiers: dict[str, str] = dataclasses.field(default_factory=dict[str, str])
	includeDeprecated: bool = False
	keywordArgumentsIdentifier: str = 'keywordArguments'
	pathFilenameDataframeAST: Path = dataclasses.field(default=settingsPackage.pathPackage / 'dataframeAST.pkl')
	pythonMinimumVersionMinor: int = 12
	versionMinor_astMinimumSupported: int = versionMinor_astMinimumSupportedHARDCODED
	versionMinorMaximum: int | None = 14

settings_astToolkit = ManufacturedPackageSettings(
	astSuperClasses=dictionary_astSuperClasses,
	identifierPackage=PackageToManufactureIdentifier,
	identifiers=dictionaryIdentifiers,
	pathPackage=pathPackageToManufacture,
)

settingsManufacturing: ManufacturedPackageSettings = deepcopy(settings_astToolkit)
"""1) An abstract, predictable identifier for the "factory".
2) Infrastructure for more than one `ManufacturedPackageSettings` instance.
It will probably never be used but it's the "right" way to design this."""

class dataTypeVariables(TypedDict):
	"""Data to manufacture a `TypeVar`.

	Attributes
	----------
	constraints : NotRequired[list[ast.expr]]
		List of constraint expressions that limit the type variable to specific types.
	bound : NotRequired[ast.expr]
		Upper bound expression that constrains the type variable to subtypes.
	tuple_keyword : NotRequired[list[tuple[str, bool]]]
		Keyword arguments as tuples of parameter name and boolean value.
	default_value : NotRequired[ast.expr]
		Default value expression for the type variable.

	"""

	constraints: NotRequired[list[ast.expr]]
	bound: NotRequired[ast.expr]
	tuple_keyword: NotRequired[list[tuple[str, bool]]]
	default_value: NotRequired[ast.expr]
