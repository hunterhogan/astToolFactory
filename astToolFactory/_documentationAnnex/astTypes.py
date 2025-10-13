"""A warehouse for docstrings added to manufactured ast tools.

NOTE Use special indentation in this file.
    1. The generated files use spaces, not tabs, so use spaces here.
    2. As of this writing, I only know how to _manually_ align the indentation of the docstrings with the associated code. So,
        indent one or two levels as appropriate.
"""
from astToolFactory import settingsManufacturing
from astToolFactory.documentation import (
	aDocument, dictionary_astClasses, diminutive2etymology, Docstring, docstrings, make1docstring)
from astToolkit import Make

def formatSubclassesOxford(subclassList: list[str]) -> str:
	"""Format a list of subclass names as an Oxford comma series."""
	if not subclassList:
		return ''
	if len(subclassList) == 1:
		return f'`ast.{subclassList[0]}`'
	if len(subclassList) == 2:
		return f'`ast.{subclassList[0]}` and `ast.{subclassList[1]}`'
	return ', '.join(f'`ast.{name}`' for name in subclassList[:-1]) + f', and `ast.{subclassList[-1]}`'

identifierToolClass: str = settingsManufacturing.identifiers['types']
listDocstring: list[Docstring] = []

"""NOTE docstring contents
bound
covariant
if bound, list of subclasses.
pinyin
meaning of the character
if part of a semiotic group, compare and contrast, e.g., 一符, 二符, 布尔符, and 比符
unicode value
"""

identifier = '个'
listDocstring.append(Docstring(identifier
	, summary=aDocument(f"Generic `TypeVar` ({diminutive2etymology['TypeVar']}).")
	, uncategorized=aDocument(f"The ideograph '{identifier}' (gè) is a generic measure word. Its decimal unicode is {ord(identifier)}.")
))
del identifier

identifier = '归个'
identifier个 = '个'
listDocstring.append(Docstring(identifier
	, summary=aDocument(f"Generic `return` `TypeVar` ({diminutive2etymology['TypeVar']}).")
	, uncategorized=aDocument(
		f"The ideograph '归' (guī) means 'return'. Its decimal unicode is {ord('归')}. "
		f"The ideograph '{identifier个}' (gè) is a generic measure word. Its decimal unicode is {ord(identifier个)}. "
		f"`{identifier}` is often paired with `{identifier个}` when the `return` type may differ from the parameter type.")
))
del identifier, identifier个

identifier = '文件'
listDocstring.append(Docstring(identifier
	, summary=aDocument(f"Dictionary key `TypeVar` ({diminutive2etymology['TypeVar']}).")
	, uncategorized=aDocument(f"The ideograph '{identifier}' (wénjiàn) means 'dictionary key'. Its decimal unicode is {ord(identifier[0])} and {ord(identifier[1])}.")
))
del identifier

identifier = '文义'
identifier文件 = '文件'
listDocstring.append(Docstring(identifier
	, summary=aDocument(f"Dictionary value `TypeVar` ({diminutive2etymology['TypeVar']}).")
	, uncategorized=aDocument(f"The ideograph '{identifier}' (wényì) means 'dictionary value'. Its decimal unicode is {ord(identifier[0])} and {ord(identifier[1])}. `{identifier}` is often paired with `{identifier文件}` for dictionary type parameters.")
))
del identifier, identifier文件

identifier = '木'
bound = 'AST'
astClassInfo = dictionary_astClasses[bound]
subclassesFormatted = formatSubclassesOxford(astClassInfo['subclasses'])
listDocstring.append(Docstring(identifier
	, summary=aDocument(f"`{bound}` `TypeVar` ({diminutive2etymology['TypeVar']}) bound to `ast.{bound}`.")
	, uncategorized=aDocument(
		f"The ideograph '{identifier}' (mù) means 'tree', short for abstract syntax tree. Its decimal unicode is {ord(identifier)}. "
		f"This `covariant` `TypeVar` is bound to `ast.{bound}`, the base class for all AST nodes, and its subclasses, {subclassesFormatted}.")
))
del bound, astClassInfo, subclassesFormatted, identifier

identifier = '本'
bound = 'mod'
astClassInfo = dictionary_astClasses[bound]
subclassesFormatted = formatSubclassesOxford(astClassInfo['subclasses'])
listDocstring.append(Docstring(identifier
	, summary=aDocument(f"`{bound}` `TypeVar` ({diminutive2etymology['TypeVar']}) bound to `ast.{bound}`.")
	, uncategorized=aDocument(
		f"The ideograph '{identifier}' (běn) means 'module'. Its decimal unicode is {ord(identifier)}. "
		f"This `covariant` `TypeVar` is bound to `ast.{bound}`, the base class for module-level AST nodes, and its subclasses, {subclassesFormatted}.")
))
del bound, astClassInfo, subclassesFormatted, identifier

