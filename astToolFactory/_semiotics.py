"""Semiotics."""

# ======= Replacements for ambiguous values =======

noMinimum: int = -1

# ======= Centralized dictionaries =======

dictionary_astSuperClasses: dict[str, str] = {
	'AST': '木',
	'mod': '本',

	'stmt': '口',
	'expr_context': '工位',
	'expr': '工',

	'unaryop': '一符',
	'operator': '二符',
	'cmpop': '比符',
	'boolop': '布尔符',

	'Constant': '常',
	'excepthandler': '拦',
	'pattern': '俪',
	'type_ignore': '忽',
	'type_param': '形',
}

dictionaryIdentifiers: dict[str, str] = {
	'Be': 'Be',
	'boolopJoinMethod': '_boolopJoinMethod',
	'DOT': 'DOT',
	'Grab': 'Grab',
	'Make': 'Make',
	'operatorJoinMethod': '_operatorJoinMethod',
	'SSOT': '_theSSOT',
	'types': '_astTypes',
}
