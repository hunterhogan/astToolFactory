"""Primary: settings for this package.

Secondary: settings for manufacturing.
Tertiary: hardcoded values until I implement a dynamic solution.
"""
from astToolFactory._theSSOTannex import (
	autoflakeSettings, dictionary_astSuperClasses, dictionaryIdentifiers, isort_codeConfiguration,
	PackageToManufactureIdentifier, pathPackageToManufacture)
from copy import deepcopy
from hunterMakesPy import PackageSettings
from pathlib import Path
from typing import Any, NamedTuple, TypeVar
import dataclasses

"""Eliminate hardcoding"""
pathRelativeRoot_typeshedHARDCODED: Path = Path('typings/stdlib')
# https://github.com/hunterhogan/astToolFactory/issues/2
versionMinor_astMinimumSupportedHARDCODED = 9

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
	autoflake: dict[str, bool] = dataclasses.field(default_factory=dict[str, bool])
	identifiers: dict[str, str] = dataclasses.field(default_factory=dict[str, str])
	includeDeprecated: bool = False
	isort_code: dict[str, int | str | list[str]] = dataclasses.field(default_factory=dict[str, int | str | list[str]])
	keywordArgumentsIdentifier: str = 'keywordArguments'
	pathFilenameDataframeAST: Path = dataclasses.field(default=settingsPackage.pathPackage / 'dataframeAST.pkl')
	pythonMinimumVersionMinor: int = 12
	versionMinor_astMinimumSupported: int = versionMinor_astMinimumSupportedHARDCODED
	versionMinorMaximum: int | None = 13

settings_astToolkit = ManufacturedPackageSettings(
	astSuperClasses=dictionary_astSuperClasses,
	autoflake=autoflakeSettings,
	identifierPackage=PackageToManufactureIdentifier,
	identifiers=dictionaryIdentifiers,
	isort_code=isort_codeConfiguration,
	pathPackage=pathPackageToManufacture,
)

settingsManufacturing: ManufacturedPackageSettings = deepcopy(settings_astToolkit)
"""1) An abstract, predictable identifier for the "factory"
2) Infrastructure for more than one `ManufacturedPackageSettings` instance.
It will probably never be used but it's the "right" way to design this."""
