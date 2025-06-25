# ruff: noqa
from collections.abc import Callable
from typing import Any
import ast

class Find:
    def __init__(self, queueOfGotten_attr: list[Callable[[Any], tuple[bool, Any]]] | None = None) -> None:
        self.queueOfGotten_attr = queueOfGotten_attr or []

    def __getattribute__(self, gotten_attrIdentifier: str):
        try:
            return object.__getattribute__(self, gotten_attrIdentifier)
        except AttributeError:
            pass

        if hasattr(ast, gotten_attrIdentifier):
            gotten_astObject: Any = getattr(ast, gotten_attrIdentifier)
            if isinstance(gotten_astObject, type) and issubclass(gotten_astObject, ast.AST):
                astClass: type[ast.AST] = gotten_astObject
                del gotten_astObject
                Z0Z_ImaQueue: list[Callable[[Any], tuple[bool, Any]]] = object.__getattribute__(self, 'queueOfGotten_attr')
                def ast_checker(attrCurrent: Any) -> tuple[bool, Any]:
                    if isinstance(attrCurrent, astClass):
                        return True, attrCurrent
                    return False, attrCurrent
                dontMutateMyQueue: list[Callable[[Any], tuple[bool, Any]]] = Z0Z_ImaQueue + [ast_checker]
                return Find(dontMutateMyQueue)

        def attribute_checker(attrCurrent: Any) -> tuple[bool, Any]:
            if hasattr(attrCurrent, gotten_attrIdentifier):
                return True, getattr(attrCurrent, gotten_attrIdentifier)
            return False, attrCurrent

        Z0Z_ImaQueue = object.__getattribute__(self, 'queueOfGotten_attr')
        dontMutateMyQueue: list[Callable[[Any], tuple[bool, Any]]] = Z0Z_ImaQueue + [attribute_checker]
        return Find(dontMutateMyQueue)

    def equal(self, valueTarget: Any) -> 'Find':
        def equality_checker(attrCurrent: Any) -> tuple[bool, Any]:
            if attrCurrent == valueTarget:
                return True, attrCurrent
            return False, attrCurrent

        dontMutateMyQueue: list[Callable[[Any], tuple[bool, Any]]] = self.queueOfGotten_attr + [equality_checker]
        return Find(dontMutateMyQueue)

    def at(self, indexTarget: int) -> 'Find':
        def index_checker(attrCurrent: Any) -> tuple[bool, Any]:
            try:
                element: Any = attrCurrent[indexTarget]
                return True, element
            except (IndexError, TypeError, KeyError):
                return False, attrCurrent

        dontMutateMyQueue: list[Callable[[Any], tuple[bool, Any]]] = self.queueOfGotten_attr + [index_checker]
        return Find(dontMutateMyQueue)

    def __call__(self, node: ast.AST) -> bool:
        attrCurrent: Any = node

        for trueFalseCallable in self.queueOfGotten_attr:
            Ima_bool, attrNext = trueFalseCallable(attrCurrent)
            if not Ima_bool:
                return False
            attrCurrent = attrNext

        return True


