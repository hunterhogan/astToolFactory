from itertools import chain  # noqa: D100
from pathlib import Path
import ast
import csv
import sys

filename: str = '.'.join(map(str, sys.version_info[0:3])) + '.Z0Z_csv'
pathFilename: Path = Path.cwd() / filename

listClassDefIdentifier_base: list[tuple[str, int, int, int, str]] = []

for astClass in [
	aClass
	for aClass in [ast.AST, *chain(*(aSubclass.__subclasses__() for aSubclass in [ast.AST, *ast.AST.__subclasses__()]))]
	if issubclass(aClass, ast.AST)
]:
	listClassDefIdentifier_base.append((str(astClass.__name__), *sys.version_info[0:3], str(astClass.__base__.__name__)))  # pyright: ignore[reportOptionalMemberAccess] # ty:ignore[unresolved-attribute]  # noqa: PERF401

with pathFilename.open('w', encoding='utf-8', newline='') as streamWrite:
	csv.writer(streamWrite).writerows(sorted(listClassDefIdentifier_base))
