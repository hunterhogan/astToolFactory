"""Primary: settings for this package.

Secondary: settings for manufacturing.
Tertiary: hardcoded values until I implement a dynamic solution.
"""

from astToolFactory import dictionary_astSuperClasses, dictionaryIdentifiers, noMinimum
from copy import deepcopy
from hunterMakesPy import PackageSettings
from pathlib import Path
import dataclasses

# ======= HARDCODED values. TODO: eliminate ======================
# https://github.com/hunterhogan/astToolFactory/issues/2
versionMinorTypeshed_astMinimumSupportedHARDCODED: int = 10
pathRelativeRoot_typeshedHARDCODED: Path = Path('typings/stdlib')
pathRootPackageToManufactureHARDCODED: Path = Path('/apps')

# ======= Settings for the package ===============================

identifierPackagePACKAGING = "astToolFactory"
settingsPackage = PackageSettings(identifierPackageFALLBACK=identifierPackagePACKAGING)
"""Settings for the `astToolFactory` package itself.

(AI generated docstring)

Contains path resolution and package identification for the running tool.

Attributes
----------
identifierPackage : str
    The name of the package ("astToolFactory").
pathPackage : Path
    The resolved path to the package root.

"""

# ======= Settings for manufacturing ===============================

# ------- define `ManufacturedPackageSettings` as a subclass of `PackageSettings` --------

# NOTE Reminder: `PackageSettings` has default values, so all fields in this subclass must have defaults.
@dataclasses.dataclass(slots=True)
class ManufacturedPackageSettings(PackageSettings):
	astSuperClasses: dict[str, str] = dataclasses.field(default_factory=dict[str, str])
	identifiers: dict[str, str] = dataclasses.field(default_factory=dict[str, str])
	includeDeprecated: bool = False
	keywordArgumentsIdentifier: str = 'keywordArguments'
	pathFilenameDataframeAST: Path = dataclasses.field(default=settingsPackage.pathPackage / 'dataframeAST.pkl')
	pythonMinimumVersionMinor: int = noMinimum
	versionMinor_astMinimumSupported: int = noMinimum
	versionMinorMaximum: int = 9001

# ------- Settings for manufacturing `astToolkit` --------

pathRootPackageToManufacture: Path = pathRootPackageToManufactureHARDCODED

PackageToManufactureIdentifier: str = 'astToolkit'
pathFilenameDataframeAST: Path = settingsPackage.pathPackage / 'datacenter' / '_dataframeAST.pkl'
pathPackageToManufacture: Path = Path(pathRootPackageToManufacture, PackageToManufactureIdentifier, PackageToManufactureIdentifier).resolve()
pathRoot_typeshed: Path = Path(settingsPackage.pathPackage, '..', pathRelativeRoot_typeshedHARDCODED).resolve()
versionMinorTypeshed_astMinimumSupported: int = versionMinorTypeshed_astMinimumSupportedHARDCODED

settings_astToolkit = ManufacturedPackageSettings(
	astSuperClasses=dictionary_astSuperClasses,
	identifierPackage=PackageToManufactureIdentifier,
	identifiers=dictionaryIdentifiers,
	pathFilenameDataframeAST=pathFilenameDataframeAST,
	pathPackage=pathPackageToManufacture,
	pythonMinimumVersionMinor=12,
	versionMinor_astMinimumSupported=versionMinorTypeshed_astMinimumSupported,
	versionMinorMaximum=14,
)

# ------- Abstracted settings identifier to use in the package --------

"""NOTE 1) An abstract, predictable identifier for the "factory".
2) Infrastructure for more than one `ManufacturedPackageSettings` instance.
It will probably never be used but it's the "right" way to design this."""

settingsManufacturing: ManufacturedPackageSettings = deepcopy(settings_astToolkit)
"""Configuration for the manufacturing process.

(AI generated docstring)

This settings object controls how the `astToolkit` (or other target package)
is manufactured.

Attributes
----------
astSuperClasses : dict[str, str]
    Mapping of AST node names to their superclass names.
identifiers : dict[str, str]
    Mapping of internal identifiers to their external names.
includeDeprecated : bool = False
    Whether to include deprecated AST nodes.
keywordArgumentsIdentifier : str = "keywordArguments"
    The identifier to use for keyword arguments.
pathFilenameDataframeAST : Path
    Path to the pickle file containing the AST dataframe.
pythonMinimumVersionMinor : int
    The minimum supported Python minor version.
versionMinor_astMinimumSupported : int
    The minimum supported AST minor version from typeshed.
versionMinorMaximum : int = 9001
    The maximum supported Python minor version.
identifierPackage : str
    The name of the package being manufactured.
pathPackage : Path
    The root path of the package being manufactured.

"""

