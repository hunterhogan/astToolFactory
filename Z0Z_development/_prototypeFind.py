from astToolkit import ConstantValueType
from collections.abc import Callable, Sequence
from typing import Any
from typing_extensions import TypeIs
import ast
import dataclasses

@dataclasses.dataclass
class Findonaut:

	attrChain: list[str] = dataclasses.field(default_factory=list[str])
	FindInstance: list[Callable] = dataclasses.field(default_factory=list[Callable])

	def __post_init__(self) -> None:
		self.attrActive = None

class Find:

	def __init__(self, state: Findonaut | None = None) -> None:
		self.state = state or Findonaut()

	@staticmethod
	def at(getable: Any, index: int, /) -> object:
		return getable.__getitem__(index)