identifier = '口'
bound = 'stmt'
astClassInfo = dictionary_astClasses[bound]
subclassesFormatted = formatSubclassesOxford(astClassInfo['subclasses'])
listDocstring.append(Docstring(identifier
	, summary=aDocument(f"`{bound}` `TypeVar` ({diminutive2etymology['TypeVar']}) bound to `ast.{bound}`.")
	, uncategorized=aDocument(
		f"The ideograph '{identifier}' (kǒu) means 'statement'. Its decimal unicode is {ord(identifier)}. "
		f"This `covariant` `TypeVar` is bound to `ast.{bound}` and its subclasses, {subclassesFormatted}.")
))
del bound, astClassInfo, subclassesFormatted, identifier

identifier = '工'
bound = 'expr'
astClassInfo = dictionary_astClasses[bound]
subclassesFormatted = formatSubclassesOxford(astClassInfo['subclasses'])
listDocstring.append(Docstring(identifier
	, summary=aDocument(f"`{bound}` `TypeVar` ({diminutive2etymology['TypeVar']}) bound to `ast.{bound}`.")
	, uncategorized=aDocument(
		f"The ideograph '{identifier}' (gōng) means 'expression'. Its decimal unicode is {ord(identifier)}. "
		f"This `covariant` `TypeVar` is bound to `ast.{bound}`, the base class for all expression nodes, and its subclasses, {subclassesFormatted}.")
))
del bound, astClassInfo, subclassesFormatted, identifier

identifier = '工位'
bound = 'expr_context'
astClassInfo = dictionary_astClasses[bound]
subclassesFormatted = formatSubclassesOxford(astClassInfo['subclasses'])
listDocstring.append(Docstring(identifier
	, summary=aDocument(f"`{bound}` `TypeVar` ({diminutive2etymology['TypeVar']}) bound to `ast.{bound}`.")
	, uncategorized=aDocument(
		f"The ideograph '{identifier}' (gōngwèi) means 'expression context'. Its decimal unicode is {ord(identifier[0])} and {ord(identifier[1])}. "
		f"This `covariant` `TypeVar` is bound to `ast.{bound}`, representing whether an expression appears in loading, storing, or deleting context, and its subclasses, {subclassesFormatted}.")
))
del bound, astClassInfo, subclassesFormatted, identifier

identifier = '一符'
bound = 'unaryop'
astClassInfo = dictionary_astClasses[bound]
subclassesFormatted = formatSubclassesOxford(astClassInfo['subclasses'])
listDocstring.append(Docstring(identifier
	, summary=aDocument(f"`{bound}` `TypeVar` ({diminutive2etymology['TypeVar']}) bound to `ast.{bound}`.")
	, uncategorized=aDocument(
		f"The ideograph '{identifier}' (yīfú) means 'unary operator'. Its decimal unicode is {ord(identifier[0])} and {ord(identifier[1])}. "
		f"This `covariant` `TypeVar` is bound to `ast.{bound}`, representing unary operators like negation and bitwise NOT, and its subclasses, {subclassesFormatted}.")
))
del bound, astClassInfo, subclassesFormatted, identifier

identifier = '二符'
bound = 'operator'
astClassInfo = dictionary_astClasses[bound]
subclassesFormatted = formatSubclassesOxford(astClassInfo['subclasses'])
listDocstring.append(Docstring(identifier
	, summary=aDocument(f"`{bound}` `TypeVar` ({diminutive2etymology['TypeVar']}) bound to `ast.{bound}`.")
	, uncategorized=aDocument(
		f"The ideograph '{identifier}' (èrfú) means 'binary operator'. Its decimal unicode is {ord(identifier[0])} and {ord(identifier[1])}. "
		f"This `covariant` `TypeVar` is bound to `ast.{bound}`, representing binary operators like addition and multiplication, and its subclasses, {subclassesFormatted}.")
))
del bound, astClassInfo, subclassesFormatted, identifier

identifier = '比符'
bound = 'cmpop'
astClassInfo = dictionary_astClasses[bound]
subclassesFormatted = formatSubclassesOxford(astClassInfo['subclasses'])
listDocstring.append(Docstring(identifier
	, summary=aDocument(f"`{bound}` `TypeVar` ({diminutive2etymology['TypeVar']}) bound to `ast.{bound}`.")
	, uncategorized=aDocument(
		f"The ideograph '{identifier}' (bǐfú) means 'comparison operator'. Its decimal unicode is {ord(identifier[0])} and {ord(identifier[1])}. "
		f"This `covariant` `TypeVar` is bound to `ast.{bound}`, representing comparison operators like less than and equality, and its subclasses, {subclassesFormatted}. "
		f"Together with '一符' (unary), '二符' (binary), and '布尔符' (boolean), these form a semiotic system for operator types.")
))
del bound, astClassInfo, subclassesFormatted, identifier

