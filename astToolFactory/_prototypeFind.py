from collections import deque
from collections.abc import Callable
from typing import Any
from typing_extensions import TypeIs
import ast

class Find:
	def __init__(self, queueOfTruth: list[Callable[[Any], tuple[bool, Any]]] | None = None, queueOfFind_attr: deque[str] | None = None) -> None:
		self.queueOfTruth = queueOfTruth or []
		self.queueOfFind_attr = queueOfFind_attr or deque()

	def __getattribute__(self, attr: str) -> Any:
		if object.__getattribute__(self, attr):
			if self.queueOfFind_attr:
				# TODO: Clarify the intended behavior here
				pass
			self.queueOfFind_attr.append(attr)
			return self

		# Handle attribute access
		def attribute_checker(attrCurrent: Any) -> tuple[bool, Any]:
			hasAttributeCheck = hasattr(attrCurrent, attr)
			if hasAttributeCheck:
				return (hasAttributeCheck, getattr(attrCurrent, attr))
			return (hasAttributeCheck, attrCurrent)

		Z0Z_ImaQueue = object.__getattribute__(self, "queueOfTruth")
		dontMutateMyQueue: list[Callable[[Any], tuple[bool, Any]]] = [*Z0Z_ImaQueue, attribute_checker]
		return Find(dontMutateMyQueue)

	def __call__(self, node: ast.AST) -> bool:
		attrCurrent: Any = node
		for trueFalseCallable in self.queueOfTruth:
			Ima_bool, attrNext = trueFalseCallable(attrCurrent)
			if not Ima_bool:
				return False
			attrCurrent = attrNext
		return True

	# def equal(self, valueTarget: Any) -> "Find":
	#     def workhorse(attrCurrent: Any) -> tuple[bool, Any]:
	#         comparisonValue = attrCurrent == valueTarget
	#         return (comparisonValue, attrCurrent)

	#     dontMutateMyQueue: list[Callable[[Any], tuple[bool, Any]]] = [*self.queueOfTruth, workhorse]
	#     return Find(dontMutateMyQueue)

	# def at(self, indexTarget: int) -> "Find":
	#     def workhorse(attrCurrent: Any) -> tuple[bool, Any]:
	#         try:
	#             element: Any = attrCurrent[indexTarget]
	#         except (IndexError, TypeError, KeyError):
	#             indexAccessFailure = False
	#             return (indexAccessFailure, attrCurrent)
	#         else:
	#             indexAccessValue = True
	#             return (indexAccessValue, element)

	#     dontMutateMyQueue: list[Callable[[Any], tuple[bool, Any]]] = [*self.queueOfTruth, workhorse]
	#     return Find(dontMutateMyQueue)

