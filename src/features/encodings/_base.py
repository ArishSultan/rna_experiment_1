from abc import ABC
from typing import Any


class Encoding(ABC):
    """
    """

    @property
    def name(self) -> str:
        """
        """

        return 'none'

    def encode(self, sequence: str, label: bool, specie: str) -> Any:
        """
        """

        return sequence