identifier = '布尔符'
bound = 'boolop'
astClassInfo = dictionary_astClasses[bound]
subclassesFormatted = formatSubclassesOxford(astClassInfo['subclasses'])
listDocstring.append(Docstring(identifier
	, summary=aDocument(f"`{bound}` `TypeVar` ({diminutive2etymology['TypeVar']}) bound to `ast.{bound}`.")
	, uncategorized=aDocument(
		f"The ideograph '{identifier}' (bùěrfú) means 'boolean operator'. Its decimal unicode is {ord(identifier[0])}, {ord(identifier[1])}, and {ord(identifier[2])}. "
		f"This `covariant` `TypeVar` is bound to `ast.{bound}`, representing boolean operators `and` and `or`, and its subclasses, {subclassesFormatted}. "
		f"Together with '一符' (unary), '二符' (binary), and '比符' (comparison), these form a semiotic system for operator types.")
))
del bound, astClassInfo, subclassesFormatted, identifier

identifier = '常'
bound = 'Constant'
astClassInfo = dictionary_astClasses[bound]
subclassesFormatted = formatSubclassesOxford(astClassInfo['subclasses'])
listDocstring.append(Docstring(identifier
	, summary=aDocument(f"`{bound}` `TypeVar` ({diminutive2etymology['TypeVar']}) bound to `ast.{bound}`.")
	, uncategorized=aDocument(
		f"The ideograph '{identifier}' (cháng) means 'constant'. Its decimal unicode is {ord(identifier)}. "
		f"This `covariant` `TypeVar` is bound to `ast.{bound}`, representing literal constant values in Python code, and its subclasses, {subclassesFormatted}.")
))
del bound, astClassInfo, subclassesFormatted, identifier

identifier = '拦'
bound = 'excepthandler'
astClassInfo = dictionary_astClasses[bound]
subclassesFormatted = formatSubclassesOxford(astClassInfo['subclasses'])
listDocstring.append(Docstring(identifier
	, summary=aDocument(f"`{bound}` `TypeVar` ({diminutive2etymology['TypeVar']}) bound to `ast.{bound}`.")
	, uncategorized=aDocument(
		f"The ideograph '{identifier}' (lán) means 'exception handler'. Its decimal unicode is {ord(identifier)}. "
		f"This `covariant` `TypeVar` is bound to `ast.{bound}`, representing `except` clauses in try statements, and its subclasses, {subclassesFormatted}.")
))
del bound, astClassInfo, subclassesFormatted, identifier

identifier = '俪'
bound = 'pattern'
astClassInfo = dictionary_astClasses[bound]
subclassesFormatted = formatSubclassesOxford(astClassInfo['subclasses'])
listDocstring.append(Docstring(identifier
	, summary=aDocument(f"`{bound}` `TypeVar` ({diminutive2etymology['TypeVar']}) bound to `ast.{bound}`.")
	, uncategorized=aDocument(
		f"The ideograph '{identifier}' (lì) means 'pattern'. Its decimal unicode is {ord(identifier)}. "
		f"This `covariant` `TypeVar` is bound to `ast.{bound}`, representing patterns used in structural pattern matching, and its subclasses, {subclassesFormatted}.")
))
del bound, astClassInfo, subclassesFormatted, identifier

identifier = '忽'
bound = 'type_ignore'
astClassInfo = dictionary_astClasses[bound]
subclassesFormatted = formatSubclassesOxford(astClassInfo['subclasses'])
listDocstring.append(Docstring(identifier
	, summary=aDocument(f"`{bound}` `TypeVar` ({diminutive2etymology['TypeVar']}) bound to `ast.{bound}`.")
	, uncategorized=aDocument(
		f"The ideograph '{identifier}' (hū) means 'ignore'. Its decimal unicode is {ord(identifier)}. "
		f"This `covariant` `TypeVar` is bound to `ast.{bound}`, representing type checker ignore comments, and its subclasses, {subclassesFormatted}.")
))
del bound, astClassInfo, subclassesFormatted, identifier

identifier = '形'
bound = 'type_param'
astClassInfo = dictionary_astClasses[bound]
subclassesFormatted = formatSubclassesOxford(astClassInfo['subclasses'])
listDocstring.append(Docstring(identifier
	, summary=aDocument(f"`{bound}` `TypeVar` ({diminutive2etymology['TypeVar']}) bound to `ast.{bound}`.")
	, uncategorized=aDocument(
		f"The ideograph '{identifier}' (xíng) means 'type parameter'. Its decimal unicode is {ord(identifier)}. "
		f"This `covariant` `TypeVar` is bound to `ast.{bound}`, representing type parameters in generic classes and functions, and its subclasses, {subclassesFormatted}.")
))
del bound, astClassInfo, subclassesFormatted, identifier

for data in listDocstring:
	docstrings[identifierToolClass][data.identifier] = Make.Expr(Make.Constant(make1docstring(data)))
