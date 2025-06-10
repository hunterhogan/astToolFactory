from astToolFactory._theSSOT import (
	listPyrightErrors as listPyrightErrors,
	settingsPackage as settingsPackage,
	settingsManufacturing as settingsManufacturing,
    ManufacturedPackageSettings as ManufacturedPackageSettings,
)

from astToolFactory._snippets import (
	astName_overload as astName_overload,
	astName_staticmethod as astName_staticmethod,
	astName_typing_TypeAlias as astName_typing_TypeAlias,
	astName_typing_TypeVar as astName_typing_TypeVar,
	format_hasDOTIdentifier as format_hasDOTIdentifier,
	formatTypeAliasSubcategory as formatTypeAliasSubcategory,
	keywordKeywordArguments4Call as keywordKeywordArguments4Call,
)

# change to _datacenter to obfuscate the source of the data: it could change
from astToolFactory.datacenter import (
	getElementsBe as getElementsBe,
	getElementsClassIsAndAttribute as getElementsClassIsAndAttribute,
	getElementsDOT as getElementsDOT,
	getElementsGrab as getElementsGrab,
	getElementsMake as getElementsMake,
	getElementsTypeAlias as getElementsTypeAlias,
)
