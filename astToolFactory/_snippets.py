from astToolFactory import settingsManufacturing
from astToolkit import Make
from typing import cast
import ast

astName_overload = Make.Name('overload')
astName_staticmethod = Make.Name('staticmethod')
astName_typing_TypeAlias: ast.expr = cast(ast.expr, Make.Name('typing_TypeAlias'))
astName_typing_TypeVar: ast.expr = cast(ast.expr, Make.Name('typing_TypeVar'))

# The `format` method continues to disappoint me.
# The type hint hover is merely: (*args: LiteralString, **kwargs: LiteralString) -> LiteralString
# I want to use these format templates to remind me which identifiers to use.
format_hasDOTIdentifier: str = "hasDOT{attribute}"
formatTypeAliasSubcategory: str = "{hasDOTIdentifier}_{TypeAliasSubcategory}"

keywordKeywordArguments4Call = Make.keyword(None, Make.Name(settingsManufacturing.keywordArgumentsIdentifier))
