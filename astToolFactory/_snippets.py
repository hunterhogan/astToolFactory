from astToolFactory import settingsManufacturing
from astToolkit import Make
from typing import cast
import ast

astASTastAttribute: ast.expr = Make.Attribute(Make.Name('ast'), 'AST')
astAttribute_builtins_str: ast.expr = Make.Attribute(Make.Name('builtins'), 'str')
astName_classmethod: ast.expr = Make.Name('classmethod')
astName_overload: ast.expr = Make.Name('overload')
astName_staticmethod: ast.expr = Make.Name('staticmethod')
astName_typing_TypeAlias: ast.expr = cast(ast.expr, Make.Name('typing_TypeAlias'))
astName_typing_TypeVar: ast.expr = cast(ast.expr, Make.Name('typing_TypeVar'))
astSubscriptUnpack_ast_attributes: ast.expr = Make.Subscript(Make.Name('Unpack'), slice=Make.Name('ast_attributes'))

# The `format` method continues to disappoint me.
# The type hint hover is merely: (*args: LiteralString, **kwargs: LiteralString) -> LiteralString
# I want to use these format templates to remind me which identifiers to use.
format_hasDOTIdentifier: str = "hasDOT{attribute}"
formatTypeAliasSubcategory: str = "{hasDOTIdentifier}_{TypeAliasSubcategory}"

keywordKeywordArguments4Call: ast.keyword = Make.keyword(None, Make.Name(settingsManufacturing.keywordArgumentsIdentifier))
