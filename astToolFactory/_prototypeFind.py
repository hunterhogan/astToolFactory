from collections import deque
from collections.abc import Callable
from typing import Any
from typing_extensions import TypeIs
import ast

class Find:
	# class _str(str):
	# 	__slots__ = ()
	# 	def equal(self, other: object) -> bool:
	# 		return super().__eq__(other)

	# class _int(int):
	# 	def equal(self, other: object) -> bool:
	# 		return super().__eq__(other)

	@classmethod
	def at(cls, getable: Any, index: int, /) -> object:
		return getable.__getitem__(index)
