"""Settings for manufacturing."""
from pathlib import Path

PackageToManufactureIdentifier: str = 'astToolkit'
pathPackageToManufacture = Path('/apps', PackageToManufactureIdentifier, PackageToManufactureIdentifier)

dictionaryIdentifiers: dict[str, str] = {
	'Be': 'Be',
	'boolopJoinMethod': '_boolopJoinMethod',
	'DOT': 'DOT',
	'Grab': 'Grab',
	'Make': 'Make',
	'operatorJoinMethod': '_operatorJoinMethod',
}

dictionary_astSuperClasses: dict[str, str] = {
	'AST': '木',
	'boolop': '布尔符',
	'cmpop': '比符',
	'Constant': '常',
	'excepthandler': '拦',
	'expr_context': '工位',
	'expr': '工',
	'mod': '本',
	'operator': '二符',
	'pattern': '俪',
	'stmt': '口',
	'type_ignore': '忽',
	'type_param': '形',
	'unaryop': '一符',
}

# https://github.com/hunterhogan/astToolFactory/issues/1
isort_codeConfiguration: dict[str, int | str | list[str]] = {
	"combine_as_imports": True,
	"force_alphabetical_sort_within_sections": True,
	"from_first": True,
	"honor_noqa": True,
	"indent": "\t",
	"line_length": 120,
	"lines_after_imports": 1,
	"lines_between_types": 0,
	"multi_line_output": 4,
	"no_sections": True,
	"skip": ["__init__.py"],
	"use_parentheses": True,
}
