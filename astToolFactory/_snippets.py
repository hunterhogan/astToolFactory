from astToolFactory import settingsManufacturing
from astToolkit import Make
from typing import cast
import ast

astASTastAttribute = Make.Attribute(Make.Name("ast"), "AST")
astName_overload = Make.Name('overload')
astName_classmethod = Make.Name('classmethod')
astName_staticmethod = Make.Name('staticmethod')
astName_typing_TypeAlias: ast.expr = cast(ast.expr, Make.Name('typing_TypeAlias'))
astName_typing_TypeVar: ast.expr = cast(ast.expr, Make.Name('typing_TypeVar'))
astSubscriptUnpack_ast_attributes = Make.Subscript(Make.Name('Unpack'), slice=Make.Name('ast_attributes'))

# The `format` method continues to disappoint me.
# The type hint hover is merely: (*args: LiteralString, **kwargs: LiteralString) -> LiteralString
# I want to use these format templates to remind me which identifiers to use.
format_hasDOTIdentifier: str = "hasDOT{attribute}"
formatTypeAliasSubcategory: str = "{hasDOTIdentifier}_{TypeAliasSubcategory}"

keywordKeywordArguments4Call = Make.keyword(None, Make.Name(settingsManufacturing.keywordArgumentsIdentifier))
