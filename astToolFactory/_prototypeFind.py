from collections.abc import Callable
from typing import Any
from typing_extensions import TypeIs
import ast

class Find:
    def __init__(self, queueOfGotten_attr: list[Callable[[Any], tuple[bool, Any]]] | None = None) -> None:
        self.queueOfGotten_attr = queueOfGotten_attr or []

    def __getattribute__(self, gotten_attrIdentifier: str) -> Any:
        try:
            return object.__getattribute__(self, gotten_attrIdentifier)
        except AttributeError:
            pass

        # Handle attribute access
        def attribute_checker(attrCurrent: Any) -> tuple[bool, Any]:
            hasAttributeCheck = hasattr(attrCurrent, gotten_attrIdentifier)
            if hasAttributeCheck:
                return (hasAttributeCheck, getattr(attrCurrent, gotten_attrIdentifier))
            return (hasAttributeCheck, attrCurrent)

        Z0Z_ImaQueue = object.__getattribute__(self, "queueOfGotten_attr")
        dontMutateMyQueue: list[Callable[[Any], tuple[bool, Any]]] = [*Z0Z_ImaQueue, attribute_checker]
        return Find(dontMutateMyQueue)

    def equal(self, valueTarget: Any) -> "Find":
        def workhorse(attrCurrent: Any) -> tuple[bool, Any]:
            comparisonValue = attrCurrent == valueTarget
            return (comparisonValue, attrCurrent)

        dontMutateMyQueue: list[Callable[[Any], tuple[bool, Any]]] = [*self.queueOfGotten_attr, workhorse]
        return Find(dontMutateMyQueue)

    def at(self, indexTarget: int) -> "Find":
        def workhorse(attrCurrent: Any) -> tuple[bool, Any]:
            try:
                element: Any = attrCurrent[indexTarget]
            except (IndexError, TypeError, KeyError):
                indexAccessFailure = False
                return (indexAccessFailure, attrCurrent)
            else:
                indexAccessValue = True
                return (indexAccessValue, element)

        dontMutateMyQueue: list[Callable[[Any], tuple[bool, Any]]] = [*self.queueOfGotten_attr, workhorse]
        return Find(dontMutateMyQueue)

    def __call__(self, node: ast.AST) -> bool:
        attrCurrent: Any = node
        for trueFalseCallable in self.queueOfGotten_attr:
            Ima_bool, attrNext = trueFalseCallable(attrCurrent)
            if not Ima_bool:
                return False
            attrCurrent = attrNext
        return True
