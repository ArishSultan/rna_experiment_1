from typing import Any

from .knc import encode_knc, KNC


def encode_dnc(sequence: str) -> tuple[Any, ...]:
    return encode_knc(sequence, 2)


class DNC(KNC):
    def __init__(self):
        super().__init__(2)
