from pathlib import Path

pythonVersionMinorMinimum: int = 12

listPylanceErrors: list[str] = ['annotation', 'arg', 'args', 'body', 'keys', 'name', 'names', 'op', 'orelse', 'pattern', 'returns', 'target', 'value',]
listPylanceErrors.extend(['argtypes', 'bases', 'cases', 'comparators', 'decorator_list', 'defaults', 'elts', 'finalbody', 'generators', 'ifs', 'items',])
listPylanceErrors.extend(['keywords', 'kw_defaults', 'kwd_patterns', 'ops', 'patterns', 'targets', 'type_params', 'values',])

# filesystem and namespace ===============================================
packageName: str = 'astToolkit'
keywordArgumentsIdentifier: str = 'keywordArguments'

pathRoot = Path('/apps') 
pathPackage = pathRoot / packageName / packageName
pathToolFactory = pathRoot / 'astToolFactory' / 'astToolFactory'

pathFilenameDataframeAST = pathToolFactory / 'dataframeAST.parquet'

fileExtension: str = '.py'

# ww='''
# @classmethod
# def join(cls, expressions: Iterable[ast.expr], **keywordArguments: Unpack[_Attributes]) -> ast.expr:
# 	return operatorJoinMethod(cls, expressions, **keywordArguments)
# '''

# print(ast.dump(ast.parse(ww, type_comments=True), indent=None))
# import ast
# from ast import *  # noqa: E402, F403
# ruff: noqa: F405

# rr='''
# Assign(lineno=0,col_offset=0, [ast.Name('key', ast.Store())], value=Lambda(args=arguments(args=[arg('x', annotation=ast.Attribute(ast.Name('pandas'), 'Series'))]), body=Call(ast.Attribute(Attribute(ast.Name('x'), attr='str'), attr='lower'))))
# '''

# print(ast.unparse(ast.Module([eval(rr)])))

