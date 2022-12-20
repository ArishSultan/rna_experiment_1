from abc import ABC
from typing import Tuple


class Encoding(ABC):
    @property
    def name(self) -> str:
        return 'none'

    def encode(self, sequence: str, label: bool = False) -> Tuple[str]:
        pass

    def __eq__(self, other):
        return other is Encoding and other.name == self.name
